"""
Modul: Konfiguration (Settings)
===============================

Zweck: Zentrale Konfiguration für die Scientific Research Tool.

Diese Datei lädt alle Einstellungen aus der .env-Datei
und stellt sie dem Rest der Anwendung zur Verfügung.


UMGEBUNGSVARIABLEN (in .env):

    # PubMed / NCBI
    NCBI_API_KEY=dein_api_key
    NCBI_EMAIL=deine_email@example.com
    
    # Europe PMC
    EUROPE_PMC_EMAIL=deine_email@example.com (optional)


VERWENDUNG:

    from src.config.settings import Settings
    
    # Zugriff auf Einstellungen
    print(Settings.NCBI_API_KEY)
    print(Settings.NCBI_EMAIL)
    
    # Validierung durchführen
    Settings.validate()
"""

import os
import logging
from dotenv import load_dotenv

# Lade die .env-Datei aus dem Root-Verzeichnis
load_dotenv()

# Logger für dieses Modul
logger = logging.getLogger(__name__)


class Settings:
    """
    Zentrale Konfigurationsklasse für die gesamte Anwendung.
    
    Diese Klasse lädt alle Einstellungen aus der .env-Datei
    und stellt sie als Klassenvariablen zur Verfügung.
    
    VORTEILE:
    - Zentrale Verwaltung aller Einstellungen
    - Sichere Behandlung von API-Keys (aus .env, nicht im Code)
    - Einfache Validierung beim Start
    - Typ-Hinweise und Dokumentation
    """

    # ========== PubMed / NCBI Settings ==========
    # Diese werden für die Kommunikation mit PubMed E-Utilities benötigt

    NCBI_API_KEY = os.getenv('NCBI_API_KEY')
    """
    API-Key für NCBI E-Utilities.
    
    Ermöglicht höhere Rate Limits (bis zu 10 Requests/Sekunde statt 3/Sekunde).
    Kostenlos unter: https://www.ncbi.nlm.nih.gov/account/
    
    Format: Beliebiger String (z.B. UUID)
    Erforderlich: Ja
    """

    NCBI_EMAIL = os.getenv('NCBI_EMAIL')
    """
    E-Mail-Adresse für NCBI.
    
    NCBI fordert eine E-Mail, um Missbrauch zu verhindern.
    Diese wird bei jeder API-Anfrage mitgesendet.
    
    Format: Gültige E-Mail-Adresse
    Erforderlich: Ja
    """

    # ========== Europe PMC Settings ==========
    # Diese werden für die Kommunikation mit Europe PMC benötigt

    EUROPE_PMC_BASE_URL = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search'
    """
    Base-URL für Europe PMC REST API.
    
    Diese URL wird für alle Europe PMC Anfragen verwendet.
    Öffentliche API, keine Authentifizierung erforderlich.
    """

    EUROPE_PMC_EMAIL = os.getenv('EUROPE_PMC_EMAIL', '')
    """
    E-Mail-Adresse für Europe PMC (optional).
    
    Kann angegeben werden, um bessere Support bei Problemen zu bekommen.
    Standard: Leer (wird ignoriert, wenn nicht gesetzt)
    """

    # ========== Allgemeine Settings ==========
    # Diese beeinflussen das Verhalten der gesamten Anwendung

    LOG_DIR = 'logs'
    """
    Verzeichnis für Log-Dateien.
    
    Log-Dateien werden täglich aktualisiert im Format: search_YYYY-MM-DD.log
    """

    REQUEST_TIMEOUT = 30
    """
    Timeout für HTTP-Requests in Sekunden.
    
    Falls eine API-Anfrage länger als 30 Sekunden dauert,
    wird die Verbindung abgebrochen.
    
    Default: 30 Sekunden
    """

    RATE_LIMIT_DELAY = 0.5
    """
    Verzögerung zwischen API-Requests in Sekunden.
    
    Dies verhindert, dass wir die API zu schnell bombardieren.
    
    Default: 0.5 Sekunden (= 2 Requests/Sekunde)
    
    NCBI empfiehlt:
    - Ohne API-Key: Mindestens 1/3 Sekunde Verzögerung (3 Requests/Sekunde)
    - Mit API-Key: Mindestens 0.1 Sekunden Verzögerung (10 Requests/Sekunde)
    """

    @staticmethod
    def validate() -> None:
        """
        Validiert, dass alle erforderlichen Einstellungen gesetzt sind.
        
        Diese Methode wird beim Start der Anwendung aufgerufen
        und prüft, ob alle notwendigen Umgebungsvariablen vorhanden sind.
        
        Raises:
            ValueError: Wenn erforderliche Einstellungen fehlen
        
        Beispiel:
            Settings.validate()  # Wirft Fehler, wenn etwas fehlt
        """

        errors = []

        # ========== NCBI-Validierung ==========
        if not Settings.NCBI_API_KEY:
            errors.append(
                "❌ NCBI_API_KEY nicht gesetzt.\n"
                "   Bitte in .env-Datei hinzufügen oder setzen:\n"
                "   NCBI_API_KEY=dein_api_key"
            )

        if not Settings.NCBI_EMAIL:
            errors.append(
                "❌ NCBI_EMAIL nicht gesetzt.\n"
                "   Bitte in .env-Datei hinzufügen oder setzen:\n"
                "   NCBI_EMAIL=deine_email@example.com"
            )

        # ========== Europe PMC-Validierung ==========
        # Nicht zwingend erforderlich, aber eine Warnung ist hilfreich
        if not Settings.EUROPE_PMC_EMAIL:
            logger.warning(
                "⚠️  EUROPE_PMC_EMAIL nicht gesetzt. "
                "Optional, aber empfohlen für bessere Support. "
                "Setze in .env: EUROPE_PMC_EMAIL=deine_email@example.com"
            )

        # ========== Fehler werfen, falls vorhanden ==========
        if errors:
            error_message = "\n".join(errors)
            print("\n" + "=" * 80)
            print("KONFIGURATIONSFEHLER")
            print("=" * 80)
            print(error_message)
            print("=" * 80)
            logger.error("Erforderliche Konfigurationen fehlen.")
            raise ValueError(
                "Erforderliche Konfigurationen fehlen. Siehe oben für Details."
            )

        logger.info("✓ Konfiguration validiert erfolgreich.")
        print("✓ Konfiguration validiert erfolgreich.")

    @staticmethod
    def print_info() -> None:
        """
        Gibt die aktuellen Einstellungen aus (ohne API-Keys).
        
        Nützlich für Debugging und Logs.
        """
        print("\n" + "=" * 80)
        print("KONFIGURATION")
        print("=" * 80)
        print(f"NCBI Email: {Settings.NCBI_EMAIL}")
        print(f"Europe PMC Email: {Settings.EUROPE_PMC_EMAIL}")
        print(f"Log Directory: {Settings.LOG_DIR}")
        print(f"Request Timeout: {Settings.REQUEST_TIMEOUT}s")
        print(f"Rate Limit Delay: {Settings.RATE_LIMIT_DELAY}s")
        print("=" * 80 + "\n")
