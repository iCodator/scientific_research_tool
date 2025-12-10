#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "tests/src/core")

"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    QUERY PARSER - TEST RUNNER v2.2                        ║
║                      Standalone Test & Report Script                      ║
║                                                                            ║
║ Verwendung:   python query_parser_tester.py <test_file.txt>              ║
║ Beispiel:     python query_parser_tester.py tests/1.txt                  ║
║                                                                            ║
║ Funktionen:                                                               ║
║   • Lädt parser_test_precedence.py als externes Modul                    ║
║   • Testet gegen beliebige .txt Dateien                                  ║
║   • Gibt ausführliches, verständliches Protokoll aus                    ║
║   • Speichert Ergebnisse in Report-Datei                                ║
║   • Unterstützt Verzeichnisstrukturen wie src/core/                     ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR:      Query Parser Development Team
DATUM:      10. Dezember 2025
VERSION:    1.1 (Unterstützung für Unterverzeichnisse)
STATUS:     ✅ PRODUCTION READY

ABHÄNGIGKEITEN:
  • parser_test_precedence.py (kann in verschiedenen Verzeichnissen sein)
  • Python 3.7+
  • Standard Library nur (kein pip install nötig)

VERZEICHNISSTRUKTUREN:
  Unterstützte Layouts:
  ├─ /root/parser_test_precedence.py
  ├─ /root/src/core/parser_test_precedence.py    ← Bevorzugt
  ├─ /root/tests/parser_test_precedence.py
  └─ Und weitere Kombinationen

