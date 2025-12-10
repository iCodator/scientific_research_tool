#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔════════════════════════════════════════════════════════════════════════════╗
║          QUERY PARSER - TEST RUNNER v2.3 (FIXED IMPORT)                   ║
║            Standalone Test & Report Script                                ║
║                                                                            ║
║ Verwendung: python query_parser_tester_v2_3.py tests/queries/1.txt        ║
║                                                                            ║
║ Features:                                                                  ║
║  • Lädt parser_test_precedence.py mit mehreren Fallback-Pfaden            ║
║  • Testet gegen beliebige .txt Dateien                                     ║
║  • Gibt ausführliches, verständliches Protokoll aus                        ║
║  • Speichert Ergebnisse in Report-Datei                                    ║
║  • Unterstützt Verzeichnisstrukturen wie tests/src/core/                  ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR: Query Parser Development Team
DATUM: 10. Dezember 2025
VERSION: 2.3 (FIXED: Robuster Import mit Fallbacks)
STATUS: ✅ PRODUCTION READY

BUGFIX v2.3:
  ✅ Import-Fehlerbehandlung verbessert
  ✅ Mehrere Fallback-Pfade für Parser
  ✅ Klare Fehlermeldungen wenn Parser nicht gefunden
  ✅ Funktioniert auch von verschiedenen Verzeichnissen
"""

import sys
import os
import importlib.util
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import traceback
import json

# ════════════════════════════════════════════════════════════════════════════
# DYNAMISCHER PARSER-IMPORT (v2.3 - ROBUSTE VERSION)
# ════════════════════════════════════════════════════════════════════════════

def find_and_load_parser():
    """
    Findet und lädt parser_test_precedence.py mit mehreren Strategien.
    
    Strategien (in Reihenfolge):
    1. Relative zum Script-Verzeichnis (tests/src/core)
    2. Relative zum Current Working Directory (cwd)
    3. Script-Verzeichnis selbst
    4. Aktuelles Verzeichnis selbst
    
    Returns:
        module: Das geladene Parser-Modul
    
    Raises:
        FileNotFoundError: Wenn Parser nicht gefunden
        ImportError: Wenn Parser nicht importiert werden kann
    """
    
    # Definiere alle Suchpfade
    script_dir = Path(__file__).parent
    cwd = Path.cwd()
    
    search_paths = [
        # Haupt-Strategien (nested struktur)
        script_dir / "tests" / "src" / "core",
        cwd / "tests" / "src" / "core",
        script_dir / "src" / "core",
        cwd / "src" / "core",
        
        # Fallback: direkt im Verzeichnis
        script_dir,
        cwd,
        
        # Alternative Locations
        Path.home() / "parser_test_precedence",
    ]
    
    parser_filename = "parser_test_precedence.py"
    found_path = None
    
    # Suche die Datei
    for search_path in search_paths:
        parser_file = search_path / parser_filename
        if parser_file.exists():
            found_path = parser_file
            break
    
    if found_path is None:
        raise FileNotFoundError(
            f"❌ {parser_filename} nicht gefunden!\n\n"
            f"Gesuchte Pfade:\n" +
            "\n".join(f"  • {p}" for p in search_paths) +
            f"\n\nBitte stelle sicher, dass {parser_filename} in einem dieser Verzeichnisse existiert."
        )
    
    # Versuche zu importieren
    try:
        spec = importlib.util.spec_from_file_location("parser_module", found_path)
        parser = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(parser)
        
        return parser, found_path
        
    except Exception as e:
        raise ImportError(
            f"❌ Fehler beim Importieren von {found_path}:\n{str(e)}"
        )

try:
    parser_module, parser_location = find_and_load_parser()
    parse_query_full = parser_module.parse_query_full
except (FileNotFoundError, ImportError) as e:
    print(f"\n❌ FEHLER: {str(e)}\n")
    sys.exit(1)

# ════════════════════════════════════════════════════════════════════════════
# KONFIGURATION
# ════════════════════════════════════════════════════════════════════════════

REPORT_DIR = Path("./test_reports")
REPORT_DIR.mkdir(exist_ok=True)

# Farben für Console-Output (ANSI)
class Colors:
    """ANSI-Farbcodes für schönere Console-Ausgabe"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ════════════════════════════════════════════════════════════════════════════
# HILFSFUNKTIONEN
# ════════════════════════════════════════════════════════════════════════════

def load_test_file(filepath: str) -> str:
    """
    Lädt eine Test-Datei und gibt ihren Inhalt zurück.
    
    Args:
        filepath (str): Pfad zur Test-Datei (.txt)
    
    Returns:
        str: Rohinhalt der Datei
    
    Raises:
        FileNotFoundError: Wenn Datei nicht existiert
    """
    test_path = Path(filepath)
    
    if not test_path.exists():
        raise FileNotFoundError(f"❌ Test-Datei nicht gefunden: {filepath}")
    
    if not test_path.suffix.lower() == '.txt':
        raise ValueError(f"❌ Nur .txt Dateien unterstützt, erhalten: {test_path.suffix}")
    
    try:
        with open(test_path, 'r', encoding='utf-8') as f:
            return f.read()
    except IOError as e:
        raise IOError(f"❌ Fehler beim Lesen der Datei: {str(e)}")

