#!/usr/bin/env python3

"""
═══════════════════════════════════════════════════════════════════════════
LOGGING-MANAGER - Zentrale Verwaltung aller Logging-Operationen
═══════════════════════════════════════════════════════════════════════════

📚 ÜBERBLICK:
=============
Dieser LoggingManager kümmert sich um ALLES, was mit Logging zu tun hat.
Damit wird der Logging-Code aus main.py komplett ausgelagert.

BESONDERHEITEN:
================
✓ Zentrale Verwaltung aller Logger
✓ Separate Log-Dateien pro Datenbank
✓ Automatisches Datum im Dateinamen
✓ Konsole + Datei gleichzeitig
✓ Konfigurierbare Log-Level
✓ Singleton-Pattern (eine Instanz pro Datenbank)

VERWENDUNG:
===========
from src.core.logging_manager import LoggingManager

# Initialisiere Manager mit Datenbank
log_manager = LoggingManager("europepmc")
logger = log_manager.get_logger(__name__)

# Nutze den Logger wie gewohnt
logger.info("Test")
logger.error("Fehler")

# Aktiviere Verbose-Mode
log_manager.set_verbose(True)

# Hol dir den Log-Datei-Pfad
log_file = log_manager.get_log_file()

═══════════════════════════════════════════════════════════════════════════
"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Optional
from src.config.settings import Settings


class LoggingManager:
    """
    Zentrale Verwaltung aller Logging-Operationen.
    
    VERANTWORTLICHKEITEN:
    ====================
    1. Logger-Initialisierung mit Datenbank-Namen
    2. Separate Log-Dateien pro Datenbank
    3. Handler-Management (Datei + Konsole)
    4. Format-Verwaltung
    5. Log-Verzeichnis-Erstellung
    
    DESIGN-PATTERN: Singleton (nur eine Instanz pro Datenbank)
    
    BEISPIEL:
    =========
    manager = LoggingManager("europepmc")
    logger = manager.get_logger(__name__)
    logger.info("Message")
    
    RESULTAT:
    =========
    logs/europepmc_search_2025-12-09.log ← separate Datei pro Datenbank!
    """
    
    # Speichert alle Manager-Instanzen (ein Manager pro Datenbank)
    _instances = {}
    
    def __new__(cls, database: str = "main"):
        """
        Singleton-Pattern: Nur eine LoggingManager-Instanz pro Datenbank.
        
        Wenn LoggingManager("europepmc") zweimal aufgerufen wird,
        wird die gleiche Instanz zurückgegeben.
        """
        if database not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[database] = instance
        return cls._instances[database]
    
    def __init__(self, database: str = "main"):
        """
        Initialisiert den LoggingManager.
        
        Args:
            database (str): Name der Datenbank ('pubmed', 'europepmc', 'cochrane')
        """
        # Verhindere mehrfache Initialisierung (Singleton-Pattern)
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self.database = database
        self.logger = None
        self.log_file = None
        
        # Führe Setup durch
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """
        Interne Funktion: Richtet das Logging ein.
        
        WORKFLOW:
        =========
        1. Log-Verzeichnis anlegen
        2. Log-Format definieren
        3. Root-Logger holen und konfigurieren
        4. Datei-Handler hinzufügen (mit Datenbank-Präfix)
        5. Konsolen-Handler hinzufügen
        6. Startup-Meldungen schreiben
        """
        
        # ════════════════════════════════════════════════════════════════
        # SCHRITT 1: Log-Verzeichnis vorbereiten
        # ════════════════════════════════════════════════════════════════
        
        log_dir = Path(Settings.LOG_DIR)
        log_dir.mkdir(exist_ok=True)
        
        
        # ════════════════════════════════════════════════════════════════
        # SCHRITT 2: Log-Format definieren
        # ════════════════════════════════════════════════════════════════
        
        log_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        
        # ════════════════════════════════════════════════════════════════
        # SCHRITT 3: Root-Logger holen und konfigurieren
        # ════════════════════════════════════════════════════════════════
        
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        
        # Alle alten Handler entfernen (falls bereits vorhanden)
        self.logger.handlers.clear()
        
        
        # ════════════════════════════════════════════════════════════════
        # SCHRITT 4: Datei-Handler (Log-Datei mit Datenbank-Präfix)
        # ════════════════════════════════════════════════════════════════
        
        self.log_file = log_dir / f"{self.database}_search_{datetime.now().strftime('%Y-%m-%d')}.log"
        
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_format)
        
        self.logger.addHandler(file_handler)
        
        
        # ════════════════════════════════════════════════════════════════
        # SCHRITT 5: Konsolen-Handler (Terminal-Ausgabe)
        # ════════════════════════════════════════════════════════════════
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(log_format)
        
        self.logger.addHandler(console_handler)
        
        
        # ════════════════════════════════════════════════════════════════
        # Startup-Meldungen
        # ════════════════════════════════════════════════════════════════
        
        self.logger.info(f"Log-Verzeichnis: {log_dir}")
        self.logger.info(f"Log-Datei ({self.database.upper()}): {self.log_file}")
        self.logger.info(f"✓ Logging-Manager initialisiert für {self.database.upper()}")
    
    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """
        Gibt einen Logger mit dem angegebenen Namen zurück.
        
        VERWENDUNG:
        ===========
        logger = manager.get_logger(__name__)
        logger = manager.get_logger("src.databases.europe_pmc")
        
        Args:
            name (str): Name des Loggers (normalerweise __name__)
            
        Returns:
            logging.Logger: Ein Logger-Objekt
        """
        return logging.getLogger(name)
    
    def set_verbose(self, verbose: bool = True) -> None:
        """
        Aktiviert/Deaktiviert Verbose-Mode (DEBUG-Level).
        
        VERWENDUNG:
        ===========
        manager.set_verbose(True)   # Zeige DEBUG-Meldungen
        manager.set_verbose(False)  # Nur INFO+
        
        Args:
            verbose (bool): True = DEBUG Level, False = INFO Level
        """
        if verbose:
            self.logger.setLevel(logging.DEBUG)
            # Aktualisiere auch alle Handler
            for handler in self.logger.handlers:
                if isinstance(handler, logging.StreamHandler):
                    handler.setLevel(logging.DEBUG)
            self.logger.debug("🔍 Verbose Mode aktiviert")
        else:
            self.logger.setLevel(logging.INFO)
            for handler in self.logger.handlers:
                if isinstance(handler, logging.StreamHandler):
                    handler.setLevel(logging.INFO)
    
    def get_log_file(self) -> Path:
        """
        Gibt den Pfad zur Log-Datei zurück.
        
        VERWENDUNG:
        ===========
        log_file = manager.get_log_file()
        print(f"Logs in: {log_file}")
        
        Returns:
            Path: Pfad zur Log-Datei
        """
        return self.log_file
    
    @staticmethod
    def reset_all() -> None:
        """
        Setzt alle Logger zurück (für Tests).
        
        VERWENDUNG:
        ===========
        LoggingManager.reset_all()
        """
        for database, manager in LoggingManager._instances.items():
            if manager.logger:
                for handler in manager.logger.handlers:
                    handler.close()
        
        LoggingManager._instances.clear()
