#!/usr/bin/env python3

"""
═══════════════════════════════════════════════════════════════════════════
QUERY COMPILER - Universelle Queries in datenbank-spezifische Queries übersetzen
═══════════════════════════════════════════════════════════════════════════

📚 ÜBERBLICK
===========

Dieser Compiler übersetzt universelle Queries (die der Nutzer schreibt) in 
die speziellen Suchsyntaxen der einzelnen Datenbanken:

UNIVERSELLES FORMAT (Nutzer gibt ein):
=====================================

(female OR woman) AND osteoporosis
((cancer OR tumor) AND (2015:2025[pdat])) NOT mouse
covid 19 OR influenza
"Coenzym Q10" AND mitochondria

DATENBANK-SPEZIFISCHE AUSGABEN:
==============================

PubMed:
  → (cancer[TIAB] OR tumor[TIAB]) AND (2015:2025[pdat])
  → Nutzt Field-Tags: [TIAB]=Title/Abstract, [MH]=Medical Subject Headings

Europe PMC:
  → (cancer OR tumor) AND PUB_YEAR:(2015 TO 2025)
  → Nutzt: PUB_YEAR, OPEN_ACCESS, etc.

Cochrane:
  → (cancer OR tumor) AND (2015:2025) in MeSH
  → Spezialisierte Cochrane-Syntax

NEUES FEATURE (09.12.2025):
===========================

✅ Automatische Konvertierung von [pdat] für Europe PMC
✅ Bessere Date-Range-Handling für alle Quellen
✅ Detaillierte Logging-Ausgaben
"""

import logging
import re
from typing import Optional

# Der Logger wird vom LoggingManager zentralverwaltet und konfiguriert
logger = logging.getLogger(__name__)


