#!/usr/bin/env python3

"""

═══════════════════════════════════════════════════════════════════════════

MAIN.PY - Scientific Research Tool (v2.3.0 - Multi-Level Query Support)

═══════════════════════════════════════════════════════════════════════════

📚 ÜBERBLICK:

=============

Dies ist die Hauptdatei des Scientific Research Tools.

Sie kümmert sich um:

1. Kommandozeilen-Argumente (--query, --source, etc.) verarbeiten

2. LoggingManager für zentrale Logging-Verwaltung

3. Query-Dateien mit Python-style Kommentaren laden

4. Multi-Level Queries (mehrzeilig) unterstützen ← NEU in v2.3.0

5. Query validieren

6. Passendem Adapter aufrufen (PubMed, Europe PMC, Cochrane)

7. Ergebnisse exportieren/anzeigen

NEU IN v2.3.0 (10.12.2025):

=============================

✅ Multi-Level Query Support! Queries können jetzt mehrzeilig sein:

Coenzyme Q10 OR ubiquinol
AND
physiology OR physiol*
NOT
animal OR mouse OR rat

Wird automatisch normalisiert zu:

((Coenzyme Q10) OR (ubiquinol)) AND ((physiology) OR (physiol*)) NOT ((animal) OR (mouse) OR (rat))

✅ UniversalQueryCompiler mit MultiLevelQueryParser

✅ Operator-Zeilen und Query-Zeilen auto-kategorisiert

✅ 100% abwärtskompatibel mit v2.2.0 (Single-Line Queries)

VERWENDUNG:

===========

python main.py --query-file queries/test.txt --source pubmed --limit 10

python main.py --query "cancer AND (2020:2025)" --source europepmc --limit 20

python main.py --query-file queries/multi_line_query.txt --source pubmed --verbose

QUERY-FORMAT (UNIVERSELL):

==========================

Multi-Line Format (NEU):
```
term1 OR term2
AND
term3 OR term4
NOT
term5
```

Single-Line Format (kompatibel):
```
((term1) OR term2) AND ((term3) OR term4) NOT (term5)
```

Der Query-Compiler unterstützt BEIDE Formate automatisch!

═══════════════════════════════════════════════════════════════════════════

"""

import sys

import argparse

from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════

# SCHRITT 1: PROJECT ROOT zu Python-Pfad hinzufügen

# ═══════════════════════════════════════════════════════════════════════════

PROJECT_ROOT = Path(__file__).parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

# ═══════════════════════════════════════════════════════════════════════════

# SCHRITT 2: LoggingManager initialisieren (zentral)

# ═══════════════════════════════════════════════════════════════════════════

from src.core.logging_manager import LoggingManager

# Wird später bei Datenbank-Wahl initialisiert

log_manager = None

logger = None

# ═══════════════════════════════════════════════════════════════════════════

# SCHRITT 3: Datenbank-Adapter importieren

# ═══════════════════════════════════════════════════════════════════════════

try:

    from src.databases.pubmed import PubMedAdapter

    from src.databases.europe_pmc import EuropePMCAdapter

    from src.databases.cochrane import CochraneAdapter

except ModuleNotFoundError as e:

    print(f"❌ Import Error: {e}")

    print(f"Stelle sicher, dass du von PROJECT ROOT ausführst:")

    print(f" cd {PROJECT_ROOT}")

    print(f" python main.py --query-file query.txt ...")

    sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════

# SCHRITT 4: QueryCompiler v2.3.0 mit Multi-Level Support importieren

# ═══════════════════════════════════════════════════════════════════════════

from src.core.query_compiler_universal import UniversalQueryCompiler, MultiLevelQueryParser

# ═══════════════════════════════════════════════════════════════════════════

# SCHRITT 5: Query-Parser mit Comment-Support importieren

# ═══════════════════════════════════════════════════════════════════════════

from src.core.query_parser_with_comments import load_query_with_comments

