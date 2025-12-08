"""
Modul: PubMed Datenbank-Adapter

===============================

Zweck: Implementiert die Kommunikation mit der PubMed REST API (NCBI E-Utilities).

PubMed ist die klassische biomedizinische Datenbank des National Center for
Biotechnology Information (NCBI) der USA.

API-Dokumentation: https://www.ncbi.nlm.nih.gov/books/NBK25499/

Dieses Modul:

- Erbt vom abstrakten 'DatabaseAdapter' Interface
- Implementiert die search() Methode
- Handhabt zwei Schritte: ESearch (IDs holen) + EFetch (Details holen)
- Parst XML-Antworten (PubMed nutzt XML, nicht JSON)
- Normalisiert Artikel-Daten in unser Standard-Format
- Formatiert Autoren für Zotero-Import (Nachname, Vorname)
- FIXIERT: Extraktion von Titeln mit XML-Tags (z.B. <i>BRAF</i>)

BESONDERHEIT GEGENÜBER EUROPE PMC:

- PubMed nutzt E-Utilities (zwei separate API-Calls pro Suche)
- Response-Format ist XML (nicht JSON)
- Pagination unterscheidet sich (retstart/retmax statt cursor)
- Keine Abstracts für alle Artikel (viele nur Metadaten)
"""

import requests
import logging
import time
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional

from src.core.database_adapter import DatabaseAdapter
from src.config.settings import Settings

logger = logging.getLogger(__name__)


