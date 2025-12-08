"""
Modul: Cochrane Library Adapter (via Europe PMC)

Zweck
-----
Dieses Modul ermöglicht eine gezielte Suche nach Cochrane-Reviews,
indem es die bereits vorhandene Europe-PMC-Anbindung wiederverwendet
und nur die Ergebnisse herausfiltert, die aus der Cochrane-Datenbank
stammen oder dort typischerweise veröffentlicht werden.

Wichtiger Hintergrund
---------------------
- Cochrane-Reviews sind in Europe PMC NICHT zuverlässig über einen
  eigenen "Source-Code" wie z.B. SRCCHR auffindbar.
- Die Analyse mit dem Debug-Tool (debug_cochrane_sources.py) zeigt,
  dass Cochrane-Inhalte hauptsächlich über Journal-Metadaten erkennbar sind,
  insbesondere über den Journal-Titel.

Strategie in einfachen Worten
-----------------------------
Statt auf einen fragwürdigen "Source-Code" zu vertrauen, nutzen wir
folgende robuste Heuristik:

1. Journalname:
   - Abkürzung: "Cochrane Database Syst Rev"
   - Vollname:  "Cochrane Database of Systematic Reviews"
   Wenn ein Artikel in diesem Journal erschienen ist, handelt es sich mit
   sehr hoher Wahrscheinlichkeit um einen Cochrane-Review.

2. Kombination mit deiner Suche:
   - Du gibst z.B. ein:  "aspirin AND headache"
   - Der Adapter macht daraus: 
       "aspirin AND headache AND (JOURNAL:\"Cochrane Database Syst Rev\" 
                                 OR JOURNAL:\"Cochrane Database of Systematic Reviews\")"
   - So bekommst du nur Cochrane-Artikel, die zu deinem Thema passen.

Vorteile dieser Lösung
----------------------
- Keine extra API oder Lizenz nötig: Alles läuft über Europe PMC.
- Saubere Trennung: Das Hauptprogramm behandelt Cochrane wie eine eigene Quelle.
- Deutlich präzisere Treffer für Cochrane-Reviews, ohne auf inoffizielle
  oder instabile Filter angewiesen zu sein.
"""

import logging
from typing import List, Dict, Any

from src.core.database_adapter import DatabaseAdapter
from src.databases.europe_pmc import EuropePMCAdapter

# Logger für dieses Modul. Damit können wir im Terminal oder Logfile sehen,
# was der Adapter macht (z.B. welche Query geschickt wurde, wie viele Treffer es gab).
logger = logging.getLogger(__name__)


