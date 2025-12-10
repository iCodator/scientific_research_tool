#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔════════════════════════════════════════════════════════════════════════════╗
║          QUERY PARSER - COMPREHENSIVE TEST & OUTPUT SCRIPT v2.2            ║
║            Mit Phase 4 Integration & Detailliertem Logging                 ║
║                    (FIXED Operator Precedence)                             ║
╚════════════════════════════════════════════════════════════════════════════╝

PROJEKT: Scientific Research Tool - QueryFormatInterpreter
DATEI:   parser_test_comprehensive.py
VERSION: 2.2 (Phase 1-4 mit Operator-Precedence-Validierung)
DATUM:   10. Dezember 2025
STATUS:  ✅ READY FOR COMPREHENSIVE TESTING

BUGFIX v2.2:
════════════
✅ FIXED: Operator Precedence Validierung hinzugefügt

  PROBLEM: "A OR B AND C" ist mehrdeutig
    ├─ Interpretation 1: (A OR B) AND C
    └─ Interpretation 2: A OR (B AND C)
  
  LÖSUNG: Validierung vor dem Parsing
    ├─ Wenn Query gemischte Operatoren hat (AND + OR oder AND + NOT oder OR + NOT)
    ├─ UND diese NICHT geklammert sind
    └─ → FEHLER mit klarer Fehlermeldung!
  
  ERLAUBT:
    ✅ "A OR B"              (nur OR)
    ✅ "A AND B"             (nur AND)
    ✅ "(A OR B) AND C"      (geklammert)
    ✅ "A OR (B AND C)"      (geklammert)
  
  NICHT ERLAUBT:
    ❌ "A OR B AND C"        (gemischte Operatoren, nicht geklammert)
    ❌ "A AND B OR C"        (gemischte Operatoren, nicht geklammert)

