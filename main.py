"""
═══════════════════════════════════════════════════════════════════════════
SCIENTIFIC RESEARCH TOOL - Main Entry Point (FULLY DOCUMENTED VERSION)
═══════════════════════════════════════════════════════════════════════════

📚 ÜBERBLICK FÜR ANFÄNGER:
==========================

Dieses Programm ermöglicht es dir, wissenschaftliche Artikel zu suchen in:
  ✅ PubMed (Medizin & Life Sciences)
  ✅ Europe PMC (Biomedizin & Forschung)
  ✅ Cochrane (Systematische Übersichtsarbeiten)

Die Suchergebnisse können exportiert werden als:
  📄 CSV-Dateien (für Excel/Calc)
  📊 JSON-Dateien (für weitere Verarbeitung)

VERWENDUNGSBEISPIELE:
====================
# Im Terminal eingeben:
python main.py --query "COVID-19" --source pubmed --limit 50 --output results.csv
→ Sucht 50 Artikel über COVID-19 in PubMed, speichert in output/pubmed_results.csv

python main.py --query "cancer treatment" --source europepmc --output data.json
→ Sucht nach Krebsbehandlung in Europe PMC, speichert als JSON

═══════════════════════════════════════════════════════════════════════════
"""

# ============================================================================
# SCHRITT 1: IMPORTS - Was das Programm benötigt
# ============================================================================
# Ein "Import" ist wie das Bestellen einer Bibliothek mit speziellen Werkzeugen
# Jede Zeile unten sagt dem Programm: "Ich brauche diese spezielle Funktion"

import sys                      # Für System-Funktionen (z.B. Programm beenden)
import logging                  # Für Protokollierung (Logs schreiben)
import argparse                 # Für Terminal-Befehle (--query, --output, etc.)
from pathlib import Path        # Für Dateipfade (Ordner & Dateien)

# ============================================================================
# SCHRITT 2: PFAD-KONFIGURATION
# ============================================================================
# Problem: Python findet manchmal unsere 'src' Ordner nicht
# Lösung: Sagen wir Python explizit, wo es suchen soll

PROJECT_ROOT = Path(__file__).resolve().parent
# ↑ Findet den Ordner, in dem dieses Skript liegt (z.B. /home/user/my_project/)

if str(PROJECT_ROOT) not in sys.path:
    # Falls dieser Pfad noch nicht bekannt ist...
    sys.path.insert(0, str(PROJECT_ROOT))
    # ...füge ihn GANZ OBEN zur Suchliste hinzu (wichtig: ganz oben!)

# ============================================================================
# SCHRITT 3: IMPORTS UNSERER EIGENEN MODULE
# ============================================================================
# Diese Module befinden sich in unserem src/ Ordner
# Sie sind die "Intelligenz" des Programms

from src.config.settings import Settings
# ↑ Lädt die Konfigurationsdatei (.env) mit API-Keys und Einstellungen

from src.core.query_detector import QueryDetector, QueryType
# ↑ Erkennt, ob eine Suchanfrage "einfach" oder "kompliziert" ist
# Beispiel: "cancer" = einfach, "(cancer AND 2020:2025)" = kompliziert

from src.core.query_validator import QueryValidator
# ↑ Überprüft, ob eine Suchanfrage syntaktisch richtig ist
# Überprüft z.B.: Sind alle Klammern geschlossen? "(cancer AND" ❌

from src.databases.pubmed import PubMedAdapter
# ↑ Das "Bindeglied" zu PubMed
# Wenn wir PubMed durchsuchen wollen, verwenden wir dieses Modul

from src.databases.europe_pmc import EuropePMCAdapter
# ↑ Das "Bindeglied" zu Europe PMC

from src.databases.cochrane import CochraneAdapter
# ↑ Das "Bindeglied" zu Cochrane

# ============================================================================
# FUNKTION: setup_logging()
# ============================================================================
# WOZU: Protokollierung einrichten
# BEDEUTUNG: Alles was das Programm macht wird protokolliert (gespeichert)
# 
# BEISPIEL WAS PROTOKOLLIERT WIRD:
# [09:55:22] Suche gestartet mit Query: "covid"
# [09:55:23] ✓ 50 Artikel gefunden
# [09:55:24] ✓ Datei gespeichert: output/pubmed_results.csv

