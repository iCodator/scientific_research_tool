#!/usr/bin/env python3
"""
main.py - Scientific Research Tool

Nur formatierte Queries (PubMed/Europe PMC Syntax):
  (female OR woman AND masturbation)
  NOT (animal OR model)
  (squirting AND (successful OR effective))
  covid 19 OR influenza
  Coenzym Q10 AND mitochondria

Keine natürlichsprachigen FRAGEN mehr - aber Fachbegriffe sind OK!

Verwendung:
  python main.py --query-file query.txt --source pubmed --limit 10 --output results.csv --verbose
"""

import sys
import logging
import argparse
from pathlib import Path
from datetime import datetime

# ========== FIX: Füge PROJECT ROOT zu sys.path hinzu ==========
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ========== IMPORTS ==========

try:
    from src.databases.pubmed import PubMedAdapter
    from src.databases.europe_pmc import EuropePMCAdapter
    from src.databases.cochrane import CochraneAdapter
except ModuleNotFoundError as e:
    print(f"❌ Import Error: {e}")
    print(f"Stelle sicher, dass du von PROJECT ROOT ausführst:")
    print(f"  cd {PROJECT_ROOT}")
    print(f"  python main.py --query-file query.txt ...")
    sys.exit(1)

# ========== LOGGING SETUP ==========

log_dir = PROJECT_ROOT / "logs"
log_dir.mkdir(exist_ok=True)

log_file = log_dir / f"search_{datetime.now().strftime('%Y-%m-%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# ========== HILFSFUNKTIONEN ==========

def load_query(filepath: str) -> str:
    """Lade Query aus Datei"""
    try:
        file_path = Path(filepath)
        if not file_path.exists():
            file_path = PROJECT_ROOT / filepath
        
        with open(file_path, 'r', encoding='utf-8') as f:
            query = f.read().strip()
        logger.info(f"✓ Query geladen aus: {file_path}")
        return query
    except FileNotFoundError:
        logger.error(f"❌ Datei nicht gefunden: {filepath}")
        sys.exit(1)

def validate_query_syntax(query: str) -> bool:
    """
    Validiere Query-Syntax
    
    Erlaubte Format:
    - Fachbegriffe: covid 19, Coenzym Q10, squirting, etc.
    - Logik: (A OR B), (A AND B), NOT (A)
    - Mit/Ohne Anführungszeichen: "self stimulation" oder self stimulation
    
    NICHT erlaubt:
    - Natürlichsprachige Fragen wie "Wirksamkeit von..." "Welche Rolle..."
    - Satzstrukturen mit Fragezeichen/Punkte am Ende
    """
    import re
    
    # 1. Klammern balanciert?
    if query.count('(') != query.count(')'):
        logger.error("❌ Klammern nicht balanciert")
        return False
    
    # 2. Prüfe auf Fragen-Markierungen (natürlichsprachig)
    if query.rstrip().endswith('?'):
        logger.error("❌ Fragen (mit ?) nicht erlaubt - nutze strukturierte Query")
        return False
    
    # 3. Prüfe auf Satzstrukturen
    suspicious_patterns = [
        r'\bwelche\b.*\brole\b',           # "welche rolle"
        r'\bwirksamkeit\s+von\b',          # "wirksamkeit von"
        r'\beffektivität\s+von\b',         # "effektivität von"
        r'\bsuche\s+nach\b',               # "suche nach"
        r'\buntersuchung\s+der\b',         # "untersuchung der"
        r'\bfunktion\s+von\b',             # "funktion von"
        r'\berfolgreich(?:er|e|es)\s+(?:als|than)\b',  # "erfolgreicher als" (Vergleich)
    ]
    
    query_lower = query.lower()
    for pattern in suspicious_patterns:
        if re.search(pattern, query_lower):
            logger.error(f"❌ Natürlichsprachige Satzstruktur erkannt: {pattern}")
            logger.error("Nutze stattdessen: (Begriff1 AND Begriff2) oder (Begriff1 OR Begriff2)")
            return False
    
    # 4. OK - es ist formatiert
    logger.info("✓ Query-Format ist korrekt")
    logger.info("  - Operatoren: AND, OR, NOT")
    logger.info("  - Struktur: (Begriff1 OR Begriff2) AND (Begriff3)")
    logger.info("  - Fachbegriffe: covid 19, Coenzym Q10, squirting, etc.")
    
    return True