class CochraneAdapter(DatabaseAdapter):
    """
    Spezialisierter Datenbank-Adapter für Cochrane-Inhalte.

    WICHTIG:
    - Diese Klasse erbt von der abstrakten Basisklasse `DatabaseAdapter`.
      Dadurch ist garantiert, dass sie eine `search`-Methode mit
      der richtigen Signatur anbietet.
    - Intern nutzt die Klasse den bereits existierenden `EuropePMCAdapter`.
      Das bedeutet:
        * Nur eine HTTP-Implementierung für Europe PMC.
        * Cochrane ist eher ein "Spezialfall" von Europe PMC.
    """

    def __init__(self) -> None:
        """
        Initialisiert den Cochrane-Adapter.

        In einfachen Worten:
        - Wir erzeugen intern eine Instanz des EuropePMCAdapter.
        - Alle Anfragen an Cochrane laufen technisch über Europe PMC.
        - Der Unterschied liegt nur in der zusätzlichen Filterlogik
          (Journal-Filter), die wir in `search` anwenden.
        """
        # "Engine" = unsere interne Suchmaschine auf Basis von Europe PMC.
        self.engine = EuropePMCAdapter()

        logger.debug("CochraneAdapter initialisiert. "
                     "Verwendet EuropePMCAdapter als Such-Engine "
                     "mit Journal-Filter für Cochrane-Reviews.")

    def search(self, query: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Führt eine Suche nach Cochrane-Artikeln aus.

        Kernidee:
        ---------
        - Der Benutzer schreibt eine ganz normale fachliche Suchanfrage,
          z.B.:
              "aspirin AND headache"
        - Dieser Adapter erweitert die Anfrage automatisch um einen
          Journal-Filter, der Cochrane-Reviews auswählt.
        - Technisch wird dann Europe PMC mit der erweiterten Query
          angesprochen und die Ergebnisse werden leicht nachbearbeitet.

        Parameter:
        ----------
        query : str
            Die Benutzer-Suchanfrage (bereits bereinigt).
            Beispiel: "COVID-19 AND vaccination"
        limit : int, optional
            Maximale Anzahl der gewünschten Ergebnisse.
            Standard: 25

        Rückgabewert:
        -------------
        List[Dict[str, Any]]
            Eine Liste von Artikel-Dictionaries im Standardformat
            des Projekts. Typische Felder sind z.B.:
            - "id"      : interne ID (z.B. Europe PMC ID)
            - "source"  : Datenquelle (wird hier auf "Cochrane Library" gesetzt)
            - "title"   : Titel des Artikels
            - "year"    : Publikationsjahr
            - "authors" : Autoren im String-Format
            - "journal" : Journalname
            - "url"     : Direktlink zum Artikel / Abstract
            - "doi"     : DOI, falls vorhanden
            - "abstract": Abstract-Text, falls verfügbar

        Verhalten:
        ----------
        - Wenn Europe PMC keine Treffer findet, wird eine leere Liste
          zurückgegeben.
        - Falls ein Fehler in der Engine auftritt, wird der Fehler in
          der Engine selbst geloggt (das macht bereits EuropePMCAdapter).
        """
        # 1. Definiere den Journal-Filter für Cochrane.
        #
        #    Wichtig: Europe PMC verwendet eine eigene Query-Syntax.
        #    Der Feldname "JOURNAL" filtert auf Journaltitel, die Anführungszeichen
        #    stellen sicher, dass die komplette Wortgruppe gemeint ist.
        #
        #    Hier verwenden wir zwei Varianten:
        #    - Abkürzung (MEDLINE-Style): "Cochrane Database Syst Rev"
        #    - Voll ausgeschrieben:       "Cochrane Database of Systematic Reviews"
        #
        #    Durch das "OR" dazwischen werden Artikel aus *einer* der beiden
        #    Varianten akzeptiert.
        cochrane_filter = (
            'JOURNAL:"Cochrane Database Syst Rev" '
            'OR JOURNAL:"Cochrane Database of Systematic Reviews"'
        )

        logger.info("Suche in Cochrane (via Europe PMC)")
        logger.info("Benutzer-Query: %s", query)
        logger.debug("Cochrane-Filter (Journal): %s", cochrane_filter)

        # 2. Kombiniere Benutzer-Query mit dem Cochrane-Journal-Filter.
        #
        #    Beispiel:
        #      Benutzer:  "aspirin AND headache"
        #      Intern:    "(aspirin AND headache) AND (JOURNAL:... OR JOURNAL:...)"
        #
        #    Die Klammern sind wichtig, damit die logische Struktur erhalten bleibt
        #    und es keine Missverständnisse zwischen den AND/OR-Teilen gibt.
        if query.strip():
            modified_query = f"({query}) AND ({cochrane_filter})"
        else:
            # Falls jemand (theoretisch) eine leere Query übergibt, suchen wir
            # nur nach dem Journal-Filter. Das ist eher ein Edge-Case, aber
            # so verhalten wir uns trotzdem sinnvoll.
            modified_query = f"({cochrane_filter})"

        logger.debug("Kombinierte Cochrane-Query für Europe PMC: %s", modified_query)

        # 3. Suche mit der Europe PMC Engine ausführen.
        #
        #    Die Engine liefert uns bereits eine Liste von standardisierten
        #    Artikel-Dictionaries. Wir ändern daran nur minimal etwas ab.
        results = self.engine.search(modified_query, limit=limit)

        logger.info("Europe PMC hat %d Treffer für Cochrane geliefert.", len(results))

        # 4. Ergebnisse nachbearbeiten:
        #
        #    - Das Feld "source" wird für den Benutzer auf "Cochrane Library"
        #      gesetzt. Damit ist auf einen Blick sichtbar, dass es sich
        #      um Cochrane-Inhalte handelt.
        #    - Optional könnten wir hier weitere Filter anwenden, z.B.
        #      nur echte "Reviews" im Titel behalten. Das ist aber heikel,
        #      weil es auch Protokolle und Editorials gibt, die interessant
        #      sein können. Deshalb wird hier bewusst NICHT hart gefiltert,
        #      sondern nur informativ geloggt.
        for article in results:
            # Ursprüngliche Source für Debugzwecke sichern (falls vorhanden).
            original_source = article.get("source", "NA")
            article["original_source"] = original_source

            # Für die Außendarstellung klarer: wir nennen die Quelle
            # jetzt explizit "Cochrane Library".
            article["source"] = "Cochrane Library"

            title = article.get("title", "") or ""
            # Optional: reine Info, kein hartes Filtering.
            if "review" not in title.lower():
                logger.debug(
                    "Artikel ohne 'review' im Titel gefunden (kann z.B. Protokoll sein): %s",
                    title,
                )

        logger.info("Finale Anzahl Cochrane-Artikel (nach Umbenennung der Quelle): %d", len(results))

        return results