def setup_logging():
    """
    Richte Protokollierung (Logging) ein.
    
    Das Programm schreibt ALLES auf:
    - Wenn eine Suche startet
    - Wenn Fehler passieren
    - Wo Dateien gespeichert werden
    - Wie lange etwas dauert
    
    Diese Informationen werden gesammelt in:
    1. Datei: logs/search_YYYY-MM-DD.log (auf der Festplatte gespeichert)
    2. Bildschirm: Konsolen-Output (du siehst es während das Programm läuft)
    """
    
    import logging.handlers
    from datetime import datetime
    
    # Schritt 1: Erstelle das logs/ Verzeichnis, falls es nicht existiert
    log_dir = Path(Settings.LOG_DIR)
    # ↑ LOG_DIR ist definiert in settings.py (normalerweise: ./logs/)
    
    log_dir.mkdir(exist_ok=True)
    # ↑ Erstelle den Ordner
    # exist_ok=True bedeutet: Wenn der Ordner schon existiert, kein Fehler
    
    # Schritt 2: Definiere das Format der Log-Meldungen
    # Format erklär: [Zeit] [Programm-Teil] [Fehlertyp] Nachricht
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # Beispiel für echte Log-Zeile:
    # 2025-12-09 09:55:22 - __main__ - INFO - ✓ Suche abgeschlossen
    
    # Schritt 3: Erstelle den "Haupt-Logger" (zentrale Verwaltung aller Logs)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # ↑ DEBUG = Akzeptiere ALLES (auch sehr detaillierte Informationen)
    
    # Schritt 4: Logger für DATEIEN-Speicherung
    log_file = log_dir / f"search_{datetime.now().strftime('%Y-%m-%d')}.log"
    # ↑ Dateiname mit Datum, z.B.: search_2025-12-09.log
    
    file_handler = logging.FileHandler(log_file)
    # ↑ "Handler" = Kümmerer, der Logs in Dateien schreibt
    
    file_handler.setLevel(logging.DEBUG)
    # ↑ Speichere ALLES in der Datei (auch DEBUG-Infos)
    
    file_handler.setFormatter(log_format)
    # ↑ Verwende obiges Format für die Datei
    
    # Schritt 5: Logger für BILDSCHIRM-Ausgabe (Konsole)
    console_handler = logging.StreamHandler()
    # ↑ "Handler" = Kümmerer, der Logs auf dem Bildschirm anzeigt
    
    console_handler.setLevel(logging.INFO)
    # ↑ Auf dem Bildschirm nur INFO und wichtigere Meldungen
    # (nicht DEBUG, weil das zu viel würde)
    
    console_handler.setFormatter(log_format)
    # ↑ Verwende obiges Format für die Bildschirm-Ausgabe
    
    # Schritt 6: Verbinde beide Handler mit dem Haupt-Logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    # ↑ Jetzt werden Logs in BEIDE Richtungen geschrieben:
    # In die Datei UND auf den Bildschirm
    
    return logger
    # ↑ Gib den Logger zurück, damit andere Funktionen ihn verwenden können


# ============================================================================
# FUNKTION: validate_query_syntax()
# ============================================================================
# WOZU: Überprüfe, ob die Suchanfrage richtig formatiert ist
# BEDEUTUNG: Verhindert fehlerhafte Suchen
#
# BEISPIELE GÜLTIGE QUERIES:
# ✅ "cancer"
# ✅ "(cancer AND tumor)"
# ✅ "(cancer OR tumor) AND (2020:2025)"
#
# BEISPIELE UNGÜLTIGE QUERIES:
# ❌ "" (leer)
# ❌ "a" (zu kurz, nur 1 Zeichen)
# ❌ "(cancer AND tumor" (schließende Klammer fehlt)

def validate_query_syntax(query: str) -> bool:
    """
    Überprüfe, ob die Query syntaktisch korrekt ist.
    
    Diese Funktion prüft:
    1. Ist die Query nicht leer?
    2. Hat die Query mindestens 2 Zeichen?
    3. Sind alle Klammern balanciert? ( = )
    
    Args:
        query (str): Die Suchanfrage (z.B. "cancer AND tumor")
    
    Returns:
        bool: True wenn OK, False wenn Fehler
    """
    
    logger = logging.getLogger(__name__)
    # ↑ Hole den Logger, um Meldungen zu protokollieren
    
    # CHECK 1: Ist die Query leer oder zu kurz?
    if not query or len(query.strip()) < 2:
        # not query = True wenn query leer ist
        # len(query.strip()) < 2 = True wenn weniger als 2 Zeichen
        # .strip() = Entfernt Leerzeichen am Anfang/Ende
        
        logger.error("❌ Query ist leer oder zu kurz!")
        return False
        # ↑ Fehler! Gib False zurück (nicht valid)
    
    # CHECK 2: Sind die Klammern balanciert?
    opening_brackets = query.count('(')
    # ↑ Zähle, wie viele öffnende Klammern es gibt
    
    closing_brackets = query.count(')')
    # ↑ Zähle, wie viele schließende Klammern es gibt
    
    if opening_brackets != closing_brackets:
        # Wenn die Zahlen nicht gleich sind...
        
        logger.error(f"❌ Klammern nicht balanciert! {opening_brackets} vs {closing_brackets}")
        return False
        # ↑ Fehler! Gib False zurück
    
    # Wenn wir bis hier gekommen sind, ist alles in Ordnung
    return True
    # ↑ Erfolg! Query ist valid