def search(query: str, source: str, limit: int) -> list:
    """Führe Suche in Datenbank durch"""
    logger.info(f"\n{'='*80}")
    logger.info(f"SUCHE IN {source.upper()}")
    logger.info(f"{'='*80}")
    logger.info(f"Query: {query}")
    logger.info(f"Limit: {limit}")
    
    # Wähle passenden Adapter
    if source.lower() == "pubmed":
        adapter = PubMedAdapter()
    elif source.lower() == "europepmc":
        adapter = EuropePMCAdapter()
    elif source.lower() == "cochrane":
        adapter = CochraneAdapter()
    else:
        logger.error(f"❌ Unbekannte Quelle: {source}")
        sys.exit(1)
    
    try:
        results = adapter.search(query, limit=limit)
        logger.info(f"\n✓ Suche abgeschlossen. {len(results)} Treffer gefunden.")
        return results
    except Exception as e:
        logger.error(f"❌ Fehler bei Suche: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        return []

def export_results(results: list, filepath: str):
    """Exportiere Ergebnisse in CSV oder JSON"""
    if not results:
        logger.warning("⚠️ Keine Ergebnisse zum Exportieren")
        return
    
    import csv
    import json
    
    output_path = Path(filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if filepath.endswith('.csv'):
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            fieldnames = results[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        logger.info(f"\n✓ CSV exportiert: {filepath}")
    
    elif filepath.endswith('.json'):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.info(f"\n✓ JSON exportiert: {filepath}")
    
    else:
        logger.warning(f"⚠️ Unbekanntes Format: {filepath}")

# ========== MAIN FUNKTION ==========

def main():
    """Hauptprogramm"""
    
    parser = argparse.ArgumentParser(
        description="Scientific Research Tool - Formatierte Queries (Fachbegriffe + AND/OR/NOT)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
ERLAUBTE Query-Formate:
  ✓ (female OR woman) AND masturbation
  ✓ (squirting) AND (successful OR effective)
  ✓ NOT (animal) AND (female OR woman)
  ✓ covid 19 OR influenza
  ✓ "Coenzym Q10" AND mitochondria
  ✓ cancer[TitleAbstract] AND 2020:2025[pdat]
  ✓ TITLE_ABSTRACT:cancer AND PUB_YEAR:2020-2025

NICHT ERLAUBT:
  ✗ "Welche Rolle spielt Coenzym Q10?"
  ✗ "Wirksamkeit von Akupunktur bei Rückenschmerzen"
  ✗ "Ist squirting erfolgreicher als Geschlechtsverkehr?"

Beispiele:
  python main.py --query-file query.txt --source pubmed --limit 10 --output results.csv
  python main.py --query "(female OR woman) AND masturbation" --source pubmed --limit 25
        """
    )
    parser.add_argument('--query', type=str, help='Formatierte Suchanfrage direkt als String')
    parser.add_argument('--query-file', type=str, help='Formatierte Suchanfrage aus Datei laden')
    parser.add_argument('--source', type=str, default='pubmed', 
                       choices=['pubmed', 'europepmc', 'cochrane'],
                       help='Datenbank (pubmed, europepmc, cochrane)')
    parser.add_argument('--limit', type=int, default=25, help='Max. Anzahl Artikel (default: 25)')
    parser.add_argument('--output', type=str, help='Output Datei (CSV oder JSON)')
    parser.add_argument('--verbose', action='store_true', help='Verbose Logging (DEBUG level)')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("🔍 Verbose Mode aktiviert")
    
    # ========== QUERY LADEN ==========
    
    logger.info("\n" + "="*80)
    logger.info("SCIENTIFIC RESEARCH TOOL - FORMATTED QUERIES ONLY")
    logger.info("="*80 + "\n")
    
    if args.query_file:
        query = load_query(args.query_file)
    elif args.query:
        query = args.query
        logger.info(f"✓ Query geladen: {query[:80]}...")
    else:
        logger.error("❌ Bitte --query oder --query-file angeben")
        parser.print_help()
        sys.exit(1)
    
    # ========== QUERY VALIDIEREN ==========
    
    logger.info(f"\n{'='*80}")
    logger.info(f"QUERY-VALIDIERUNG")
    logger.info(f"{'='*80}")
    
    if not validate_query_syntax(query):
        logger.error("\n❌ Query-Validierung fehlgeschlagen!")
        logger.error("Struktur: (Begriff1 OR Begriff2) AND (Begriff3)")
        logger.error("Fachbegriffe sind OK: squirting, covid 19, Coenzym Q10")
        sys.exit(1)
    
    # ========== SUCHE DURCHFÜHREN ==========
    
    results = search(query, args.source, args.limit)
    
    # ========== ERGEBNISSE EXPORTIEREN ==========
    
    if args.output:
        export_results(results, args.output)
    else:
        if results:
            logger.info(f"\n{'='*80}")
            logger.info(f"ERGEBNISSE ({len(results)} Artikel):")
            logger.info(f"{'='*80}\n")
            for i, result in enumerate(results[:5], 1):
                logger.info(f"{i}. {result.get('title', 'N/A')}")
                logger.info(f"   Authors: {result.get('authors', 'N/A')}")
                logger.info(f"   Year: {result.get('year', 'N/A')}")
                logger.info()
    
    logger.info("="*80)
    logger.info("✓ ERFOLGREICH ABGESCHLOSSEN")
    logger.info("="*80)

# ========== ENTRY POINT ==========

if __name__ == "__main__":
    main()
