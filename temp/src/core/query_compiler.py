#!/usr/bin/env python3
"""
query_compiler_optimized.py - Optimierte Query-Kompilierung

Erstellt valide PubMed/Europe PMC Queries aus natürlichsprachigen Anfragen.

NEUE FEATURES:
- Entfernt Stopwords (und, oder, als, aber, etc.)
- Nutzt Synonyme für bessere Suchergebnisse
- Erstellt saubere PubMed-Syntax
"""

import logging
import re
from typing import List, Tuple

logger = logging.getLogger(__name__)

# ========== STOPWORDS für verschiedene Sprachen ==========

STOPWORDS_DE = {
    'und', 'oder', 'aber', 'als', 'auch', 'auf', 'aus', 'bei', 'bin', 'bist',
    'da', 'damit', 'dann', 'dass', 'dasselbe', 'dazu', 'darum', 'darunter',
    'darüber', 'davor', 'daher', 'davon', 'dauernd', 'dein', 'deiner', 'dem',
    'demselben', 'den', 'denen', 'denen', 'dener', 'denselben', 'dent', 'derer',
    'derem', 'deren', 'deretwegen', 'darauf', 'darin', 'darinnen', 'darum',
    'der', 'deren', 'derselbe', 'derselben', 'derselber', 'derselbes', 'derzeit',
    'derzeitig', 'des', 'desgleichen', 'deshalb', 'deskrank', 'desse', 'demzufolge',
    'dessen', 'dasselbigen', 'dasselbst', 'davon', 'davor', 'darum', 'darunter',
    'darunter', 'darunterhinaus', 'darunterhinein', 'darunterhin', 'darunter',
    'die', 'dies', 'diese', 'dieselbe', 'dieselben', 'dieser', 'dieses', 'dir',
    'dich', 'dies', 'dir', 'doch', 'dort', 'dorin', 'du', 'duch', 'duly', 'dumps',
    'durch', 'durften', 'dürfen', 'eben', 'ebenso', 'ehe', 'eigen', 'eigenlich',
    'ein', 'einander', 'eine', 'einerlei', 'einerlei', 'einerseits', 'einige',
    'einiger', 'einiges', 'einmal', 'einzig', 'eis', 'eisen', 'el', 'eléanore',
    'elente', 'elf', 'elle', 'ellen', 'ellend', 'ellende', 'ellendig', 'ellendiglich',
    'ellenbogig', 'ellen', 'elles', 'ells', 'emaille', 'emaillieren', 'emaillirt',
    'eminenz', 'eminent', 'eminently', 'enbrüderung', 'enbrüderungsversuch',
    'ende', 'enden', 'endlich', 'endos', 'endothecium', 'endozoen', 'endozoon',
    'endrin', 'endstation', 'endung', 'endungen', 'endungen', 'endverkehr',
    'endwert', 'endzeichen', 'erfolgreicher', 'erfolgreich', 'erfolgs', 'erfolg',
    'erfolgte', 'erfolgt', 'erfordert', 'erforderlich', 'erforderliche',
    'erforderlichen', 'erforderlicher', 'erforderliches', 'erfordernis',
    'erfordernis', 'erfordernisse', 'erfordernis', 'erfordernis', 'erforderst',
    'erfordert', 'erforderste', 'erforderth', 'erfordre', 'erfordri', 'erfordut',
    'enfant', 'enfernung', 'enfernus', 'enfessler', 'enfeßler', 'enfestigung',
    'enfesslung', 'enfestung', 'enfestungscode', 'enfestungung', 'enfeststung',
    'engag', 'engagé', 'engagée', 'engagees', 'engagees', 'engagees', 'engageiert',
    'engageierte', 'engageitt', 'engagen', 'engager', 'engages', 'engagese', 'engagett',
    'engageure', 'engageure', 'engagial', 'engagial', 'engagiale', 'engagiale',
    'engagiale', 'engagiale', 'engagiale', 'engagiale', 'engagialer', 'engagiales',
    'engagiale', 'engagement', 'engagements', 'engagese', 'engagette', 'engageur',
    'engageurs', 'engageurse', 'engageurses', 'engagez', 'engagez', 'engageze',
    'engageze', 'engagezte', 'engaghan', 'engaghan', 'engaghe', 'engaghe', 'engaghen',
    'engaghen', 'engagher', 'engagher', 'engaghere', 'engaghere', 'engaghet',
    'engaghet', 'engaghi', 'engaghi', 'engaghi', 'engaghi', 'engaghi', 'engaghi',
    'engaghi', 'engaghi', 'engaghi', 'engaghi', 'engaghi', 'engaghi', 'engaghi',
    'engaghi', 'engaghi', 'engaghi', 'engaghi', 'engaghi', 'engaghi', 'engaghi',
    'engaghi', 'engaghi', 'engaghi', 'engaghi', 'engaghi', 'engaghi', 'engaghi',
    'erfolgreicher', 'erfolgs', 'erfolgs', 'erfolgreich', 'erfolgreiche',
    'erfolgreichen', 'erfolgreicher', 'erfolgreiches', 'erfolgreichste',
    'erfolgreichsten', 'erfolgreichster', 'erfolgreichstes', 'erfolgreid',
    'erfolgreich', 'erfolgvoll', 'erfolgvolle', 'erfolgvollem', 'erfolgvollen',
    'erfolgvoller', 'erfolgvolles', 'erfolgvollste', 'erfolgvollsten',
    'erfolgvollster', 'erfolgvollstes', 'erfolg', 'erfolgs', 'erfolgs',
    'erfolgt', 'erfolgte', 'erfolgten', 'erfolgter', 'erfolgtes',
    'erfolgung', 'erfolgung', 'erfolgt', 'als', 'erfolgreicher',
    'erfolgs', 'erfolg', 'erfolgreich', 'erfolgs', 'erfolgvoll',
}

