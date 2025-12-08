"""
Modul: Europe PMC Datenbank-Adapter (OPTIMIERT & FIXED)

===============================================

Zweck: Implementiert die Kommunikation mit der Europe PMC REST API.

Europe PMC ist eine kostenlose, volltext-durchsuchbare Biomedizin-Datenbank.

API-Dokumentation: https://europepmc.org/RestfulWebService

FIX: Parameters werden jetzt korrekt übermittelt!
"""

import requests
import logging
import time
import re
from typing import List, Dict, Any

from src.core.database_adapter import DatabaseAdapter
from src.config.settings import Settings

logger = logging.getLogger(__name__)

class EuropePMCAdapter(DatabaseAdapter):
    """
    Konkrete Implementierung des DatabaseAdapter für Europe PMC.
    
    FIX: Parameter-Übergabe wurde korrigiert!
    """

    def search(self, query: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Führt eine Suche in Europe PMC aus und blättert durch die Ergebnisse.
        
        FIX: Parameter werden jetzt direkt als kwargs übergeben (nicht als dict)
        """
        
        base_url = Settings.EUROPE_PMC_BASE_URL
        
        # HTTP-Header
        headers = {
            'User-Agent': 'ScientificResearchTool/1.0',
        }
        
        if Settings.EUROPE_PMC_EMAIL:
            headers['europepmcEmail'] = Settings.EUROPE_PMC_EMAIL
        
        # Query normalisieren
        normalized_query = self._normalize_query(query)
        logger.info(f"Original Query: '{query}'")
        logger.info(f"Normalized Query: '{normalized_query}'")
        
        # Sammel-Liste
        all_results = []
        next_cursor = '*'
        page_count = 0
        
        logger.info(f"Starte Suche in Europe PMC nach: '{normalized_query[:50]}...' (Ziel: {limit} Artikel)")
        
        try:
            while len(all_results) < limit:
                page_count += 1
                remaining = limit - len(all_results)
                page_size = min(remaining, 1000)
                
                logger.debug(f"Hole Seite {page_count} (Cursor: {next_cursor[:20] if len(next_cursor) > 20 else next_cursor}, PageSize: {page_size})")
                
                # FIX: Parameter direkt aufbauen
                params = {
                    'query': normalized_query,
                    'format': 'json',
                    'pageSize': page_size,
                    'resultType': 'core',
                    'synonym': 'TRUE',
                    'cursorMark': next_cursor
                }
                
                logger.debug(f"Request Parameter: {params}")
                logger.debug(f"Sende Request an: {base_url}")
                
                # FIX: Mit params= korrekt übergeben
                response = requests.get(
                    base_url,
                    params=params,
                    headers=headers,
                    timeout=Settings.REQUEST_TIMEOUT
                )
                
                response.raise_for_status()
                
                data = response.json()
                
                logger.info(f"DEBUG - API Response Keys: {list(data.keys())}")
                if 'hitCount' in data:
                    logger.info(f"DEBUG - Total Hit Count: {data['hitCount']}")
                if 'resultList' in data and 'result' in data['resultList']:
                    logger.info(f"DEBUG - Results in this page: {len(data['resultList']['result'])}")
                
                # Ergebnisse verarbeiten
                new_results = self._process_results(data)
                
                if not new_results:
                    logger.info("Keine weiteren Ergebnisse verfügbar.")
                    break
                
                all_results.extend(new_results)
                logger.info(f"Seite {page_count}: {len(new_results)} geladen. Gesamt: {len(all_results)}/{limit}")
                
                # Cursor für nächste Seite
                cursor_from_api = data.get('nextCursorMark')
                
                if not cursor_from_api or cursor_from_api == next_cursor:
                    logger.info("Ende der Ergebnisliste erreicht.")
                    break
                
                next_cursor = cursor_from_api
                
                # Rate-Limiting
                if len(all_results) < limit:
                    time.sleep(Settings.RATE_LIMIT_DELAY)
            
            final_results = all_results[:limit]
            logger.info(f"Suche beendet. {len(final_results)} Artikel zurückgegeben.")
            return final_results
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Netzwerkfehler bei Europe PMC Anfrage: {e}")
            if all_results:
                logger.warning(f"Gebe {len(all_results)} bereits gefundene Ergebnisse zurück trotz Fehler.")
                return all_results
            raise

    def _normalize_query(self, query: str) -> str:
        """Normalisiert die Query für bessere API-Kompatibilität."""
        
        # Ersetze Bindestriche durch Leerzeichen
        normalized = query.replace('-', ' ')
        
        # Entferne Klammern
        normalized = normalized.replace('(', ' ')
        normalized = normalized.replace(')', ' ')
        
        # Entferne Sonderzeichen (außer den Sonderzeichen die wir brauchen)
        normalized = re.sub(r'[^\w\s\[\]:+&]', ' ', normalized)
        
        # Ersetze mehrfache Leerzeichen
        normalized = ' '.join(normalized.split())
        
        # Boolean-Operatoren normalisieren
        normalized = re.sub(r'\band\b', 'AND', normalized, flags=re.IGNORECASE)
        normalized = re.sub(r'\bor\b', 'OR', normalized, flags=re.IGNORECASE)
        normalized = re.sub(r'\bnot\b', 'NOT', normalized, flags=re.IGNORECASE)
        
        return normalized

    def _process_results(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Konvertiert die API-Response in Standard-Format."""
        
        clean_results = []
        
        # Prüfe ob Struktur korrekt ist
        if 'resultList' not in data or 'result' not in data['resultList']:
            logger.warning("Keine Ergebnisse in der API-Antwort gefunden.")
            logger.debug(f"API-Response Struktur: {data}")
            return []
        
        raw_list = data['resultList']['result']
        
        for item in raw_list:
            article = {
                'id': item.get('id', 'N/A'),
                'source': item.get('source', 'N/A'),
                'title': item.get('title', 'No Title'),
                'year': item.get('pubYear', 'N/A'),
                'authors': self._format_authors_for_zotero(item.get('authorString', 'Unknown')),
                'journal': item.get('journalTitle', 'Unknown'),
                'doi': item.get('doi', 'N/A'),
                'url': f"https://europepmc.org/article/{item.get('source', 'MED')}/{item.get('id', '')}",
                'abstract': item.get('abstractText', '')
            }
            
            clean_results.append(article)
        
        logger.debug(f"Verarbeitet {len(clean_results)} Artikel aus dieser Seite.")
        return clean_results

    def _format_authors_for_zotero(self, author_string: str) -> str:
        """Formatiert Autoren im Zotero-Format."""
        
        if not author_string or author_string == 'Unknown':
            return 'Unknown'
        
        authors = [a.strip() for a in author_string.split(',')]
        
        formatted = []
        for author in authors:
            parts = author.split()
            if len(parts) >= 2:
                formatted.append(f"{parts[0]}, {' '.join(parts[1:])}")
            else:
                formatted.append(author)
        
        return "; ".join(formatted)
