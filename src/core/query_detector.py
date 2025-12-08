"""
Modul: Query-Detektor (Auto-Detection für Queries)
===================================================
Zweck: Erkennt automatisch, ob eine Query bereits formatiert ist.

LOGIK:
1. Prüfe auf PubMed-Syntax Marker ([Title/Abstract], [MeSH Terms], [pdat])
2. Prüfe auf Europe PMC-Syntax Marker (PUB_YEAR:, TITLE_ABSTRACT:)
3. Falls keine Marker: Behandle als natürlichsprachige Anfrage → LLM

BEISPIELE:
  Input: '("Ubiquinone"[Title/Abstract] OR "CoQ10"[Title/Abstract]) AND (2005:2025[pdat])'
  → Erkannt als: PubMed Pre-formatted
  → Aktion: Direkt nutzen, keine LLM-Verarbeitung

  Input: 'Physiologische Funktionen des Coenzym Q10'
  → Erkannt als: Natural Language (Deutsch)
  → Aktion: An LLM schicken zur Analyse

VERWENDUNG:
  from src.core.query_detector import QueryDetector, QueryType
  
  detector = QueryDetector()
  query_type, is_formatted, detected_source = detector.detect(query_string)
  
  if is_formatted:
      # Direkt verwenden
      results = search_database(query_string, source=detected_source)
  else:
      # An LLM schicken
      analysis = compiler.compile_from_text(query_string)
"""

import re
import logging
from enum import Enum
from typing import Tuple

logger = logging.getLogger(__name__)


class QueryType(Enum):
    """Enumeration für erkannte Query-Typen."""
    PUBMED_FORMATTED = "pubmed_formatted"
    EUROPE_PMC_FORMATTED = "europe_pmc_formatted"
    NATURAL_LANGUAGE_DE = "natural_language_de"
    NATURAL_LANGUAGE_EN = "natural_language_en"
    UNKNOWN = "unknown"


