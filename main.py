#!/usr/bin/env python3

"""
═══════════════════════════════════════════════════════════════════════════
MAIN.PY - Scientific Research Tool
═══════════════════════════════════════════════════════════════════════════

📚 ÜBERBLICK:
=============
Dies ist die Hauptdatei des Scientific Research Tools.
Sie kümmert sich um:
1. Kommandozeilen-Argumente (--query, --source, etc.) verarbeiten
2. Query validieren
3. Passendem Adapter aufrufen (PubMed, Europe PMC, Cochrane)
4. Ergebnisse exportieren/anzeigen

VERWENDUNG:
===========
python main.py --query-file queries/sehr_komplex.txt --source europepmc --limit 20
python main.py --query "cancer AND (2020:2025)" --source pubmed --limit 10 --output results.csv

QUERY-FORMAT (UNIVERSELL):
==========================
((a OR b) AND (c NOT d)) mit Datumsbereichen wie 2020:2025

Der Query-Compiler übersetzt das automatisch für die gewählte Datenbank!

═══════════════════════════════════════════════════════════════════════════
"""

import sys
import argparse
import re
import csv
import json
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════
# SCHRITT 1: PROJECT ROOT zu Python-Pfad hinzufügen
# ═══════════════════════════════════════════════════════════════════════════

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ═══════════════════════════════════════════════════════════════════════════
# SCHRITT 2: Adapter und Utils importieren
# ═══════════════════════════════════════════════════════════════════════════

try:
    from src.databases.pubmed import PubMedAdapter
    from src.databases.europe_pmc import EuropePMCAdapter
    from src.databases.cochrane import CochraneAdapter
    from src.core.query_compiler import QueryCompiler
    from src.core.logging_manager import LoggingManager
except ModuleNotFoundError as e:
    print(f"❌ Import Error: {e}")
    print(f"Stelle sicher, dass du von PROJECT ROOT ausführst:")
    print(f" cd {PROJECT_ROOT}")
    print(f" python main.py --query-file query.txt ...")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════
# HILFSFUNKTIONEN
# ═══════════════════════════════════════════════════════════════════════════

def load_query(filepath: str, logger) -> str:
    """Lädt Query aus Datei"""
    try:
        file_path = Path(filepath)
        if not file_path.exists():
            file_path = PROJECT_ROOT / filepath
        
        with open(file_path, 'r', encoding='utf-8') as f:
            query = f.read().strip()
        
        logger.info(f"📂 Query aus Datei geladen: {file_path}")
        return query
        
    except FileNotFoundError:
        logger.error(f"❌ Datei nicht gefunden: {filepath}")
        sys.exit(1)


def validate_query_syntax(query: str, logger) -> bool:
    """Validiert die Query-Syntax"""
    
    # PRÜFUNG 1: Sind Klammern balanciert?
    if query.count('(') != query.count(')'):
        logger.error("❌ Klammern nicht balanciert")
        logger.error("   Beispiel OK:    (cancer OR tumor) AND (2020:2025)")
        logger.error("   Beispiel FALSCH: (cancer OR tumor AND (2020:2025)")
        return False
    
    # PRÜFUNG 2: Prüfe auf Fragen-Markierungen (?)
    if query.rstrip().endswith('?'):
        logger.error("❌ Fragen (mit ?) nicht erlaubt - nutze strukturierte Query")
        logger.error("   Falsch:  'Wirksamkeit von...?'")
        logger.error("   Richtig: '(Wirksamkeit) AND (Akupunktur)'")
        return False
    
    # PRÜFUNG 3: Prüfe auf natürlichsprachige Satzstrukturen
    suspicious_patterns = [
        r'\bwelche\b.*\brolle\b',
        r'\bwirksamkeit\s+von\b',
        r'\beffektivität\s+von\b',
        r'\bsuche\s+nach\b',
        r'\buntersuchung\s+der\b',
        r'\bfunktion\s+von\b',
    ]
    
    query_lower = query.lower()
    for pattern in suspicious_patterns:
        if re.search(pattern, query_lower):
            logger.error(f"❌ Natürlichsprachige Satzstruktur erkannt")
            logger.error(f"   Nutze stattdessen: (Begriff1 AND Begriff2) oder (Begriff1 OR Begriff2)")
            return False
    
    # Alles ok!
    logger.info("✓ Query-Format ist korrekt")
    logger.info("  Operatoren: AND, OR, NOT")
    logger.info("  Struktur: (Begriff1 OR Begriff2) AND (Begriff3)")
    logger.info("  Beispiel: ((cancer OR tumor) AND (2020:2025)) NOT mouse")
    return True


def search(query: str, source: str, limit: int, logger) -> list:
    """Führt die Suche durch"""
    
    logger.info(f"\n{'='*80}")
    logger.info(f"STARTE SUCHE")
    logger.info(f"{'='*80}")
    logger.info(f"Query: {query}")
    logger.info(f"Quelle: {source.upper()}")
    logger.info(f"Limit: {limit} Artikel")
    
    # Wähle Adapter
    if source.lower() == "pubmed":
        adapter = PubMedAdapter()
    elif source.lower() == "europepmc":
        adapter = EuropePMCAdapter()
    elif source.lower() == "cochrane":
        adapter = CochraneAdapter()
    else:
        logger.error(f"❌ Unbekannte Quelle: {source}")
        logger.error(f"   Akzeptiert: pubmed, europepmc, cochrane")
        sys.exit(1)
    
    logger.info(f"✓ {source.upper()}-Adapter initialisiert")
    
    # Kompiliere Query
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


