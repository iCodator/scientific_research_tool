#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Query Compiler für PubMed und Europe PMC - v2.4.1 (BUGFIX)
BUGFIX in v2.4.1:
- ✅ MultiLevelQueryParser wird IMMER aufgerufen für mehrzeilige Queries
- ✅ Klammerung für Query-Zeilen: ((term1) OR (term2))
- ✅ Operatoren werden zwischen geklammerten Blöcken gesetzt
- ✅ Datumsformat-Konvertierung funktioniert korrekt
"""

import json
import re
import logging
from typing import Dict, List, Optional, Tuple

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MultiLevelQueryParser:
    """
    Parser für mehrzeilige Queries mit Multi-Level Grouping.
    BUGFIX v2.4.1: Klammerung wird KORREKT gesetzt!
    """
    
    def __init__(self, raw_query: str, source: str = "pubmed"):
        self.raw_query = raw_query
        self.source = source
        self.lines = []
        self.categorized_lines = []
        self.processed_parts = []
        self.final_query = ""
    
    def parse(self) -> str:
        """Hauptmethode zum Parsen."""
        self._split_lines()
        self._categorize_lines()
        self._normalize_lines()
        self._combine_with_operators()
        return self.final_query
    
    def _split_lines(self):
        """Teilt rohe Query in Zeilen auf."""
        self.lines = [line.strip() for line in self.raw_query.strip().split('\n')]
    
    def _categorize_lines(self):
        """Kategorisiert Zeilen in OPERATOR, QUERY oder DATE."""
        for line in self.lines:
            # Ignoriere leere Zeilen
            if not line:
                continue
            
            # Ignoriere Kommentare
            if line.startswith('#'):
                continue
            
            # Prüfe ob reine Operator-Zeile
            if line in ['AND', 'OR', 'NOT']:
                self.categorized_lines.append(('OPERATOR', line))
            # Prüfe ob Datumszeile
            elif self._is_date_format(line):
                self.categorized_lines.append(('DATE', line))
            else:
                self.categorized_lines.append(('QUERY', line))
    
    def _is_date_format(self, line: str) -> bool:
        """Prüft ob die Zeile ein Datumsformat ist."""
        pattern = r'^\(?(\d{4})[-:](\d{4})\)?$'
        return bool(re.match(pattern, line))
    
    def _normalize_date_line(self, date_line: str) -> str:
        """Normalisiert eine Datumszeile für die Zielquelle."""
        match = re.search(r'(\d{4})[-:](\d{4})', date_line)
        if not match:
            return date_line
        
        start_year = match.group(1)
        end_year = match.group(2)
        
        if self.source == "pubmed":
            return f"({start_year}:{end_year}[pdat])"
        else:  # europepmc
            return f"(FIRST_PDATE:[{start_year} TO {end_year}])"
    
    def _normalize_query_line(self, query_line: str) -> str:
        """
        BUGFIX v2.4.1: Normalisiert Query-Zeile mit korrekter Klammerung.
        
        Input:  "Coenzyme Q10 OR ubiquinol"
        Output: "((Coenzyme Q10) OR (ubiquinol))"
        """
        # Tokenisiere nach Boolean-Operatoren
        tokens = self._tokenize_line(query_line)
        
        # Verarbeite Tokens: Operatoren bleiben, Terms werden geklammert
        result_parts = []
        for token in tokens:
            if token in ['AND', 'OR', 'NOT']:
                # Operator: wird später zwischen Blöcken gesetzt, nicht hier
                result_parts.append(('OPERATOR', token))
            else:
                # Term: wird geklammert
                result_parts.append(('TERM', token))
        
        # Baue Query-Zeile mit Klammerung
        # Format: ((term1) OR (term2))
        output = []
        output.append('(')  # Äußere Klammer öffnen
        
        for i, (token_type, content) in enumerate(result_parts):
            if token_type == 'TERM':
                output.append(f"({content})")
            else:  # OPERATOR
                output.append(f" {content} ")
        
        output.append(')')  # Äußere Klammer schließen
        
        return ''.join(output)
    
    def _tokenize_line(self, line: str) -> List[str]:
        """Tokenisiert eine Zeile nach Boolean-Operatoren."""
        tokens = []
        current_token = ""
        depth = 0
        in_quotes = False
        i = 0
        
        while i < len(line):
            char = line[i]
            
            if char == '"':
                in_quotes = not in_quotes
                current_token += char
            elif char == '(' and not in_quotes:
                depth += 1
                current_token += char
            elif char == ')' and not in_quotes:
                depth -= 1
                current_token += char
            elif depth == 0 and not in_quotes:
                # Prüfe auf Operatoren bei depth 0
                if line[i:i+4] == ' OR ':
                    if current_token.strip():
                        tokens.append(current_token.strip())
                    tokens.append('OR')
                    current_token = ""
                    i += 4
                    continue
                elif line[i:i+5] == ' AND ':
                    if current_token.strip():
                        tokens.append(current_token.strip())
                    tokens.append('AND')
                    current_token = ""
                    i += 5
                    continue
                elif line[i:i+5] == ' NOT ':
                    if current_token.strip():
                        tokens.append(current_token.strip())
                    tokens.append('NOT')
                    current_token = ""
                    i += 5
                    continue
                else:
                    current_token += char
            else:
                current_token += char
            
            i += 1
        
        if current_token.strip():
            tokens.append(current_token.strip())
        
        return tokens
    
    def _normalize_lines(self):
        """Normalisiert alle Zeilen (Queries, Dates, Operators)."""
        for line_type, content in self.categorized_lines:
            if line_type == 'QUERY':
                normalized = self._normalize_query_line(content)
                self.processed_parts.append(('NORMALIZED_QUERY', normalized))
            elif line_type == 'DATE':
                normalized = self._normalize_date_line(content)
                self.processed_parts.append(('NORMALIZED_QUERY', normalized))
            else:  # OPERATOR
                self.processed_parts.append(('OPERATOR', content))
    
    def _combine_with_operators(self):
        """
        BUGFIX v2.4.1: Kombiniert Query-Blöcke mit Operatoren korrekt.
        
        Query1 + OPERATOR + Query2 + OPERATOR + Query3
        ↓
        (Query1) OPERATOR (Query2) OPERATOR (Query3)
        """
        parts = []
        
        for line_type, content in self.processed_parts:
            if line_type == 'NORMALIZED_QUERY':
                parts.append(content)
            else:  # OPERATOR
                parts.append(f" {content} ")
        
        self.final_query = ''.join(parts)
    
    def get_info(self) -> Dict:
        """Gibt Informationen über das Parsing zurück."""
        return {
            'total_lines': len(self.lines),
            'query_lines': sum(1 for t, _ in self.categorized_lines if t == 'QUERY'),
            'date_lines': sum(1 for t, _ in self.categorized_lines if t == 'DATE'),
            'operator_lines': sum(1 for t, _ in self.categorized_lines if t == 'OPERATOR'),
            'final_length': len(self.final_query),
            'parentheses_open': self.final_query.count('('),
            'parentheses_close': self.final_query.count(')'),
            'balanced': self.final_query.count('(') == self.final_query.count(')')
        }


class UniversalQueryCompiler:
    """
    Universal Query Compiler v2.4.1 (BUGFIX)
    
    BUGFIX in v2.4.1:
    ✅ MultiLevelQueryParser wird IMMER für mehrzeilige Queries aufgerufen
    ✅ Klammerung wird korrekt gesetzt
    ✅ Alle Features aus v2.4.0 beibehalten
    """
    
    def __init__(self, query: str = "", source: str = "pubmed"):
        self.query = query
        self.source = source
        self.normalized_query = ""
        self.ruleset = None
        self.errors = []
        self.warnings = []
        self.conversions = []
        self.is_multiline = '\n' in query
        
        logger.info(f"QueryCompiler v2.4.1 initialisiert: multiline={self.is_multiline}, source={source}")
    
    def load_ruleset(self, ruleset_path: str) -> bool:
        """Lädt ein Regelwerk aus JSON-Datei."""
        try:
            with open(ruleset_path, 'r', encoding='utf-8') as f:
                self.ruleset = json.load(f)
            logger.info(f"Regelwerk geladen: {ruleset_path}")
            return True
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Regelwerk-Fehler: {e}")
            return False
    
    def load_ruleset_from_dict(self, ruleset: Dict) -> None:
        """Lädt ein Regelwerk aus Dictionary."""
        self.ruleset = ruleset
        logger.info("Regelwerk aus Dictionary geladen")
    
    def normalize(self) -> str:
        """
        Normalisiert die Query nach Quelle.
        BUGFIX v2.4.1: MultiLevelQueryParser für mehrzeilige Queries!
        """
        if self.is_multiline:
            # BUGFIX: MultiLevelQueryParser wird IMMER aufgerufen für '\n' Queries
            logger.info("Multi-Line Query erkannt - nutze MultiLevelQueryParser")
            parser = MultiLevelQueryParser(self.query, source=self.source)
            self.normalized_query = parser.parse()
            
            # Logging
            info = parser.get_info()
            logger.info(f"Multi-Level Parsing: {info['query_lines']} Queries, "
                       f"{info['operator_lines']} Operators, "
                       f"{info['date_lines']} Dates")
            logger.info(f"Klammern: {info['parentheses_open']} öffnend, "
                       f"{info['parentheses_close']} schließend, "
                       f"balanciert: {info['balanced']}")
        else:
            # Single-Line Queries
            if self.source == "pubmed":
                self.normalized_query = self._normalize_pubmed(self.query)
            elif self.source == "europepmc":
                self.normalized_query = self._normalize_europepmc(self.query)
            else:
                self.normalized_query = self._normalize_universal(self.query)
        
        logger.info(f"Query normalisiert (Länge: {len(self.normalized_query)})")
        return self.normalized_query
    
    def _normalize_pubmed(self, query: str) -> str:
        """PubMed Normalisierung (Single-Line)."""
        result = re.sub(r'\s+', ' ', query).strip()
        result = self._convert_dates_single_line(result, "pubmed")
        return result
    
    def _normalize_europepmc(self, query: str) -> str:
        """Europe PMC Normalisierung (Single-Line)."""
        result = re.sub(r'\s+', ' ', query).strip()
        result = self._convert_dates_single_line(result, "europepmc")
        return result
    
    def _normalize_universal(self, query: str) -> str:
        """Universelle Normalisierung."""
        return re.sub(r'\s+', ' ', query).strip()
    
    def _convert_dates_single_line(self, query: str, source: str) -> str:
        """Konvertiert Datumsformate auch in Single-Line Queries."""
        if source == "pubmed":
            query = re.sub(r'\((\d{4})-(\d{4})\)', r'(\1:\2[pdat])', query)
            query = re.sub(r'(?<!\()(\d{4})-(\d{4})(?!\))', r'(\1:\2[pdat])', query)
        else:  # europepmc
            query = re.sub(r'\((\d{4})-(\d{4})\)', r'(FIRST_PDATE:[\1 TO \2])', query)
            query = re.sub(r'(?<!\()?(\d{4})-(\d{4})(?!\))?', r'(FIRST_PDATE:[\1 TO \2])', query)
        
        return query
    
    def validate(self) -> bool:
        """Validiert die Query."""
        self.errors = []
        self.warnings = []
        
        if not self._check_balanced_parentheses(self.normalized_query):
            self.errors.append("Klammern nicht balanciert")
            return False
        
        if not self._check_valid_operators(self.normalized_query):
            self.errors.append("Ungültige Boolean-Operatoren")
            return False
        
        if not self._check_double_quotes(self.normalized_query):
            self.errors.append("Einfache Anführungszeichen gefunden")
            return False
        
        logger.info("Query-Validierung erfolgreich ✓")
        return True
    
    def _check_balanced_parentheses(self, query: str) -> bool:
        """Prüft balancierte Klammern."""
        return query.count('(') == query.count(')')
    
    def _check_valid_operators(self, query: str) -> bool:
        """Prüft gültige Boolean-Operatoren."""
        invalid_operators = re.findall(r'\b(and|or|not)\b', query)
        return len(invalid_operators) == 0
    
    def _check_double_quotes(self, query: str) -> bool:
        """Prüft nur doppelte Anführungszeichen."""
        return "'" not in query
    
    def convert_to_europepmc(self) -> str:
        """Konvertiert Query zu Europe PMC-Format."""
        result = self.normalized_query
        self.conversions = []
        
        # Datumskonvertierung (falls noch nicht geschehen)
        result = self._convert_dates_if_needed(result, "europepmc")
        
        # NOT-Operator verdoppeln
        result = re.sub(r'NOT\s+\(\(([^()]+)\)\)', r'NOT (((\1)))', result)
        
        # Äußere Klammern (wenn nicht vorhanden)
        if not result.startswith('(('):
            result = f"({result})"
        
        self.conversions.append("Europe PMC Format angewandt")
        return result
    
    def _convert_dates_if_needed(self, query: str, source: str) -> str:
        """Konvertiert Datumsformate bei Bedarf."""
        if source == "europepmc":
            # Konvertiere [pdat] zu FIRST_PDATE
            query = re.sub(r'\((\d{4}):(\d{4})\[pdat\]\)', r'(FIRST_PDATE:[\1 TO \2])', query)
        return query
    
    def get_stats(self) -> Dict:
        """Gibt Statistiken zurück."""
        return {
            'source': self.source,
            'is_multiline': self.is_multiline,
            'query_length': len(self.query),
            'normalized_length': len(self.normalized_query),
            'parentheses': self.normalized_query.count('('),
            'balanced': self.normalized_query.count('(') == self.normalized_query.count(')'),
            'errors': len(self.errors),
            'warnings': len(self.warnings),
            'conversions': len(self.conversions)
        }
    
    def print_info(self) -> None:
        """Gibt Informationen aus."""
        print("\n" + "="*70)
        print("QUERY COMPILER v2.4.1 (BUGFIX) - INFORMATIONEN")
        print("="*70)
        print(f"\nQuelle:           {self.source}")
        print(f"Mehrzeilig:       {self.is_multiline}")
        print(f"Original Query:   {self.query[:50]}...")
        print(f"Normalisiert:     {self.normalized_query[:80]}...")
        
        if self.errors:
            print(f"\n❌ Fehler ({len(self.errors)}):")
            for error in self.errors:
                print(f"   - {error}")
        
        if self.conversions:
            print(f"\n🔄 Konvertierungen ({len(self.conversions)}):")
            for conversion in self.conversions:
                print(f"   - {conversion}")
        
        print("\n" + "="*70 + "\n")