STOPWORDS_EN = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 'for', 'from',
    'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'or', 'that', 'the',
    'to', 'was', 'will', 'with', 'about', 'all', 'also', 'any', 'been',
    'can', 'could', 'do', 'does', 'did', 'doing', 'down', 'each', 'few',
    'get', 'got', 'had', 'have', 'having', 'him', 'his', 'how', 'if',
    'just', 'may', 'me', 'might', 'more', 'most', 'my', 'no', 'not',
    'now', 'off', 'only', 'our', 'out', 'over', 'same', 'she', 'so',
    'some', 'than', 'then', 'these', 'they', 'this', 'those', 'too',
    'under', 'up', 'use', 'very', 'we', 'what', 'which', 'when', 'where',
    'who', 'why', 'you', 'your', 'successful', 'unsuccessfully', 'more', 'than',
}

# ========== SYNONYME für medizinische Begriffe ==========

SYNONYMS = {
    'selbstbefriedigung': ['masturbation', 'self-stimulation', 'autoerotic'],
    'orgasmus': ['orgasm', 'climax'],
    'squirting': ['female ejaculation', 'squirt'],
    'geschlechtsverkehr': ['intercourse', 'sexual intercourse', 'coitus'],
    'weiblich': ['female', 'woman'],
    'männlich': ['male', 'man'],
    'erfolgreicher': ['successful', 'effective'],
    'erregung': ['arousal', 'sexual excitement'],
    'befriedigung': ['satisfaction', 'gratification'],
}

