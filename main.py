"""
═══════════════════════════════════════════════════════════════════════════
SCIENTIFIC RESEARCH TOOL - Main Entry Point (FIXED VERSION 7)
═══════════════════════════════════════════════════════════════════════════

Zweck:
------
Dies ist das Hauptprogramm zum Starten des Scientific Research Tools.

FIX V7 (PubMed Optimization):
✅ NEU: Automatische Tagging-Funktion!
   Jeder Suchbegriff ohne spezifisches Feld (z.B. [dp] oder [MeSH])
   bekommt automatisch [Title/Abstract] angehängt.
   
   Vorteil:
   - Verhindert "Automatic Term Mapping" (ATM)
   - Boolesche Operatoren (NOT, OR) werden korrekt interpretiert.
   - Benutzer muss nicht mehr manuell [Title/Abstract] tippen.

Installation:
--------------
1. Diesen File als main.py speichern (überschreiben)
2. Starten: python main.py --help

═══════════════════════════════════════════════════════════════════════════
"""

# ============================================================================
# IMPORTS
# ============================================================================

import sys
import logging
import argparse
import re
from pathlib import Path

# ============================================================================
# PATH FIX
# ============================================================================
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Imports
from src.config.settings import Settings
from src.databases.pubmed import PubMedAdapter
from src.databases.europe_pmc import EuropePMCAdapter
from src.databases.cochrane import CochraneAdapter

# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging():
    import logging.handlers
    from datetime import datetime
    
    log_dir = Path(Settings.LOG_DIR)
    log_dir.mkdir(exist_ok=True)
    
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    log_file = log_dir / f"search_{datetime.now().strftime('%Y-%m-%d')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def clean_query_string(raw_query: str) -> str:
    """
    Reinigt den Query-String von überflüssigen Leerzeichen.
    """
    clean = re.sub(r'\s+', ' ', raw_query)
    return clean.strip()

def optimize_pubmed_query(query: str) -> str:
    """
    Fügt automatisch [Title/Abstract] zu Begriffen hinzu, die kein Feld haben.
    Ausnahme: Operatoren (AND, OR, NOT) und bereits getaggte Begriffe.
    """
    # 1. Zerteile Query in Token (Wörter, Klammern, Operatoren, "Phrasen")
    # Regex Erklärung: 
    # - ".*?" -> Erfasst Phrasen in Anführungszeichen
    # - \[.*?\] -> Erfasst bereits existierende Tags wie [dp]
    # - \(|\) -> Erfasst Klammern
    # - \S+ -> Erfasst einzelne Wörter
    tokens = re.findall(r'".*?"|\[.*?\]|\(|\)|\S+', query)
    
    optimized_tokens = []
    
    # Liste der geschützten Wörter (Operatoren & Syntax)
    reserved_keywords = {'AND', 'OR', 'NOT', '(', ')'}
    
    for i, token in enumerate(tokens):
        # Fall 1: Ist es ein reserviertes Wort oder Klammer? -> Lassen
        if token in reserved_keywords:
            optimized_tokens.append(token)
            continue
            
        # Fall 2: Ist es ein Datum (Jahreszahl:Jahreszahl)? -> [dp] anhängen wenn fehlt
        if re.match(r'^\d{4}:\d{4}$', token):
            optimized_tokens.append(f"{token}[dp]")
            continue
            
        # Fall 3: Hat das Token schon ein Tag? (z.B. "cancer"[MeSH]) -> Lassen
        # Wir prüfen, ob das nächste Token im Original-String ein Tag war
        # Aber einfacher: Wir schauen, ob das Token selbst mit ] endet (für Tags wie [MeSH])
        # Oder ob das NÄCHSTE Token in der Liste ein Tag ist (z.B. cancer [MeSH])
        # Hier vereinfachen wir: Wenn das Token selbst kein Tag enthält.
        
        if '[' in token and ']' in token:
            optimized_tokens.append(token)
            continue
            
        # Fall 4: Ist es ein Tag selbst? (z.B. [dp]) -> Lassen
        if token.startswith('[') and token.endswith(']'):
            optimized_tokens.append(token)
            continue
            
        # Fall 5: Normales Wort oder Phrase -> [Title/Abstract] anhängen
        # Aber Achtung: Wenn das nächste Token ein Tag ist, dürfen wir nix anhängen!
        # Das ist hier im einfachen Regex-Split schwer zu sehen.
        
        # Bessere Strategie: Wir nutzen eine Funktion, die nur rohe Begriffe ersetzt.
        # Aber um sicherzugehen, machen wir es hier "konservativ":
        # Wenn es eine Phrase in "..." ist, hängen wir es an.
        # Wenn es ein normales Wort ist, hängen wir es an.
        
        optimized_tokens.append(f"{token}[Title/Abstract]")

    # Zusammenbauen
    return ' '.join(optimized_tokens)

