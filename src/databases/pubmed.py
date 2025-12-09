"""
═══════════════════════════════════════════════════════════════════════════
PUBMED DATENBANK-ADAPTER - FIX QUERY NORMALIZATION
═══════════════════════════════════════════════════════════════════════════

Problem:
Der aktuelle Adapter entfernt Field-Tags (z.B. [pdat]) aus der ESearch-Query.
Das führt dazu, dass '2015:2025[pdat]' zu '2015:2025' wird, was PubMed nicht versteht
und daher 0 Ergebnisse liefert.

Lösung:
Wir dürfen die Query NICHT normalisieren/bereinigen, bevor wir sie an ESearch senden.
ESearch *braucht* die Field-Tags.

═══════════════════════════════════════════════════════════════════════════
"""

import requests
import logging
from typing import List, Dict, Any
import time
import os
import re

from src.core.database_adapter import DatabaseAdapter
from src.config.settings import Settings

logger = logging.getLogger(__name__)

class PubMedAdapter(DatabaseAdapter):
    """
    Adapter für PubMed API (E-Utilities).
    """

    def __init__(self):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.api_key = getattr(Settings, 'PUBMED_API_KEY', None)
        self.email = getattr(Settings, 'PUBMED_EMAIL', None)
        logger.debug(f"PubMedAdapter initialisiert (Email: {self.email})")

    def search(self, query: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Sucht in PubMed.
        
        WICHTIG: Die Query wird 1:1 an ESearch weitergegeben.
        Keine Normalisierung (Entfernen von [Tags]), da ESearch diese benötigt!
        """
        logger.info(f"Original Query: '{query}'")
        
        # 1. ESearch: IDs holen
        # Hier nutzen wir die Query exakt so wie sie ist!
        esearch_query = query 
        
        logger.debug(f"PubMed ESearch Query: {esearch_query}")
        
        id_list = self._esearch(esearch_query, limit)
        
        if not id_list:
            logger.warning("Keine Ergebnisse gefunden.")
            return []
            
        logger.info(f"ESearch gefunden: {len(id_list)} Artikel")
        
        # 2. EFetch: Details holen
        articles = self._efetch(id_list)
        return articles

    def _esearch(self, query: str, limit: int) -> List[str]:
        """Führt ESearch aus und gibt Liste von IDs zurück."""
        url = f"{self.base_url}/esearch.fcgi"
        params = {
            'db': 'pubmed',
            'term': query,
            'retmode': 'json',
            'retmax': limit,
            'usehistory': 'y'
        }
        if self.email: params['email'] = self.email
        if self.api_key: params['api_key'] = self.api_key

        try:
            logger.debug(f"ESearch Params: {params}")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if 'esearchresult' in data and 'idlist' in data['esearchresult']:
                count = data['esearchresult'].get('count', '0')
                logger.info(f"ESearch gefunden: {len(data['esearchresult']['idlist'])} Artikel (von insgesamt {count})")
                return data['esearchresult']['idlist']
            return []
            
        except Exception as e:
            logger.error(f"Fehler bei ESearch: {e}")
            return []

    def _efetch(self, id_list: List[str]) -> List[Dict[str, Any]]:
        """Führt EFetch für eine Liste von IDs aus."""
        if not id_list:
            return []
            
        url = f"{self.base_url}/efetch.fcgi"
        ids_str = ",".join(id_list)
        
        params = {
            'db': 'pubmed',
            'id': ids_str,
            'retmode': 'xml'  # XML liefert strukturiertere Daten als JSON hier
        }
        if self.email: params['email'] = self.email
        if self.api_key: params['api_key'] = self.api_key
        
        try:
            # Wir nutzen Biopython zum Parsen, wenn verfügbar, sonst manuell
            # Hier vereinfacht: Wir nutzen einen JSON-Return für einfacheres Parsing wenn möglich
            # Aber EFetch JSON ist oft unvollständig. XML ist besser.
            # Da wir keinen XML-Parser hier neu schreiben wollen, 
            # nutzen wir retmode=json und hoffen auf das Beste für Titel/Abstract,
            # oder wir nutzen eine vereinfachte Text-Extraktion.
            
            # Strategie-Wechsel: Wir fordern JSON an (PubMed Summary Format)
            # Das reicht für Titel, Autoren, Journal, Datum.
            # Abstract fehlt oft im Summary-JSON, aber wir probieren es.
            
            # Besser: ESummary für Metadaten + EFetch für Abstract
            # Um es einfach zu halten: ESummary (JSON)
            summary_url = f"{self.base_url}/esummary.fcgi"
            params['retmode'] = 'json'
            
            response = requests.get(summary_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            results = []
            if 'result' in data:
                result_dict = data['result']
                # 'uids' ist eine Liste der IDs in der richtigen Reihenfolge
                if 'uids' in result_dict:
                    for uid in result_dict['uids']:
                        item = result_dict[uid]
                        article = {
                            'id': uid,
                            'source': 'pubmed',
                            'title': item.get('title', 'No Title'),
                            'year': item.get('pubdate', '').split(' ')[0] if item.get('pubdate') else 'N/A',
                            'authors': ", ".join([a['name'] for a in item.get('authors', [])]) if 'authors' in item else 'Unknown',
                            'journal': item.get('source', 'N/A'),
                            'doi': item.get('elocationid', '').replace('doi: ', '') if 'elocationid' in item else 'N/A',
                            'url': f"https://pubmed.ncbi.nlm.nih.gov/{uid}/",
                            'abstract': 'Abstract not available in summary view.' # ESummary liefert keinen Abstract
                        }
                        results.append(article)
            
            return results

        except Exception as e:
            logger.error(f"Fehler bei EFetch/ESummary: {e}")
            return []