# ============================================================================
# FUNKTION: search()
# ============================================================================
# WOZU: Führe die eigentliche Datenbank-Suche durch
# BEDEUTUNG: Das Kernstück des Programms - hier passiert die Magie!
#
# SCHRITTE:
# 1. Log-Meldung schreiben (Was wird gesucht?)
# 2. Richtigen Adapter wählen (PubMed/Europe PMC/Cochrane)
# 3. Suche durchführen
# 4. Ergebnisse zurückgeben

def search(query: str, source: str, limit: int) -> list:
    """
    Führe eine Suche in der angegebenen Datenbank aus.
    
    Diese Funktion:
    1. Wählt die richtige Datenbank (PubMed, Europe PMC oder Cochrane)
    2. Verbindet sich mit der Datenbank-API
    3. Sendet die Suchanfrage
    4. Sammelt die Ergebnisse
    5. Gibt sie zurück als Liste
    
    Args:
        query (str): Die Suchanfrage (z.B. "COVID-19 vaccine")
        source (str): Welche Datenbank (pubmed, europepmc, cochrane)
        limit (int): Wie viele Artikel maximal zurückgeben (z.B. 50)
    
    Returns:
        list: Liste mit Artikel-Daten
              Jeder Artikel ist ein Dictionary mit:
              {
                  'id': '12345',
                  'title': 'Artikel-Titel',
                  'authors': 'Author 1, Author 2',
                  'year': 2025,
                  'journal': 'Journal Name',
                  'doi': '10.1234/xyz',
                  'source': 'pubmed',
                  'url': 'https://...',
                  'abstract': 'Zusammenfassung...'
              }
    
    Beispiel-Verwendung:
        results = search("cancer", "pubmed", 10)
        # Gibt Liste mit 10 Artikel-Dictionaries zurück
    """
    
    logger = logging.getLogger(__name__)
    
    # Schritt 1: Schöne Log-Trennlinie und Info ausgeben
    logger.info(f"\n{'='*80}")
    logger.info(f"STARTE SUCHE")
    logger.info(f"{'='*80}")
    logger.info(f"Query: {query}")
    logger.info(f"Quelle: {source.upper()}")
    logger.info(f"Limit: {limit} Artikel")
    # ↑ Das hilft später beim Debugging zu sehen, was gesucht wurde
    
    # Schritt 2: Definiere die verfügbaren Adapter (Datenbank-Verbindungen)
    adapters = {
        'pubmed': PubMedAdapter,
        # ↑ Wenn Benutzer "pubmed" angibt, verwende PubMedAdapter
        
        'europepmc': EuropePMCAdapter,
        # ↑ Wenn Benutzer "europepmc" angibt, verwende EuropePMCAdapter
        
        'cochrane': CochraneAdapter,
        # ↑ Wenn Benutzer "cochrane" angibt, verwende CochraneAdapter
    }
    
    # Schritt 3: Überprüfe, ob die gewählte Quelle existiert
    if source not in adapters:
        # Falls Benutzer etwas Falsches eingegeben hat (z.B. "google")...
        
        logger.error(f"❌ Unbekannte Quelle: {source}")
        logger.error(f"   Erlaubte Quellen: {', '.join(adapters.keys())}")
        return []
        # ↑ Gib leere Liste zurück (keine Ergebnisse)
    
    # Schritt 4: Erstelle eine Instanz des richtigen Adapters
    adapter = adapters[source]()
    # Beispiel: adapters['pubmed']() = erstellt ein PubMedAdapter-Objekt
    
    logger.info(f"✓ {source.upper()}-Adapter initialisiert")
    # ↑ Melde, dass wir erfolgreich verbunden sind
    
    # Schritt 5: Führe die Suche durch (IN TRY-EXCEPT für Fehlerbehandlung)
    try:
        # "try" = Versuche folgendes zu machen
        
        results = adapter.search(query, limit=limit)
        # ↑ Rufe die search()-Methode des Adapters auf
        # Das ist wie: "Sag der Datenbank, dass sie suchen soll"
        
        logger.info(f"✓ Suche abgeschlossen: {len(results)} Artikel gefunden")
        # ↑ Melde, wie viele Artikel gefunden wurden
        
        return results
        # ↑ Gib die Ergebnisse zurück
        
    except Exception as e:
        # "except" = Falls etwas schief geht (z.B. Internet-Problem)...
        
        logger.error(f"❌ Fehler bei der Suche: {e}")
        # ↑ Melde den Fehler
        
        return []
        # ↑ Gib leere Liste zurück (keine Ergebnisse wegen Fehler)