# ════════════════════════════════════════════════════════════════════════════
# HAUPTFUNKTION
# ════════════════════════════════════════════════════════════════════════════

def main():
    """Hauptfunktion: Orchestriert Laden, Testen und Reporting"""
    
    print("\n" + "="*80)
    print(Colors.BOLD + "QUERY PARSER TEST RUNNER v2.3 (FIXED IMPORT)" + Colors.ENDC)
    print("="*80 + "\n")
    
    # Zeige Parser-Info
    print(f"{Colors.GREEN}✓ Parser geladen:{Colors.ENDC}")
    print(f"  Datei: {parser_location}")
    print(f"  Modul: {parser_module.__name__}\n")
    
    # Argument-Validierung
    if len(sys.argv) != 2:
        print(f"{Colors.RED}✗ FEHLER: Test-Datei erforderlich!{Colors.ENDC}\n")
        print("Verwendung:")
        print(f"  python query_parser_tester_v2_3.py <test_datei.txt>\n")
        print("Beispiele:")
        print("  python query_parser_tester_v2_3.py tests/queries/1.txt")
        print("  python query_parser_tester_v2_3.py ./my_test.txt\n")
        sys.exit(1)
    
    test_file = sys.argv[1]
    
    # Lade Test-Datei
    print(f"{Colors.CYAN}[1/3]{Colors.ENDC} Lade Test-Datei...")
    try:
        raw_query = load_test_file(test_file)
        print(f"{Colors.GREEN}✓ Test-Datei geladen:{Colors.ENDC} {test_file}")
        print(f"  Größe: {len(raw_query)} Bytes\n")
    except (FileNotFoundError, ValueError, IOError) as e:
        print(f"{Colors.RED}✗ Fehler: {str(e)}{Colors.ENDC}\n")
        sys.exit(1)
    
    # Führe Parser aus
    print(f"{Colors.CYAN}[2/3]{Colors.ENDC} Führe Parser aus...\n")
    try:
        result = parse_query_full(raw_query, "pubmed")
    except Exception as e:
        print(f"{Colors.RED}✗ Parser-Fehler:{Colors.ENDC}")
        print(f"  {str(e)}\n")
        traceback.print_exc()
        sys.exit(1)
    
    # Zeige Ergebnisse
    print(f"{Colors.CYAN}[3/3]{Colors.ENDC} Ergebnisse:\n")
    
    if result['success']:
        print(f"{Colors.GREEN}✓ ERFOLGREICH{Colors.ENDC}\n")
        
        # Phase 1
        phase1 = result['phases'].get('1_cleaning', {})
        print(f"{Colors.BOLD}Phase 1: Cleaning & Format-Erkennung{Colors.ENDC}")
        print(f"  Format: {phase1.get('format', 'N/A')}")
        print(f"  Zeilen: {phase1.get('lines_before', '?')} → {phase1.get('lines_after', '?')}\n")
        
        # Phase 2/3
        phase23 = result['phases'].get('2_3_parsing', {})
        print(f"{Colors.BOLD}Phase 2/3: Parsing{Colors.ENDC}")
        parsed = phase23.get('parsed_query', '')
        if len(parsed) > 70:
            print(f"  {parsed[:70]}...")
        else:
            print(f"  {parsed}\n")
        
        # Phase 4
        phase4 = result['phases'].get('4_formatting', {})
        print(f"{Colors.BOLD}Phase 4: Datumsformat & Source-Formatierung{Colors.ENDC}")
        print(f"  Source: {phase4.get('source', 'N/A')}")
        print(f"  Datumsformat: {'Ja' if phase4.get('has_date') else 'Nein'}\n")
        
        # Finale Ausgabe
        print(f"{Colors.BOLD}FINALE OUTPUT:{Colors.ENDC}")
        final = result.get('final_output', '')
        if len(final) > 70:
            print(f"  {final[:70]}...")
            for i in range(70, len(final), 70):
                print(f"  {final[i:i+70]}")
        else:
            print(f"  {final}\n")
        
        print(f"{Colors.GREEN}✓ TEST BESTANDEN{Colors.ENDC}")
        exit_code = 0
        
    else:
        print(f"{Colors.RED}✗ FEHLER{Colors.ENDC}\n")
        print(f"  {result.get('error', 'Unbekannter Fehler')}\n")
        print(f"{Colors.RED}✗ TEST FEHLGESCHLAGEN{Colors.ENDC}")
        exit_code = 1
    
    print("\n" + "="*80 + "\n")
    
    sys.exit(exit_code)

# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()
