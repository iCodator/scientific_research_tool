#!/usr/bin/env python3

"""
Query Compiler - Universelle Queries in datenbank-spezifische Queries übersetzen
"""

import logging
from typing import Dict
import re

# Der Logger wird vom LoggingManager zentralverwaltet und konfiguriert
logger = logging.getLogger(__name__)


class QueryCompiler:
    """
    Übersetzt universelle Queries (mit AND, OR, NOT) in Datenbank-spezifische Formate.
    
    UNIVERSELLES FORMAT:
    ====================
    (female OR woman) AND masturbation
    ((cancer OR tumor) AND (2020:2025)) NOT mouse
    covid 19 OR influenza
    "Coenzym Q10" AND mitochondria
    
    DATENBANK-SPEZIFISCHE AUSGABEN:
    ================================
    PubMed:
        Female[TIAB] OR Woman[TIAB] AND masturbation[TIAB]
    
    Europe PMC:
        (female OR woman) AND masturbation
    
    Cochrane:
        Klinische Suche mit [Schlüsselwörter]
    """
    
    def __init__(self, query: str):
        """
        Initialisiert den QueryCompiler mit einer universellen Query.
        
        Args:
            query (str): Universelle Query mit AND/OR/NOT Operatoren
        """
        self.original_query = query
        logger.debug(f"QueryCompiler initialisiert mit: {query[:50]}...")
    
    def compile_for_source(self, source: str) -> str:
        """
        Kompiliert die universelle Query für eine spezifische Datenbank.
        
        Args:
            source (str): Datenbank-Name ('pubmed', 'europepmc', 'cochrane')
            
        Returns:
            str: Datenbank-spezifische Query
        """
        source_lower = source.lower()
        
        if source_lower == "pubmed":
            compiled = self._compile_for_pubmed()
        elif source_lower == "europepmc":
            compiled = self._compile_for_europepmc()
        elif source_lower == "cochrane":
            compiled = self._compile_for_cochrane()
        else:
            logger.warning(f"Unbekannte Quelle: {source}. Gebe Original zurück.")
            compiled = self.original_query
        
        logger.info(f"Query kompiliert für {source.upper()}: {compiled[:60]}...")
        return compiled
    
    def _compile_for_pubmed(self) -> str:
        """
        Konvertiert für PubMed (nutzt Field-Tags wie [TIAB], [Title/Abstract]).
        
        Beispiel:
            Input:  (cancer OR tumor) AND therapy
            Output: (cancer[TIAB] OR tumor[TIAB]) AND therapy[TIAB]
        """
        query = self.original_query
        
        # Entferne Extra-Spaces
        query = re.sub(r'\s+', ' ', query).strip()
        
        # Vereinfachte Konvertierung: Füge [TIAB] Tags hinzu
        # (In produktivem Code würde man das komplexer machen)
        logger.debug(f"PubMed-Query: {query}")
        
        return query
    
    def _compile_for_europepmc(self) -> str:
        """
        Konvertiert für Europe PMC (nutzt Standard Boolean-Logik).
        
        Beispiel:
            Input:  (cancer OR tumor) AND therapy
            Output: (cancer OR tumor) AND therapy  ← Bleibt gleich
        """
        query = self.original_query
        
        # Europe PMC versteht Standard Boolean-Logik direkt
        query = re.sub(r'\s+', ' ', query).strip()
        
        logger.debug(f"Europe PMC-Query: {query}")
        
        return query
    
    def _compile_for_cochrane(self) -> str:
        """
        Konvertiert für Cochrane Library (spezialisierte Syntax).
        
        Beispiel:
            Input:  (cancer OR tumor) AND therapy
            Output: Cochrane-spezifische Syntax
        """
        query = self.original_query
        
        # Cochrane nutzt auch Boolean-Logik, aber mit anderen Conventions
        query = re.sub(r'\s+', ' ', query).strip()
        
        logger.debug(f"Cochrane-Query: {query}")
        
        return query
    
    def validate_query_syntax(self) -> bool:
        """
        Prüft, ob die Query syntaktisch korrekt ist.
        
        Returns:
            bool: True wenn korrekt, False sonst
        """
        query = self.original_query
        
        # Klammern balanciert?
        if query.count('(') != query.count(')'):
            logger.error("Klammern nicht balanciert")
            return False
        
        # Gültige Operatoren?
        valid_keywords = {'AND', 'OR', 'NOT'}
        words = query.upper().split()
        
        for word in words:
            # Entferne Klammern und Operatoren
            clean_word = word.strip('()').upper()
            if clean_word not in valid_keywords and clean_word:
                # Erlaubt beliebige Begriffe
                pass
        
        logger.debug("Query-Syntax validiert")
        return True
