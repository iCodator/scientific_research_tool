# GitHub Setup Anleitung

So stellst du das Projekt auf GitHub bereit:

## 1. GitHub Repository erstellen

### Option A: Web-Interface
1. Gehe zu https://github.com/new
2. **Repository name**: `scientific-research-tool`
3. **Description**: "A Python tool for searching scientific databases (PubMed, Europe PMC, Cochrane) with structured queries"
4. **Public** oder **Private**: Wähle das Beste für dich
5. **Initialize this repository with:**
   - ✅ Add a README file (können wir überschreiben)
   - ❌ Don't add .gitignore (haben wir bereits)
   - ❌ Don't add a license (haben wir bereits)
6. Klick "Create repository"

### Option B: Kommandozeile
```bash
# Installiere GitHub CLI (falls noch nicht vorhanden)
# macOS
brew install gh

# Linux
sudo apt install gh

# Windows
choco install gh

# Login
gh auth login

# Repository erstellen
gh repo create scientific-research-tool \
  --description "A Python tool for searching scientific databases with structured queries" \
  --public \
  --source=. \
  --remote=origin \
  --push
```

## 2. Lokales Git-Repository initialisieren

Falls noch nicht geschehen:

```bash
# Gehe ins Projekt-Verzeichnis
cd scientific-research-tool

# Initialisiere Git
git init

# Füge alle Dateien hinzu
git add .

# Committen
git commit -m "Initial commit: Scientific Research Tool v1.0.0"

# Remote hinzufügen (ersetze USERNAME)
git remote add origin https://github.com/USERNAME/scientific-research-tool.git

# Branch zu 'main' umbenennen (falls noch 'master')
git branch -M main

# Auf GitHub pushen
git push -u origin main
```

## 3. Projekt-Struktur auf GitHub

Nach dem Push solltest du folgende Struktur sehen:

```
scientific-research-tool/
├── README.md              ← Wird auf GitHub angezeigt
├── INSTALL.md
├── QUERIES.md
├── CONTRIBUTING.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── config.env.template
├── main.py                ← Hauptskript
├── logs/                  ← (wird ignoriert)
├── output/                ← (wird ignoriert)
└── src/
    ├── core/
    │   ├── query_detector.py
    │   └── query_compiler.py
    └── databases/
        ├── pubmed.py
        ├── europe_pmc.py
        └── cochrane.py
```

## 4. GitHub Badges hinzufügen (Optional)

Füge zu README.md am Anfang ein:

```markdown
# Scientific Research Tool 🔬

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/scientific-research-tool.svg)](https://github.com/yourusername/scientific-research-tool)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/scientific-research-tool.svg)](https://github.com/yourusername/scientific-research-tool)

...
```

## 5. GitHub Topics hinzufügen

1. Gehe zu deinem Repository
2. Klick auf "Settings" (Zahnrad oben rechts)
3. Scrolle zu "About" (rechts oben)
4. Klick auf Zahnrad neben Repository description
5. Füge Topics hinzu:
   - `scientific-research`
   - `pubmed`
   - `bioinformatics`
   - `python`
   - `data-science`
   - `api`

## 6. Releases erstellen (Optional aber empfohlen)

```bash
# Erstelle ein Git Tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push den Tag zu GitHub
git push origin v1.0.0
```

Oder über Web:
1. Gehe zu "Releases" auf GitHub
2. Klick "Create a new release"
3. **Tag**: `v1.0.0`
4. **Release title**: `Scientific Research Tool v1.0.0`
5. **Description**: 
```markdown
Initial release of the Scientific Research Tool

### Features
- ✅ PubMed, Europe PMC, Cochrane support
- ✅ Structured query validation
- ✅ CSV and JSON export
- ✅ Comprehensive logging

### Installation
See [INSTALL.md](INSTALL.md) for detailed instructions.

### Usage
```bash
python main.py --query "cancer AND therapy" --source pubmed --limit 100 --output results.csv
```

See [README.md](README.md) and [QUERIES.md](QUERIES.md) for more examples.
```

## 7. Nachfolgende Commits