# ═══════════════════════════════════════════════════════════════════════════

# HILFSFUNKTIONEN

# ═══════════════════════════════════════════════════════════════════════════

def load_query(filepath: str) -> str:

    """

    Lädt eine Query aus einer Textdatei mit Comment-Support.

    NEU IN v2.3.0:

    ==============

    ✅ Multi-Line Queries werden automatisch erkannt!

    ✅ Operator-Zeilen (AND, OR, NOT) werden korrekt verarbeitet

    ✅ Jede Query-Zeile wird mit ((...)) geklammert

    ✅ Operator-Zeilen verbinden die Parts

    ✅ Python-style Kommentare (#) werden entfernt

    Format (Multi-Line):

    ```

    term1 OR term2

    AND

    term3 OR term4

    NOT

    term5

    ```

    Nach dem Parsing wird die Query zu:

    ```

    ((term1) OR term2) AND ((term3) OR term4) NOT ((term5))

    ```

    Was diese Funktion tut:

    =======================

    1. Versucht, die Datei zu öffnen

    2. Lädt Query mit Comment-Support

    3. Entfernt Python-style Kommentare (# und inline comments)

    4. Gibt die bereinigte Query zurück

    Args:

        filepath (str): Pfad zur Query-Datei

    Returns:

        str: Die geladene und bereinigte Query

    Beispiel:

        query = load_query("queries/test.txt")

        # → liest Datei ein, erkennt Multi-Level, gibt normalisierte Query zurück

    """

    try:

        query, original = load_query_with_comments(filepath)

        file_path = Path(filepath)

        if not file_path.exists():

            file_path = PROJECT_ROOT / filepath

        logger.info(f"📂 Query aus Datei geladen: {file_path}")

        logger.debug(f"Original-Inhalt mit Kommentaren:\n{original}")

        logger.debug(f"Bereinigte Query (Kommentare entfernt): {query}")

        return query

    except (FileNotFoundError, IOError) as e:

        logger.error(f"❌ {e}")

        sys.exit(1)

def validate_query_syntax(query: str) -> bool:

    """

    Validiert die Query-Syntax.

    Was wird überprüft?

    ====================

    1. Sind die Klammern ( ) balanciert?

    2. Sind nur erlaubte Zeichen vorhanden?

    3. Beginnt die Query nicht mit einer natürlichsprachigen Frage?

    Erlaubte Formate:

    =================

    ✓ (female OR woman) AND masturbation

    ✓ (squirting) AND (successful OR effective)

    ✓ NOT (animal) AND (female OR woman)

    ✓ covid 19 OR influenza

    ✓ "Coenzym Q10" AND mitochondria

    ✓ Multi-Line Format (wird auto-erkannt):
      ```
      term1 OR term2
      AND
      term3 OR term4
      ```

    Nicht erlaubt:

    ==============

    ✗ "Welche Rolle spielt Coenzym Q10?"

    ✗ "Wirksamkeit von Akupunktur bei Rückenschmerzen"

    ✗ "Ist squirting erfolgreicher als Geschlechtsverkehr?"

    """

    import re

    # PRÜFUNG 1: Sind Klammern balanciert?

    if query.count('(') != query.count(')'):

        logger.error("❌ Klammern nicht balanciert")

        logger.error(" Beispiel OK: (cancer OR tumor) AND (2020:2025)")

        logger.error(" Beispiel FALSCH: (cancer OR tumor AND (2020:2025)")

        return False

    # PRÜFUNG 2: Prüfe auf Fragen-Markierungen (?)

    if query.rstrip().endswith('?'):

        logger.error("❌ Fragen (mit ?) nicht erlaubt - nutze strukturierte Query")

        logger.error(" Falsch: 'Wirksamkeit von...?'")

        logger.error(" Richtig: '(Wirksamkeit) AND (Akupunktur)'")

        return False

    # PRÜFUNG 3: Prüfe auf natürlichsprachige Satzstrukturen

    suspicious_patterns = [

        r'\bwelche\b.*\brolle\b', # "welche rolle"

        r'\bwirksamkeit\s+von\b', # "wirksamkeit von"

        r'\beffektivität\s+von\b', # "effektivität von"

        r'\bsuche\s+nach\b', # "suche nach"

        r'\buntersuchung\s+der\b', # "untersuchung der"

        r'\bfunktion\s+von\b', # "funktion von"

    ]

    query_lower = query.lower()

    for pattern in suspicious_patterns:

        if re.search(pattern, query_lower):

            logger.error(f"❌ Natürlichsprachige Satzstruktur erkannt")

            logger.error(f" Nutze stattdessen: (Begriff1 AND Begriff2) oder (Begriff1 OR Begriff2)")

            return False

    # Alles ok!

    logger.info("✓ Query-Format ist korrekt")

    logger.info(" Operatoren: AND, OR, NOT")

    logger.info(" Struktur: (Begriff1 OR Begriff2) AND (Begriff3)")

    logger.info(" Beispiel: ((cancer OR tumor) AND (2020:2025)) NOT mouse")

    logger.info(" Multi-Line: term1 OR term2 \\n AND \\n term3")

    return True

