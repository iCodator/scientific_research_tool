#!/usr/bin/env python3

"""
═══════════════════════════════════════════════════════════════════════════
MAIN.PY - Scientific Research Tool (WITH COMMENT SUPPORT & LOGGING MANAGER)
═══════════════════════════════════════════════════════════════════════════

📚 ÜBERBLICK
===========

Dies ist die Hauptdatei des Scientific Research Tools.

Sie kümmert sich um:
1. Kommandozeilen-Argumente (--query, --source, etc.) verarbeiten
2. Logging über den zentralen LoggingManager
3. Query-Dateien mit Python-style Kommentaren laden
4. Query validieren
5. Passenden Adapter aufrufen (PubMed, Europe PMC, Cochrane)
6. Ergebnisse exportieren/anzeigen

NEUES FEATURE (09.12.2025)
==========================

✅ Query-Dateien können jetzt Python-ähnliche Kommentare enthalten:

    # Das ist ein Kommentar
    'Coenzym Q10'  # Inline-Kommentar
    AND
    (2015:2025[pdat])  # Datumbereich

Die Kommentare werden vor der Validierung automatisch entfernt.

VERWENDUNG
==========

python main.py --query-file queries/sehr_komplex.txt --source europepmc --limit 20
python main.py --query "cancer AND (2020:2025)" --source pubmed --limit 10 --output results.csv
python main.py --query-file queries/coenzym_q10.txt --source pubmed --verbose

QUERY-FORMAT (UNIVERSELL)
=========================

((a OR b) AND (c NOT d)) mit Datumsbereichen wie 2020:2025

Der Query-Compiler übersetzt das automatisch für die gewählte Datenbank!
"""

import sys
import argparse
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════
# SCHRITT 1: PROJECT ROOT zu Python-Pfad hinzufügen
# ═══════════════════════════════════════════════════════════════════════════

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# ═══════════════════════════════════════════════════════════════════════════
# SCHRITT 2: LoggingManager initialisieren (zentral)
# ═══════════════════════════════════════════════════════════════════════════

from src.core.logging_manager import LoggingManager

# Werden in main() initialisiert
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
    print("Stelle sicher, dass du von PROJECT ROOT ausführst, z.B.:")
    print(f"  cd {PROJECT_ROOT}")
    print("  python main.py --query-file queries/test.txt --source pubmed")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════
# SCHRITT 4: QueryCompiler für Queries importieren
# ═══════════════════════════════════════════════════════════════════════════