════════════════════════════════════════════════════════════════════════════════
"""

import sys
import logging
from pathlib import Path
from typing import Tuple, Optional, Dict
from datetime import datetime
import traceback
import re

# ════════════════════════════════════════════════════════════════════════════
# LOGGER SETUP - File + Console Output
# ════════════════════════════════════════════════════════════════════════════

def setup_logging(output_dir: str = "./test_results"):
    """
    Richtet Logging ein für Console + Datei.
    
    Args:
        output_dir (str): Verzeichnis für Log-Dateien
    """
    # Erstelle Output-Verzeichnis
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Logger konfigurieren
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    # Console Handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    
    # File Handler (Protokoll)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = output_path / f"test_protocol_{timestamp}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(file_formatter)
    
    # Handler hinzufügen
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger, log_file


# ════════════════════════════════════════════════════════════════════════════
# PARSER PHASE 1-4 IMPLEMENTIERUNG (INTEGRIERT)
# ════════════════════════════════════════════════════════════════════════════

class InvalidQueryFormatError(Exception):
    """Fehler für ungültige Query-Formate"""
    pass


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 1: Cleaning & Format-Erkennung
# ─────────────────────────────────────────────────────────────────────────────

def clean_query(raw_query: str) -> str:
    """
    PHASE 1: Entfernt Kommentare und Leerzeilen.
    
    Args:
        raw_query (str): Query mit Kommentaren
    
    Returns:
        str: Bereinigte Query
    """
    lines = raw_query.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Entferne Kommentare
        if '#' in line:
            line = line[:line.index('#')]
        
        # Strip whitespace
        line = line.strip()
        
        # Nur nicht-leere Zeilen behalten
        if line:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)


def is_multiline(cleaned_query: str) -> bool:
    """
    PHASE 1: Prüft, ob Query Multi-Line ist.
    
    Args:
        cleaned_query (str): Bereinigte Query
    
    Returns:
        bool: True wenn Multi-Line
    """
    return '\n' in cleaned_query


def validate_complex_format(cleaned_query: str) -> None:
    """
    PHASE 1: Validiert ODD/EVEN Muster.
    
    Args:
        cleaned_query (str): Bereinigte Query
    
    Raises:
        InvalidQueryFormatError: Bei Muster-Verletzung
    """
    lines = cleaned_query.split('\n')
    operators = {'AND', 'OR', 'NOT'}
    
    for line_number, line in enumerate(lines, start=1):
        is_odd = line_number % 2 == 1
        is_operator = line.upper() in operators
        
        if is_odd and is_operator:
            raise InvalidQueryFormatError(
                f"ODD-Zeile {line_number}: '{line}' sollte QUERY sein, nicht Operator"
            )
        
        if not is_odd and not is_operator:
            raise InvalidQueryFormatError(
                f"EVEN-Zeile {line_number}: '{line}' sollte OPERATOR sein, nicht QUERY"
            )


def is_complex_format(cleaned_query: str) -> bool:
    """
    PHASE 1: Prüft ODD/EVEN Format sicher.
    
    Args:
        cleaned_query (str): Bereinigte Query
    
    Returns:
        bool: True wenn valides Complex Format
    """
    lines = cleaned_query.split('\n')
    
    if len(lines) < 3:
        return False
    
    try:
        validate_complex_format(cleaned_query)
        return True
    except InvalidQueryFormatError:
        return False


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 2: Operator Precedence Validierung
# ─────────────────────────────────────────────────────────────────────────────

def has_mixed_operators(query: str) -> bool:
    """
    ╔════════════════════════════════════════════════════════════════════════╗
    ║        OPERATOR PRECEDENCE VALIDIERUNG (v2.2 NEU)                      ║
    ╚════════════════════════════════════════════════════════════════════════╝
    
    Prüft, ob Query gemischte Operatoren hat OHNE Klammern.
    
    PROBLEM (Mehrdeutigkeit):
    ═════════════════════════
    "A OR B AND C" ist mehrdeutig:
    - Interpretation 1: (A OR B) AND C
    - Interpretation 2: A OR (B AND C)
    
    Diese beiden Interpretationen können UNTERSCHIEDLICHE Ergebnisse liefern!
    
    LÖSUNG:
    ═══════
    Wenn Query gemischte Operatoren hat (z.B. AND UND OR):
    1. Entferne alle geklammerten Ausdrücke (diese sind eindeutig)
    2. Prüfe, welche Operatoren noch vorhanden sind
    3. Wenn > 1 verschiedene Operator-Typen → FEHLER!
    
    ERLAUBTE FÄLLE:
    ════════════════
    ✅ "A OR B OR C"              (nur OR)
    ✅ "A AND B AND C"            (nur AND)
    ✅ "(A OR B) AND C"           (geklammert)
    ✅ "A OR (B AND C)"           (geklammert)
    ✅ "NOT A"                    (nur NOT)
    ✅ "(A OR B) AND (C OR D)"    (vollständig geklammert)
    
    NICHT ERLAUBTE FÄLLE:
    ═════════════════════
    ❌ "A OR B AND C"             (gemischte Operatoren)
    ❌ "A AND B OR C"             (gemischte Operatoren)
    ❌ "A OR B NOT C"             (gemischte Operatoren)
    ❌ "A AND B NOT C"            (gemischte Operatoren)
    
    Args:
        query (str): Single-Line Query
    
    Returns:
        bool: True wenn gemischte Operatoren ohne Klammern vorhanden
    """
    
    # Entferne alle geklammerten Ausdrücke
    # Beispiel: "A OR (B AND C) OR D" → "A OR  OR D"
    # Die geklammerten Teile sind eindeutig, brauchen wir nicht zu prüfen
    cleaned = re.sub(r'\([^)]+\)', '', query)
    
    # Prüfe welche Operatoren OHNE Klammern vorhanden sind
    has_and = re.search(r'\bAND\b', cleaned, re.IGNORECASE) is not None
    has_or = re.search(r'\bOR\b', cleaned, re.IGNORECASE) is not None
    has_not = re.search(r'\bNOT\b', cleaned, re.IGNORECASE) is not None
    
    # Zähle verschiedene Operator-Typen (ohne Klammern)
    operator_types = sum([has_and, has_or, has_not])
    
    # Wenn mehr als 1 Operator-Typ ohne Klammern: FEHLER
    if operator_types > 1:
        return True
    
    return False


def get_mixed_operators_info(query: str) -> Tuple[str, str]:
    """
    Hilfsfunktion für Fehlermeldung.
    
    Args:
        query (str): Query
    
    Returns:
        tuple: (gefundene_operatoren, beispiel)
    """
    cleaned = re.sub(r'\([^)]+\)', '', query)
    
    operators_found = []
    if re.search(r'\bAND\b', cleaned, re.IGNORECASE):
        operators_found.append("AND")
    if re.search(r'\bOR\b', cleaned, re.IGNORECASE):
        operators_found.append("OR")
    if re.search(r'\bNOT\b', cleaned, re.IGNORECASE):
        operators_found.append("NOT")
    
    ops_str = " + ".join(operators_found)
    
    # Beispiel-Korrektur
    if "AND" in operators_found and "OR" in operators_found:
        example = f"Beispiele:\n    ✓ '(A OR B) AND C'  oder\n    ✓ 'A OR (B AND C)'"
    elif "AND" in operators_found and "NOT" in operators_found:
        example = f"Beispiele:\n    ✓ 'NOT (A AND B)'  oder\n    ✓ '(NOT A) AND B'"
    else:  # OR + NOT
        example = f"Beispiele:\n    ✓ 'NOT (A OR B)'  oder\n    ✓ '(NOT A) OR B'"
    
    return ops_str, example


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 2: Single-Line Parsing
# ─────────────────────────────────────────────────────────────────────────────

def tokenize_by_operators(query: str) -> Tuple:
    """
    PHASE 2: Tokenisiert Query nach AND/OR/NOT.
    
    ⚠️  WICHTIG (v2.2): Validiert ZUERST auf gemischte Operatoren!
    
    Args:
        query (str): Single-Line Query
    
    Returns:
        tuple: (terms, operators)
        
    Raises:
        InvalidQueryFormatError: Bei gemischten Operatoren ohne Klammern
    """
    
    # VALIDATION (v2.2): Prüfe auf Operator-Mehrdeutigkeit
    if has_mixed_operators(query):
        ops_str, example = get_mixed_operators_info(query)
        raise InvalidQueryFormatError(
            f"❌ MEHRDEUTIGE OPERATOREN: {ops_str}\n"
            f"\n"
            f"Query: '{query}'\n"
            f"\n"
            f"Problem: Gemischte Operatoren ohne Klammern!\n"
            f"\n"
            f"Diese Query ist mehrdeutig und kann unterschiedlich\n"
            f"interpretiert werden. Bitte klammern Sie den Ausdruck:\n"
            f"\n{example}"
        )
    
    pattern = r'\b(AND|OR|NOT)\b'
    parts = re.split(pattern, query, flags=re.IGNORECASE)
    
    terms = []
    operators = []
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        if part.upper() in {'AND', 'OR', 'NOT'}:
            operators.append(part.upper())
        else:
            terms.append(part)
    
    return terms, operators


def parse_simple_query(query: str) -> str:
    """
    PHASE 2: Parst Single-Line Query.
    
    Args:
        query (str): Single-Line Query
    
    Returns:
        str: Geparste Query mit Klammern
    """
    terms, operators = tokenize_by_operators(query)
    
    wrapped_terms = [f"({term})" for term in terms]
    result = wrapped_terms[0]
    
    for i, operator in enumerate(operators):
        result += f" {operator} {wrapped_terms[i + 1]}"
    
    return f"({result})"


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 3: Multi-Line ODD/EVEN Parsing
# ─────────────────────────────────────────────────────────────────────────────

def parse_query_line(line: str) -> str:
    """
    PHASE 3: Parst eine einzelne Query-Zeile.
    
    Args:
        line (str): Eine Zeile
    
    Returns:
        str: Geparste Zeile
    """
    pattern = r'\b(AND|OR|NOT)\b'
    parts = re.split(pattern, line, flags=re.IGNORECASE)
    
    terms = []
    operators = []
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if part.upper() in {'AND', 'OR', 'NOT'}:
            operators.append(part.upper())
        else:
            terms.append(part)
    
    # Single-Term: nur einfache Klammern
    if len(terms) == 1 and len(operators) == 0:
        return f"({terms[0]})"
    
    # Multiple Terms: doppelte Klammern
    wrapped = [f"({t})" for t in terms]
    result = wrapped[0]
    for i, op in enumerate(operators):
        result += f" {op} {wrapped[i + 1]}"
    
    return f"({result})"


def parse_complex_query(cleaned_query: str) -> str:
    """
    PHASE 3: Parst Multi-Line Query im ODD/EVEN Format.
    
    Args:
        cleaned_query (str): Bereinigte Multi-Line Query
    
    Returns:
        str: Geparste Query
    """
    lines = cleaned_query.split('\n')
    processed_lines = []
    
    for line_num, line in enumerate(lines, start=1):
        is_odd = line_num % 2 == 1
        
        if is_odd:
            processed = parse_query_line(line)
            processed_lines.append(processed)
        else:
            processed = f" {line.upper()} "
            processed_lines.append(processed)
    
    return ''.join(processed_lines)


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 4: Datumsformat & Source-Formatierung
# ─────────────────────────────────────────────────────────────────────────────

class DateFormatConverter:
    """PHASE 4: Konvertiert Datumsformate"""
    
    def __init__(self, source: str):
        self.source = source.lower()
    
    def detect_date_format(self, query: str) -> Tuple[bool, Optional[str], str]:
        """Erkennt Datumsformat (YYYY-YYYY)"""
        pattern = r'(\d{4})-(\d{4})'
        match = re.search(pattern, query)
        
        if match:
            date_range = f"{match.group(1)}-{match.group(2)}"
            query_without_date = query[:match.start()] + query[match.end():]
            query_without_date = query_without_date.replace('()', '').replace('  ', ' ').strip()
            return True, date_range, query_without_date
        
        return False, None, query
    
    def convert_date_format(self, date_range: str) -> str:
        """Konvertiert Datumsformat für Source"""
        start_year, end_year = date_range.split('-')
        
        if self.source == "pubmed":
            return f"({start_year}:{end_year}[pdat])"
        elif self.source == "europepmc":
            return f"(FIRST_PDATE:[{start_year} TO {end_year}])"
        else:
            return f"({date_range})"


class SourceFormatter:
    """PHASE 4: Source-spezifische Formatierung"""
    
    def __init__(self, source: str):
        self.source = source.lower()
    
    def apply_source_formatting(self, query: str) -> str:
        """
        Wendet Source-spezifische Formatierung an.
        
        WICHTIG (v2.1 BUGFIX):
        ═══════════════════════
        Europe PMC braucht NICHT die zusätzlichen äußeren Klammern!
        
        Die äußersten Klammern sind bereits vom Parser vorhanden.
        Zusätzliche Klammern würden zu überflüssigen Verschachtelungen führen.
        """
        if self.source == "pubmed":
            return query
        elif self.source == "europepmc":
            # Europe PMC braucht KEINE zusätzlichen Klammern
            return query
        else:
            return query


# ─────────────────────────────────────────────────────────────────────────────
# UNIFIED PARSER
# ─────────────────────────────────────────────────────────────────────────────

def parse_query_full(raw_query: str, source: str = "pubmed") -> Dict:
    """
    Führt ALLE Phasen (1-4) aus.
    
    Args:
        raw_query (str): Original Query
        source (str): "pubmed" oder "europepmc"
    
    Returns:
        dict: Ergebnisse aus allen Phasen
    """
    result = {
        'success': False,
        'error': None,
        'phases': {}
    }
    
    try:
        # PHASE 1: Cleaning & Format-Erkennung
        cleaned = clean_query(raw_query)
        
        if not cleaned.strip():
            raise InvalidQueryFormatError("Query ist leer!")
        
        is_multi = is_multiline(cleaned)
        format_type = "multi-line" if is_multi else "single-line"
        
        result['phases']['1_cleaning'] = {
            'cleaned_query': cleaned,
            'format': format_type,
            'lines_before': len(raw_query.split('\n')),
            'lines_after': len(cleaned.split('\n'))
        }
        
        # Validierung für Multi-Line
        if is_multi and not is_complex_format(cleaned):
            raise InvalidQueryFormatError("ODD/EVEN Muster verletzt!")
        
        # PHASE 2/3: Parsing
        if is_multi:
            parsed = parse_complex_query(cleaned)
        else:
            parsed = parse_simple_query(cleaned)
        
        result['phases']['2_3_parsing'] = {
            'parsed_query': parsed,
            'format': format_type
        }
        
        # PHASE 4: Datumsformat & Source-Formatierung
        date_converter = DateFormatConverter(source)
        has_date, date_range, query_without_date = date_converter.detect_date_format(raw_query)
        
        final_query = parsed
        
        if has_date:
            converted_date = date_converter.convert_date_format(date_range)
            final_query = parsed + f" AND {converted_date}"
        
        source_formatter = SourceFormatter(source)
        final_output = source_formatter.apply_source_formatting(final_query)
        
        result['phases']['4_formatting'] = {
            'has_date': has_date,
            'date_range': date_range,
            'source': source,
            'final_output': final_output
        }
        
        result['success'] = True
        result['final_output'] = final_output
        
    except Exception as e:
        result['success'] = False
        result['error'] = str(e)
        result['error_traceback'] = traceback.format_exc()
    
    return result


# ════════════════════════════════════════════════════════════════════════════
# PROTOKOLL-GENERATOR
# ════════════════════════════════════════════════════════════════════════════

class ProtocolGenerator:
    """Erstellt detailliertes Protokoll"""
    
    def __init__(self, logger):
        self.logger = logger
    
    def log_header(self, title: str, level: int = 1) -> None:
        """Loggt Header"""
        if level == 1:
            self.logger.info("╔" + "="*78 + "╗")
            self.logger.info("║" + f" {title}".ljust(79) + "║")
            self.logger.info("╚" + "="*78 + "╝")
        elif level == 2:
            self.logger.info("")
            self.logger.info("="*80)
            self.logger.info(title)
            self.logger.info("="*80)
        else:
            self.logger.info("")
            self.logger.info("─"*80)
            self.logger.info(title)
            self.logger.info("─"*80)
    
    def log_test_start(self, filename: str, test_num: int, total: int) -> None:
        """Loggt Test-Start"""
        self.logger.info("")
        self.logger.info("┌" + "─"*78 + "┐")
        self.logger.info(f"│ TEST {test_num}/{total}: {filename}".ljust(79) + "│")
        self.logger.info("└" + "─"*78 + "┘")
        self.logger.info("")
    
    def log_input(self, query: str) -> None:
        """Loggt Input-Query"""
        self.logger.info("INPUT QUERY:")
        self.logger.info("────────────")
        for i, line in enumerate(query.split('\n')[:20], 1):
            self.logger.info(f"  {i:2d}: {line}")
        if len(query.split('\n')) > 20:
            self.logger.info(f"  ... ({len(query.split('\n')) - 20} weitere Zeilen)")
        self.logger.info("")
    
    def log_phase1_results(self, phase1_data: Dict) -> None:
        """Loggt Phase 1 Ergebnisse"""
        self.logger.info("PHASE 1: CLEANING & FORMAT-ERKENNUNG")
        self.logger.info("─" * 40)
        self.logger.info(f"Format erkannt:        {phase1_data['format']}")
        self.logger.info(f"Zeilen vorher:         {phase1_data['lines_before']}")
        self.logger.info(f"Zeilen nachher:        {phase1_data['lines_after']}")
        self.logger.info("")
        self.logger.info("BEREINIGTE QUERY:")
        self.logger.info("────────────────")
        for i, line in enumerate(phase1_data['cleaned_query'].split('\n')[:20], 1):
            self.logger.info(f"  {i:2d}: {line}")
        if len(phase1_data['cleaned_query'].split('\n')) > 20:
            self.logger.info(f"  ... ({len(phase1_data['cleaned_query'].split('\n')) - 20} weitere)")
        self.logger.info("")
    
    def log_phase2_3_results(self, parse_data: Dict) -> None:
        """Loggt Phase 2/3 Ergebnisse"""
        self.logger.info("PHASE 2/3: PARSING & KLAMMERUNG")
        self.logger.info("─" * 40)
        self.logger.info(f"Format:                {parse_data['format']}")
        self.logger.info("")
        self.logger.info("GEPARSTE QUERY:")
        self.logger.info("───────────────")
        parsed_str = parse_data['parsed_query']
        if len(parsed_str) > 70:
            self.logger.info(f"  {parsed_str[:70]}...")
            self.logger.info(f"  {parsed_str[70:]}")
        else:
            self.logger.info(f"  {parsed_str}")
        self.logger.info("")
    
    def log_phase4_results(self, format_data: Dict) -> None:
        """Loggt Phase 4 Ergebnisse"""
        self.logger.info("PHASE 4: DATUMSFORMAT & SOURCE-FORMATIERUNG")
        self.logger.info("─" * 40)
        self.logger.info(f"Datumsformat erkannt:  {format_data['has_date']}")
        if format_data['has_date']:
            self.logger.info(f"Datumsbereich:         {format_data['date_range']}")
        self.logger.info(f"Source:                {format_data['source']}")
        self.logger.info("")
        self.logger.info("FINALE OUTPUT:")
        self.logger.info("──────────────")
        output_str = format_data['final_output']
        if len(output_str) > 70:
            self.logger.info(f"  {output_str[:70]}...")
            self.logger.info(f"  {output_str[70:]}")
        else:
            self.logger.info(f"  {output_str}")
        self.logger.info("")
    
    def log_error(self, error: str, traceback_str: str) -> None:
        """Loggt Fehler"""
        self.logger.info("❌ FEHLER AUFGETRETEN")
        self.logger.info("═" * 40)
        self.logger.info(f"Fehlermeldung:")
        self.logger.info("──────────────")
        for line in error.split('\n'):
            self.logger.info(f"  {line}")
        self.logger.info("")
        self.logger.info("Traceback:")
        self.logger.info("──────────")
        for line in traceback_str.split('\n'):
            if line.strip():
                self.logger.info(f"  {line}")
        self.logger.info("")
    
    def log_success(self, pubmed_output: str, europepmc_output: str) -> None:
        """Loggt erfolgreiche Ausgabe"""
        self.logger.info("✅ ERFOLGREICH VERARBEITET")
        self.logger.info("═" * 40)
        self.logger.info("")
        self.logger.info("OUTPUT - PubMed Format:")
        self.logger.info("──────────────────────")
        if len(pubmed_output) > 70:
            self.logger.info(f"  {pubmed_output[:70]}...")
            for i in range(70, len(pubmed_output), 70):
                self.logger.info(f"  {pubmed_output[i:i+70]}")
        else:
            self.logger.info(f"  {pubmed_output}")
        self.logger.info("")
        
        self.logger.info("OUTPUT - Europe PMC Format:")
        self.logger.info("───────────────────────────")
        if len(europepmc_output) > 70:
            self.logger.info(f"  {europepmc_output[:70]}...")
            for i in range(70, len(europepmc_output), 70):
                self.logger.info(f"  {europepmc_output[i:i+70]}")
        else:
            self.logger.info(f"  {europepmc_output}")
        self.logger.info("")
    
    def log_summary(self, total: int, successful: int) -> None:
        """Loggt Zusammenfassung"""
        self.log_header("FINALE ZUSAMMENFASSUNG", level=2)
        self.logger.info("")
        self.logger.info(f"Tests insgesamt:       {total}")
        self.logger.info(f"Erfolgreich:           {successful} ✅")
        self.logger.info(f"Fehler:                {total - successful} ❌")
        self.logger.info(f"Success Rate:          {(successful/total*100):.1f}%")
        self.logger.info("")


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════

def main():
    """Hauptfunktion"""
    
    # Setup
    logger, log_file = setup_logging()
    protocol = ProtocolGenerator(logger)
    
    # Header
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*10 + "QUERY PARSER - COMPREHENSIVE TEST v2.2 (Precedence)" + " "*17 + "║")
    print("╚" + "="*78 + "╝" + "\n")
    
    logger.info("╔" + "="*78 + "╗")
    logger.info("║" + " "*10 + "QUERY PARSER - COMPREHENSIVE TEST v2.2 (Precedence)" + " "*17 + "║")
    logger.info("║" + " "*15 + "Mit Operator-Precedence-Validierung" + " "*29 + "║")
    logger.info("╚" + "="*78 + "╝")
    logger.info("")
    logger.info("BUGFIX v2.2:")
    logger.info("  ✅ Operator Precedence Validierung")
    logger.info("  ✅ Verhindert mehrdeutige Queries (z.B. 'A OR B AND C')")
    logger.info("")
    logger.info(f"Protokoll-Datei: {log_file}")
    logger.info("")
    
    # Eingabe: Verzeichnis
    test_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    test_path = Path(test_dir)
    
    if not test_path.exists():
        logger.error(f"❌ Verzeichnis nicht gefunden: {test_path.absolute()}")
        return
    
    logger.info(f"Test-Verzeichnis: {test_path.absolute()}")
    logger.info("")
    
    # Lade Test-Dateien
    test_files = sorted(test_path.glob('*.txt'))
    
    if not test_files:
        logger.warning(f"⚠️  Keine .txt Dateien in {test_path.absolute()} gefunden!")
        logger.info("")
        logger.info("Bitte erstelle Test-Dateien im Format:")
        logger.info("──────────────────────────────────────")
        logger.info("""
