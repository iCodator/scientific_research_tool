"""
═══════════════════════════════════════════════════════════════════════════
SCIENTIFIC RESEARCH TOOL - Main Entry Point (VERSION 5 - FULLY DOCUMENTED)
═══════════════════════════════════════════════════════════════════════════

📚 ÜBERBLICK:
=============
Dies ist die aktuellste Version des Tools.
Neue Funktion in V5: Du kannst Suchanfragen aus Textdateien laden!

WARUM IST DAS NÜTZLICH?
-----------------------
Bei komplexen Suchen (viele Klammern, "Gänsefüßchen", OR/AND) kommt die 
Kommandozeile oft durcheinander. In einer Textdatei kannst du deine Query 
ganz entspannt schreiben, ohne Sorgen um technische Sonderzeichen.

VERWENDUNG:
===========
1. Textdatei erstellen: queries/meine_suche.txt
2. Tool starten:
   python main.py --query-file queries/meine_suche.txt --source pubmed

═══════════════════════════════════════════════════════════════════════════
"""

# ============================================================================
# 1. IMPORTS
# ============================================================================

import sys                      # Systemfunktionen (Beenden, Pfade)
import logging                  # Protokollierung (Logs schreiben)
import argparse                 # Terminal-Befehle verarbeiten
from pathlib import Path        # Einfacher Umgang mit Dateipfaden

# ============================================================================
# 2. PFAD-KONFIGURATION (WICHTIG!)
# ============================================================================
# Damit Python unsere eigenen Module im 'src' Ordner findet

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Jetzt können wir unsere eigenen "Bausteine" laden
from src.config.settings import Settings
from src.databases.pubmed import PubMedAdapter
from src.databases.europe_pmc import EuropePMCAdapter
from src.databases.cochrane import CochraneAdapter

# ============================================================================
# 3. LOGGING (PROTOKOLLIERUNG)
# ============================================================================

def setup_logging():
    """
    Richte das Tagebuch (Log) des Programms ein.
    Schreibt Fehler und Infos in eine Datei im 'logs/' Ordner UND auf den Schirm.
    """
    import logging.handlers
    from datetime import datetime
    
    # Ordner erstellen, falls nicht da
    log_dir = Path(Settings.LOG_DIR)
    log_dir.mkdir(exist_ok=True)
    
    # Wie soll eine Zeile im Log aussehen?
    # [Zeit] - [Modul] - [Wichtigkeit] - Nachricht
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG) # Alles aufzeichnen
    
    # 1. Schreiber für die DATEI
    log_file = log_dir / f"search_{datetime.now().strftime('%Y-%m-%d')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)
    
    # 2. Schreiber für den BILDSCHIRM (Konsole)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO) # Nur wichtige Infos zeigen
    console_handler.setFormatter(log_format)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# ============================================================================
# 4. HILFSFUNKTIONEN
# ============================================================================

def validate_query_syntax(query: str) -> bool:
    """
    Prüft, ob die Suchanfrage "sinnvoll" aussieht.
    Verhindert Fehler wie vergessene Klammern "((cancer".
    """
    logger = logging.getLogger(__name__)
    
    # Ist die Query leer?
    if not query or len(query.strip()) < 2:
        logger.error("❌ Query ist leer oder zu kurz!")
        return False
        
    # Klammern zählen
    opening_brackets = query.count('(')
    closing_brackets = query.count(')')
    
    # Müssen gleich viele sein
    if opening_brackets != closing_brackets:
        logger.error(f"❌ Klammern nicht balanciert! {opening_brackets} vs {closing_brackets}")
        return False
        
    return True


def search(query: str, source: str, limit: int) -> list:
    """
    Die eigentliche Suche.
    Verbindet sich mit der gewählten Datenbank (Source).
    """
    logger = logging.getLogger(__name__)
    
    # Info für den Benutzer
    logger.info(f"\n{'='*80}")
    logger.info(f"STARTE SUCHE")
    logger.info(f"{'='*80}")
    logger.info(f"Query: {query}")
    logger.info(f"Quelle: {source.upper()}")
    logger.info(f"Limit: {limit} Artikel")
    
    # Mapping: Welcher Name gehört zu welchem Programm-Code?
    adapters = {
        'pubmed': PubMedAdapter,
        'europepmc': EuropePMCAdapter,
        'cochrane': CochraneAdapter,
    }
    
    # Sicherheitscheck
    if source not in adapters:
        logger.error(f"❌ Unbekannte Quelle: {source}")
        return []
    
    # Adapter starten (z.B. PubMedAdapter())
    adapter = adapters[source]()
    logger.info(f"✓ {source.upper()}-Adapter initialisiert")
    
    try:
        # SUCHE AUSFÜHREN
        results = adapter.search(query, limit=limit)
        logger.info(f"✓ Suche abgeschlossen: {len(results)} Artikel gefunden")
        return results
    except Exception as e:
        logger.error(f"❌ Fehler bei der Suche: {e}")
        return []