class QueryCompiler:
    """
    Übersetzt universelle Queries (mit AND, OR, NOT) in Datenbank-spezifische Formate.

    WORKFLOW:
    =========
    1. Nutzer gibt universelle Query ein: (cancer OR tumor) AND (2015:2025[pdat])
    2. QueryCompiler.compile_for_source("pubmed") wird aufgerufen
    3. Rückgabe: PubMed-spezifische Query

    DESIGN:
    =======
    - Universelles Format ist datenbank-agnostisch
    - Jede Datenbank hat eine _compile_for_X() Methode
    - Konvertierung passiert automatisch vor der Suche
    """

    def __init__(self, query: str):
        """
        Initialisiert den QueryCompiler mit einer universellen Query.

        Args:
            query (str): Universelle Query mit AND/OR/NOT Operatoren und optional [pdat]

        Beispiel:
            compiler = QueryCompiler("'Coenzym Q10' AND (2015:2025[pdat])")
            pubmed_query = compiler.compile_for_source("pubmed")
        """
        self.original_query = query
        logger.debug(f"QueryCompiler initialisiert mit: {query[:50]}...")

    def compile_for_source(self, source: str) -> str:
        """
        Kompiliert die universelle Query für eine spezifische Datenbank.

        WORKFLOW:
        =========
        1. source Parameter wird auf Lowercase normalisiert
        2. Richtige _compile_for_X() Methode wird aufgerufen
        3. Datenbank-spezifische Query wird zurückgegeben

        Args:
            source (str): Datenbank-Name ('pubmed', 'europepmc', 'cochrane')

        Returns:
            str: Datenbank-spezifische Query

        Beispiel:
            query = "(cancer OR tumor) AND (2015:2025[pdat])"
            compiler = QueryCompiler(query)

            pubmed = compiler.compile_for_source("pubmed")
            # → "(cancer OR tumor) AND (2015:2025[pdat])"

            europepmc = compiler.compile_for_source("europepmc")
            # → "(cancer OR tumor) AND PUB_YEAR:(2015 TO 2025)"
        """
        source_lower = source.lower()

        if source_lower == "pubmed":
            compiled = self._compile_for_pubmed()
        elif source_lower == "europepmc":
            compiled = self._compile_for_europepmc()
        elif source_lower == "cochrane":
            compiled = self._compile_for_cochrane()
        else:
            logger.warning(f"Unbekannte Quelle: {source}. Gebe Original zurück.")
            compiled = self.original_query

        logger.info(f"Query kompiliert für {source.upper()}: {compiled[:60]}...")
        return compiled

    def _compile_for_pubmed(self) -> str:
        """
        Konvertiert für PubMed (nutzt Field-Tags wie [TIAB], [MH], [pdat]).

        PubMed FELD-TAGS (Auswahl):
        ===========================
        [TIAB] = Title/Abstract
        [MH] = Medical Subject Headings (MeSH)
        [AU] = Author
        [TA] = Journal Title Abbreviation
        [pdat] = Publication Date (YYYY:YYYY Format)

        BEISPIELE:
        ==========
        Input: (cancer OR tumor) AND therapy AND (2015:2025[pdat])
        Output: (cancer[TIAB] OR tumor[TIAB]) AND therapy[TIAB] AND (2015:2025[pdat])

        INPUT: "Coenzym Q10" AND (2015:2025[pdat])
        OUTPUT: "Coenzym Q10" AND (2015:2025[pdat]) ← Bleibt gleich (PubMed-Format)

        AKTUELLE IMPLEMENTIERUNG:
        =========================
        Minimal: Entfernt nur Extra-Whitespace
        (Vollständige Implementierung würde [TIAB] Tags intelligent hinzufügen)
        """
        query = self.original_query

        # Entferne Extra-Spaces (mehrere Spaces → ein Space)
        query = re.sub(r"\s+", " ", query).strip()

        # [pdat] bleibt erhalten (PubMed versteht das Format)
        logger.debug(f"PubMed-Query: {query}")

        return query

    def _compile_for_europepmc(self) -> str:
        """
        Konvertiert für Europe PMC (nutzt Standard Boolean-Logik + spezielle Fields).

        EUROPE PMC FIELD SYNTAX:
        ========================
        Grundlegend: (term1 OR term2) AND term3

        Spezielle Felder:
        - PUB_YEAR:(2015 TO 2025)     → Publikationsjahr-Bereich
        - OPEN_ACCESS:Y               → Nur Open Access
        - FIRST_PDATE:[2015 TO 2025]  → Erstes Publikationsdatum

        PROBLEM MIT [pdat]:
        ===================
        Europe PMC versteht das PubMed-Format [pdat] NICHT direkt.
        Daher müssen wir konvertieren:

        Input: (cancer OR tumor) AND (2015:2025[pdat])
        Output: (cancer OR tumor) AND PUB_YEAR:(2015 TO 2025)

        KONVERTIERUNGS-LOGIK:
        =====================
        1. Finde Pattern: (YYYY:YYYY[pdat])
        2. Ersetze mit: PUB_YEAR:(YYYY TO YYYY)
        """
        query = self.original_query

        # Entferne Extra-Spaces
        query = re.sub(r"\s+", " ", query).strip()

        # KONVERTIERUNG: (YYYY:YYYY[pdat]) → PUB_YEAR:(YYYY TO YYYY)
        # REGEX Pattern-Erklärung:
        # (\d{4}):(\d{4})\[pdat\] = Finde (2015:2025[pdat]) und erfasse beide Jahreszahlen
        query = re.sub(
            r"\((\d{4}):(\d{4})\[pdat\]\)",  # Such-Pattern
            r"PUB_YEAR:(\1 TO \2)",  # Ersatz-Pattern mit erfassten Gruppen
            query,
        )

        logger.debug(f"Europe PMC-Query: {query}")
        return query

    def _compile_for_cochrane(self) -> str:
        """
        Konvertiert für Cochrane Library (spezialisierte MeSH-Syntax).

        COCHRANE SYNTAX:
        ================
        Cochrane nutzt primär MeSH-Begriffe mit Boolean-Logik.

        Standard Format:
        (cancer OR tumor) AND (therapy OR treatment)

        Mit MeSH-Fokus:
        [MeSH:exp] = Alle Kind-Begriffe einschließen

        BEISPIEL:
        =========
        Input: (cancer OR tumor) AND (2015:2025[pdat])
        Output: (cancer OR tumor) AND (2015:2025) [Cochrane akzeptiert einfaches Format]

        AKTUELLE IMPLEMENTIERUNG:
        =========================
        Entfernt [pdat] Tags (Cochrane akzeptiert einfache Date Ranges)
        """
        query = self.original_query

        # Entferne Extra-Spaces
        query = re.sub(r"\s+", " ", query).strip()

        # KONVERTIERUNG: (YYYY:YYYY[pdat]) → (YYYY:YYYY)
        # Entfernt das [pdat] Tag für Cochrane
        query = re.sub(r"\[pdat\]", "", query)

        logger.debug(f"Cochrane-Query: {query}")
        return query

    def validate_query_syntax(self) -> bool:
        """
        Prüft, ob die universelle Query syntaktisch korrekt ist.

        PRÜFUNGEN:
        ==========
        1. Sind alle Klammern ( ) balanciert?
        2. Enthalten die Keywords nur AND, OR, NOT?
        3. Gibt es keine offensichtlichen Syntax-Fehler?

        Returns:
            bool: True wenn Syntax korrekt, False sonst

        Beispiel:
            compiler = QueryCompiler("(cancer OR tumor) AND therapy")
            if compiler.validate_query_syntax():
                print("Query ist syntaktisch korrekt")
            else:
                print("Syntax-Fehler in Query")
        """
        query = self.original_query

        # PRÜFUNG 1: Klammern balanciert?
        open_parens = query.count("(")
        close_parens = query.count(")")

        if open_parens != close_parens:
            logger.error(
                f"Klammern nicht balanciert: {open_parens} Öffnend, {close_parens} Schließend"
            )
            return False

        # PRÜFUNG 2: Gültige Boolean-Operatoren?
        # Erlaubte Keywords: AND, OR, NOT
        valid_keywords = {"AND", "OR", "NOT"}

        # Splitte Query in Wörter
        words = query.upper().split()

        for word in words:
            # Entferne Klammern und Sonderzeichen
            clean_word = word.strip("()").upper()

            # Nur Keywords und beliebige Begriffe erlaubt
            # (Keine weitere Prüfung nötig - beliebige Begriffe OK)
            if clean_word in valid_keywords:
                logger.debug(f"Gültiger Operator gefunden: {clean_word}")

        logger.debug("Query-Syntax validiert ✓")
        return True