# ============================================================================
# FUNKTION: export_results()
# ============================================================================
# WOZU: Speichere Suchergebnisse als CSV oder JSON Datei
# BEDEUTUNG: Damit der Benutzer die Ergebnisse verwenden kann
#
# DATEIFORMATE:
# CSV = Tabellen-Format (öffnen mit Excel, Calc, etc.)
# JSON = Struktur-Format (für weitere Verarbeitung mit Programmen)

def export_results(results: list, output_file: str, source: str) -> None:
    """
    Exportiere Suchergebnisse in eine Datei (CSV oder JSON).
    
    Diese Funktion:
    1. Überprüft, ob es Ergebnisse gibt
    2. Fügt den Datenbankname in den Dateinamen ein
       (z.B. "results.csv" → "pubmed_results.csv")
    3. Erstellt das output/ Verzeichnis, falls nicht vorhanden
    4. Speichert die Datei im richtigen Format
    
    Args:
        results (list): Die Artikel-Liste (von der search() Funktion)
        output_file (str): Dateiname (z.B. "results.csv" oder "data.json")
        source (str): Name der Datenbank (pubmed, europepmc, cochrane)
    
    Beispiel-Verwendung:
        export_results(results, "results.csv", "pubmed")
        # Speichert in: output/pubmed_results.csv
    """
    
    logger = logging.getLogger(__name__)
    # ↑ Hole den Logger
    
    # CHECK: Gibt es überhaupt Ergebnisse?
    if not results:
        # Falls results leer ist...
        
        logger.warning("⚠️ Keine Ergebnisse zum Exportieren")
        return
        # ↑ Beende die Funktion (es gibt nichts zu speichern)
    
    # ========================================================================
    # SCHRITT 1: Datenbankname in den Dateinamen einfügen
    # ========================================================================
    # Beispiel:
    # Eingabe: "results.csv", source="pubmed"
    # Ausgabe: "pubmed_results.csv"
    
    output_path = Path(output_file)
    # ↑ Konvertiere String in Path-Objekt (für bessere Dateiverwaltung)
    
    file_stem = output_path.stem
    # ↑ Hole den Namen ohne Extension
    # Beispiel: "results.csv" → "results"
    
    file_suffix = output_path.suffix
    # ↑ Hole nur die Extension
    # Beispiel: "results.csv" → ".csv"
    
    new_filename = f"{source}_{file_stem}{file_suffix}"
    # ↑ Füge alles zusammen
    # Beispiel: "pubmed" + "_" + "results" + ".csv" = "pubmed_results.csv"
    
    logger.info(f"📝 Dateiname angepasst: {new_filename}")
    # ↑ Melde den neuen Dateinamen
    
    # ========================================================================
    # SCHRITT 2: Stelle sicher, dass die Datei im output/ Verzeichnis landet
    # ========================================================================
    
    output_path = Path(new_filename)
    # ↑ Konvertiere neuen Dateinamen zu Path
    
    # Falls Benutzer nur einen Namen gab (z.B. "results.csv")
    # und nicht "output/results.csv" oder "custom/results.csv"...
    
    if output_path.parent == Path('.'):
        # output_path.parent = der Ordner (z.B. "output" oder ".")
        # Path('.') = das aktuelle Verzeichnis
        # Also: Falls der Benutzer kein Verzeichnis angegeben hat...
        
        output_dir = PROJECT_ROOT / 'output'
        # ↑ Erstelle den Pfad: /home/user/project/output/
        
        output_dir.mkdir(exist_ok=True)
        # ↑ Erstelle den output/ Ordner, falls nicht vorhanden
        # exist_ok=True = Kein Fehler, falls Ordner schon existiert
        
        output_path = output_dir / output_path.name
        # ↑ Neue vollständige Pfad: output/pubmed_results.csv
        
        logger.info(f"📁 Speichern in output-Verzeichnis: {output_path}")
        # ↑ Melde den endgültigen Pfad
        
    else:
        # Falls Benutzer einen eigenen Ordner angegeben hat...
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        # ↑ Erstelle alle nötigen Ordner automatisch
        # parents=True = Erstelle auch Überordner, falls nötig
    
    # ========================================================================
    # SCHRITT 3: Speichere die Datei (CSV oder JSON)
    # ========================================================================
    
    if str(output_path).endswith('.csv'):
        # Falls die Datei mit .csv endet...
        
        import csv
        # ↑ Importiere das CSV-Modul
        
        try:
            # Versuche, die CSV-Datei zu schreiben
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                # ↑ Öffne eine neue Datei zum Schreiben
                # 'w' = write (schreiben)
                # newline='' = Windows/Mac/Linux kompatibel
                # encoding='utf-8' = Unicode für Umlaute/Sonderzeichen
                
                # Definiere die Spalten der Tabelle
                fieldnames = [
                    'id',          # Artikel-ID (z.B. PMID für PubMed)
                    'title',       # Titel des Artikels
                    'authors',     # Autoren (komma-getrennt)
                    'year',        # Publikationsjahr
                    'journal',     # Name des Journals
                    'doi',         # Digital Object Identifier (eindeutige ID)
                    'source',      # Von welcher Datenbank (pubmed, europepmc, etc.)
                    'url',         # Link zum Artikel online
                    'abstract',    # Zusammenfassung des Artikels
                ]
                
                writer = csv.DictWriter(
                    f,
                    fieldnames=fieldnames,
                    extrasaction='ignore'
                    # ↑ 'ignore' = Falls ein Artikel ein Feld hat, das nicht in
                    # fieldnames ist, ignoriere es einfach (stürze nicht ab)
                )
                
                writer.writeheader()
                # ↑ Schreibe die Kopfzeile (id, title, authors, ...)
                
                writer.writerows(results)
                # ↑ Schreibe alle Artikel-Zeilen
            
            logger.info(f"✓ Exportiert als CSV: {output_path}")
            print(f"\n✓ Ergebnisse gespeichert: {output_path}")
            # ↑ Melde Erfolg (in Datei und auf Bildschirm)
            
        except Exception as e:
            # Falls beim Schreiben etwas schief geht...
            
            logger.error(f"❌ Fehler beim CSV-Export: {e}")
            # ↑ Melde den Fehler
    
    elif str(output_path).endswith('.json'):
        # Falls die Datei mit .json endet...
        
        import json
        # ↑ Importiere das JSON-Modul
        
        try:
            # Versuche, die JSON-Datei zu schreiben
            
            with open(output_path, 'w', encoding='utf-8') as f:
                # ↑ Öffne eine neue Datei zum Schreiben
                
                json.dump(
                    results,           # Was soll gespeichert werden?
                    f,                 # In welche Datei?
                    indent=2,          # Mit 2-Leerzeichen Einrückung (lesbar)
                    ensure_ascii=False # Unterstütze Umlaute (ö, ä, ü, etc.)
                )
            
            logger.info(f"✓ Exportiert als JSON: {output_path}")
            print(f"\n✓ Ergebnisse gespeichert: {output_path}")
            # ↑ Melde Erfolg
            
        except Exception as e:
            # Falls beim Schreiben etwas schief geht...
            
            logger.error(f"❌ Fehler beim JSON-Export: {e}")
            # ↑ Melde den Fehler
    
    else:
        # Falls die Datei weder .csv noch .json ist...
        
        logger.error(f"❌ Unbekanntes Format: {output_path}")
        logger.error(f"   Unterstützte Formate: .csv, .json")
        # ↑ Melde welche Formate unterstützt werden


