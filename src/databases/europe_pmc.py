"""
═══════════════════════════════════════════════════════════════════════════
EUROPE PMC DATENBANK-ADAPTER
═══════════════════════════════════════════════════════════════════════════

Modul: Europe PMC API Integration

Zweck: 
Implementiert die Kommunikation mit der Europe PMC REST API zur Suche
in wissenschaftlichen Publikationen.

WICHTIG - FIXES:
================
✓ Klammern ( ) werden NICHT mehr entfernt!
✓ Anführungszeichen " werden beibehalten (Phrasensuche)
✓ Bindestriche - werden beibehalten (chemische Namen: CRISPR-Cas9)
✓ Query-Normalisierung ist minimal (nur Whitespace)

═══════════════════════════════════════════════════════════════════════════
"""

import requests
import logging
import time
import re
from typing import List, Dict, Any

from src.core.database_adapter import DatabaseAdapter
from src.config.settings import Settings

# Der Logger wird vom LoggingManager zentralverwaltet und konfiguriert
logger = logging.getLogger(__name__)


class EuropePMCAdapter(DatabaseAdapter):
    """
    Konkrete Implementierung des DatabaseAdapter für Europe PMC.
    
    API-ENDPOINTS:
    ==============
    - REST API: https://www.ebi.ac.uk/europepmc/webservices/rest
    - Format: JSON
    - Authentifizierung: Optional (Email für besser Support)
    
    PAGINATION:
    ===========
    Europe PMC nutzt Cursor-basierte Pagination mit 'cursorMark'.
    Das ist besser für große Ergebnismengen als Offset-Pagination.
    
    RATE LIMITS:
    ============
    - Ohne API-Key: ~1 Request pro Sekunde
    - Mit API-Key: Höhere Limits
    """
    
    def search(self, query: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Führt eine Suche in Europe PMC aus und blättert durch die Ergebnisse.
        
        WORKFLOW:
        =========
        1. Normalisiere die Query (minimal - nur Whitespace)
        2. Setze Standard URL (falls nicht in Settings definiert)
        3. Setze HTTP-Header (User-Agent ist wichtig für API)
        4. Starte Pagination mit cursorMark='*'
        5. Sammle Ergebnisse bis zum Limit
        6. Gebe strukturierte Ergebnisse zurück
        
        Args:
            query (str): Suchquery in Universe Format (mit AND/OR/NOT)
            limit (int): Maximale Anzahl Artikel zu holen
            
        Returns:
            List[Dict]: Strukturierte Artikel-Daten
        """
        
        # Standard URL falls nicht in Settings definiert
        base_url = getattr(Settings, 'EUROPEPMC_BASE_URL', 
                          "https://www.ebi.ac.uk/europepmc/webservices/rest/search")
        
        # Header setzen (User-Agent ist wichtig)
        headers = {
            'User-Agent': 'ScientificResearchTool/1.0'
        }
        
        # Optional: Email für bessere API-Nutzung
        email = getattr(Settings, 'EUROPEPMC_EMAIL', None) or \
                getattr(Settings, 'NCBI_EMAIL', None)
        if email:
            headers['europepmc-Email'] = email
        
        # Query normalisieren (jetzt SANFT - keine Entfernung von Klammern!)
        normalized_query = self.normalize_query(query)
        
        logger.info(f"Original Query: '{query}'")
        logger.info(f"Normalized Query: '{normalized_query}'")
        logger.info(f"Starte Suche in Europe PMC nach: '{normalized_query[:50]}...' (Ziel: {limit} Artikel)")
        
        all_results = []
        next_cursor = '*'
        page_count = 0
        
        try:
            while len(all_results) < limit:
                page_count += 1
                remaining = limit - len(all_results)
                
                # Europe PMC erlaubt max 1000 pro Seite
                page_size = min(remaining, 1000)
                
                # Wenn Cursor '*' ist, ist es die erste Seite.
                # Achtung: cursorMark muss URL-encoded sein (requests macht das automatisch)
                params = {
                    'query': normalized_query,
                    'format': 'json',
                    'pageSize': page_size,
                    'resultType': 'core',
                    'synonym': 'TRUE',
                    'cursorMark': next_cursor
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
                new_results = self.process_results(data)
                
                if not new_results:
                    logger.info("Keine weiteren Ergebnisse verfügbar.")
                    break
                
                all_results.extend(new_results)
                logger.info(f"Seite {page_count}: {len(new_results)} geladen. Gesamt: {len(all_results)}/{limit}")
                
                # Nächster Cursor
                cursor_from_api = data.get('nextCursorMark')
                
                # Wenn Cursor gleich bleibt oder fehlt -> Ende
                if not cursor_from_api or cursor_from_api == next_cursor:
                    logger.info("Ende der Ergebnisliste erreicht.")
                    break
                
                next_cursor = cursor_from_api
                
                # Rate Limit einhalten
                if len(all_results) < limit:
                    time.sleep(getattr(Settings, 'RATE_LIMIT_DELAY', 0.5))
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Netzwerkfehler bei Europe PMC Anfrage: {e}")
            # Gib zurück was wir haben, auch wenn Fehler auftrat
            if all_results:
                logger.warning(f"Gebe {len(all_results)} bereits gefundene Ergebnisse zurück trotz Fehler.")
                return all_results
            return []
        
        final_results = all_results[:limit]
        logger.info(f"Suche beendet. {len(final_results)} Artikel zurückgegeben.")
        
        return final_results
    
    def normalize_query(self, query: str) -> str:
        """
        Normalisiert die Query für bessere API-Kompatibilität.
        
        WICHTIGER FIX (September 2025):
        ===============================
        Klammern () und Anführungszeichen "" werden BEIBEHALTEN!
        Bindestriche - werden BEIBEHALTEN!
        
        Nur überflüssige Whitespaces werden entfernt.
        
        Beispiele:
        - Input:  "(cancer OR tumor) AND therapy"
          Output: "(cancer OR tumor) AND therapy"  ← Klammern bleiben!
        
        - Input:  '"Coenzym Q10" AND mitochondria'
          Output: '"Coenzym Q10" AND mitochondria'  ← Anführungszeichen bleiben!
        
        - Input:  'CRISPR-Cas9 OR gene-therapy'
          Output: 'CRISPR-Cas9 OR gene-therapy'  ← Bindestriche bleiben!
        
        Args:
            query (str): Universelle Query
            
        Returns:
            str: Normalisierte Query für Europe PMC
        """
        
        # 1. Newlines und Tabs zu Spaces
        normalized = re.sub(r'\s+', ' ', query)
        
        # 2. Trimmen
        normalized = normalized.strip()
        
        # Das war's! Keine weiteren Änderungen!
        # Europe PMC versteht Boolean-Logik und Phrasen direkt.
        
        return normalized
    
    def process_results(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Konvertiert die API-Response in Standard-Format.
        
        STRUKTUR DER API-RESPONSE:
        ==========================
        {
          "resultList": {
            "result": [
              {
                "id": "12345678",
                "source": "MED",
                "title": "Article Title",
                "pubYear": 2023,
                "authorString": "Smith J, Jones M, ...",
                "journalTitle": "Journal Name",
                "doi": "10.1234/example",
                "abstractText": "Long abstract..."
              },
              ...
            ]
          }
        }
        
        Args:
            data (Dict): API Response als Dictionary
            
        Returns:
            List[Dict]: Strukturierte Artikel
        """
        clean_results = []
        
        if 'resultList' not in data or 'result' not in data['resultList']:
            logger.warning("Keine Ergebnisse in der API-Antwort gefunden.")
            return []
        
        raw_list = data['resultList']['result']
        
        for item in raw_list:
            # Extrahiere Felder sicher mit .get()
            article = {
                'id': item.get('id', 'N/A'),
                'source': item.get('source', 'europe_pmc'),  # Meistens 'MED' oder 'PMC'
                'title': item.get('title', 'No Title'),
                'year': item.get('pubYear', 'N/A'),
                'authors': item.get('authorString', 'Unknown'),
                'journal': item.get('journalTitle', 'Unknown'),
                'doi': item.get('doi', 'N/A'),
                # URL bauen: Meistens europepmc.org/article/{source}/{id}
                'url': f"https://europepmc.org/article/{item.get('source', 'MED')}/{item.get('id', '')}",
                'abstract': item.get('abstractText', '')
            }
            
            clean_results.append(article)
        
        return clean_results
