# 📦 Projekt-Übersicht - Alle wichtigen Dateien

Diese Datei gibt dir einen Überblick über alle Dateien des Projekts und wofür sie sind.

## 🎯 Struktur

```
scientific-research-tool/
│
├── 📖 DOKUMENTATION & README
│   ├── README.md                    # Hauptdokumentation (START HIER!)
│   ├── INSTALL.md                  # Detaillierte Installation (alle Systeme)
│   ├── QUERIES.md                  # Query-Syntax Referenz
│   ├── CONTRIBUTING.md             # Kurz-Dokumentation auf Deutsch
│   ├── GITHUB_SETUP.md             # So stellst du es auf GitHub bereit
│   ├── PROJECT_OVERVIEW.md         # Diese Datei
│   └── LICENSE                      # MIT License
│
├── 🐍 PYTHON CODE
│   ├── main.py                      # Hauptskript (ENTRY POINT)
│   ├── requirements.txt             # Dependencies (pip install -r)
│   ├── config.env.template         # Template für API-Keys
│   └── src/
│       ├── __init__.py
│       ├── core/
│       │   ├── query_detector.py   # Query-Typ Erkennung
│       │   └── query_compiler.py   # Query-Kompilierung & Stopwords
│       └── databases/
│           ├── pubmed.py            # PubMed Adapter
│           ├── europe_pmc.py        # Europe PMC Adapter
│           └── cochrane.py          # Cochrane Adapter
│
├── 🚫 GIT KONFIGURATION
│   └── .gitignore                  # Was Git nicht tracked
│
├── 📁 AUTOMATISCH ERSTELLT (bei Bedarf)
│   ├── venv/                        # Virtuelle Umgebung
│   ├── logs/                        # Logdateien
│   └── output/                      # Exportierte Ergebnisse
│
└── 📋 OPTIONAL (für GitHub)
    └── .github/workflows/          # CI/CD Pipelines (GitHub Actions)
        ├── tests.yml               # Automated Tests
        └── lint.yml                # Code Quality Check
```

## 📄 Datei-Beschreibungen

### Hauptdateien (WICHTIG!)

#### `main.py` ⭐
**Was**: Das Hauptskript - das einzige Skript das du normalerweise nutzt
**Nutzer**: Du
**Inhalt**:
- Query-Validierung
- Adapter-Auswahl
- CSV/JSON Export
- Logging

**Verwendung**:
```bash
python main.py --query "cancer AND therapy" --source pubmed --limit 100 --output results.csv
```

#### `README.md` 📖
**Was**: Die erste Dokumentation, die Nutzer lesen
**Inhalt**:
- Features
- Installation (kurz)
- Verwendungsbeispiele
- Fehlerbehandlung
- FAQ
- Support-Links

**Wer liest das**: Jeder, der das Projekt zum ersten Mal nutzt

#### `INSTALL.md` 🔧
**Was**: Detaillierte Installationsanleitung für ALLE Systeme
**Inhalt**:
- System-Voraussetzungen (Windows, macOS, Linux)
- Schritt-für-Schritt Installation
- Virtual Environment Setup
- Fehlerbehandlung
- Tipps & Tricks

**Wer nutzt das**: Anfänger, die Python nicht kennen

#### `QUERIES.md` 📋
**Was**: Vollständige Query-Syntax Referenz
**Inhalt**:
- Basis-Operatoren (AND, OR, NOT)
- Syntax-Regeln
- 20+ Query-Beispiele
- PubMed Field-Tags
- Europe PMC Syntax
- Wildcards
- Häufige Fehler
- Tipps für bessere Ergebnisse

**Wer nutzt das**: Nutzer die komplexe Queries schreiben wollen

#### `CONTRIBUTING.md` 🤝
**Was**: Deutsche Kurz-Übersicht des Projekts
**Inhalt**:
- Was ist das Tool?
- 5-Minuten Quick Start
- Links zu anderen Dokumenten
- Verwendungsbeispiele

**Wer nutzt das**: Nutzer die Deutsch bevorzugen

### Konfigurations-Dateien

#### `requirements.txt` 📦
**Was**: Liste aller Python Dependencies
**Inhalt**:
- `requests==2.28.1` - HTTP-Anfragen
- `biopython==1.81` - Bioinformatik
- `python-dotenv==0.21.0` - .env-Dateien lesen

**Installation**:
```bash
pip install -r requirements.txt
```

#### `config.env.template` 🔑
**Was**: Template für deine geheimen API-Keys
**Nutzer**: Solltest du copieren zu `config.env` und mit deinen Keys füllen
**Inhalt**:
- PUBMED_API_KEY
- PUBMED_EMAIL
- EUROPEPMC_API_KEY
- LOG_LEVEL

**WICHTIG**: `config.env` selbst gehört NICHT ins GitHub!

#### `.gitignore` 🚫
**Was**: Sagt Git welche Dateien es NICHT tracken soll
**Inhalt**:
- `venv/` - Virtuelle Umgebung
- `config.env` - Deine API-Keys (GEHEIM!)
- `__pycache__/` - Python Cache
- `logs/` - Logdateien
- `output/` - Exportierte Daten
- `.env` - Environment-Dateien

**Warum**: Schützt deine Geheimtaten und verhindert lokale Dateien im GitHub

### GitHub-spezifisch

#### `GITHUB_SETUP.md` 🚀
**Was**: Anleitung wie du das Projekt auf GitHub stellst
**Enthält**:
- Repository erstellen (Web oder Kommandozeile)
- Git initialisieren
- Commits und Push
- GitHub Features (Badges, Topics, Releases)
- CI/CD Setup
- Checkliste vor finalen Push