cancer OR tumor
AND
treatment

Oder Single-Line:

cancer OR tumor AND treatment

Test mit Operator-Precedence-Validierung:

A OR B AND C  ← Dies wird FEHLER geben (mehrdeutig!)
(A OR B) AND C  ← Dies ist korrekt (geklammert)
""")
        return
    
    logger.info(f"✓ {len(test_files)} Test-Dateien gefunden:")
    for f in test_files:
        logger.info(f"  - {f.name}")
    logger.info("")
    
    protocol.log_header("TEST-EXECUTION", level=2)
    
    # Führe Tests aus
    results = []
    
    for test_num, test_file in enumerate(test_files, 1):
        protocol.log_test_start(test_file.name, test_num, len(test_files))
        
        try:
            # Lese Datei
            with open(test_file, 'r', encoding='utf-8') as f:
                raw_query = f.read()
            
            protocol.log_input(raw_query)
            
            # Verarbeite für beide Sources
            pubmed_result = parse_query_full(raw_query, "pubmed")
            europepmc_result = parse_query_full(raw_query, "europepmc")
            
            # Protokoll
            if pubmed_result['success']:
                protocol.log_phase1_results(pubmed_result['phases']['1_cleaning'])
                protocol.log_phase2_3_results(pubmed_result['phases']['2_3_parsing'])
                protocol.log_phase4_results(pubmed_result['phases']['4_formatting'])
                protocol.log_success(
                    pubmed_result['final_output'],
                    europepmc_result['final_output']
                )
                
                results.append({
                    'file': test_file.name,
                    'success': True,
                    'pubmed': pubmed_result['final_output'],
                    'europepmc': europepmc_result['final_output']
                })
                
                logger.info("RESULT: ✅ TEST BESTANDEN")
            else:
                protocol.log_error(
                    pubmed_result['error'],
                    pubmed_result.get('error_traceback', '')
                )
                
                results.append({
                    'file': test_file.name,
                    'success': False,
                    'error': pubmed_result['error']
                })
                
                logger.info("RESULT: ❌ TEST FEHLGESCHLAGEN")
            
            logger.info("")
            
        except Exception as e:
            logger.error(f"❌ Unerwarteter Fehler: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            results.append({
                'file': test_file.name,
                'success': False,
                'error': str(e)
            })
    
    # Zusammenfassung
    successful = sum(1 for r in results if r['success'])
    protocol.log_summary(len(test_files), successful)
    
    # Detaillierte Ergebnisse
    logger.info("DETAILLIERTE ERGEBNISSE:")
    logger.info("────────────────────────")
    logger.info("")
    
    for result in results:
        if result['success']:
            logger.info(f"✅ {result['file']}")
            logger.info(f"   PubMed:     {result['pubmed'][:60]}...")
            logger.info(f"   Europe PMC: {result['europepmc'][:60]}...")
        else:
            logger.info(f"❌ {result['file']}")
            logger.info(f"   Error: {result['error'][:60]}...")
        logger.info("")
    
    logger.info("="*80)
    logger.info(f"Protokoll gespeichert: {log_file}")
    logger.info("="*80)
    
    print(f"\n✅ Test-Protokoll gespeichert: {log_file}\n")


if __name__ == "__main__":
    main()