"""

import sys
import os
import importlib.util
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import traceback
import json

# Dynamischer Import des Parsers
parser_path = Path(__file__).parent / "tests" / "src" / "core"
sys.path.insert(0, str(parser_path))

from parser_test_precedence import parse_query_full

# ════════════════════════════════════════════════════════════════════════════
# KONFIGURATION
# ════════════════════════════════════════════════════════════════════════════

# Suchpfade für parser_test_precedence.py
# Unterstützt sowohl flache als auch verschachtelte Verzeichnisstrukturen
PARSER_SEARCH_PATHS = [
    Path.cwd(),                                    # Aktuelles Verzeichnis
    Path.cwd() / "src" / "core",                  # src/core/ Subdir
    Path.cwd() / "src",                           # src/ Subdir
    Path.cwd().parent,                            # Parent-Verzeichnis
    Path.cwd().parent / "src" / "core",           # ../src/core/ Subdir
    Path.cwd().parent / "src",                    # ../src/ Subdir
    Path(__file__).parent,                        # Script-Verzeichnis
    Path(__file__).parent / "src" / "core",       # Script/src/core/
    Path(__file__).parent / "src",                # Script/src/
    Path(__file__).parent.parent,                 # Script Parent-Verzeichnis
    Path(__file__).parent.parent / "src" / "core", # Script Parent/src/core/
    Path(__file__).parent.parent / "src",        # Script Parent/src/
]

# Ausgabe-Verzeichnis für Reports
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

def load_parser_module():
    """
    Lädt parser_test_precedence.py als externes Modul.
    
    Sucht in mehreren Verzeichnissen nach der Datei (inklusive src/core/)
    und importiert sie. Falls nicht gefunden, gibt aussagekräftige Fehlermeldung.
    
    Returns:
        module: Das importierte parser Modul
        
    Raises:
        FileNotFoundError: Wenn parser nicht gefunden
        ImportError: Wenn parser nicht importiert werden kann
    """
    parser_filename = "parser_test_precedence.py"
    
    print(f"{Colors.CYAN}Suche Parser in folgenden Pfaden:{Colors.ENDC}")
    for search_path in PARSER_SEARCH_PATHS:
        parser_file = search_path / parser_filename
        print(f"  • {parser_file}", end="")
        
        if parser_file.exists():
            print(f" {Colors.GREEN}✓ GEFUNDEN{Colors.ENDC}")
            
            try:
                # Importiere als Modul
                spec = importlib.util.spec_from_file_location("parser_module", parser_file)
                parser = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(parser)
                
                print(f"{Colors.GREEN}✓ Parser erfolgreich importiert!{Colors.ENDC}\n")
                return parser
                
            except Exception as e:
                print(f"{Colors.RED}✗ Fehler beim Importieren:{Colors.ENDC} {str(e)}")
                raise ImportError(f"Parser konnte nicht importiert werden: {str(e)}")
        else:
            print(" (nicht gefunden)")
    
    # Parser nicht gefunden - hilfreiche Fehlermeldung
    print(f"\n{Colors.RED}✗ FEHLER: parser_test_precedence.py nicht gefunden!{Colors.ENDC}\n")
    print("Mögliche Lösungen:")
    print("  1. Stelle sicher, dass parser_test_precedence.py existiert")
    print("  2. Verzeichnisse prüfen:")
    print("     - .", "/src", "/src/core", "..", "../src", "../src/core")
    print("  3. Aktuelles Verzeichnis prüfen: pwd")
    print("  4. Datei suchen: find . -name parser_test_precedence.py")
    
    raise FileNotFoundError(f"{parser_filename} nicht gefunden")

def load_test_file(filepath: str) -> str:
    """
    Lädt eine Test-Datei und gibt ihren Inhalt zurück.
    
    Args:
        filepath (str): Pfad zur Test-Datei (.txt)
        
    Returns:
        str: Rohinhalt der Datei
        
    Raises:
        FileNotFoundError: Wenn Datei nicht existiert
        IOError: Wenn Datei nicht gelesen werden kann
    """
    test_path = Path(filepath)
    
    # Validierung
    if not test_path.exists():
        raise FileNotFoundError(f"Test-Datei nicht gefunden: {filepath}")
    
    if not test_path.suffix.lower() == '.txt':
        raise ValueError(f"Nur .txt Dateien unterstützt, erhalten: {test_path.suffix}")
    
    try:
        with open(test_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except IOError as e:
        raise IOError(f"Fehler beim Lesen der Datei: {str(e)}")

def validate_parser_functions(parser) -> bool:
    """
    Validiert, dass alle notwendigen Parser-Funktionen verfügbar sind.
    
    Args:
        parser: Das importierte Parser-Modul
        
    Returns:
        bool: True wenn alle Funktionen vorhanden, False sonst
    """
    required_functions = [
        'clean_query',
        'is_multiline',
        'is_complex_format',
        'has_mixed_operators',
        'get_mixed_operators_info',
    ]
    
    missing = []
    for func_name in required_functions:
        if not hasattr(parser, func_name):
            missing.append(func_name)
    
    if missing:
        print(f"{Colors.RED}✗ Fehlendes Funktionen im Parser:{Colors.ENDC}")
        for func in missing:
            print(f"  • {func}()")
        return False
    
    return True

# ════════════════════════════════════════════════════════════════════════════
# HAUPT-TESTFUNKTIONEN
# ════════════════════════════════════════════════════════════════════════════

def run_parser_phases(parser, raw_query: str) -> Dict[str, Any]:
    """
    Führt den Parser durch alle Phasen aus und sammelt Ergebnisse.
    
    Phasen:
      1. Cleaning & Format Detection
      2. Operator Precedence Validation
      3. (Parsing - abhängig von Phase 1-2)
    
    Args:
        parser: Das Parser-Modul
        raw_query (str): Rohe Query mit Kommentaren/Formatierung
        
    Returns:
        Dict mit Ergebnissen aus jeder Phase
    """
    results = {
        'raw_input': raw_query,
        'phases': {},
        'errors': []
    }
    
    # ─────────────────────────────────────────────────────────────────────────
    # PHASE 1: CLEANING & FORMAT DETECTION
    # ─────────────────────────────────────────────────────────────────────────
    
    try:
        cleaned = parser.clean_query(raw_query)
        is_multiline = parser.is_multiline(cleaned)
        is_complex = parser.is_complex_format(cleaned) if is_multiline else False
        
        results['phases']['phase_1'] = {
            'name': 'Cleaning & Format Detection',
            'status': 'SUCCESS',
            'cleaned_query': cleaned,
            'is_multiline': is_multiline,
            'is_complex_format': is_complex,
            'format_type': 'COMPLEX' if is_complex else ('MULTI-LINE' if is_multiline else 'SINGLE-LINE')
        }
    except Exception as e:
        results['phases']['phase_1'] = {
            'name': 'Cleaning & Format Detection',
            'status': 'ERROR',
            'error': str(e)
        }
        results['errors'].append(f"Phase 1 Fehler: {str(e)}")
        return results
    
    cleaned_query = cleaned
    
    # ─────────────────────────────────────────────────────────────────────────
    # PHASE 2: OPERATOR PRECEDENCE VALIDATION
    # ─────────────────────────────────────────────────────────────────────────
    
    try:
        # Für Complex Format: Prüfe jede Zeile
        has_mixed = False
        mixed_info = None
        
        if is_multiline:
            # Prüfe jede ODD-Zeile auf gemischte Operatoren
            lines = cleaned_query.split('\n')
            for i, line in enumerate(lines):
                if (i + 1) % 2 == 1:  # ODD-Zeile (1-indexed)
                    if parser.has_mixed_operators(line):
                        has_mixed = True
                        mixed_info = parser.get_mixed_operators_info(line)
                        break
        else:
            # Single-Line: direkt prüfen
            has_mixed = parser.has_mixed_operators(cleaned_query)
            if has_mixed:
                mixed_info = parser.get_mixed_operators_info(cleaned_query)
        
        results['phases']['phase_2'] = {
            'name': 'Operator Precedence Validation',
            'status': 'ERROR' if has_mixed else 'SUCCESS',
            'has_mixed_operators': has_mixed,
            'valid': not has_mixed,
            'mixed_operators_info': mixed_info if has_mixed else None
        }
        
        if has_mixed:
            results['errors'].append(
                f"Phase 2 Fehler: Gemischte Operatoren ohne Klammern erkannt\n"
                f"  Details: {mixed_info}"
            )
    
    except Exception as e:
        results['phases']['phase_2'] = {
            'name': 'Operator Precedence Validation',
            'status': 'ERROR',
            'error': str(e)
        }
        results['errors'].append(f"Phase 2 Fehler: {str(e)}")
    
    return results

# ════════════════════════════════════════════════════════════════════════════
# REPORTING & AUSGABE
# ════════════════════════════════════════════════════════════════════════════

def format_console_report(test_file: str, results: Dict[str, Any]) -> str:
    """
    Formatiert Ergebnisse für ansprechende Console-Ausgabe.
    
    Args:
        test_file (str): Name der Test-Datei
        results (Dict): Ergebnisse von run_parser_phases()
        
    Returns:
        str: Formatierter Report als String
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    output = []
    
    # Header
    output.append("\n" + "="*80)
    output.append(f"{Colors.BOLD}{Colors.BLUE}QUERY PARSER TEST REPORT v2.2{Colors.ENDC}")
    output.append("="*80)
    
    output.append(f"\n{Colors.CYAN}Test-Datei:{Colors.ENDC}  {test_file}")
    output.append(f"{Colors.CYAN}Zeitstempel:{Colors.ENDC}  {timestamp}")
    output.append(f"{Colors.CYAN}Status:{Colors.ENDC}      {'✓ VALID' if not results['errors'] else '✗ INVALID'}")
    
    # Eingabe-Übersicht
    output.append(f"\n{Colors.BOLD}{Colors.YELLOW}─────────────────────────────────────────────────────────────────────────────{Colors.ENDC}")
    output.append(f"{Colors.BOLD}INPUT (Rohe Query):{Colors.ENDC}")
    output.append("─" * 80)
    
    raw_input = results['raw_input']
    if len(raw_input) > 500:
        output.append(raw_input[:500] + f"\n... ({len(raw_input)} Zeichen total)")
    else:
        output.append(raw_input)
    
    # Phase 1 Report
    output.append(f"\n{Colors.BOLD}{Colors.YELLOW}─────────────────────────────────────────────────────────────────────────────{Colors.ENDC}")
    output.append(f"{Colors.BOLD}PHASE 1: CLEANING & FORMAT DETECTION{Colors.ENDC}")
    output.append("─" * 80)
    
    phase1 = results['phases'].get('phase_1', {})
    
    if phase1.get('status') == 'SUCCESS':
        output.append(f"{Colors.GREEN}✓ Status: ERFOLGREICH{Colors.ENDC}")
        output.append(f"  Format-Typ:        {phase1.get('format_type', 'UNKNOWN')}")
        output.append(f"  Multi-Line:        {phase1.get('is_multiline', False)}")
        output.append(f"  Complex Format:    {phase1.get('is_complex_format', False)}")
        
        output.append(f"\n  {Colors.CYAN}Gereinigte Query:{Colors.ENDC}")
        cleaned = phase1.get('cleaned_query', '')
        if len(cleaned) > 300:
            output.append(f"    {cleaned[:300]}...")
        else:
            output.append(f"    {cleaned}")
    else:
        output.append(f"{Colors.RED}✗ Status: FEHLER{Colors.ENDC}")
        output.append(f"  {phase1.get('error', 'Unbekannter Fehler')}")
    
    # Phase 2 Report
    output.append(f"\n{Colors.BOLD}{Colors.YELLOW}─────────────────────────────────────────────────────────────────────────────{Colors.ENDC}")
    output.append(f"{Colors.BOLD}PHASE 2: OPERATOR PRECEDENCE VALIDATION{Colors.ENDC}")
    output.append("─" * 80)
    
    phase2 = results['phases'].get('phase_2', {})
    
    if phase2.get('status') == 'SUCCESS':
        output.append(f"{Colors.GREEN}✓ Status: GÜLTIG{Colors.ENDC}")
        output.append(f"  Gemischte Operatoren: {phase2.get('has_mixed_operators', False)}")
        output.append(f"  Validität:           {phase2.get('valid', True)}")
    else:
        output.append(f"{Colors.RED}✗ Status: FEHLER{Colors.ENDC}")
        output.append(f"  Gemischte Operatoren: {phase2.get('has_mixed_operators', False)}")
        
        mixed_info = phase2.get('mixed_operators_info')
        if mixed_info:
            output.append(f"  Details:")
            output.append(f"    {mixed_info}")
    
    # Fehler-Zusammenfassung
    if results['errors']:
        output.append(f"\n{Colors.BOLD}{Colors.RED}─────────────────────────────────────────────────────────────────────────────{Colors.ENDC}")
        output.append(f"{Colors.BOLD}{Colors.RED}FEHLER UND WARNUNGEN{Colors.ENDC}")
        output.append("─" * 80)
        
        for error in results['errors']:
            output.append(f"{Colors.RED}✗ {error}{Colors.ENDC}")
    
    # Footer
    output.append(f"\n{Colors.BOLD}{Colors.YELLOW}─────────────────────────────────────────────────────────────────────────────{Colors.ENDC}")
    output.append(f"Report erstellt: {timestamp}")
    output.append("="*80 + "\n")
    
    return "\n".join(output)