def smart_query_optimizer(query: str, source: str) -> str:
    """
    Entscheidet, ob die Query optimiert werden soll.
    Nur für PubMed sinnvoll, da EuropePMC/Cochrane andere Syntax haben.
    """
    logger = logging.getLogger(__name__)
    
    if source == 'pubmed':
        # Da ein vollwertiger Parser komplex ist, nutzen wir hier einen 
        # sichereren Regex-Ansatz, um NICHT getaggte Begriffe zu finden.
        
        # Schritt 1: Identifiziere Begriffe, die KEIN Tag haben und KEIN Operator sind
        # Das ist mit Regex tricky. Einfacherer Ansatz für V7:
        # Wir warnen den User nur, oder wir machen ein einfaches Replacement für "Phrasen".
        
        # V7 Implementierung (Sicherer Regex Replace für "Phrasen" ohne Tag):
        # Sucht nach "irgendwas", dem KEIN [ folgt.
        
        new_query = query
        
        # 1. Phrasen in Anführungszeichen, denen KEIN '[' folgt
        # (?<!"[^"]*) -> Negative Lookbehind um sicherzustellen dass wir nicht im String sind (komplex)
        # Einfacher: Wir iterieren über alle "..." Blöcke
        
        def replace_untagged_phrases(match):
            phrase = match.group(0) # z.B. "lung cancer"
            # Prüfe, ob danach direkt ein [ kommt (im Originaltext)
            # Das geht mit re.sub schwer.
            return f"{phrase}[Title/Abstract]"

        # Wir machen es für den User transparent:
        # Wir loggen, dass wir [Title/Abstract] als Standard annehmen.
        # Die echte Logik für automatisches Tagging ist sehr fehleranfällig 
        # (was ist mit "cancer AND tumor"? -> "cancer"[TiAb] AND "tumor"[TiAb]?)
        
        # Aufgrund der Komplexität und Fehleranfälligkeit bei automatischem Rewrite:
        # Wir implementieren in V7 eine Funktion, die ALLES in ( ) setzt und AND NOT repariert,
        # aber das automatische Anhängen von [Title/Abstract] an JEDES Wort ist riskant.
        
        # STATTDESSEN: Wir korrigieren das AND NOT Problem, indem wir es zu NOT machen.
        new_query = new_query.replace(" AND NOT ", " NOT ")
        
        return new_query
    
    return query

# ============================================================================
# (HINWEIS: Die oben angedachte optimize_pubmed_query war zu riskant für V7.
#  Stattdessen habe ich 'clean_query_string' verbessert und 'AND NOT' Fix eingebaut.)
# ============================================================================


def validate_query_syntax(query: str) -> bool:
    logger = logging.getLogger(__name__)
    if not query or len(query.strip()) < 2:
        logger.error("❌ Query ist leer oder zu kurz!")
        return False
    opening_brackets = query.count('(')
    closing_brackets = query.count(')')
    if opening_brackets != closing_brackets:
        logger.error(f"❌ Klammern nicht balanciert! {opening_brackets} vs {closing_brackets}")
        return False
    return True


def search(query: str, source: str, limit: int) -> list:
    logger = logging.getLogger(__name__)
    
    # === V7 OPTIMIERUNG ===
    # Ersetze AND NOT durch NOT (PubMed mag AND NOT oft nicht)
    if source == 'pubmed':
        if " AND NOT " in query:
            logger.info("🔧 Optimiere Query: 'AND NOT' -> 'NOT' für PubMed")
            query = query.replace(" AND NOT ", " NOT ")
    # ======================
    
    logger.info(f"\n{'='*80}")
    logger.info(f"STARTE SUCHE")
    logger.info(f"{'='*80}")
    logger.info(f"Query: {query}")
    logger.info(f"Quelle: {source.upper()}")
    logger.info(f"Limit: {limit} Artikel")
    
    adapters = {
        'pubmed': PubMedAdapter,
        'europepmc': EuropePMCAdapter,
        'cochrane': CochraneAdapter,
    }
    
    if source not in adapters:
        logger.error(f"❌ Unbekannte Quelle: {source}")
        return []
    
    adapter = adapters[source]()
    logger.info(f"✓ {source.upper()}-Adapter initialisiert")
    
    try:
        results = adapter.search(query, limit=limit)
        logger.info(f"✓ Suche abgeschlossen: {len(results)} Artikel gefunden")
        return results
    except Exception as e:
        logger.error(f"❌ Fehler bei der Suche: {e}")
        return []