def search(query: str, source: str, limit: int) -> list:

    """

    Führt die Suche in der gewählten Datenbank durch.

    NEU IN v2.3.0:

    ===============

    - Unterstützt Multi-Level Queries (auto-erkannt)

    - UniversalQueryCompiler v2.3.0 mit MultiLevelQueryParser

    - Besseres Logging mit Normalisierungs-Info

    Workflow:

    =========

    1. Wähle passenden Adapter basierend auf 'source' Parameter

    2. Kompiliere die universelle Query mit UniversalQueryCompiler

    3. Normalisierung unterstützt jetzt Multi-Line Queries

    4. Validiere die normalisierte Query

    5. Rufe adapter.search() auf

    6. Gebe die Ergebnisse zurück

    Args:

        query (str): Die Universelle Query (Single-Line oder Multi-Line)

        source (str): Die Datenbank ('pubmed', 'europepmc', 'cochrane')

        limit (int): Maximale Anzahl Artikel

    Returns:

        list: Liste von Artikel-Dictionaries

    """

    logger.info(f"\n{'='*80}")

    logger.info(f"STARTE SUCHE")

    logger.info(f"{'='*80}")

    logger.info(f"Query: {query[:100]}{'...' if len(query) > 100 else ''}")

    logger.info(f"Quelle: {source.upper()}")

    logger.info(f"Limit: {limit} Artikel")

    # Wähle passenden Adapter

    if source.lower() == "pubmed":

        adapter = PubMedAdapter()

    elif source.lower() == "europepmc":

        adapter = EuropePMCAdapter()

    elif source.lower() == "cochrane":

        adapter = CochraneAdapter()

    else:

        logger.error(f"❌ Unbekannte Quelle: {source}")

        logger.error(f" Akzeptiert: pubmed, europepmc, cochrane")

        sys.exit(1)

    logger.info(f"✓ {source.upper()}-Adapter initialisiert")

    # NEU in v2.3.0: Kompiliere mit UniversalQueryCompiler

    compiler = UniversalQueryCompiler(query, source=source.lower())

    # Normalisierung (unterstützt Multi-Level Queries automatisch)

    compiler.normalize()

    normalized_query = compiler.normalized_query

    logger.info(f"✓ Query normalisiert für {source.upper()}")

    logger.info(f"  Normalisiert: {normalized_query[:100]}{'...' if len(normalized_query) > 100 else ''}")

    # Validiere

    if not compiler.validate():

        logger.error(f"❌ Query-Validierung fehlgeschlagen")

        for error in compiler.errors:

            logger.error(f"  - {error}")

        return []

    logger.info(f"✓ Query-Validierung erfolgreich")

    # Führe Suche durch

    try:

        results = adapter.search(normalized_query, limit=limit)

        logger.info(f"✓ Suche abgeschlossen: {len(results)} Artikel gefunden")

        return results

    except Exception as e:

        logger.error(f"❌ Fehler bei Suche: {e}")

        import traceback

        logger.debug(traceback.format_exc())

        return []

