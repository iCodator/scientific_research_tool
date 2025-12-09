"""
═══════════════════════════════════════════════════════════════════════════
COCHRANE LIBRARY DATENBANK-ADAPTER
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

═══════════════════════════════════════════════════════════════════════════
"""

import requests
import logging
from typing import List, Dict, Any
from xml.etree import ElementTree as ET

from src.core.database_adapter import DatabaseAdapter
from src.config.settings import Settings

# Der Logger wird vom LoggingManager zentralverwaltet und konfiguriert
logger = logging.getLogger(__name__)


class CochraneAdapter(DatabaseAdapter):
    """
    Konkrete Implementierung des DatabaseAdapter für Cochrane Library.
    
    API-ENDPOINTS:
    ==============
    - REST API: https://api.cochrane.org/v1/
    - Format: JSON/XML
    - Authentifizierung: Optional (API-Key für höhere Limits)
    
    BESONDERHEITEN:
    ===============
    - Spezialisiert auf systematische Reviews
    - Hochwertige, peer-reviewed Daten
    - Fokus auf klinische Evidenz
    - Kleinere Datenbank als PubMed, aber hohe Qualität
    """
    
    def search(self, query: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Führt eine Suche in der Cochrane Library durch.
        
        WORKFLOW:
        =========
        1. Normalisiere die Query
        2. Sende Request an Cochrane API
        3. Parse XML/JSON Response
        4. Gebe strukturierte Ergebnisse zurück
        
        Args:
            query (str): Suchquery in universeller Syntax (AND/OR/NOT)
            limit (int): Maximale Anzahl Artikel zu holen
            
        Returns:
            List[Dict]: Strukturierte Review-Daten
        """
        
        # Standard URL falls nicht in Settings definiert
        base_url = getattr(Settings, 'COCHRANE_BASE_URL',
                          "https://api.cochrane.org/v1/search")
        
        # Header setzen
        headers = {
            'User-Agent': 'ScientificResearchTool/1.0'
        }
        
        # Query normalisieren
        normalized_query = self.normalize_query(query)
        
        logger.info(f"Original Query: '{query}'")
        logger.info(f"Normalized Query: '{normalized_query}'")
        logger.info(f"Starte Suche in Cochrane nach: '{normalized_query[:50]}...' (Ziel: {limit} Artikel)")
        
        try:
            # Sende API-Request
            params = {
                'q': normalized_query,
                'limit': limit,
                'type': 'review',  # Nur systematische Reviews
                'format': 'json'
            }
            
            logger.debug(f"Request Parameter: {params}")
            
            response = requests.get(
                base_url,
                params=params,
                headers=headers,
                timeout=getattr(Settings, 'REQUEST_TIMEOUT', 30)
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Ergebnisse verarbeiten
            results = self.process_results(data)
            
            logger.info(f"Suche beendet. {len(results)} Reviews gefunden.")
            
            return results[:limit]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Netzwerkfehler bei Cochrane Anfrage: {e}")
            return []
    
    def normalize_query(self, query: str) -> str:
        """
        Normalisiert die Query für Cochrane Library.
        
        Cochrane versteht Standard Boolean-Logik mit AND, OR, NOT.
        Minimal processing - nur Whitespace normalisieren.
        
        Args:
            query (str): Universelle Query
            
        Returns:
            str: Normalisierte Query
        """
        
        # Entferne Extra-Spaces und Newlines
        import re
        normalized = re.sub(r'\s+', ' ', query).strip()
        
        logger.debug(f"Cochrane-Query: {normalized}")
        
        return normalized
    
    def process_results(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Konvertiert die API-Response in Standard-Format.
        
        COCHRANE API RESPONSE STRUKTUR:
        ================================
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
        
        if 'records' not in data:
            logger.warning("Keine Ergebnisse in der API-Antwort gefunden.")
            return []
        
        for item in data.get('records', []):
            # Extrahiere Felder sicher mit .get()
            article = {
                'id': item.get('id', 'N/A'),
                'source': 'cochrane',
                'title': item.get('title', 'No Title'),
                'year': item.get('date', 'N/A'),
                'authors': item.get('author', 'Unknown'),
                'journal': 'Cochrane Library',
                'doi': item.get('doi', 'N/A'),
                'url': item.get('url', ''),
                'abstract': item.get('abstract', '')
            }
            
            clean_results.append(article)
        
        return clean_results