# ============================================================================
# FUNKTION: print_results()
# ============================================================================
# WOZU: Zeige die Suchergebnisse auf dem Bildschirm an
# BEDEUTUNG: Wenn Benutzer NICHT exportiert, wollen sie die Ergebnisse sehen

def print_results(results: list, max_show: int = 5) -> None:
    """
    Zeige die ersten Ergebnisse in der Konsole an (auf dem Bildschirm).
    
    Diese Funktion:
    1. Überprüft, ob es Ergebnisse gibt
    2. Zeigt die ersten N Artikel (Standard: 5)
    3. Gibt eine Vorschau der wichtigsten Infos
    
    Args:
        results (list): Die Artikel-Liste
        max_show (int): Wie viele Artikel anzeigen (Standard: 5)
    
    Beispiel-Output:
    ================================================================================
    ERGEBNISSE (50 Artikel total):
    ================================================================================
    
    1. COVID-19 Vaccine Efficacy: A Systematic Review
       Autoren: Smith J, Johnson K, Williams M
       Jahr: 2024
       Journal: Nature Medicine
    
    2. SARS-CoV-2 Variants of Concern
       Autoren: Brown A, Davis L
       Jahr: 2024
       Journal: The Lancet
    
    ... und 48 weitere Artikel
    """
    
    logger = logging.getLogger(__name__)
    
    # CHECK: Gibt es überhaupt Ergebnisse?
    if not results:
        # Falls results leer ist...
        
        logger.info("❌ Keine Ergebnisse zum Anzeigen")
        return
        # ↑ Beende die Funktion
    
    # Schöne Kopfzeile mit Separator
    logger.info(f"\n{'='*80}")
    logger.info(f"ERGEBNISSE ({len(results)} Artikel total):")
    logger.info(f"{'='*80}\n")
    # ↑ {len(results)} = Wie viele Artikel wurden gefunden?
    
    # Schleife: Für jeden Artikel (aber nur die ersten max_show)
    for i, article in enumerate(results[:max_show], 1):
        # enumerate() = Zählt automatisch (1, 2, 3, ...)
        # results[:max_show] = Nur die ersten 5 Artikel
        # Beispiel: enumerate(['a', 'b', 'c'], 1) → (1, 'a'), (2, 'b'), (3, 'c')
        
        # Zeige Titel
        logger.info(f"{i}. {article.get('title', 'N/A')}")
        # ↑ article.get('title', 'N/A') = Hole das Feld 'title'
        # Falls nicht vorhanden, zeige 'N/A' (Not Available)
        
        # Zeige Autoren
        logger.info(f"   Autoren: {article.get('authors', 'N/A')}")
        
        # Zeige Jahr
        logger.info(f"   Jahr: {article.get('year', 'N/A')}")
        
        # Zeige Journal
        logger.info(f"   Journal: {article.get('journal', 'N/A')}")
        
        logger.info("")  # Leere Zeile (für bessere Lesbarkeit)
    
    # Falls es mehr Artikel gibt, als wir zeigen...
    if len(results) > max_show:
        # Falls z.B. 50 Artikel insgesamt, aber nur 5 gezeigt...
        
        remaining = len(results) - max_show
        # ↑ Wie viele Artikel werden NICHT gezeigt? 50 - 5 = 45
        
        logger.info(f"... und {remaining} weitere Artikel")
        # ↑ "... und 45 weitere Artikel"