```bash
# Nach Änderungen
git add .
git commit -m "Fix: Query validation for multi-word terms"
git push origin main

# Mit Feature-Branch
git checkout -b feature/new-database
# ... mache Änderungen ...
git add .
git commit -m "Add support for new database X"
git push origin feature/new-database

# Dann erstelle einen Pull Request auf GitHub
```

## 8. Zusätzliche GitHub-Einstellungen (Optional)

### Automatisierte Tests (CI/CD)
Erstelle `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest
    
    - name: Run tests
      run: pytest tests/ -v
```

### Code Quality Check
Erstelle `.github/workflows/lint.yml`:

```yaml
name: Code Quality

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8 black
    
    - name: Lint with flake8
      run: flake8 src/ main.py --count --select=E9,F63,F7,F82 --show-source --statistics
    
    - name: Check formatting with black
      run: black --check src/ main.py
```

## 9. .gitignore überprüfen

Stelle sicher, dass diese Dateien ignoriert werden:

```bash
# Überprüfe .gitignore
cat .gitignore

# Sollte diese Einträge haben:
# - venv/
# - config.env
# - *.log
# - output/
# - __pycache__/
# - .DS_Store

# Überprüfe welche Dateien tracked sind
git ls-files

# Falls config.env versehentlich hinzugefügt wurde:
git rm --cached config.env
git commit -m "Remove config.env from tracking"
git push origin main
```

## 10. Dokumentation Review

Überprüfe auf GitHub:

- [ ] README.md wird richtig angezeigt
- [ ] Alle Links funktionieren
- [ ] Code-Beispiele sind korrekt formatiert
- [ ] Markdown Syntax ist richtig
- [ ] Bilder/Emojis werden angezeigt
- [ ] INSTALL.md ist verständlich
- [ ] QUERIES.md ist vollständig
- [ ] LICENSE ist vorhanden

## 11. GitHub README Verbesserungen

Füge zu README.md hinzu:

```markdown
## 🌟 Highlights

- **34M+ Artikel** in PubMed durchsuchen
- **Strukturierte Queries** für präzise Ergebnisse
- **Mehrere Datenbanken** gleichzeitig nutzen
- **Automatische Validierung** der Query-Syntax
- **CSV/JSON Export** für Datenanalyse
- **Vollständige Dokumentation** auf Deutsch und Englisch

## 📊 Statistiken

- **Stars**: ![GitHub stars](https://img.shields.io/github/stars/yourusername/scientific-research-tool.svg)
- **Forks**: ![GitHub forks](https://img.shields.io/github/forks/yourusername/scientific-research-tool.svg)
- **License**: MIT
- **Python Version**: 3.8+
- **Status**: ✅ Active Development

## 🔗 Links

- 📖 [Vollständige Dokumentation](https://github.com/yourusername/scientific-research-tool/wiki)
- 🐛 [Issues & Bugs](https://github.com/yourusername/scientific-research-tool/issues)
- 💬 [Diskussionen](https://github.com/yourusername/scientific-research-tool/discussions)
- 📝 [Changelog](CHANGELOG.md)
```

## 12. Weitere GitHub Features

- **Wiki**: Umfangreiche Dokumentation
- **Discussions**: Q&A und Austausch mit Nutzern
- **Projects**: Kanban Board für Features/Bugs
- **Pages**: Website für das Projekt (ghpages)
- **Releases**: Download-Links für stabile Versionen

## 📋 Checkliste vor dem finalen Push

- [ ] Alle Dateien sind in `.gitignore` außer notwendigen
- [ ] `config.env` ist NICHT im Repository (auch nicht im History!)
- [ ] Alle Dokumentations-Dateien sind vorhanden
- [ ] Requirements.txt ist aktuell
- [ ] `main.py` funktioniert und ist getestet
- [ ] Alle Code-Kommentare sind sinnvoll
- [ ] README.md ist verständlich und vollständig
- [ ] LICENSE ist vorhanden
- [ ] `.gitignore` ist richtig konfiguriert

Fertig! Dein Projekt ist jetzt auf GitHub! 🎉