def export_results(results: list, filepath: str):

    """

    Exportiert die Suchergebnisse in eine Datei.

    Unterstützte Formate:

    =====================

    • CSV (.csv) - für Excel/Spreadsheets

    • JSON (.json) - für weitere Verarbeitung

    Args:

        results (list): Liste von Artikel-Dictionaries

        filepath (str): Zieldatei-Pfad (muss .csv oder .json sein)

    Beispiel:

        export_results(results, "output/results.csv")

        export_results(results, "output/results.json")

    """

    import csv

    import json

    if not results:

        logger.warning("⚠️ Keine Ergebnisse zum Exportieren")

        return

    output_path = Path(filepath)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if filepath.endswith('.csv'):

        # CSV Export

        with open(filepath, 'w', newline='', encoding='utf-8') as f:

            fieldnames = results[0].keys()

            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()

            writer.writerows(results)

        logger.info(f"✓ Ergebnisse als CSV exportiert: {filepath}")

    elif filepath.endswith('.json'):

        # JSON Export

        with open(filepath, 'w', encoding='utf-8') as f:

            json.dump(results, f, indent=2, ensure_ascii=False)

        logger.info(f"✓ Ergebnisse als JSON exportiert: {filepath}")

    else:

        logger.warning(f"⚠️ Unbekanntes Format: {filepath}")

        logger.warning(f" Akzeptiert: .csv oder .json")

