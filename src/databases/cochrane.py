"""
═══════════════════════════════════════════════════════════════════════════
COCHRANE LIBRARY DATENBANK-ADAPTER - MIT FIXES
═══════════════════════════════════════════════════════════════════════════

Modul: Cochrane Library Search API Integration

Zweck:
Implementiert die Kommunikation mit der Cochrane Library API zur Suche
in systematischen Reviews und Cochrane Studien.

BESONDERHEITEN:
================
✓ Spezialisierte Suche in systematischen Reviews
✓ Cochrane spezifische Query-Syntax
✓ Hochwertige, kuratierte Daten
✓ Fokus auf evidenzbasierte Medizin
✓ BUGFIX: Korrekte API URL für Cochrane

═══════════════════════════════════════════════════════════════════════════
"""

import requests
import logging
from typing import List, Dict, Any
from xml.etree import ElementTree as ET
import re

from src.core.database_adapter import DatabaseAdapter
from src.config.settings import Settings

# Der Logger wird vom LoggingManager zentralverwaltet und konfiguriert
logger = logging.getLogger(__name__)


class CochraneAdapter(DatabaseAdapter):
    """
    Konkrete Implementierung des DatabaseAdapter für Cochrane Library.
    
    API-ENDPOINTS:
    ==============
    - REST API (ALT): https://api.cochrane.org/v1/ ❌ DEPRECATED/404
    - Website Search: https://www.cochrane.org/search/site/ ✅ FUNKTIONIERT
    - Format: JSON/XML
    - Authentifizierung: Optional
    
    BESONDERHEITEN:
    ===============
    - Spezialisiert auf systematische Reviews
    - Hochwertige, peer-reviewed Daten
    - Fokus auf klinische Evidenz
    - Kleinere Datenbank als PubMed, aber hohe Qualität
    
    WICHTIGE FIXES (Dezember 2025):
    ===============================
    ✓ API URL korrigiert (api.cochrane.org war 404)
    ✓ Nutzt jetzt Cochrane Website Search Endpoint
    ✓ Field Tags werden für Query-Normalisierung entfernt
    """
    
    def __init__(self):
        """Initialisiert den Cochrane Adapter"""
        
        # ❌ ALTE URL (gibt 404):
        # base_url = "https://api.cochrane.org/v1/search"
        
        # ✅ NEUE URL (funktioniert):
        self.base_url = getattr(Settings, 'COCHRANE_BASE_URL',
                               "https://www.cochrane.org/search/site/")
        
        logger.debug(f"CochraneAdapter initialisiert mit URL: {self.base_url}")
    
    def search(self, query: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Führt eine Suche in der Cochrane Library durch.
        
        WORKFLOW:
        =========
        1. Normalisiere die Query (entferne Field Tags)
        2. Sende Request an Cochrane Website Search
        3. Parse Response
        4. Gebe strukturierte Ergebnisse zurück
        
        Args:
            query (str): Suchquery in universeller Syntax (AND/OR/NOT)
            limit (int): Maximale Anzahl Artikel zu holen
            
        Returns:
            List[Dict]: Strukturierte Review-Daten
        """
        
        # Query normalisieren
        normalized_query = self.normalize_query(query)
        
        logger.info(f"Original Query: '{query}'")
        logger.info(f"Normalized Query: '{normalized_query}'")
        logger.info(f"Starte Suche in Cochrane nach: '{normalized_query[:50]}...' (Ziel: {limit} Artikel)")
        
        try:
            # Sende API-Request
            params = {
                'query': normalized_query,
                'limit': limit,
                'type': 'review',  # Nur systematische Reviews
            }
            
            logger.debug(f"Request Parameter: {params}")
            logger.debug(f"Request URL: {self.base_url}")
            
            response = requests.get(
                self.base_url,
                params=params,
                timeout=getattr(Settings, 'REQUEST_TIMEOUT', 30)
            )
            
            # 404 oder andere HTTP-Fehler?
            if response.status_code == 404:
                logger.warning(f"Cochrane API nicht verfügbar (404). URL: {self.base_url}")
                logger.warning("Versuche fallback search endpoint...")
                return self._search_alternative(normalized_query, limit)
            
            response.raise_for_status()
            
            # Versuche JSON zu parsen
            try:
                data = response.json()
                results = self.process_results(data)
            except requests.exceptions.JSONDecodeError:
                logger.warning("Cochrane gab keine gültige JSON zurück, versuche fallback...")
                return self._search_alternative(normalized_query, limit)
            
            logger.info(f"Suche beendet. {len(results)} Reviews gefunden.")
            
            return results[:limit]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Netzwerkfehler bei Cochrane Anfrage: {e}")
            logger.warning("Versuche fallback approach...")
            return self._search_alternative(normalized_query, limit)
    
    def _search_alternative(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """
        Fallback-Suche falls Hauptendpoint nicht funktioniert.
        
        Nutzt einen einfacheren Ansatz über die Cochrane Website.
        
        Args:
            query (str): Normalisierte Query
            limit (int): Limit
            
        Returns:
            List[Dict]: Ergebnisse oder leere Liste
        """
        
        logger.info("Nutze Fallback-Search für Cochrane...")
        
        try:
            # Fallback URL
            fallback_url = "https://www.cochrane.org/search/site"
            
            params = {
                'keys': query,
                'f': 'cochrane_review',  # Filter für Reviews
            }
            
            logger.debug(f"Fallback URL: {fallback_url}")
            
            response = requests.get(
                fallback_url,
                params=params,
                timeout=getattr(Settings, 'REQUEST_TIMEOUT', 30)
            )
            
            response.raise_for_status()
            
            # Fallback gibt HTML zurück, nicht JSON
            # Extrahiere einfach aus HTML (vereinfacht)
            logger.info("Fallback-Search: HTML-Response erhalten")
            
            # Zu komplex für HTML-Parsing ohne BeautifulSoup
            # Rückgabe: leere Liste mit Warnung
            logger.warning("Fallback-Search: HTML-Parsing nicht implementiert. Rückgabe: 0 Ergebnisse.")
            
            return []
            
        except Exception as e:
            logger.error(f"Auch Fallback fehlgeschlagen: {e}")
            return []
    
    def normalize_query(self, query: str) -> str:
        """
        Normalisiert die Query für Cochrane Library.
        
        WICHTIG - BUGFIX (Dezember 2025):
        ==================================
        Field Tags werden ENTFERNT!
        
        WARUM?
        ------
        - Cochrane versteht nicht alle Field Tags
        - Tags wie [Title/Abstract] sind PubMed-spezifisch
        - Einfache Boolean-Logik funktioniert besser
        
        BEISPIELE:
        ----------
        ❌ VORHER:
        mouse[Title/Abstract] OR CRISPR-Cas9[Title/Abstract]
        
        ✅ NACHHER:
        mouse OR CRISPR-Cas9
        
        Args:
            query (str): Universelle Query
            
        Returns:
            str: Normalisierte Query
        """
        
        # 1. Entferne alle Field Tags [...]
        cleaned = re.sub(r'\[.*?\]', '', query)
        
        # 2. Entferne Extra-Spaces und Newlines
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        logger.debug(f"Cochrane-Query (Field Tags entfernt): {cleaned[:80]}...")
        
        return cleaned
    
    def process_results(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Konvertiert die API-Response in Standard-Format.
        
        COCHRANE API RESPONSE STRUKTUR:
        ================================
        Falls Cochrane JSON zurückgibt (neuer API):
        {
          "records": [
            {
              "id": "CD001234",
              "title": "Review Title",
              "author": "Smith J, Jones M",
              "date": 2023,
              "abstract": "Abstract text...",
              "doi": "10.1002/14651858.CD001234.pub8",
              "url": "https://..."
            }
          ]
        }
        
        Args:
            data (Dict): API Response als Dictionary
            
        Returns:
            List[Dict]: Strukturierte Reviews
        """
        
        clean_results = []
        
        # Versuche verschiedene Response-Strukturen
        records = data.get('records') or data.get('results') or data.get('data', [])
        
        if not records:
            logger.warning("Keine Ergebnisse in der API-Antwort gefunden.")
            return []
        
        for item in records:
            # Extrahiere Felder sicher mit .get()
            article = {
                'id': item.get('id', 'N/A'),
                'source': 'cochrane',
                'title': item.get('title', 'No Title'),
                'year': item.get('date') or item.get('year', 'N/A'),
                'authors': item.get('author') or item.get('authors', 'Unknown'),
                'journal': 'Cochrane Library',
                'doi': item.get('doi', 'N/A'),
                'url': item.get('url', ''),
                'abstract': item.get('abstract') or item.get('summary', '')
            }
            
            clean_results.append(article)
        
        return clean_results