#### `LICENSE` 📜
**Was**: MIT License - erlaubt freie Nutzung
**Bedeutung**: Andere können das Projekt nutzen, müssen aber die Lizenz anerkennen

### Quellcode-Dateien

#### `src/core/query_detector.py` 🔍
**Was**: Erkennt den Query-Typ
**Funktion**:
- Ist es PubMed-formatiert?
- Ist es Europe PMC-formatiert?
- Ist es natürlichsprachig?
- Welche Sprache (Deutsch/Englisch)?

#### `src/core/query_compiler.py` 🔧
**Was**: Optimiert Queries (Stopwords, Synonyme)
**Funktion**:
- Entfernt Stopwords (und, oder, als)
- Ersetzt mit Synonymen (selbstbefriedigung → masturbation)
- Entfernt Duplikate
- Formatiert für PubMed/Europe PMC

#### `src/databases/pubmed.py` 🔬
**Was**: Adapter für PubMed API
**Funktion**:
- Queries an NCBI ESearch senden
- Ergebnisse von NCBI EFetch holen
- Results strukturieren

#### `src/databases/europe_pmc.py` 🌍
**Was**: Adapter für Europe PMC API
**Funktion**:
- Queries an Europe PMC senden
- Results parsen

#### `src/databases/cochrane.py` 📚
**Was**: Adapter für Cochrane Library
**Funktion**:
- Systematische Reviews durchsuchen

## 🚀 Workflow: Erste Nutzung

1. **Lese README.md** (2 Min)
2. **Folge INSTALL.md** (10 Min)
3. **Versuche erste Query** (5 Min)
   ```bash
   python main.py --query "cancer" --source pubmed --limit 10
   ```
4. **Lese QUERIES.md für komplexe Queries** (20 Min)
5. **Nutze das Tool** 🎉

## 📚 Workflow: Für Entwickler

1. **Lese README.md** (2 Min)
2. **Folge INSTALL.md** (10 Min)
3. **Nutze CONTRIBUTING.md zum Verstehen** (10 Min)
4. **Schau in `src/` Code** (30 Min)
5. **Stelle auf GitHub** mit GITHUB_SETUP.md (20 Min)
6. **Aktualisiere Docs wenn du Features hinzufügst**

## 🔄 Datei-Abhängigkeiten

```
main.py
├── Nutzt: requirements.txt (was installieren)
├── Nutzt: config.env (optional, für API-Keys)
├── Importiert: src/core/query_detector.py
├── Importiert: src/core/query_compiler.py
├── Importiert: src/databases/pubmed.py
├── Importiert: src/databases/europe_pmc.py
├── Importiert: src/databases/cochrane.py
└── Erstellt: logs/search_*.log (automatisch)

query_detector.py
├── Nutzt: RE (regular expressions)
└── Gibt zurück: QueryType Enum

query_compiler.py
├── Nutzt: RE
├── Nutzt: Logging
└── Gibt zurück: Kompilierte Query String

pubmed.py
├── Nutzt: requests
├── Nutzt: Logging
├── Nutzt: PUBMED_API_KEY aus config.env
└── Gibt zurück: List[Dict] (Artikel)

QUERIES.md
└── Referenziert: query_compiler.py (Beispiele)

INSTALL.md
└── Referenziert: requirements.txt (Dependencies)
```

## 💡 Datei-Checkliste vor GitHub Push

```bash
# ✅ Alle notwendigen Dateien vorhanden?
ls -la *.md          # README, INSTALL, QUERIES, CONTRIBUTING, GITHUB_SETUP
ls -la *.py          # main.py
ls -la *.txt         # requirements.txt
ls -la src/          # src/ Verzeichnis
ls -la .git*         # .gitignore

# ✅ Keine sensiblen Dateien?
grep -r "APIKEY" .   # Sollte nichts finden
grep -r "config.env" .gitignore  # Sollte darin sein

# ✅ Alle Dateien mit richtigen Inhalten?
head -20 main.py     # Sollte #!/usr/bin/env python3 anfangen
head -20 README.md   # Sollte mit # Scientific Research Tool starten
```

## 🔐 Geheime Dateien (Sollten NICHT im GitHub sein)

- `config.env` ← DEINE API-KEYS! (in .gitignore)
- `venv/` ← Virtuelle Umgebung (in .gitignore)
- `.env` ← Environment Dateien (in .gitignore)
- `logs/` ← Logdateien (in .gitignore)
- `output/*.csv` ← Deine exportierten Daten (in .gitignore)

## 📊 Datei-Größen (approximativ)

| Datei | Größe | Typ |
|-------|-------|-----|
| README.md | ~15 KB | Dokumentation |
| INSTALL.md | ~12 KB | Dokumentation |
| QUERIES.md | ~18 KB | Dokumentation |
| main.py | ~8 KB | Python Code |
| requirements.txt | 0.1 KB | Config |
| src/core/*.py | ~8 KB | Python Code |
| src/databases/*.py | ~20 KB | Python Code |
| Gesamt | ~80 KB | Mit Doku |

## 🎯 Zusammenfassung

**Du brauchst hauptsächlich:**
1. `main.py` - Das Skript das du ausführst
2. `src/` - Die Datenbank-Adapter
3. `requirements.txt` - Dependencies
4. `README.md` - Was ist das Projekt?
5. `QUERIES.md` - Wie nutze ich es?

**Für GitHub brauchst du zusätzlich:**
6. `.gitignore` - Was nicht hochladen
7. `LICENSE` - Lizenz
8. Alle anderen `.md` Dateien - Dokumentation

**Optional aber empfohlen:**
9. `.github/workflows/` - Automatisierte Tests
10. `config.env.template` - API-Key Template

Viel Erfolg! 🚀