# ============================================================================
# FUNKTION: main()
# ============================================================================
# WOZU: Das Hauptprogramm - orchestriert alles
# BEDEUTUNG: Diese Funktion wird aufgerufen, wenn das Skript startet
#
# ABLAUF:
# 1. Parse Terminal-Befehle (--query, --output, etc.)
# 2. Validiere die Eingaben
# 3. Führe Suche durch
# 4. Exportiere oder zeige Ergebnisse

def main():
    """
    Das Hauptprogramm - die zentrale Steuerung.
    
    Wenn du das Skript startest, wird diese Funktion aufgerufen.
    Sie koordiniert alle anderen Funktionen.
    
    Terminal-Befehle (die der Benutzer eingeben kann):
    ===================================================
    
    python main.py --help
        → Zeige alle verfügbaren Optionen
        Ausgabe: Hilfetext mit allen --flags
    
    python main.py --query "cancer" --source pubmed --limit 20
        → Suche 20 Artikel über "cancer" in PubMed
        → Zeige Ergebnisse auf dem Bildschirm
    
    python main.py --query "covid" --source europepmc --output results.csv
        → Suche nach "covid" in Europe PMC
        → Speichere in: output/europepmc_results.csv
    
    python main.py --query "diabetes" --source pubmed --output data.json --verbose
        → Suche nach "diabetes" in PubMed
        → Speichere als JSON
        → Zeige DEBUG-Informationen (sehr ausführlich)
    """
    
    logger = logging.getLogger(__name__)
    
    # ========================================================================
    # SCHRITT 1: PARSE TERMINAL-ARGUMENTE
    # ========================================================================
    # "Argumente" sind die Befehle, die der Benutzer eingibt
    # Beispiel: python main.py --query "cancer" --source pubmed
    #           ↑ Programmname        ↑ Argument 1    ↑ Argument 2
    
    parser = argparse.ArgumentParser(
        description='🔬 Scientific Research Tool - Suche in PubMed, Europe PMC, Cochrane',
        # ↑ Das wird angezeigt wenn Benutzer --help eingibt
        
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # ↑ Erlaubt Multi-Zeilen Text in der Hilfe
        
        epilog="""
Beispiele (Copy & Paste zum Testen):
  
  # Einfache Suche (Ergebnisse nur auf Bildschirm)
  python main.py --query "cancer" --source pubmed --limit 20
  
  # Mit Export als CSV (speichert in output/pubmed_results.csv)
  python main.py --query "covid AND vaccine" --source europepmc --limit 100 --output results.csv
  
  # Mit Export als JSON (speichert in output/pubmed_results.json)
  python main.py --query "diabetes AND treatment" --source pubmed --output results.json
  
  # Cochrane Suche
  python main.py --query "aspirin AND headache" --source cochrane --limit 10

Unterstützte Datenbanken:
  pubmed       → Medizin & Life Sciences (USA)
  europepmc    → Biomedizin & Forschung (Europa)
  cochrane     → Systematische Reviews & klinische Studien

Wichtig: 
  - Output-Dateien werden automatisch im output/ Verzeichnis gespeichert
  - Der Name der Datenbank wird automatisch eingefügt
    (z.B. results.csv → pubmed_results.csv)
        """
    )
    
    # Definiere alle möglichen Terminal-Optionen (--flags)
    
    parser.add_argument(
        '--query',
        type=str,
        required=True,
        # ↑ ERFORDERLICH - Benutzer MUSS dies angeben
        
        help='Suchanfrage (erforderlich) - z.B. "cancer" oder "(cancer AND 2020:2025)"'
    )
    # Beispiel: --query "COVID-19 vaccine"
    
    parser.add_argument(
        '--source',
        type=str,
        choices=['pubmed', 'europepmc', 'cochrane'],
        # ↑ NUR diese drei Werte sind erlaubt
        
        default='pubmed',
        # ↑ Falls Benutzer nichts angibt, verwende 'pubmed'
        
        help='Datenbank (Standard: pubmed)'
    )
    # Beispiel: --source europepmc
    
    parser.add_argument(
        '--limit',
        type=int,
        # ↑ Eingabe muss eine Ganzzahl sein
        
        default=25,
        # ↑ Falls nicht angegeben, 25 Artikel
        
        help='Maximale Anzahl Artikel (Standard: 25, Max: 1000)'
    )
    # Beispiel: --limit 50
    
    parser.add_argument(
        '--output',
        type=str,
        help='Speichern in Datei (.csv oder .json) - z.B. results.csv'
    )
    # Beispiel: --output results.csv
    # Falls nicht angegeben, wird auf dem Bildschirm angezeigt
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        # ↑ 'store_true' = True falls Benutzer --verbose eingibt, sonst False
        
        help='Zeige DEBUG-Ausgaben (sehr ausführlich)'
    )
    # Beispiel: --verbose
    # Ohne Wert, einfach nur das Flag
    
    # Schritt 2: Parse die Argumente
    args = parser.parse_args()
    # ↑ Lese was der Benutzer eingegeben hat
    # Jetzt können wir args.query, args.source, etc. verwenden
    
    # ========================================================================
    # SCHRITT 2: PASSE LOGGING-LEVEL AN
    # ========================================================================
    
    if args.verbose:
        # Falls Benutzer --verbose angegeben hat...
        
        for handler in logger.handlers:
            # Für jeden Handler (Datei und Konsole)...
            
            if isinstance(handler, logging.StreamHandler):
                # Falls es die Konsole ist (nicht die Datei)...
                
                handler.setLevel(logging.DEBUG)
                # ↑ Zeige ALLES (auch DEBUG-Infos)
        
        logger.info("🔍 Debug-Mode aktiviert (verbose)")
        # ↑ Melde, dass Debug-Mode an ist
    
    # ========================================================================
    # SCHRITT 3: VALIDIERE DIE QUERY
    # ========================================================================
    
    logger.info(f"\n{'='*80}")
    logger.info(f"QUERY-VALIDIERUNG")
    logger.info(f"{'='*80}")
    # ↑ Schöne Kopfzeile
    
    if not validate_query_syntax(args.query):
        # Rufe die validate_query_syntax() Funktion auf
        # Falls sie False zurückgibt (Query ungültig)...
        
        logger.error("❌ Query-Validierung fehlgeschlagen!")
        sys.exit(1)
        # ↑ Beende das Programm mit Fehlercode 1
    
    logger.info("✓ Query-Validierung erfolgreich")
    # ↑ Query ist gültig, weiter geht's
    
    # ========================================================================
    # SCHRITT 4: VALIDIERE EINSTELLUNGEN
    # ========================================================================
    # Überprüfe, ob die .env Datei korrekt ist, API-Keys vorhanden, etc.
    
    try:
        # Versuche die Settings zu validieren
        
        Settings.validate()
        # ↑ Rufe die validate() Methode auf
        
    except ValueError as e:
        # Falls etwas mit den Settings nicht stimmt...
        
        logger.error(f"❌ Konfigurationsfehler: {e}")
        sys.exit(1)
        # ↑ Beende das Programm
    
    # ========================================================================
    # SCHRITT 5: FÜHRE SUCHE DURCH
    # ========================================================================
    
    results = search(args.query, args.source, args.limit)
    # ↑ Rufe die search() Funktion auf
    # Sie gibt eine Liste mit Artikel-Dictionaries zurück
    
    # ========================================================================
    # SCHRITT 6: VERARBEITE ERGEBNISSE
    # ========================================================================
    
    if not results:
        # Falls search() eine leere Liste zurückgab (keine Artikel gefunden)...
        
        logger.warning("⚠️ Keine Ergebnisse gefunden")
        sys.exit(0)
        # ↑ Beende das Programm sauber (Fehlercode 0 = Erfolg)
    
    # Jetzt haben wir Ergebnisse. Was tun damit?
    
    if args.output:
        # Falls Benutzer --output angegeben hat (z.B. --output results.csv)...
        
        export_results(results, args.output, args.source)
        # ↑ Speichere die Ergebnisse in einer Datei
        
    else:
        # Falls Benutzer KEIN --output angegeben hat...
        
        print_results(results, max_show=5)
        # ↑ Zeige die Ergebnisse auf dem Bildschirm (nur 5 Stück)
    
    # ========================================================================
    # SCHRITT 7: ABSCHLUSSMELDUNG
    # ========================================================================
    
    logger.info(f"\n{'='*80}")
    logger.info("✓ ERFOLGREICH ABGESCHLOSSEN")
    logger.info(f"{'='*80}\n")
    # ↑ Schöne Abschlussmeldung