def export_results(results: list, filepath: str, logger) -> None:
    """Exportiert Ergebnisse in CSV oder JSON"""
    
    if not results:
        logger.warning("⚠️ Keine Ergebnisse zum Exportieren")
        return
    
    # Erstelle Zielordner
    output_path = Path(filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if filepath.endswith('.csv'):
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            fieldnames = results[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        logger.info(f"✓ Ergebnisse als CSV exportiert: {filepath}")
        
    elif filepath.endswith('.json'):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.info(f"✓ Ergebnisse als JSON exportiert: {filepath}")
        
    else:
        logger.warning(f"⚠️ Unbekanntes Format: {filepath}")
        logger.warning(f"   Akzeptiert: .csv oder .json")


def main():
    """Hauptprogramm"""
    
    # ═══════════════════════════════════════════════════════════════════
    # Parse Kommandozeilen-Argumente ZUERST
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
python main.py --query "cancer AND (2020:2025)" --source pubmed --limit 10 --output result.csv
python main.py --query-file query.txt --source cochrane --limit 50 --verbose

        """
    )
    
    parser.add_argument('--query', type=str,
                       help='Universelle Query direkt als String')
    parser.add_argument('--query-file', type=str,
                       help='Universelle Query aus Textdatei laden')
    parser.add_argument('--source', type=str, default='pubmed',
                       choices=['pubmed', 'europepmc', 'cochrane'],
                       help='Datenbank (default: pubmed)')
    parser.add_argument('--limit', type=int, default=25,
                       help='Maximale Anzahl Artikel (default: 25)')
    parser.add_argument('--output', type=str,
                       help='Exportiere Ergebnisse in Datei (.csv oder .json)')
    parser.add_argument('--verbose', action='store_true',
                       help='Verbose Logging (DEBUG Level)')
    
    args = parser.parse_args()
    
    # ═══════════════════════════════════════════════════════════════════
    # Initialisiere LoggingManager mit der gewählten Datenbank
    # ═══════════════════════════════════════════════════════════════════
    
    log_manager = LoggingManager(args.source)
    logger = log_manager.get_logger(__name__)
    
    # Aktiviere Verbose-Mode falls gewünscht
    if args.verbose:
        log_manager.set_verbose(True)
    
    # ═══════════════════════════════════════════════════════════════════
    # Lade Query
    # ═══════════════════════════════════════════════════════════════════
    
    logger.info("\n" + "="*80)
    logger.info("SCIENTIFIC RESEARCH TOOL")
    logger.info("="*80 + "\n")
    
    if args.query_file:
        query = load_query(args.query_file, logger)
    elif args.query:
        query = args.query
        logger.info(f"📝 Query aus Kommandozeile: {query[:80]}...")
    else:
        logger.error("❌ Bitte --query oder --query-file angeben")
        parser.print_help()
        sys.exit(1)
    
    # ═══════════════════════════════════════════════════════════════════
    # Validiere Query
    # ═══════════════════════════════════════════════════════════════════
    
    logger.info(f"\n{'='*80}")
    logger.info("QUERY-VALIDIERUNG")
    logger.info(f"{'='*80}")
    
    if not validate_query_syntax(query, logger):
        logger.error("\n❌ Query-Validierung fehlgeschlagen!")
        logger.error("Struktur: (Begriff1 OR Begriff2) AND (Begriff3)")
        logger.error("Fachbegriffe sind OK: squirting, covid 19, Coenzym Q10")
        sys.exit(1)
    
    # ═══════════════════════════════════════════════════════════════════
    # Führe Suche durch
    # ═══════════════════════════════════════════════════════════════════
    
    results = search(query, args.source, args.limit, logger)
    
    # ═══════════════════════════════════════════════════════════════════
    # Exportiere oder zeige Ergebnisse
    # ═══════════════════════════════════════════════════════════════════
    
    if args.output:
        # Füge Datenbank-Präfix hinzu
        if not args.output.startswith('output/'):
            filename = f"{args.source}_{args.output}"
            output_file = f"output/{filename}"
        else:
            output_file = args.output
        
        logger.info(f"\n{'='*80}")
        logger.info("EXPORTIERE ERGEBNISSE")
        logger.info(f"{'='*80}")
        logger.info(f"Zieldatei: {output_file}")
        
        export_results(results, output_file, logger)
    else:
        # Zeige Ergebnisse im Terminal
        if results:
            logger.info(f"\n{'='*80}")
            logger.info(f"ERGEBNISSE ({len(results)} Artikel)")
            logger.info(f"{'='*80}\n")
            
            for i, result in enumerate(results[:5], 1):
                logger.info(f"{i}. {result.get('title', 'N/A')}")
                logger.info(f"   Authors: {result.get('authors', 'N/A')}")
                logger.info(f"   Year: {result.get('year', 'N/A')}")
                logger.info(f"   DOI: {result.get('doi', 'N/A')}")
    
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
