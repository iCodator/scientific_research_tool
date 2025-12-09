"""
═══════════════════════════════════════════════════════════════════════════
PUBMED DATENBANK-ADAPTER
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

═══════════════════════════════════════════════════════════════════════════
"""

import requests
import logging
from xml.etree import ElementTree as ET
from typing import List, Dict, Any
import time

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
        1. ESearch: Finde UIDs für die Query
        2. Bestimme Anzahl Treffer
        3. EFetch: Hole Details zu den Top-UIDs
        4. Parse XML und strukturiere Daten
        
        Args:
            query (str): Suchquery in universeller Syntax (AND/OR/NOT)
            limit (int): Maximale Anzahl Artikel zu holen (max. 10.000)
            
        Returns:
            List[Dict]: Strukturierte Artikel-Daten
        """
        
        logger.info(f"Original Query: '{query}'")
        logger.info(f"Starte Suche in PubMed nach: '{query[:50]}...' (Ziel: {limit} Artikel)")
        
        try:
            # SCHRITT 1: ESearch - Finde UIDs
            logger.debug("Führe ESearch aus...")
            
            esearch_params = {
                'db': 'pubmed',
                'term': query,
                'rettype': 'json',
                'retmax': min(limit, 10000),  # PubMed max 10.000
                'usehistory': 'y',
                'email': self.email
            }
            
            if self.api_key:
                esearch_params['api_key'] = self.api_key
            
            esearch_url = f"{self.base_url}/esearch.fcgi"
            esearch_response = requests.get(esearch_url, params=esearch_params,
                                          timeout=getattr(Settings, 'REQUEST_TIMEOUT', 30))
            esearch_response.raise_for_status()
            
            esearch_data = esearch_response.json()
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
                'rettype': 'xml',
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
        Normalisiert die Query für PubMed.
        
        PubMed nutzt Standard Boolean-Logik mit einigen Besonderheiten:
        - Field Tags: [TIAB], [Title], [Abstract], [Author], etc.
        - Phrase Search: "exact phrase"
        - Date Ranges: 2020:2025
        
        Momentan: Minimal processing (nur Whitespace)
        
        Args:
            query (str): Universelle Query
            
        Returns:
            str: Normalisierte Query für PubMed
        """
        
        import re
        normalized = re.sub(r'\s+', ' ', query).strip()
        
        logger.debug(f"PubMed-Query: {normalized}")
        
        return normalized
    
    def parse_efetch_xml(self, xml_string: str) -> List[Dict[str, Any]]:
        """
        Parsed die XML-Response von PubMed EFetch.
        
        STRUKTUR DES XML (vereinfacht):
        ================================
        <PubmedArticleSet>
          <PubmedArticle>
            <MedlineCitation>
              <PMID>12345678</PMID>
              <Article>
                <ArticleTitle>Article Title</ArticleTitle>
                <AuthorList>
                  <Author>
                    <LastName>Smith</LastName>
                    <ForeName>John</ForeName>
                  </Author>
                </AuthorList>
                <Journal>
                  <Title>Journal Name</Title>
                  <JournalIssue>
                    <PubDate>
                      <Year>2023</Year>
                    </PubDate>
                  </JournalIssue>
                </Journal>
                <Abstract>
                  <AbstractText>...</AbstractText>
                </Abstract>
              </Article>
            </MedlineCitation>
            <Article>
              <ELocationID EIdType="doi">10.1234/example</ELocationID>
            </Article>
          </PubmedArticle>
        </PubmedArticleSet>
        
        Args:
            xml_string (str): Raw XML Response von EFetch
            
        Returns:
            List[Dict]: Strukturierte Artikel
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
        
        return clean_results
    
    def _extract_authors(self, article_elem) -> str:
        """
        Extrahiert Autoren aus dem XML-Element.
        
        Format: "LastName, FirstName; LastName, FirstName; ..."
        
        Args:
            article_elem: XML Element des Artikels
            
        Returns:
            str: Autoren-String im Zotero-Format, oder "Unknown"
        """
        
        try:
            author_list_elem = article_elem.find('.//AuthorList')
            
            if author_list_elem is None:
                return 'Unknown'
            
            authors = []
            
            for author in author_list_elem.findall('Author'):
                
                # ========== Nachname ==========
                last_name_elem = author.find('LastName')
                last_name = last_name_elem.text if last_name_elem is not None else None
                
                if not last_name:
                    continue
                
                # ========== Vorname / Initialen ==========
                fore_name_elem = author.find('ForeName')
                initials_elem = author.find('Initials')
                
                if fore_name_elem is not None and fore_name_elem.text:
                    fore_name = fore_name_elem.text
                elif initials_elem is not None and initials_elem.text:
                    fore_name = initials_elem.text
                else:
                    fore_name = ''
                
                # ========== Formatieren ==========
                if fore_name:
                    authors.append(f"{last_name}, {fore_name}")
                else:
                    authors.append(last_name)
            
            if authors:
                return "; ".join(authors)
            else:
                return 'Unknown'
                
        except Exception as e:
            logger.warning(f"Fehler beim Extrahieren von Autoren: {e}")
            return 'Unknown'