# ============================================================================
# ENTRY POINT - Programm-Start
# ============================================================================
# Diese Sektion wird ausgeführt wenn das Skript gestartet wird
# Sie ist nicht in einer Funktion, sondern auf "Top-Level"

if __name__ == "__main__":
    # ↑ if __name__ == "__main__" heißt:
    # "Führe das folgende nur aus, wenn dieses Skript DIREKT gestartet wird"
    # (nicht wenn es als Modul importiert wird)
    
    try:
        # Versuche das Programm zu laufen
        
        # Schritt 1: Richte Logging ein
        logger = setup_logging()
        # ↑ Erstelle den Logger (Protokollierungs-System)
        
        # Schritt 2: Starte das Hauptprogramm
        main()
        # ↑ Rufe die main() Funktion auf
    
    except KeyboardInterrupt:
        # Falls Benutzer Ctrl+C drückt (Programm abbrechen)...
        
        logger.info("\n\n⚠️ Programm vom Benutzer unterbrochen (Ctrl+C)")
        # ↑ Melde sauber ab
        
        sys.exit(130)
        # ↑ Exit-Code 130 = Standard-Code für Ctrl+C
    
    except Exception as e:
        # Falls ein unerwarteter Fehler auftritt...
        
        logger.exception(f"🔴 KRITISCHER FEHLER: {e}")
        # ↑ logger.exception() zeigt auch den kompletten Stack-Trace
        # Das hilft beim Debugging
        
        sys.exit(1)
        # ↑ Beende mit Fehler-Code 1 (es ist etwas schiefgelaufen)

"""
═══════════════════════════════════════════════════════════════════════════
END OF FILE - Viel Spaß mit dem Scientific Research Tool! 🚀
═══════════════════════════════════════════════════════════════════════════
"""