def main():

    """

    Hauptprogramm - orchestriert den gesamten Ablauf.

    NEU IN v2.3.0:

    ===============

    - Multi-Level Query Support

    - Automatische Erkennung von Single-Line vs Multi-Line

    Workflow:

    =========

    1. Parse Kommandozeilen-Argumente

    2. Initialisiere LoggingManager

    3. Lade Query (aus Datei oder direkter Eingabe)

    4. Validiere Query-Syntax

    5. Führe Suche durch (mit v2.3.0 Compiler)

    6. Exportiere Ergebnisse (oder zeige sie an)

    """

    global log_manager, logger

    # ═══════════════════════════════════════════════════════════════════

    # Kommandozeilen-Parser definieren

    # ═══════════════════════════════════════════════════════════════════

    parser = argparse.ArgumentParser(

        description="Scientific Research Tool - Formatierte Queries mit Multi-Level Support (v2.3.0)",

        formatter_class=argparse.RawDescriptionHelpFormatter,

        epilog="""

ERLAUBTE Query-Formate (UNIVERSELL - Compiler übersetzt automatisch):

Single-Line:
✓ (female OR woman) AND masturbation
✓ (squirting) AND (successful OR effective)
✓ ((cancer OR tumor) AND (2020:2025)) NOT mouse
✓ covid 19 OR influenza
✓ "Coenzym Q10" AND mitochondria

Multi-Line (NEU in v2.3.0):
✓ Coenzyme Q10 OR ubiquinol
  AND
  physiology OR physiol*
  NOT
  animal OR mouse OR rat

NICHT ERLAUBT:
✗ "Welche Rolle spielt Coenzym Q10?"
✗ "Wirksamkeit von Akupunktur bei Rückenschmerzen"
✗ "Ist squirting erfolgreicher als Geschlechtsverkehr?"

BEISPIELE:

python main.py --query-file queries/test.txt --source pubmed --limit 10
python main.py --query "cancer AND (2020:2025)" --source europepmc --limit 20
python main.py --query-file queries/multi_line.txt --source pubmed --verbose

        """

    )

    parser.add_argument(

        '--query',

        type=str,

        help='Universelle Query direkt als String (Alternative zu --query-file)'

    )

    parser.add_argument(

        '--query-file',

        type=str,

        help='Universelle Query aus Textdatei laden (unterstützt Python-style Kommentare # und Multi-Line)'

    )

    parser.add_argument(

        '--source',

        type=str,

        default='pubmed',

        choices=['pubmed', 'europepmc', 'cochrane'],

        help='Datenbank (default: pubmed)'

    )

    parser.add_argument(

        '--limit',

        type=int,

        default=25,

        help='Maximale Anzahl Artikel zu holen (default: 25)'

    )

    parser.add_argument(

        '--output',

        type=str,

        help='Exportiere Ergebnisse in Datei (.csv oder .json)'

    )

    parser.add_argument(

        '--verbose',

        action='store_true',

        help='Verbose Logging (DEBUG Level - sehr detailliert)'

    )

    args = parser.parse_args()

    # ═══════════════════════════════════════════════════════════════════

    # Initialisiere LoggingManager mit der gewählten Datenbank

    # ═══════════════════════════════════════════════════════════════════

    log_manager = LoggingManager(args.source.lower())

    logger = log_manager.get_logger(__name__)

    # ═══════════════════════════════════════════════════════════════════

    # Verbose-Mode aktivieren (falls gewünscht)

    # ═══════════════════════════════════════════════════════════════════

    if args.verbose:

        log_manager.set_verbose(True)

    # ═══════════════════════════════════════════════════════════════════

    # Query laden (aus Datei oder direkter Eingabe)

    # ═══════════════════════════════════════════════════════════════════

    logger.info("\n" + "="*80)

    logger.info("SCIENTIFIC RESEARCH TOOL v2.3.0")

    logger.info("="*80 + "\n")

    if args.query_file:

        query = load_query(args.query_file)

    elif args.query:

        query = args.query

        logger.info(f"📝 Query aus Kommandozeile: {query[:80]}...")

    else:

        logger.error("❌ Bitte --query oder --query-file angeben")

        parser.print_help()

        sys.exit(1)

    # ═══════════════════════════════════════════════════════════════════

    # Query validieren

    # ═══════════════════════════════════════════════════════════════════

    logger.info(f"\n{'='*80}")

    logger.info("QUERY-VALIDIERUNG")

    logger.info(f"{'='*80}")

    if not validate_query_syntax(query):

        logger.error("\n❌ Query-Validierung fehlgeschlagen!")

        logger.error("Struktur: (Begriff1 OR Begriff2) AND (Begriff3)")

        logger.error("Fachbegriffe sind OK: squirting, covid 19, Coenzym Q10")

        sys.exit(1)

    # ═══════════════════════════════════════════════════════════════════

    # Suche durchführen

    # ═══════════════════════════════════════════════════════════════════

    results = search(query, args.source, args.limit)

    # ═══════════════════════════════════════════════════════════════════

    # Ergebnisse exportieren oder anzeigen

    # ═══════════════════════════════════════════════════════════════════

    if args.output:

        export_results(results, args.output)

    else:

        # Zeige Ergebnisse im Terminal an

        if results:

            logger.info(f"\n{'='*80}")

            logger.info(f"ERGEBNISSE ({len(results)} Artikel)")

            logger.info(f"{'='*80}\n")

            for i, result in enumerate(results[:5], 1):

                logger.info(f"{i}. {result.get('title', 'N/A')}")

                logger.info(f" Authors: {result.get('authors', 'N/A')}")

                logger.info(f" Year: {result.get('year', 'N/A')}")

                logger.info(f" DOI: {result.get('doi', 'N/A')}")

                logger.info("")

    # ═══════════════════════════════════════════════════════════════════

    # Programm erfolgreich beendet

    # ═══════════════════════════════════════════════════════════════════

    logger.info("="*80)

    logger.info("✓ ERFOLGREICH ABGESCHLOSSEN")

    logger.info("="*80)

# ═══════════════════════════════════════════════════════════════════════════

# ENTRY POINT

# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":

    main()