def format_detailed_report(test_file: str, results: Dict[str, Any]) -> str:
    """
    Erstellt ausführliche technische Report mit allen Details.
    
    Args:
        test_file (str): Name der Test-Datei
        results (Dict): Ergebnisse von run_parser_phases()
        
    Returns:
        str: Detaillierter Report als String
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
    
    lines = []
    
    # Header
    lines.append("╔" + "="*78 + "╗")
    lines.append("║" + " "*78 + "║")
    lines.append("║" + "  QUERY PARSER - DETAILLIERTER TEST-REPORT v2.2".center(78) + "║")
    lines.append("║" + "  Ausführliche Analyse & Debugging-Informationen".center(78) + "║")
    lines.append("║" + " "*78 + "║")
    lines.append("╚" + "="*78 + "╝\n")
    
    # Allgemeine Informationen
    lines.append("ALLGEMEINE INFORMATIONEN")
    lines.append("─" * 80)
    lines.append(f"Test-Datei:          {test_file}")
    lines.append(f"Dateigröße:          {len(results['raw_input'])} Bytes")
    lines.append(f"Anzahl Zeilen:       {len(results['raw_input'].split(chr(10)))}")
    lines.append(f"Zeitstempel:         {timestamp}")
    lines.append(f"Report-Status:       {'✓ VALID' if not results['errors'] else '✗ ERRORS FOUND'}")
    
    # Eingabe
    lines.append("\n" + "─"*80)
    lines.append("EINGABE (RAW QUERY)")
    lines.append("─" * 80)
    lines.append("Länge: {} Zeichen".format(len(results['raw_input'])))
    lines.append("\nInhalt:")
    lines.append(repr(results['raw_input']))
    
    # Phase Details
    lines.append("\n" + "─"*80)
    lines.append("PHASE-WEISE ANALYSE")
    lines.append("─" * 80)
    
    for phase_key, phase_data in results['phases'].items():
        lines.append(f"\n{phase_key.upper()}: {phase_data.get('name', 'Unknown')}")
        lines.append("─" * 80)
        
        status = phase_data.get('status', 'UNKNOWN')
        lines.append(f"Status: {status}")
        
        for key, value in phase_data.items():
            if key not in ['name', 'status']:
                if isinstance(value, (dict, list)):
                    lines.append(f"{key}: {json.dumps(value, indent=2, ensure_ascii=False)}")
                else:
                    lines.append(f"{key}: {value}")
    
    # Fehleranalyse
    if results['errors']:
        lines.append("\n" + "─"*80)
        lines.append("FEHLER-ANALYSE")
        lines.append("─" * 80)
        
        for i, error in enumerate(results['errors'], 1):
            lines.append(f"\nFehler #{i}:")
            lines.append(f"  {error}")
    
    # Empfehlungen
    lines.append("\n" + "─"*80)
    lines.append("EMPFEHLUNGEN")
    lines.append("─" * 80)
    
    if results['errors']:
        lines.append("\n⚠️  PROBLEME ERKANNT:\n")
        
        if any('Mixed operators' in str(e) for e in results['errors']):
            lines.append("• Gemischte Operatoren ohne Klammern erkannt")
            lines.append("  Lösung: Setzen Sie explizite Klammern, z.B.:")
            lines.append("    ❌ \"A OR B AND C\"")
            lines.append("    ✓  \"(A OR B) AND C\"")
        
        if any('ODD' in str(e) or 'EVEN' in str(e) for e in results['errors']):
            lines.append("\n• ODD/EVEN Format-Verletzung erkannt")
            lines.append("  Lösung: Folgen Sie ODD/EVEN Muster:")
            lines.append("    Zeile 1 (ODD):   Query-Ausdruck")
            lines.append("    Zeile 2 (EVEN):  Operator (AND/OR/NOT)")
            lines.append("    Zeile 3 (ODD):   Query-Ausdruck")
    else:
        lines.append("\n✓ KEINE FEHLER GEFUNDEN")
        lines.append("\nQuery ist gültig und kann weiterverarbeitet werden.")
    
    # Footer
    lines.append("\n" + "="*80)
    lines.append(f"Report erstellt: {timestamp}")
    lines.append("="*80 + "\n")
    
    return "\n".join(lines)

# ════════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ════════════════════════════════════════════════════════════════════════════

def main():
    """
    Haupt-Funktion: Orchestriert Laden, Testen und Reporting.
    """
    
    print("\n" + "="*80)
    print(Colors.BOLD + "QUERY PARSER TEST RUNNER v2.2" + Colors.ENDC)
    print("="*80 + "\n")
    
    # ─────────────────────────────────────────────────────────────────────────
    # ARGUMENT VALIDIERUNG
    # ─────────────────────────────────────────────────────────────────────────
    
    if len(sys.argv) != 2:
        print(f"{Colors.RED}✗ FEHLER: Verwendung erforderlich!{Colors.ENDC}\n")
        print("Verwendung:")
        print(f"  python query_parser_tester.py <test_file.txt>\n")
        print("Beispiele:")
        print("  python query_parser_tester.py tests/1.txt")
        print("  python query_parser_tester.py queries/cancer_search.txt")
        print("  python query_parser_tester.py ./my_test.txt\n")
        sys.exit(1)
    
    test_file = sys.argv[1]
    
    # ─────────────────────────────────────────────────────────────────────────
    # PARSER LADEN
    # ─────────────────────────────────────────────────────────────────────────
    
    print(f"{Colors.CYAN}[1/4]{Colors.ENDC} Lade Parser-Modul...")
    
    try:
        parser = load_parser_module()
    except (FileNotFoundError, ImportError) as e:
        print(f"{Colors.RED}✗ Fehler beim Laden des Parsers:{Colors.ENDC}")
        print(f"  {str(e)}\n")
        sys.exit(1)
    
    # Validiere Parser-Funktionen
    print(f"{Colors.CYAN}[2/4]{Colors.ENDC} Validiere Parser-Funktionen...")
    if not validate_parser_functions(parser):
        print(f"{Colors.RED}✗ Parser hat nicht alle benötigten Funktionen!{Colors.ENDC}\n")
        sys.exit(1)
    print(f"{Colors.GREEN}✓ Alle Parser-Funktionen verfügbar{Colors.ENDC}\n")
    
    # ─────────────────────────────────────────────────────────────────────────
    # TEST-DATEI LADEN
    # ─────────────────────────────────────────────────────────────────────────
    
    print(f"{Colors.CYAN}[3/4]{Colors.ENDC} Lade Test-Datei...")
    
    try:
        raw_query = load_test_file(test_file)
        print(f"{Colors.GREEN}✓ Test-Datei geladen:{Colors.ENDC} {test_file}")
        print(f"  Größe: {len(raw_query)} Bytes\n")
    except (FileNotFoundError, ValueError, IOError) as e:
        print(f"{Colors.RED}✗ Fehler beim Laden der Test-Datei:{Colors.ENDC}")
        print(f"  {str(e)}\n")
        sys.exit(1)
    
    # ─────────────────────────────────────────────────────────────────────────
    # PARSER AUSFÜHREN
    # ─────────────────────────────────────────────────────────────────────────
    
    print(f"{Colors.CYAN}[4/4]{Colors.ENDC} Führe Parser aus...")
    
    try:
        results = run_parser_phases(parser, raw_query)
        print(f"{Colors.GREEN}✓ Parser erfolgreich ausgeführt{Colors.ENDC}\n")
    except Exception as e:
        print(f"{Colors.RED}✗ Fehler bei Parser-Ausführung:{Colors.ENDC}")
        print(f"  {str(e)}")
        print(f"\n{Colors.YELLOW}Traceback:{Colors.ENDC}")
        traceback.print_exc()
        sys.exit(1)
    
    # ─────────────────────────────────────────────────────────────────────────
    # REPORTS GENERIEREN UND AUSGEBEN
    # ─────────────────────────────────────────────────────────────────────────
    
    # Console Report (kurz & ansprechend)
    console_report = format_console_report(test_file, results)
    print(console_report)
    
    # Detaillierter Report (ausführlich)
    detailed_report = format_detailed_report(test_file, results)
    
    # Reports speichern
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_filename = Path(test_file).stem
    
    console_file = REPORT_DIR / f"report_console_{test_filename}_{timestamp}.txt"
    detailed_file = REPORT_DIR / f"report_detailed_{test_filename}_{timestamp}.txt"
    
    try:
        with open(console_file, 'w', encoding='utf-8') as f:
            f.write(console_report)
        
        with open(detailed_file, 'w', encoding='utf-8') as f:
            f.write(detailed_report)
        
        print(f"{Colors.GREEN}✓ Reports gespeichert:{Colors.ENDC}")
        print(f"  • {console_file}")
        print(f"  • {detailed_file}\n")
    
    except IOError as e:
        print(f"{Colors.YELLOW}⚠ Warnung: Reports konnten nicht gespeichert werden:{Colors.ENDC}")
        print(f"  {str(e)}\n")
    
    # Exit-Code basierend auf Ergebnissen
    exit_code = 0 if not results['errors'] else 1
    
    print(f"{Colors.BOLD}{'─'*80}{Colors.ENDC}")
    if exit_code == 0:
        print(f"{Colors.GREEN}✓ TEST ERFOLGREICH{Colors.ENDC} - Keine Fehler gefunden")
    else:
        print(f"{Colors.RED}✗ TEST FEHLGESCHLAGEN{Colors.ENDC} - Fehler wurden gefunden")
    print(f"{Colors.BOLD}{'─'*80}{Colors.ENDC}\n")
    
    sys.exit(exit_code)

# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()
