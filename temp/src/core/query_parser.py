"""
Modul: Query Parser
====================
Zweck: Liest Suchanfragen aus Textdateien ein und bereitet sie für die Europe PMC API auf.

Beispiel-Eingabedatei:
    (COVID-19 OR SARS-CoV-2) AND (vaccine OR vaccination) AND PubYear 2020-2024

Das Modul:
- Prüft, ob die Datei existiert
- Prüft, ob die Datei nicht leer ist
- Bereinigt die Anfrage (entfernt Zeilenumbrüche, extra Leerzeichen)
- Gibt die saubere Anfrage zurück, bereit für die API
"""

import os
import logging

# Logger initialisieren (für Fehlerbehandlung und Info-Ausgaben)
logger = logging.getLogger(__name__)


class QueryParser:
    """
    Klasse zur Verarbeitung von Suchanfragen.
    
    Diese Klasse behandelt alles, was mit dem Lesen und Bereinigen
    von Suchanfrage-Dateien zu tun hat.
    """

    @staticmethod
    def load_query_from_file(file_path: str) -> str:
        """
        Liest eine Suchanfrage aus einer Textdatei ein und bereitet sie auf.

        Diese Funktion macht folgendes:
        1. Prüft, ob die Datei existiert (wenn nicht: Fehler)
        2. Öffnet die Datei und liest den Inhalt
        3. Bereinigt den Text: entfernt Zeilenumbrüche und extra Leerzeichen
        4. Prüft, ob noch etwas übrig ist (nicht leer)
        5. Gibt die saubere Suchanfrage zurück

        Argumente:
            file_path (str): Der Pfad zur Textdatei mit der Suchanfrage.
                            Beispiel: "queries/meine_anfrage.txt"

        Rückgabewert:
            str: Die bereinigte Suchanfrage, bereit für die Europe PMC API.
                 Beispiel: "(COVID-19 OR SARS-CoV-2) AND vaccine"

        Fehler (Exceptions):
            FileNotFoundError: Die Datei existiert nicht oder der Pfad ist falsch.
            ValueError: Die Datei ist leer (keine Suchanfrage vorhanden).
        """
        
        # ========== SCHRITT 1: Datei-Existenz prüfen ==========
        if not os.path.exists(file_path):
            logger.error(f"Suchanfrage-Datei nicht gefunden: {file_path}")
            raise FileNotFoundError(f"Suchanfrage-Datei nicht gefunden: {file_path}")

        try:
            # ========== SCHRITT 2: Datei öffnen und lesen ==========
            # encoding='utf-8': Damit Umlaute (ä, ö, ü) korrekt gelesen werden
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # ========== SCHRITT 3: Text bereinigen ==========
            # .split(): Trennt den Text an jedem Leerzeichen/Zeilenumbruch
            # " ".join(...): Fügt alle Teile mit einem einzelnen Leerzeichen zusammen
            # Effekt: Zeilenumbrüche werden zu Leerzeichen, extra Leerzeichen werden entfernt
            # Beispiel: "COVID-19\n    AND\n    vaccine" → "COVID-19 AND vaccine"
            query = " ".join(content.split()).strip()

            # ========== SCHRITT 4: Prüfe, ob Query nicht leer ist ==========
            if not query:
                logger.error(f"Suchanfrage-Datei ist leer: {file_path}")
                raise ValueError(f"Suchanfrage-Datei ist leer: {file_path}")

            # ========== SCHRITT 5: Erfolgs-Meldungen loggen ==========
            # logger.info: Wichtige Informationen (z.B. "Datei erfolgreich geladen")
            logger.info(f"Suchanfrage erfolgreich geladen aus: {file_path}")
            # logger.debug: Detaillierte Informationen für Fehlersuche
            logger.debug(f"Suchanfrage-Inhalt: {query}")
            
            # ========== SCHRITT 6: Fertige Suchanfrage zurückgeben ==========
            return query

        # Falls irgendein Fehler passiert (z.B. Datei-Lesefehler)
        except Exception as e:
            logger.error(f"Fehler beim Lesen der Suchanfrage-Datei: {e}")
            raise