class QueryDetector:
    """
    Intelligenter Query-Detektor.
    
    Diese Klasse analysiert eine Anfrage und erkennt automatisch,
    ob sie bereits in Datenbank-Syntax formatiert ist oder
    noch in natürlichsprachiger Form vorliegt.
    """
    
    # ========== PubMed-Syntax Marker ==========
    PUBMED_MARKERS = [
        r'\[Title/Abstract\]',      # Standard PubMed Field
        r'\[MeSH Terms\]',          # MeSH Hierarchy
        r'\[MeSH Major Topic\]',    # MeSH Major Topic
        r'\[pdat\]',                # Publication Date
        r'\[AU\]',                  # Author
        r'\[TA\]',                  # Journal Title Abbreviation
        r'\[All Fields\]',          # All Fields
    ]
    
    # ========== Europe PMC-Syntax Marker ==========
    EUROPE_PMC_MARKERS = [
        r'TITLE_ABSTRACT:',         # Titel/Abstract Field
        r'ABSTRACT:',               # Abstract nur
        r'TITLE:',                  # Titel nur
        r'PUB_YEAR:\[',             # Publication Year Range
        r'AUTHOR:',                 # Author Field
        r'IS_OPEN_ACCESS:',         # Open Access Filter
        r'JOURNAL:',                # Journal Field
    ]
    
    # ========== Syntaktische Komplexität ==========
    # Wenn Query viele Operatoren und Klammern hat, ist sie wahrscheinlich formatiert
    OPERATORS = ['AND', 'OR', 'NOT']
    
    def detect(self, query_string: str) -> Tuple[QueryType, bool, str]:
        """
        Erkennt den Query-Typ und ob er bereits formatiert ist.
        
        Argumente:
            query_string (str): Die zu analysierende Query
        
        Rückgabewert:
            Tuple[QueryType, bool, str]:
            - QueryType: Der erkannte Query-Typ
            - bool: Ist die Query bereits formatiert?
            - str: Erkannte Quellendatenbank ("pubmed" oder "europe_pmc")
        
        Beispiele:
            >>> detector = QueryDetector()
            
            >>> query = '("Ubiquinone"[Title/Abstract]) AND (2005:2025[pdat])'
            >>> typ, is_fmt, src = detector.detect(query)
            >>> print(typ, is_fmt, src)
            QueryType.PUBMED_FORMATTED True pubmed
            
            >>> query = 'Suche nach Coenzym Q10 Funktionen'
            >>> typ, is_fmt, src = detector.detect(query)
            >>> print(typ, is_fmt, src)
            QueryType.NATURAL_LANGUAGE_DE False pubmed
        """
        
        logger.debug(f"Analysiere Query: {query_string[:60]}...")
        
        # ========== SCHRITT 1: PubMed-Syntax prüfen ==========
        if self._has_pubmed_syntax(query_string):
            logger.info("✓ PubMed-formatierte Query erkannt")
            return QueryType.PUBMED_FORMATTED, True, "pubmed"
        
        # ========== SCHRITT 2: Europe PMC-Syntax prüfen ==========
        if self._has_europe_pmc_syntax(query_string):
            logger.info("✓ Europe PMC-formatierte Query erkannt")
            return QueryType.EUROPE_PMC_FORMATTED, True, "europe_pmc"
        
        # ========== SCHRITT 3: Sprache erkennen (Deutsch vs. Englisch) ==========
        if self._is_german(query_string):
            logger.info("✓ Natürlichsprachige Query (Deutsch) erkannt")
            return QueryType.NATURAL_LANGUAGE_DE, False, "pubmed"
        else:
            logger.info("✓ Natürlichsprachige Query (Englisch) erkannt")
            return QueryType.NATURAL_LANGUAGE_EN, False, "pubmed"
    
    def _has_pubmed_syntax(self, query_string: str) -> bool:
        """
        Prüft, ob die Query PubMed-Syntax-Marker enthält.
        
        Argumente:
            query_string (str): Die zu prüfende Query
        
        Rückgabewert:
            bool: True wenn mindestens 2 PubMed-Marker gefunden
        """
        
        marker_count = 0
        
        for marker in self.PUBMED_MARKERS:
            if re.search(marker, query_string, re.IGNORECASE):
                marker_count += 1
                logger.debug(f"  PubMed-Marker gefunden: {marker}")
        
        # Mindestens 2 Marker für hohe Confidence
        if marker_count >= 2:
            logger.debug(f"  PubMed-Syntax erkannt ({marker_count} Marker)")
            return True
        
        # Falls nur 1 Marker aber mit komplexer Syntax
        if marker_count >= 1:
            if self._has_complex_syntax(query_string):
                logger.debug(f"  PubMed-Syntax erkannt (1 Marker + komplexe Syntax)")
                return True
        
        return False
    
    def _has_europe_pmc_syntax(self, query_string: str) -> bool:
        """
        Prüft, ob die Query Europe PMC-Syntax-Marker enthält.
        
        Argumente:
            query_string (str): Die zu prüfende Query
        
        Rückgabewert:
            bool: True wenn mindestens 1 Europe PMC-Marker gefunden
        """
        
        marker_count = 0
        
        for marker in self.EUROPE_PMC_MARKERS:
            if re.search(marker, query_string, re.IGNORECASE):
                marker_count += 1
                logger.debug(f"  Europe PMC-Marker gefunden: {marker}")
        
        # Mindestens 1 Marker für Europe PMC
        if marker_count >= 1:
            logger.debug(f"  Europe PMC-Syntax erkannt ({marker_count} Marker)")
            return True
        
        return False
    
    def _has_complex_syntax(self, query_string: str) -> bool:
        """
        Prüft, ob die Query komplexe syntaktische Struktur hat.
        
        Indikationen:
        - Viele Klammern
        - Multiple AND/OR/NOT Operatoren
        - Anführungszeichen für exakte Phrasen
        
        Argumente:
            query_string (str): Die zu prüfende Query
        
        Rückgabewert:
            bool: True wenn komplexe Syntax erkannt
        """
        
        # Zähle Klammern
        bracket_count = query_string.count('(') + query_string.count('[')
        
        # Zähle Operatoren
        operator_count = 0
        for op in self.OPERATORS:
            operator_count += query_string.count(f" {op} ")
        
        # Zähle Anführungszeichen (Phrasensuche)
        quote_count = query_string.count('"')
        
        logger.debug(f"  Syntax-Komplexität: {bracket_count} Klammern, {operator_count} Operatoren, {quote_count} Zitate")
        
        # Komplexität liegt vor, wenn:
        # - Mindestens 2 Klammern UND mindestens 1 Operator
        # - Oder mindestens 4 Klammern
        # - Oder mindestens 2 Operatoren
        
        if (bracket_count >= 2 and operator_count >= 1) or bracket_count >= 4 or operator_count >= 2:
            return True
        
        return False
    
    def _is_german(self, query_string: str) -> bool:
        """
        Erkennt, ob ein Text auf Deutsch ist (vs. Englisch).
        
        Heuristische Methoden:
        - Prüfe auf deutsche Umlaute (ä, ö, ü, ß)
        - Prüfe auf häufige deutsche Wörter
        - Prüfe auf deutsche Satzstruktur
        
        Argumente:
            query_string (str): Der zu analysierende Text
        
        Rückgabewert:
            bool: True wenn Text auf Deutsch erkannt
        """
        
        # ========== Deutsche Umlaute ==========
        if re.search(r'[äöüß]', query_string, re.IGNORECASE):
            logger.debug("  Deutsch erkannt: Umlaute vorhanden")
            return True
        
        # ========== Deutsche Schlüsselwörter ==========
        german_keywords = [
            'funktionen', 'funktionalität', 'physiologisch', 'grundlagenforschung',
            'keine tierversuche', 'ausgenommen', 'koenzym', 'forschung', 'studie',
            'untersuchung', 'analyse', 'mechanismus', 'wirkung', 'effekt',
            'veränderung', 'unterstützung', 'rolle', 'bedeutung', 'beeinflussung',
        ]
        
        query_lower = query_string.lower()
        german_count = sum(1 for kw in german_keywords if kw in query_lower)
        
        if german_count >= 2:
            logger.debug(f"  Deutsch erkannt: {german_count} deutsche Keywords")
            return True
        
        # ========== Fallback: Text-Länge und Struktur ==========
        # Sehr kurze Queries oder pure Datenbank-Syntax → nicht als Deutsch klassifizieren
        if len(query_string) < 10 or query_string.count('[') > 0:
            logger.debug("  Englisch/Unbekannt: Sehr kurz oder syntaktisch")
            return False
        
        # Längere natürlichsprachige Queries ohne deutsche Marker → vermutlich Englisch
        logger.debug("  Englisch/Unbekannt: Keine eindeutigen Marker")
        return False
    
    def print_detection_result(self, query_string: str):
        """
        Gibt eine benutzerfreundliche Analyse der Query aus.
        
        Argumente:
            query_string (str): Die zu analysierende Query
        """
        
        query_type, is_formatted, source = self.detect(query_string)
        
        print("\n" + "=" * 80)
        print("QUERY-ANALYSE")
        print("=" * 80)
        
        print(f"\nEingabe: {query_string[:100]}{'...' if len(query_string) > 100 else ''}")
        
        print(f"\n🔍 Erkannter Typ: {query_type.value}")
        
        if is_formatted:
            print(f"✓ Query ist bereits formatiert")
            print(f"  Datenbank: {source.upper()}")
            print(f"  Aktion: Direkt in DB-Suche verwenden, KEINE LLM-Verarbeitung")
        else:
            print(f"❌ Query ist noch natürlichsprachig")
            print(f"  Sprache: Deutsch" if query_type == QueryType.NATURAL_LANGUAGE_DE else "  Sprache: Englisch")
            print(f"  Aktion: An Perplexity LLM schicken zur Analyse")
        
        print("\n" + "=" * 80)


# ========== Hilfsfunktion für einfache Nutzung ==========
def detect_query_type(query_string: str) -> Tuple[QueryType, bool, str]:
    """
    Convenience-Funktion zum Erkennen von Query-Typen.
    
    Argumente:
        query_string (str): Die zu analysierende Query
    
    Rückgabewert:
        Tuple[QueryType, bool, str]: (Typ, ist_formatiert, Quelle)
    
    Beispiel:
        >>> query_type, is_formatted, source = detect_query_type("my search query")
        >>> if is_formatted:
        ...     search_database(query, source=source)
        ... else:
        ...     compile_with_llm(query)
    """
    detector = QueryDetector()
    return detector.detect(query_string)