from src.core.query_compiler import QueryCompiler

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

    NEUES FEATURE (09.12.2025)
    ==========================

    Diese Funktion unterstützt Python-ähnliche Kommentare (#).

    Beispiel-Query-Datei (queries/coenzym_q10.txt):

        # Suche nach Coenzym Q10
        'Coenzym Q10'  # Hauptterm
        AND
        # Zeitraum-Filter
        (2015:2025[pdat])  # Nur Artikel ab 2015

    Nach dem Parsing wird die Query zu:

        'Coenzym Q10' AND (2015:2025[pdat])

    Was diese Funktion tut:
    =======================

    1. Versucht, die Datei zu öffnen
    2. Lädt Query mit Comment-Support
    3. Entfernt Python-style Kommentare (volle Zeilen + Inline-Kommentare)
    4. Gibt die bereinigte Query zurück

    Args:
        filepath (str): Pfad zur Query-Datei

    Returns:
        str: Die geladene und bereinigte Query
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
    3. Sieht die Query nicht wie eine natürlichsprachige Frage aus?

    Erlaubte Formate:
    =================

    ✓ (female OR woman) AND masturbation
    ✓ (squirting) AND (successful OR effective)
    ✓ NOT (animal) AND (female OR woman)
    ✓ covid 19 OR influenza
    ✓ "Coenzym Q10" AND mitochondria

    Nicht erlaubt (natürlichsprachig):
    ==================================

    ✗ "Welche Rolle spielt Coenzym Q10?"
    ✗ "Wirksamkeit von Akupunktur bei Rückenschmerzen"
    ✗ "Ist squirting erfolgreicher als Geschlechtsverkehr?"
    """
    import re

    # PRÜFUNG 1: Sind Klammern balanciert?
    if query.count("(") != query.count(")"):
        logger.error("❌ Klammern nicht balanciert")
        logger.error(" Beispiel OK: (cancer OR tumor) AND (2020:2025)")
        logger.error(" Beispiel FALSCH: (cancer OR tumor AND (2020:2025)")
        return False

    # PRÜFUNG 2: Prüfe auf Fragen-Markierungen (?)
    if query.rstrip().endswith("?"):
        logger.error("❌ Fragen (mit ?) nicht erlaubt - nutze strukturierte Query")
        logger.error(" Falsch: 'Wirksamkeit von...?'\n Richtig: '(Wirksamkeit) AND (Akupunktur)'")
        return False

    # PRÜFUNG 3: Prüfe auf natürlichsprachige Satzstrukturen
    suspicious_patterns = [
        r"\bwelche\b.*\brolle\b",      # "welche rolle"
        r"\bwirksamkeit\s+von\b",      # "wirksamkeit von"
        r"\beffektivität\s+von\b",     # "effektivität von"
        r"\bsuche\s+nach\b",           # "suche nach"
        r"\buntersuchung\s+der\b",     # "untersuchung der"
        r"\bfunktion\s+von\b",         # "funktion von"
    ]

    query_lower = query.lower()

    for pattern in suspicious_patterns:
        if re.search(pattern, query_lower):
            logger.error("❌ Natürlichsprachige Satzstruktur erkannt")
            logger.error(" Nutze stattdessen: (Begriff1 AND Begriff2) oder (Begriff1 OR Begriff2)")
            return False

    # Alles ok!
    logger.info("✓ Query-Format ist korrekt")
    logger.info(" Operatoren: AND, OR, NOT")
    logger.info(" Struktur: (Begriff1 OR Begriff2) AND (Begriff3)")
    logger.info(" Beispiel: ((cancer OR tumor) AND (2020:2025)) NOT mouse")

    return True


def search(query: str, source: str, limit: int) -> list:
    """
    Führt die Suche in der gewählten Datenbank durch.

    Workflow:
    =========
    1. Wähle passenden Adapter basierend auf 'source'
    2. Kompiliere die universelle Query für die Datenbank
    3. Rufe adapter.search() auf
    4. Gebe die Ergebnisse zurück

    Args:
        query (str): Die universelle Query
        source (str): 'pubmed', 'europepmc' oder 'cochrane'
        limit (int): Maximale Anzahl Artikel

    Returns:
        list[dict]: Liste von Artikel-Dictionaries
    """
    logger.info("\n" + "=" * 80)
    logger.info("STARTE SUCHE")
    logger.info("=" * 80)
    logger.info(f"Query: {query}")
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
        logger.error(" Akzeptiert: pubmed, europepmc, cochrane")
        sys.exit(1)

    logger.info(f"✓ {source.upper()}-Adapter initialisiert")

    # Kompiliere die Query für die gewählte Datenbank
    compiler = QueryCompiler(query)
    compiled_query = compiler.compile_for_source(source)

    # Führe Suche durch
    try:
        results = adapter.search(compiled_query, limit=limit)
        logger.info(f"✓ Suche abgeschlossen: {len(results)} Artikel gefunden")
        return results
    except Exception as e:
        logger.error(f"❌ Fehler bei Suche: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        return []


def export_results(results: list, filepath: str) -> None:
    """
    Exportiert die Suchergebnisse in eine Datei.

    Unterstützte Formate:
    =====================
    • CSV (.csv)  - für Excel/Spreadsheets
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

    if filepath.endswith(".csv"):
        # CSV Export
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            fieldnames = results[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        logger.info(f"✓ Ergebnisse als CSV exportiert: {filepath}")

    elif filepath.endswith(".json"):
        # JSON Export
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        logger.info(f"✓ Ergebnisse als JSON exportiert: {filepath}")
    else:
        logger.warning(f"⚠️ Unbekanntes Format: {filepath}")
        logger.warning(" Akzeptiert: .csv oder .json")


def main() -> None:
    """
    Hauptprogramm - orchestriert den gesamten Ablauf.

    Workflow:
    =========
    1. Parse Kommandozeilen-Argumente
    2. Initialisiere LoggingManager
    3. Lade Query (aus Datei oder direkter Eingabe)
    4. Validiere Query-Syntax
    5. Führe Suche durch
    6. Exportiere Ergebnisse (oder zeige sie an)
    """
    global log_manager, logger

    # ═══════════════════════════════════════════════════════════════════
    # Kommandozeilen-Parser definieren
    # ═══════════════════════════════════════════════════════════════════

    parser = argparse.ArgumentParser(
        description="Scientific Research Tool - Formatierte Queries mit automatischem Query-Compiler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
ERLAUBTE Query-Formate (UNIVERSELL - Compiler übersetzt automatisch):

✓ (female OR woman) AND masturbation
✓ (squirting) AND (successful OR effective)
✓ ((cancer OR tumor) AND (2020:2025)) NOT mouse
✓ covid 19 OR influenza
✓ "Coenzym Q10" AND mitochondria

NICHT ERLAUBT:
✗ "Welche Rolle spielt Coenzym Q10?"
✗ "Wirksamkeit von Akupunktur bei Rückenschmerzen"
✗ "Ist squirting erfolgreicher als Geschlechtsverkehr?"

BEISPIELE:
python main.py --query-file queries/sehr_komplex.txt --source europepmc --limit 20
python main.py --query "cancer AND (2020:2025)" --source pubmed --limit 10 --output results.csv
python main.py --query-file queries/coenzym_q10.txt --source pubmed --verbose
"""
    )

    parser.add_argument(
        "--query",
        type=str,
        help="Universelle Query direkt als String (Alternative zu --query-file)",
    )

    parser.add_argument(
        "--query-file",
        type=str,
        help="Universelle Query aus Textdatei laden (unterstützt Python-style Kommentare #)",
    )

    parser.add_argument(
        "--source",
        type=str,
        default="pubmed",
        choices=["pubmed", "europepmc", "cochrane"],
        help="Datenbank (default: pubmed)",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=25,
        help="Maximale Anzahl Artikel zu holen (default: 25)",
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Exportiere Ergebnisse in Datei (.csv oder .json)",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose Logging (DEBUG Level - sehr detailliert)",
    )

    args = parser.parse_args()

    # ═══════════════════════════════════════════════════════════════════
    # LoggingManager mit gewählter Datenbank initialisieren
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

    logger.info("\n" + "=" * 80)
    logger.info("SCIENTIFIC RESEARCH TOOL")
    logger.info("=" * 80 + "\n")

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

    logger.info("\n" + "=" * 80)
    logger.info("QUERY-VALIDIERUNG")
    logger.info("=" * 80)

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
            logger.info("\n" + "=" * 80)
            logger.info(f"ERGEBNISSE ({len(results)} Artikel)")
            logger.info("=" * 80 + "\n")

            for i, result in enumerate(results[:5], 1):
                logger.info(f"{i}. {result.get('title', 'N/A')}")
                logger.info(f" Authors: {result.get('authors', 'N/A')}")
                logger.info(f" Year: {result.get('year', 'N/A')}")
                logger.info(f" DOI: {result.get('doi', 'N/A')}")
                logger.info("")  # Leerzeile für bessere Lesbarkeit

    # ═══════════════════════════════════════════════════════════════════
    # Programm erfolgreich beendet
    # ═══════════════════════════════════════════════════════════════════

    logger.info("=" * 80)
    logger.info("✓ ERFOLGREICH ABGESCHLOSSEN")
    logger.info("=" * 80)


# ═══════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()