class PubMedAdapter(DatabaseAdapter):
    """
    Konkrete Implementierung des DatabaseAdapter für PubMed.

    Diese Klasse kommuniziert mit der PubMed E-Utilities REST API,
    holt Suchergebnisse und konvertiert sie in unser Standard-Format.

    ZWEI-SCHRITT-PROZESS:

    1. ESearch: Suche durchführen, PMID-Listen bekommen
    2. EFetch: Details (Titel, Autoren, Abstract, etc.) holen

    Das ist nötig, weil PubMed nicht alles in einer Anfrage zurückgibt.
    """

    # Base URLs für E-Utilities
    ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    def search(self, query: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Führt eine Suche in PubMed aus mit Pagination.

        ZWEI-SCHRITT-PROZESS:

        SCHRITT 1: ESearch - PMIDs holen
        ================================

        Wir senden eine ESearch-Anfrage, um die Artikel-IDs (PMIDs) zu bekommen.
        ESearch gibt uns nur IDs zurück, nicht die vollständigen Daten.

        SCHRITT 2: EFetch - Artikel-Details holen
        =========================================

        Mit den PMIDs rufen wir EFetch auf, um die kompletten Artikel-Details zu bekommen
        (Titel, Autoren, Abstract, Journal, etc.).

        Argumente:

        query (str): Die Suchanfrage in PubMed-Syntax
            Z.B. "aspirin AND headache"
            Unterstützt MeSH-Terms: "aspirin[MeSH Terms]"
            Filter: "2020:2024[pdat]" (Publikationsjahr)

        limit (int): Maximale Anzahl Artikel (Default: 25)

        Rückgabewert:

        List[Dict]: Liste von normalisierten Artikel-Dictionaries.
            Jedes Dictionary hat die Felder:
            - pmid, source, title, year, authors, journal, doi, url, abstract

        Exception-Handling:

        Falls API-Fehler auftreten, werden bisherige Ergebnisse zurückgegeben
        (Graceful Degradation).
        """

        logger.info(f"Starte PubMed-Suche nach: '{query[:50]}...' (Ziel: {limit} Artikel)")

        # ========== SCHRITT 1: ESearch - PMIDs holen ==========

        pmids = self._esearch(query, limit)

        if not pmids:
            logger.warning("Keine PMIDs gefunden.")
            return []

        logger.info(f"ESearch: {len(pmids)} PMIDs gefunden")

        # ========== SCHRITT 2: EFetch - Artikel-Details holen ==========

        results = self._efetch(pmids)

        logger.info(f"Suche beendet. {len(results)} Artikel zurückgegeben.")

        return results

    def _esearch(self, query: str, limit: int) -> List[str]:
        """
        Hilfsmethode: ESearch durchführen und PMIDs zurückbekommen.

        Diese Methode sendet einen GET-Request an PubMed ESearch
        und extrahiert die Artikel-IDs (PMIDs) aus der XML-Response.

        Argumente:

        query (str): Die Suchanfrage
        limit (int): Maximale Anzahl IDs zu holen

        Rückgabewert:

        List[str]: Liste von PMIDs (Strings wie "35123456")
        """

        try:
            # ========== Parameter für ESearch zusammenstellen ==========

            params = {
                'db': 'pubmed',                          # Datenbank: PubMed
                'term': query,                           # Unsere Suchanfrage
                'retmax': min(limit, 1000),              # Max. 1000 pro Anfrage
                'rettype': 'uilist',                     # Gib nur IDs zurück
                'api_key': Settings.NCBI_API_KEY,        # API-Key für Rate Limiting
                'email': Settings.NCBI_EMAIL,            # E-Mail (gefordert von NCBI)
            }

            logger.debug(f"ESearch Request an: {self.ESEARCH_URL}")
            logger.debug(f"Parameter: {params}")

            # ========== ESearch-Request senden ==========

            response = requests.get(
                self.ESEARCH_URL,
                params=params,
                timeout=Settings.REQUEST_TIMEOUT
            )

            response.raise_for_status()

            # ========== XML parsen ==========

            root = ET.fromstring(response.text)

            # ========== PMIDs extrahieren ==========

            pmids = []
            for id_elem in root.findall('.//Id'):
                if id_elem.text:
                    pmids.append(id_elem.text)

            logger.info(f"ESearch gefunden: {len(pmids)} Artikel")

            return pmids

        except requests.exceptions.RequestException as e:
            logger.error(f"Netzwerkfehler bei ESearch: {e}")
            return []

        except ET.ParseError as e:
            logger.error(f"XML Parse-Fehler bei ESearch: {e}")
            return []

        except Exception as e:
            logger.error(f"Fehler bei ESearch: {e}")
            return []

    def _efetch(self, pmids: List[str]) -> List[Dict[str, Any]]:
        """
        Hilfsmethode: EFetch durchführen und Artikel-Details holen.

        Diese Methode sendet GET-Requests an PubMed EFetch
        (kann max. 10.000 Artikel pro Request, aber 500 IDs pro Request empfohlen)
        und extrahiert die Artikel-Details aus der XML-Response.

        Argumente:

        pmids (List[str]): Liste von PMIDs

        Rückgabewert:

        List[Dict]: Liste von normalisierten Artikel-Dictionaries
        """

        all_results = []

        # Teile die PMIDs in Batches (max. 500 pro Request)
        batch_size = 500

        for batch_start in range(0, len(pmids), batch_size):
            batch_end = min(batch_start + batch_size, len(pmids))
            batch_pmids = pmids[batch_start:batch_end]

            logger.debug(f"EFetch Batch {batch_start//batch_size + 1}: {len(batch_pmids)} PMIDs")

            try:
                # ========== Parameter für EFetch zusammenstellen ==========

                params = {
                    'db': 'pubmed',
                    'id': ','.join(batch_pmids),      # Komma-getrennte PMID-Liste
                    'rettype': 'xml',                 # XML-Format (mit vollständigen Details)
                    'retmode': 'xml',
                    'api_key': Settings.NCBI_API_KEY,
                    'email': Settings.NCBI_EMAIL,
                }

                # ========== EFetch-Request senden ==========

                response = requests.get(
                    self.EFETCH_URL,
                    params=params,
                    timeout=Settings.REQUEST_TIMEOUT
                )

                response.raise_for_status()

                # ========== XML parsen ==========

                root = ET.fromstring(response.text)

                # ========== Artikel extrahieren ==========

                for pubmed_article in root.findall('.//PubmedArticle'):
                    article = self._parse_article(pubmed_article)
                    if article:
                        all_results.append(article)

                # ========== Rate Limiting beachten ==========

                # NCBI empfiehlt: Mit API-Key min. 1 Request/Sekunde
                if batch_end < len(pmids):
                    time.sleep(Settings.RATE_LIMIT_DELAY)

            except requests.exceptions.RequestException as e:
                logger.error(f"Netzwerkfehler bei EFetch Batch: {e}")
                continue

            except ET.ParseError as e:
                logger.error(f"XML Parse-Fehler bei EFetch Batch: {e}")
                continue

            except Exception as e:
                logger.error(f"Fehler bei EFetch Batch: {e}")
                continue

        return all_results

    def _parse_article(self, pubmed_article_elem: ET.Element) -> Optional[Dict[str, Any]]:
        """
        Hilfsmethode: Parst ein einzelnes PubmedArticle XML-Element
        und konvertiert es in unser Standard-Format.

        WICHTIG FIX:
        Der Titel kann XML-Tags enthalten (z.B. <i>BRAF</i> für kursiv).
        Diese Methode extrahiert ALLE Text-Nodes korrekt und kombiniert sie,
        um den vollständigen Titel zu bekommen.

        Beispiel:
            Original XML: <ArticleTitle>Targeted therapy in <i>BRAF</i>-mutated cancer</ArticleTitle>
            Ergebnis: "Targeted therapy in BRAF-mutated cancer"

        Argumente:

        pubmed_article_elem (ET.Element): XML Element vom Typ <PubmedArticle>

        Rückgabewert:

        Optional[Dict]: Normalisierter Artikel mit unseren Standard-Feldern
            oder None bei Parse-Fehler
        """

        try:
            # Finde das MedlineCitation Element (enthält die meisten Infos)
            med_citation = pubmed_article_elem.find('.//MedlineCitation')
            if med_citation is None:
                return None

            # Finde das Article Element
            article = med_citation.find('.//Article')
            if article is None:
                return None

            # ========== Basis-Felder extrahieren ==========

            pmid_elem = med_citation.find('.//PMID')
            pmid = pmid_elem.text if pmid_elem is not None else 'N/A'

            # ========== TITEL (FIXIERT) ==========
            # WICHTIG: Verwendet itertext() um alle Text-Nodes zu sammeln
            # Das funktioniert mit XML-Tags wie <i>BRAF</i>
            title_elem = article.find('.//ArticleTitle')
            if title_elem is not None:
                # itertext() kombiniert alle Text-Teile rekursiv
                # Beispiel: "<ArticleTitle>Foo <i>bar</i> baz</ArticleTitle>"
                # -> itertext() gibt: "Foo ", "bar", " baz"
                # -> Kombiniert: "Foo bar baz"
                title_parts = list(title_elem.itertext())
                title = ''.join(title_parts).strip() if title_parts else 'No Title'
            else:
                title = 'No Title'

            # ========== Jahr extrahieren ==========

            # Kann an verschiedenen Orten sein
            year = 'N/A'
            pub_date = article.find('.//PubDate')
            if pub_date is not None:
                year_elem = pub_date.find('.//Year')
                if year_elem is not None and year_elem.text:
                    year = year_elem.text

            # ========== Journal ==========

            journal_elem = article.find('.//Journal/Title')
            journal = journal_elem.text if journal_elem is not None else 'Unknown'

            # ========== DOI ==========

            # WICHTIG: ArticleIdList ist unter PubmedArticle/PubmedData, nicht unter Article!
            doi = 'N/A'
            article_id_list = pubmed_article_elem.find('.//PubmedData/ArticleIdList')
            if article_id_list is not None:
                for article_id in article_id_list.findall('ArticleId'):
                    if article_id.get('IdType') == 'doi':
                        doi = article_id.text
                        break

            # ========== Autoren ==========

            authors = self._extract_authors(article)

            # ========== Abstract ==========

            abstract_elem = article.find('.//Abstract/AbstractText')
            abstract = abstract_elem.text if abstract_elem is not None else ''

            # ========== URL ==========

            url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

            # ========== Zusammenstellen ==========

            result = {
                'id': pmid,
                'source': 'PubMed',
                'title': title,
                'year': year,
                'authors': authors,
                'journal': journal,
                'doi': doi,
                'url': url,
                'abstract': abstract
            }

            return result

        except Exception as e:
            logger.warning(f"Fehler beim Parsen eines Artikels: {e}")
            return None

    def _extract_authors(self, article_elem: ET.Element) -> str:
        """
        Hilfsmethode: Extrahiert und formatiert die Autoren.

        Format: "Nachname, Vorname; Nachname2, Vorname2"
        (Zotero-kompatibel)

        Argumente:

        article_elem (ET.Element): Das XML-Element <Article>

        Rückgabewert:

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