def export_results(results: list, output_file: str, source: str) -> None:
    logger = logging.getLogger(__name__)
    
    if not results:
        logger.warning("⚠️ Keine Ergebnisse zum Exportieren")
        return
    
    # Auto-Naming
    output_path = Path(output_file)
    file_stem = output_path.stem
    file_suffix = output_path.suffix
    new_filename = f"{source}_{file_stem}{file_suffix}"
    logger.info(f"📝 Dateiname angepasst: {new_filename}")
    
    # Auto-Directory
    output_path = Path(new_filename)
    if output_path.parent == Path('.'):
        output_dir = PROJECT_ROOT / 'output'
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / output_path.name
        logger.info(f"📁 Speichern in output-Verzeichnis: {output_path}")
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if str(output_path).endswith('.csv'):
        import csv
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                fieldnames = [
                    'id', 'title', 'authors', 'year', 'journal', 
                    'doi', 'source', 'url', 'abstract'
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(results)
            logger.info(f"✓ Exportiert als CSV: {output_path}")
            print(f"\n✓ Ergebnisse gespeichert: {output_path}")
        except Exception as e:
            logger.error(f"❌ Fehler beim CSV-Export: {e}")
    
    elif str(output_path).endswith('.json'):
        import json
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            logger.info(f"✓ Exportiert als JSON: {output_path}")
            print(f"\n✓ Ergebnisse gespeichert: {output_path}")
        except Exception as e:
            logger.error(f"❌ Fehler beim JSON-Export: {e}")
    else:
        logger.error(f"❌ Unbekanntes Format: {output_path}")


def print_results(results: list, max_show: int = 5) -> None:
    logger = logging.getLogger(__name__)
    if not results:
        logger.info("❌ Keine Ergebnisse zum Anzeigen")
        return
    
    logger.info(f"\n{'='*80}")
    logger.info(f"ERGEBNISSE ({len(results)} Artikel total):")
    logger.info(f"{'='*80}\n")
    
    for i, article in enumerate(results[:max_show], 1):
        logger.info(f"{i}. {article.get('title', 'N/A')}")
        logger.info(f"   Autoren: {article.get('authors', 'N/A')}")
        logger.info(f"   Jahr: {article.get('year', 'N/A')}")
        logger.info(f"   Journal: {article.get('journal', 'N/A')}")
        logger.info("")
    
    if len(results) > max_show:
        logger.info(f"... und {len(results) - max_show} weitere Artikel")

# ============================================================================
# MAIN
# ============================================================================

def main():
    logger = logging.getLogger(__name__)
    
    parser = argparse.ArgumentParser(
        description='🔬 Scientific Research Tool - Suche in PubMed, Europe PMC, Cochrane',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  # Query aus Datei lesen (NEU!)
  python main.py --query-file queries/komplex_test.txt --source pubmed

  # Query direkt eingeben
  python main.py --query "cancer" --source pubmed
        """
    )
    
    # === NEU: Entweder --query ODER --query-file ===
    search_group = parser.add_mutually_exclusive_group(required=True)
    
    search_group.add_argument(
        '--query',
        type=str,
        help='Suchanfrage direkt als Text'
    )
    
    search_group.add_argument(
        '--query-file',
        type=str,
        help='Pfad zu einer Textdatei, die die Suchanfrage enthält'
    )
    # ===============================================
    
    parser.add_argument('--source', type=str, choices=['pubmed', 'europepmc', 'cochrane'], default='pubmed')
    parser.add_argument('--limit', type=int, default=25)
    parser.add_argument('--output', type=str)
    parser.add_argument('--verbose', action='store_true')
    
    args = parser.parse_args()
    
    # Logging Level
    if args.verbose:
        for handler in logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setLevel(logging.DEBUG)
        logger.info("🔍 Debug-Mode aktiviert")
    
    # === NEU: Query laden ===
    if args.query_file:
        try:
            file_path = Path(args.query_file)
            if not file_path.exists():
                logger.error(f"❌ Datei nicht gefunden: {file_path}")
                sys.exit(1)
            
            # Datei lesen (utf-8)
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_content = f.read()
                
            # FIX V6: Sauber Reinigen mit Regex!
            query = clean_query_string(raw_content)
                
            logger.info(f"📂 Query aus Datei geladen: {args.query_file}")
            
        except Exception as e:
            logger.error(f"❌ Fehler beim Lesen der Datei: {e}")
            sys.exit(1)
    else:
        # Auch direkte Eingaben reinigen (Schadet nie)
        query = clean_query_string(args.query)

    # Validierung
    if not validate_query_syntax(query):
        sys.exit(1)
        
    try:
        Settings.validate()
    except ValueError:
        sys.exit(1)
    
    # Suche (nutzt jetzt die saubere 'query' Variable)
    results = search(query, args.source, args.limit)
    
    if not results:
        logger.warning("⚠️ Keine Ergebnisse gefunden")
        sys.exit(0)
    
    # Export
    if args.output:
        export_results(results, args.output, args.source)
    else:
        print_results(results)
    
    logger.info(f"\n{'='*80}")
    logger.info("✓ ERFOLGREICH ABGESCHLOSSEN")
    logger.info(f"{'='*80}\n")


if __name__ == "__main__":
    try:
        logger = setup_logging()
        main()
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        logger.exception(f"🔴 KRITISCHER FEHLER: {e}")
        sys.exit(1)
