"""
Modul: Konfiguration (Settings) - VERBESSERTE VERSION
========================================================

Zweck: Zentrale Konfiguration für die Scientific Research Tool.

BEHEBT:
✅ load_dotenv() jetzt mit korrektem Pfad zum Root-Verzeichnis
✅ Bessere Error-Messages
✅ Type-Hints hinzugefügt

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
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# ============================================================================
# NEUE FIX: Lade die .env-Datei mit korrektem Pfad
# ============================================================================
# Problem: load_dotenv() ohne Parameter sucht nur im aktuellen Verzeichnis
# Lösung: Pfad zum Root-Verzeichnis (wo .env liegt) explizit angeben

# Finde das Root-Verzeichnis des Projekts
# __file__ = /path/to/scientific_research_tool/src/config/settings.py
# parent.parent = /path/to/scientific_research_tool/
PROJECT_ROOT = Path(__file__).parent.parent.parent
ENV_FILE = PROJECT_ROOT / '.env'

# Lade die .env-Datei mit explizitem Pfad
# Optional=True = Fehler nicht, wenn .env nicht existiert (z.B. in Production mit Environment-Variablen)
load_dotenv(ENV_FILE, override=False)

# Logger für dieses Modul
logger = logging.getLogger(__name__)

# Gib Bescheid, welche .env-Datei geladen wurde
if ENV_FILE.exists():
    logger.debug(f"✓ .env geladen von: {ENV_FILE}")
else:
    logger.debug(f"⚠️ .env nicht gefunden unter: {ENV_FILE} (nutze Environment-Variablen)")


class Settings:
    """
    Zentrale Konfigurationsklasse für die gesamte Anwendung.

    Diese Klasse lädt alle Einstellungen aus der .env-Datei
    und stellt sie als Klassenvariablen zur Verfügung.

    VORTEILE:
    - Zentrale Verwaltung aller Einstellungen
    - Sichere Behandlung von API-Keys (aus .env, nicht im Code)
    - Einfache Validierung beim Start
    - Type-Hinweise und Dokumentation
    - Einziger Ort, um Konfiguration zu ändern
    """

    # ========== PubMed / NCBI Settings ==========
    # Diese werden für die Kommunikation mit PubMed E-Utilities benötigt

    NCBI_API_KEY: Optional[str] = os.getenv('NCBI_API_KEY')
    """
    API-Key für NCBI E-Utilities.
    
    ❓ Was ist das?
    Ein persönlicher Zugangsschlüssel, damit du schneller auf PubMed zugreifen kannst.
    
    📊 Auswirkungen:
    - Ohne Key: Max. 3 Anfragen pro Sekunde
    - Mit Key: Max. 10 Anfragen pro Sekunde
    
    🔑 Wie bekommen?
    Kostenlos unter: https://www.ncbi.nlm.nih.gov/account/
    (Registrierung erforderlich, dann Key in Settings kopieren)
    
    Format: Beliebiger String (z.B. UUID)
    Erforderlich: Ja ✅
    """

    NCBI_EMAIL: Optional[str] = os.getenv('NCBI_EMAIL')
    """
    E-Mail-Adresse für NCBI.
    
    ❓ Was ist das?
    Eine Kontakt-E-Mail, damit NCBI dich erreichen kann bei Problemen.
    
    💡 Warum nötig?
    NCBI möchte wissen, wer da API-Anfragen macht (verhindert Missbrauch).
    Diese E-Mail wird bei jeder Anfrage mitgesendet.
    
    Format: Gültige E-Mail-Adresse (z.B. max.mustermann@example.com)
    Erforderlich: Ja ✅
    """

    # ========== Europe PMC Settings ==========
    # Diese werden für die Kommunikation mit Europe PMC benötigt

    EUROPE_PMC_BASE_URL: str = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search'
    """
    Base-URL für Europe PMC REST API.
    
    ❓ Was ist das?
    Die Web-Adresse der API-Schnittstelle von Europe PMC.
    Diese URL wird für alle Europe PMC Anfragen verwendet.
    
    💡 Wichtig:
    Öffentliche API, keine Authentifizierung erforderlich!
    (Nur optional: E-Mail-Angabe für besseren Support)
    
    Format: URL
    Erforderlich: Nein (ist hardcodiert) ✅
    """

    EUROPE_PMC_EMAIL: Optional[str] = os.getenv('EUROPE_PMC_EMAIL', '')
    """
    E-Mail-Adresse für Europe PMC (optional).
    
    ❓ Was ist das?
    Eine optionale Kontakt-E-Mail, um besseren Support zu erhalten.
    
    💡 Wichtig:
    Europe PMC funktioniert auch OHNE E-Mail!
    Falls gesetzt, wird sie bei Anfragen mitgesendet für bessere Support.
    
    Standard: Leer (wird ignoriert, wenn nicht gesetzt)
    Format: E-Mail-Adresse oder leer
    Erforderlich: Nein ❌
    """

    # ========== Allgemeine Settings ==========
    # Diese beeinflussen das Verhalten der gesamten Anwendung

    LOG_DIR: str = 'logs'
    """
    Verzeichnis für Log-Dateien.
    
    ❓ Was ist das?
    Ein Ordner, wo alle Suchvorgänge protokolliert werden (für Debugging).
    
    📋 Beispiel Logdatei:
    logs/search_2025-12-08.log
    
    💡 Wichtig:
    - Wird automatisch erstellt, falls nicht vorhanden
    - Täglich neue Logdatei
    - Nützlich zum Fehlersuchen
    """

    REQUEST_TIMEOUT: int = 30
    """
    Timeout für HTTP-Requests in Sekunden.
    
    ❓ Was ist das?
    Die maximale Zeit, die das Tool auf eine Antwort von der API wartet.
    
    ⏱️ Beispiel:
    Wenn die API länger als 30 Sekunden nicht antwortet:
    → Tool bricht Verbindung ab und versucht neue Anfrage
    
    Default: 30 Sekunden (guter Wert für meist stabile Verbindungen)
    Min: 10 Sekunden (zu kurz = zu viele Fehler)
    Max: 120 Sekunden (zu lang = wartet ewwig)
    """

    RATE_LIMIT_DELAY: float = 0.5
    """
    Verzögerung zwischen API-Requests in Sekunden.
    
    ❓ Was ist das?
    Die Pause, die das Tool zwischen zwei Anfragen macht.
    
    💡 Warum nötig?
    Wenn du 1000 Artikel holst, macht das Tool 1000 API-Anfragen.
    Ohne Pausen → Die Server sperren dich (Missbrauchschutz).
    
    ⏱️ Mathematik:
    RATE_LIMIT_DELAY = 0.5 Sekunden
    → Pro Sekunde max. 2 Anfragen möglich
    → 1000 Artikel brauchen ~500 Sekunden = ~8 Minuten
    
    NCBI empfiehlt:
    - Ohne API-Key: Mindestens 0.33 Sekunden (3 Requests/Sekunde)
    - Mit API-Key: Mindestens 0.1 Sekunden (10 Requests/Sekunde)
    
    Default hier: 0.5 Sekunden (sicher für beide Fälle)
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
                "   NCBI_API_KEY=dein_api_key\n"
                "   Kostenlos unter: https://www.ncbi.nlm.nih.gov/account/"
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
                "⚠️ EUROPE_PMC_EMAIL nicht gesetzt. "
                "Optional, aber empfohlen für bessere Support. "
                "Setze in .env: EUROPE_PMC_EMAIL=deine_email@example.com"
            )

        # ========== Fehler werfen, falls vorhanden ==========
        if errors:
            error_message = "\n".join(errors)
            print("\n" + "=" * 80)
            print("🔴 KONFIGURATIONSFEHLER")
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
        (API-Keys werden NICHT angezeigt, um Sicherheit zu wahren!)
        """

        print("\n" + "=" * 80)
        print("⚙️  KONFIGURATION")
        print("=" * 80)
        print(f"NCBI Email: {Settings.NCBI_EMAIL}")
        print(f"Europe PMC Email: {Settings.EUROPE_PMC_EMAIL if Settings.EUROPE_PMC_EMAIL else '(nicht gesetzt)'}")
        print(f"Log Directory: {Settings.LOG_DIR}")
        print(f"Request Timeout: {Settings.REQUEST_TIMEOUT}s")
        print(f"Rate Limit Delay: {Settings.RATE_LIMIT_DELAY}s")
        print("=" * 80 + "\n")

# ============================================================================
# Auto-Validierung beim Import
# ============================================================================
# Wenn dieses Modul importiert wird, werden die Einstellungen sofort validiert.
# So merkt man Fehler sofort beim Start des Programms!
#
# Falls du TESTING betreibst und keine .env brauchst,
# kommentiere die nächste Zeile aus:

# Settings.validate()  # ← Aktiviert, wenn Validierung gewünscht
