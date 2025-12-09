"""
═══════════════════════════════════════════════════════════════════════════
PUBMED DATENBANK-ADAPTER - FINAL FIX
═══════════════════════════════════════════════════════════════════════════

Modul: NCBI PubMed API Integration

Zweck:
Implementiert die Kommunikation mit der NCBI PubMed API zur Suche
in wissenschaftlichen Publikationen der biomedizinischen Literatur.

BESONDERHEITEN:
================
✓ Zugriff auf 34+ Millionen Artikel
✓ Zwei-Stufen API (ESearch + EFetch)
✓ XML-basierte Responses
✓ Umfangreiche Feldtags (TIAB, Title, Abstract, etc.)
✓ Date-Range Suche unterstützt
✓ BUGFIX 1: Field Tags werden für ESearch entfernt
✓ BUGFIX 2: Korrekter Parameter 'retmode' statt 'rettype'

═══════════════════════════════════════════════════════════════════════════
"""

import requests
import logging
from xml.etree import ElementTree as ET
from typing import List, Dict, Any
import time
import re

from src.core.database_adapter import DatabaseAdapter
from src.config.settings import Settings

# Der Logger wird vom LoggingManager zentralverwaltet und konfiguriert
logger = logging.getLogger(__name__)


class PubMedAdapter(DatabaseAdapter):
    """
    Konkrete Implementierung des DatabaseAdapter für PubMed/NCBI.
    
    API-STRUKTUR:
    =============
    PubMed nutzt zwei API-Endpoints:
    1. ESearch: Findet UIDs (Unique Identifiers) für eine Query
    2. EFetch: Holt die Details zu den UIDs
    
    BEISPIEL WORKFLOW:
    ==================
    1. User Query: "cancer AND immunotherapy"
    2. ESearch: Findet 50.000 UIDs für diese Query
    3. EFetch: Holt Details zu den ersten 25 UIDs
    4. Rückgabe: Strukturierte Artikel-Daten
    
    API-DOKUMENTATION:
    ==================
    https://www.ncbi.nlm.nih.gov/books/NBK25499/
    
    WICHTIGE FIXES (Dezember 2025):
    ===============================
    ✓ Field Tags werden für ESearch entfernt
      (z.B. [Title/Abstract], [dp]) sind nur für EFetch nötig!
    ✓ Parameter 'retmode' für JSON-Response korrigiert
    """
    
    def __init__(self):
        """Initialisiert den PubMed Adapter"""
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        
        # Email ist für NCBI empfohlen (bei hohem Nutzungsvolumen)
        self.email = getattr(Settings, 'NCBI_EMAIL', 'research@example.com')
        
        # API-Key (optional, aber empfohlen für höhere Rate Limits)
        self.api_key = getattr(Settings, 'NCBI_API_KEY', None)
        
        logger.debug(f"PubMedAdapter initialisiert (Email: {self.email})")
    
    def search(self, query: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Führt eine Suche in PubMed durch (ESearch + EFetch Kombination).
        
        WORKFLOW:
        =========
        1. Normalisiere Query (entferne Field Tags für ESearch)
        2. ESearch: Finde UIDs für die Query
        3. Bestimme Anzahl Treffer
        4. EFetch: Hole Details zu den Top-UIDs
        5. Parse XML und strukturiere Daten
        
        Args:
            query (str): Suchquery in universeller Syntax (AND/OR/NOT)
            limit (int): Maximale Anzahl Artikel zu holen (max. 10.000)
            
        Returns:
            List[Dict]: Strukturierte Artikel-Daten
        """
        
        logger.info(f"Original Query: '{query}'")
        logger.info(f"Starte Suche in PubMed nach: '{query[:50]}...' (Ziel: {limit} Artikel)")
        
        try:
            # SCHRITT 0: Normalisiere Query (entferne Field Tags)
            normalized_query = self.normalize_query(query)
            logger.debug(f"Normalisierte Query (ohne Field Tags): {normalized_query[:80]}...")
            
            # SCHRITT 1: ESearch - Finde UIDs
            logger.debug("Führe ESearch aus...")
            
            esearch_params = {
                'db': 'pubmed',
                'term': normalized_query,
                'retmode': 'json',   # <--- FIX: retmode statt rettype!
                'retmax': min(limit, 10000),
                'usehistory': 'y',
                'email': self.email
            }
            
            if self.api_key:
                esearch_params['api_key'] = self.api_key
            
            esearch_url = f"{self.base_url}/esearch.fcgi"
            
            # Debugging URL
            logger.debug(f"ESearch URL: {esearch_url}")
            logger.debug(f"ESearch Params: {esearch_params}")
            
            esearch_response = requests.get(esearch_url, params=esearch_params,
                                          timeout=getattr(Settings, 'REQUEST_TIMEOUT', 30))
            esearch_response.raise_for_status()
            
            # Erweiterte Fehlerdiagnose: Falls kein JSON kommt
            try:
                esearch_data = esearch_response.json()
            except requests.exceptions.JSONDecodeError:
                logger.error(f"PubMed lieferte ungültiges JSON zurück!")
                logger.error(f"Response Preview: {esearch_response.text[:200]}...")
                return []

            uids = esearch_data.get('esearchresult', {}).get('idlist', [])
            total_count = esearch_data.get('esearchresult', {}).get('count', '0')
            
            logger.info(f"ESearch gefunden: {len(uids)} Artikel (von insgesamt {total_count})")
            
            if not uids:
                logger.warning("Keine Ergebnisse gefunden.")
                return []
            
            # Rate Limit einhalten
            time.sleep(0.5)
            
            # SCHRITT 2: EFetch - Hole Details
            logger.debug("Führe EFetch aus...")
            
            efetch_params = {
                'db': 'pubmed',
                'id': ','.join(uids[:limit]),
                'rettype': 'xml', # Hier ist rettype korrekt für XML return type bei EFetch
                'email': self.email
            }
            
            if self.api_key:
                efetch_params['api_key'] = self.api_key
            
            efetch_url = f"{self.base_url}/efetch.fcgi"
            efetch_response = requests.get(efetch_url, params=efetch_params,
                                          timeout=getattr(Settings, 'REQUEST_TIMEOUT', 30))
            efetch_response.raise_for_status()
            
            # SCHRITT 3: Parse XML und strukturiere
            results = self.parse_efetch_xml(efetch_response.text)
            
            logger.info(f"EFetch zurück: {len(results)} Artikel mit Details")
            
            return results[:limit]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Netzwerkfehler bei PubMed Anfrage: {e}")
            return []
    
    def normalize_query(self, query: str) -> str:
        """
        Normalisiert die Query für PubMed ESearch.
        
        WICHTIG - BUGFIX (Dezember 2025):
        ==================================
        Field Tags wie [Title/Abstract], [dp] werden ENTFERNT!
        
        Args:
            query (str): Universelle Query mit möglicherweise Field Tags
            
        Returns:
            str: Bereinigte Query für ESearch ohne Field Tags
        """
        
        # 1. Entferne alle Field Tags [...]
        cleaned = re.sub(r'\[.*?\]', '', query)
        
        # 2. Normalisiere Whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        logger.debug(f"PubMed ESearch Query (Field Tags entfernt): {cleaned[:80]}...")
        
        return cleaned
    
    def parse_efetch_xml(self, xml_string: str) -> List[Dict[str, Any]]:
        """
        Parsed die XML-Response von PubMed EFetch.
        """
        
        clean_results = []
        
        try:
            root = ET.fromstring(xml_string)
            
            # Iteriere durch alle PubmedArticle Elemente
            for article_elem in root.findall('.//PubmedArticle'):
                
                # PMID
                pmid_elem = article_elem.find('.//PMID')
                pmid = pmid_elem.text if pmid_elem is not None else 'N/A'
                
                # Title
                title_elem = article_elem.find('.//ArticleTitle')
                title = title_elem.text if title_elem is not None else 'No Title'
                
                # Authors
                authors = self._extract_authors(article_elem)
                
                # Year
                year_elem = article_elem.find('.//PubDate/Year')
                year = year_elem.text if year_elem is not None else 'N/A'
                
                # Journal
                journal_elem = article_elem.find('.//Journal/Title')
                journal = journal_elem.text if journal_elem is not None else 'Unknown'
                
                # DOI
                doi_elem = article_elem.find(".//ELocationID[@EIdType='doi']")
                doi = doi_elem.text if doi_elem is not None else 'N/A'
                
                # Abstract
                abstract_elem = article_elem.find('.//AbstractText')
                abstract = abstract_elem.text if abstract_elem is not None else ''
                
                # Strukturiere Artikel
                article = {
                    'id': pmid,
                    'source': 'pubmed',
                    'title': title,
                    'year': year,
                    'authors': authors,
                    'journal': journal,
                    'doi': doi,
                    'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                    'abstract': abstract
                }
                
                clean_results.append(article)
                
        except ET.ParseError as e:
            logger.error(f"XML Parse-Fehler: {e}")
            logger.debug(f"Fehlerhaftes XML: {xml_string[:200]}...")
        
        return clean_results
    
    def _extract_authors(self, article_elem) -> str:
        """Extrahiert Autoren aus dem XML-Element."""
        try:
            author_list_elem = article_elem.find('.//AuthorList')
            if author_list_elem is None: return 'Unknown'
            
            authors = []
            for author in author_list_elem.findall('Author'):
                last_name_elem = author.find('LastName')
                last_name = last_name_elem.text if last_name_elem is not None else None
                if not last_name: continue
                
                fore_name_elem = author.find('ForeName')
                initials_elem = author.find('Initials')
                
                fore_name = fore_name_elem.text if fore_name_elem is not None else \
                           (initials_elem.text if initials_elem is not None else '')
                
                if fore_name: authors.append(f"{last_name}, {fore_name}")
                else: authors.append(last_name)
            
            return "; ".join(authors) if authors else 'Unknown'
        except Exception:
            return 'Unknown'