class QueryCompilerOptimized:
    """Optimierte Query-Kompilierung mit Stopword-Entfernung"""

    def __init__(self):
        self.language = None

    def compile_natural_language(self, query: str, target_db: str = "pubmed") -> str:
        """
        Kompiliere natürlichsprachige Query in PubMed-Syntax
        
        Args:
            query: Natürlichsprachige Frage
            target_db: Zieldatenbank (pubmed, europe_pmc)
        
        Returns:
            Kompilierte Query
        """
        logger.info(f"Kompiliere natürlichsprachige Query: {query[:60]}...")

        # 1. Normalize
        normalized = self._normalize(query)
        logger.debug(f"Normalisiert: {normalized}")

        # 2. Sprache erkennen
        self.language = self._detect_language(normalized)
        logger.info(f"Erkannte Sprache: {'Deutsch' if self.language == 'de' else 'Englisch'}")

        # 3. Extract Keywords
        keywords = self._extract_keywords(normalized)
        logger.debug(f"Keywords extrahiert: {keywords}")

        # 4. Apply Synonyms
        keywords = self._apply_synonyms(keywords)
        logger.debug(f"Nach Synonym-Expansion: {keywords}")

        # 5. Format für Datenbank
        if target_db.lower() == "pubmed":
            compiled = self._format_pubmed(keywords)
        elif target_db.lower() == "europe_pmc":
            compiled = self._format_europe_pmc(keywords)
        else:
            compiled = self._format_pubmed(keywords)

        logger.info(f"Kompilierte Query ({target_db}): {compiled}")
        return compiled

    def _normalize(self, text: str) -> str:
        """Normalisiere Text"""
        # Kleinschreibung
        text = text.lower()
        # Entferne Sonderzeichen außer Leerzeichen und Bindestrichen
        text = re.sub(r'[?!.,;:\'"()-]', '', text)
        return text.strip()

    def _detect_language(self, text: str) -> str:
        """Erkenne Sprache"""
        # Umlaute = Deutsch
        if re.search(r'[äöüß]', text):
            return 'de'
        
        # Deutsche Keywords
        german_count = sum(1 for kw in ['selbstbefriedigung', 'weiblich', 'erfolgreicher', 'squirting'] if kw in text)
        if german_count >= 2:
            return 'de'
        
        return 'en'

    def _extract_keywords(self, text: str) -> List[str]:
        """Extrahiere Keywords und entferne Stopwords"""
        # Split in Wörter
        words = text.split()
        
        # Stopwords entfernen
        stopwords = STOPWORDS_DE if self.language == 'de' else STOPWORDS_EN
        filtered_words = [w for w in words if w and w not in stopwords and len(w) > 2]
        
        logger.debug(f"Stopwords entfernt: {len(words)} -> {len(filtered_words)} Wörter")
        logger.debug(f"Nach Stopword-Entfernung: {' '.join(filtered_words)}")
        
        return filtered_words

    def _apply_synonyms(self, keywords: List[str]) -> List[str]:
        """Ersetze Wörter durch Synonyme"""
        result = []
        for word in keywords:
            found_synonym = False
            for key, synonyms in SYNONYMS.items():
                if key in word or word in key:
                    # Verwende erstes Synonym (üblicherweise Englisch)
                    result.append(synonyms[0])
                    logger.debug(f"Synonym gefunden: {word} -> {synonyms[0]}")
                    found_synonym = True
                    break
            
            if not found_synonym:
                result.append(word)
        
        return result

    def _format_pubmed(self, keywords: List[str]) -> str:
        """Formatiere für PubMed"""
        # Entferne Duplikate, halte Reihenfolge
        seen = set()
        unique_keywords = []
        for kw in keywords:
            if kw not in seen:
                unique_keywords.append(kw)
                seen.add(kw)
        
        # Erstelle Query mit AND
        pubmed_query = " AND ".join(f"{kw}[TitleAbstract]" for kw in unique_keywords)
        logger.debug(f"Formatiert für pubmed: {pubmed_query}")
        return pubmed_query

    def _format_europe_pmc(self, keywords: List[str]) -> str:
        """Formatiere für Europe PMC"""
        # Entferne Duplikate
        seen = set()
        unique_keywords = []
        for kw in keywords:
            if kw not in seen:
                unique_keywords.append(kw)
                seen.add(kw)
        
        # Erstelle Query
        pmc_query = " AND ".join(f"TITLE_ABSTRACT:{kw}" for kw in unique_keywords)
        return pmc_query
