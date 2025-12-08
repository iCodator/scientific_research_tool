"""
Modul: Query Validator
======================
Zweck: Überprüft, ob eine Suchanfrage für die jeweilige Datenbank
       syntaktisch korrekt und ausreichend formatiert ist.

Warum?
- Verhindert unnötige API-Calls mit kaputten Queries.
- Gibt dem Nutzer Feedback, wenn er natürlichsprachige Fragen statt
  strukturierter Queries eingibt.
"""

import logging
import re
from enum import Enum

logger = logging.getLogger(__name__)

class QueryType(Enum):
    FORMATTED = "formatted"
    NATURAL = "natural"
    UNKNOWN = "unknown"

class QueryValidator:
    """
    Analysiert und validiert Suchanfragen.
    """
    
    def __init__(self):
        pass
        
    def analyze(self, query: str, source: str) -> tuple[bool, str]:
        """
        Analysiert eine Query.
        
        Args:
            query (str): Der Suchtext
            source (str): 'pubmed', 'europe_pmc', oder 'cochrane'
            
        Returns:
            tuple[bool, str]: (is_valid, message)
        """
        if not query or len(query.strip()) < 3:
            return False, "Query ist zu kurz oder leer."
            
        # Check: Ist es eine formatierte Query?
        is_formatted = self._is_formatted(query, source)
        
        if not is_formatted:
            return False, (
                f"⚠ Das sieht nach einer natürlichsprachigen Frage aus.\n"
                f"Bitte verwende eine strukturierte Query für {source.upper()}.\n"
                f"Beispiel: (cancer AND therapy) AND (2020:2025[pdat])"
            )
            
        # Check: Basis-Syntax (Klammern)
        if not self._check_brackets(query):
            return False, "Klammern sind nicht balanciert (Anzahl '(' != Anzahl ')')."
            
        return True, "Query ist gültig."

    def _is_formatted(self, query: str, source: str) -> bool:
        """Prüft auf typische Syntax-Merkmale."""
        
        # Gemeinsame Merkmale für alle: AND/OR/NOT
        has_operators = any(op in query for op in [" AND ", " OR ", " NOT ", ") AND ("])
        
        if source == 'pubmed':
            # PubMed spezifisch: [Title/Abstract], [MeSH], [pdat]
            has_tags = '[' in query and ']' in query
            return has_operators or has_tags
            
        elif source == 'europe_pmc':
            # Europe PMC spezifisch: TITLE_ABSTRACT:, PUB_YEAR:
            has_fields = 'TITLE:' in query or 'ABSTRACT:' in query or 'PUB_YEAR:' in query
            return has_operators or has_fields
            
        return has_operators  # Fallback

    def _check_brackets(self, query: str) -> bool:
        """Prüft, ob Klammern aufgehen und wieder zugehen."""
        return query.count('(') == query.count(')')