def export_results(results: list, output_file: str, source: str) -> None:
    """
    Speichert die Ergebnisse in eine Datei.
    """
    logger = logging.getLogger(__name__)
    
    if not results:
        logger.warning("⚠️ Keine Ergebnisse zum Exportieren")
        return
    
    # --- AUTOMATISCHE NAMENSGEBUNG ---
    # Wir fügen die Quelle in den Namen ein.
    # Aus "daten.csv" wird "pubmed_daten.csv"
    output_path = Path(output_file)
    file_stem = output_path.stem      # "daten"
    file_suffix = output_path.suffix  # ".csv"
    new_filename = f"{source}_{file_stem}{file_suffix}"
    logger.info(f"📝 Dateiname angepasst: {new_filename}")
    
    # --- AUTOMATISCHER ORDNER ---
    # Wir speichern immer im 'output/' Ordner, wenn nichts anderes gesagt wird.
    output_path = Path(new_filename)
    if output_path.parent == Path('.'):
        output_dir = PROJECT_ROOT / 'output'
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / output_path.name
        logger.info(f"📁 Speichern in output-Verzeichnis: {output_path}")
    else:
        # Falls Benutzer einen eigenen Ordner angegeben hat, erstellen wir ihn
        output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # --- SPEICHERN ---
    if str(output_path).endswith('.csv'):
        import csv
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                # Spalten definieren
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
    """
    Zeigt Ergebnisse einfach auf dem Bildschirm an.
    """
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
# 5. MAIN (HAUPTPROGRAMM)
# ============================================================================

def main():
    logger = logging.getLogger(__name__)
    
    # Argumente definieren (was darf der Benutzer eingeben?)
    parser = argparse.ArgumentParser(
        description='🔬 Scientific Research Tool - Suche in PubMed, Europe PMC, Cochrane',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  # NEU in V5: Query aus Datei lesen (Besser für komplexe Suchen!)
  python main.py --query-file queries/komplex_test.txt --source pubmed

  # Query direkt eingeben (Für einfache Suchen)
  python main.py --query "cancer" --source pubmed
        """
    )
    
    # === NEUE LOGIK: Entweder Text ODER Datei ===
    # add_mutually_exclusive_group sorgt dafür, dass man nicht beides gleichzeitig nutzen kann.
    # required=True heißt: Eines von beiden MUSS angegeben werden.
    search_group = parser.add_mutually_exclusive_group(required=True)
    
    search_group.add_argument(
        '--query',
        type=str,
        help='Suchanfrage direkt als Text (z.B. --query "cancer")'
    )
    
    search_group.add_argument(
        '--query-file',
        type=str,
        help='Pfad zu einer Textdatei mit der Suchanfrage (z.B. --query-file queries/test.txt)'
    )
    # ============================================
    
    parser.add_argument('--source', type=str, choices=['pubmed', 'europepmc', 'cochrane'], default='pubmed')
    parser.add_argument('--limit', type=int, default=25)
    parser.add_argument('--output', type=str)
    parser.add_argument('--verbose', action='store_true')
    
    args = parser.parse_args()
    
    # Debug-Modus aktivieren?
    if args.verbose:
        for handler in logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setLevel(logging.DEBUG)
        logger.info("🔍 Debug-Mode aktiviert")
    
    # === QUERY VERARBEITUNG ===
    # Hier entscheiden wir, woher die Suchanfrage kommt.
    
    if args.query_file:
        # Fall A: Benutzer hat eine DATEI angegeben
        try:
            file_path = Path(args.query_file)
            
            # Existiert die Datei überhaupt?
            if not file_path.exists():
                logger.error(f"❌ Datei nicht gefunden: {file_path}")
                sys.exit(1)
            
            # Datei öffnen und lesen
            with open(file_path, 'r', encoding='utf-8') as f:
                # .read() liest den ganzen Text
                # .strip() entfernt leere Zeilen am Anfang/Ende
                # .replace() macht aus mehreren Zeilen eine lange Zeile (wichtig für APIs)
                query = f.read().strip().replace('\n', ' ')
                
            logger.info(f"📂 Query aus Datei geladen: {args.query_file}")
            
        except Exception as e:
            logger.error(f"❌ Fehler beim Lesen der Datei: {e}")
            sys.exit(1)
            
    else:
        # Fall B: Benutzer hat TEXT direkt eingegeben
        query = args.query

    # Validierung (Klammern prüfen etc.)
    if not validate_query_syntax(query):
        sys.exit(1)
        
    # Settings prüfen (.env)
    try:
        Settings.validate()
    except ValueError:
        sys.exit(1)
    
    # === SUCHE STARTEN ===
    # Wir übergeben die 'query' Variable, egal woher sie kam
    results = search(query, args.source, args.limit)
    
    if not results:
        logger.warning("⚠️ Keine Ergebnisse gefunden")
        sys.exit(0)
    
    # === ERGEBNISSE AUSGEBEN ===
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
        # Falls Benutzer Ctrl+C drückt
        sys.exit(130)
    except Exception as e:
        # Falls ein unerwarteter Fehler passiert
        logger.exception(f"🔴 KRITISCHER FEHLER: {e}")
        sys.exit(1)
