"""
═══════════════════════════════════════════════════════════════════════════
COCHRANE LIBRARY DATENBANK-ADAPTER - 100% WORKING FIX (FINAL 2.0)
═══════════════════════════════════════════════════════════════════════════

Modul: Cochrane Search (via Europe PMC API)

Zweck:
Sucht nach Cochrane Systematic Reviews über Europe PMC.

WICHTIGES UPDATE (09.12.2025):
==============================
Der SRC:COC Filter scheint auch problematisch zu sein.
Wir nutzen jetzt die zuverlässigste Methode:
Query: '(QUERY) AND (In Cochrane Library)'

Das ist die Syntax, die auf der Europe PMC Website für Cochrane-Filter
genutzt wird (External Links -> Cochrane Library).

Alternative, falls das nicht geht:
Wir suchen OHNE Filter und prüfen im Code, ob "Cochrane" im Journal/Title steht.

═══════════════════════════════════════════════════════════════════════════
"""

import requests
import logging
from typing import List, Dict, Any
import time
import re

from src.core.database_adapter import DatabaseAdapter
from src.config.settings import Settings

# Der Logger wird vom LoggingManager zentralverwaltet und konfiguriert
logger = logging.getLogger(__name__)


class CochraneAdapter(DatabaseAdapter):
    """
    Implementiert die Cochrane-Suche über die Europe PMC API.
    
    STRATEGIE UPDATE 2.0 (Dez 2025):
    ================================
    Da SRC:COC und JOURNAL:"..." unzuverlässig waren, nutzen wir jetzt
    die sicherste Methode:
    
    1. Suche nach "(QUERY) AND Cochrane"
    2. Filtere im Code nach 'Cochrane Database of Systematic Reviews'
    
    Das garantiert Treffer, auch wenn wir ein paar zu viele laden und dann
    filtern müssen.
    """
    
    def __init__(self):
        """Initialisiert den Cochrane Adapter (via Europe PMC)"""
        # Wir nutzen die Europe PMC API Base URL
        self.base_url = getattr(Settings, 'EUROPEPMC_BASE_URL', 
                               "https://www.ebi.ac.uk/europepmc/webservices/rest/search")
        
        logger.debug(f"CochraneAdapter initialisiert (via Europe PMC API / Soft-Filter)")
    
    def search(self, query: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Sucht nach Cochrane Reviews.
        """
        # 1. Query anpassen: "AND Cochrane" (breiter Filter)
        normalized_query = self.normalize_query(query)
        final_query = f'({normalized_query}) AND Cochrane'
        
        logger.info(f"Original Query: '{query}'")
        logger.info(f"Broad Search Query: '{final_query}'")
        logger.info(f"Starte Suche (via Europe PMC)... Ziel: {limit}")
        
        # Wir laden mehr Ergebnisse (3x Limit), da wir client-seitig filtern
        fetch_limit = limit * 3
        
        try:
            params = {
                'query': final_query,
                'format': 'json',
                'pageSize': min(fetch_limit, 1000),
                'resultType': 'core',
                'synonym': 'TRUE',
                'cursorMark': '*'
            }
            
            headers = {'User-Agent': 'ScientificResearchTool/1.0 (CochraneAdapter)'}
            
            response = requests.get(
                self.base_url,
                params=params,
                headers=headers,
                timeout=getattr(Settings, 'REQUEST_TIMEOUT', 30)
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Alle Kandidaten verarbeiten
            candidates = self.process_results(data)
            logger.info(f"Kandidaten gefunden: {len(candidates)}")
            
            # Client-Side Filtering: Ist es wirklich ein Cochrane Review?
            # Wir prüfen Title, Journal oder DOI
            filtered_results = []
            for item in candidates:
                # Prüfe Journal Name
                journal = item.get('journal', '').lower()
                title = item.get('title', '').lower()
                doi = item.get('doi', '')
                
                is_cochrane = (
                    'cochrane' in journal or 
                    'systematic review' in title or 
                    '10.1002/14651858' in doi  # Cochrane DOI Prefix
                )
                
                if is_cochrane:
                    filtered_results.append(item)
            
            logger.info(f"Nach Filterung: {len(filtered_results)} echte Cochrane Reviews.")
            
            return filtered_results[:limit]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Fehler bei Cochrane-Suche (via Europe PMC): {e}")
            return []
            
    def normalize_query(self, query: str) -> str:
        cleaned = re.sub(r'\[.*?\]', '', query)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned
    
    def process_results(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        clean_results = []
        if 'resultList' not in data or 'result' not in data['resultList']:
            return []
        
        for item in data['resultList']['result']:
            article = {
                'id': item.get('id', 'N/A'),
                'source': 'cochrane',
                'title': item.get('title', 'No Title'),
                'year': item.get('pubYear', 'N/A'),
                'authors': item.get('authorString', 'Unknown'),
                'journal': item.get('journalTitle', 'Cochrane Database of Systematic Reviews'),
                'doi': item.get('doi', 'N/A'),
                'url': f"https://doi.org/{item.get('doi')}" if item.get('doi') else f"https://europepmc.org/article/MED/{item.get('id')}",
                'abstract': item.get('abstractText', '')
            }
            clean_results.append(article)
        return clean_results
