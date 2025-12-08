# Installation - Detailliertes Handbuch

Dieses Dokument führt dich **Schritt für Schritt** durch die Installation.

## 🖥️ System-Voraussetzungen

### Linux / macOS

```bash
# Python Version überprüfen
python3 --version
# Sollte mind. 3.8 sein

# pip überprüfen
pip3 --version
```

### Windows

1. Gehe zu: https://www.python.org/downloads/
2. Lade die neueste Python-Version herunter
3. Installiere sie (**wichtig**: Häkchen bei "Add Python to PATH" setzen)
4. Öffne PowerShell/CMD und gib ein:

```powershell
python --version
pip --version
```

## 📦 Installation Schritt-für-Schritt

### 1. Repository klonen

**Option A: Mit Git** (empfohlen)

```bash
git clone https://github.com/yourusername/scientific-research-tool.git
cd scientific-research-tool
```

**Option B: Zip herunterladen**

1. Gehe zu https://github.com/yourusername/scientific-research-tool
2. Klicke auf grünen "Code" Button
3. Wähle "Download ZIP"
4. Entpacke die Datei
5. Öffne Terminal/PowerShell im entpackten Ordner

### 2. Virtuelle Python-Umgebung

Die virtuelle Umgebung isoliert das Projekt - wichtig für Stabilität!

#### Linux / macOS

```bash
# Umgebung erstellen
python3 -m venv venv

# Umgebung aktivieren
source venv/bin/activate

# Prompt sollte jetzt "(venv)" anzeigen
(venv) $ _
```

#### Windows (PowerShell)

```powershell
# Umgebung erstellen
python -m venv venv

# Umgebung aktivieren (PowerShell)
venv\Scripts\Activate.ps1

# Falls "Execution Policy" Fehler kommt:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Windows (CMD)

```cmd
# Umgebung erstellen
python -m venv venv

# Umgebung aktivieren (CMD)
venv\Scripts\activate.bat

# Prompt sollte jetzt "(venv)" anzeigen
(venv) C:\Pfad\zu\Projekt>
```

### 3. Dependencies installieren

```bash
# Stelle sicher, dass die venv aktiviert ist!
# (venv) sollte vorne im Terminal stehen

pip install --upgrade pip
pip install -r requirements.txt
```

Wenn Fehler auftreten:

```bash
# Versuche mit Python direkt
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Installation überprüfen

```bash
# Prüfe ob alles installiert ist
pip list

# Sollte zeigen:
# biopython        1.79
# requests         2.28.1
# ...

# Starte das Tool
python main.py --help
```

## 🔑 API-Keys konfigurieren (Optional)

Die Tool funktioniert auch ohne Keys, API-Limits sind dann stricter.

### PubMed/NCBI API Key

1. Gehe zu: https://www.ncbi.nlm.nih.gov/account/
2. Klicke "Sign in" oder "Create account"
3. Logge dich ein/registriere dich
4. Gehe zum Account-Dashboard
5. Klicke auf "API Key Management"
6. Klicke "Create API Key"
7. Kopiere den angezeigten Key

Jetzt erstelle eine `config.env` Datei:

```bash
# Im Projekt-Stammverzeichnis
cat > config.env << 'EOF'
PUBMED_API_KEY=dein_ncbi_api_key_hier
PUBMED_EMAIL=deine_email@example.com
EUROPEPMC_API_KEY=dein_europepmc_key_hier
EOF
```

**Wichtig**: Gib `config.env` **NICHT** auf GitHub ein!

```bash
# .gitignore überprüfen
cat .gitignore
# Sollte "config.env" enthalten
```

## 🚀 Erste Nutzung

### Test-Query ausführen

```bash
# Aktiviere die venv (falls nicht aktiv)
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Einfache Test-Query
python main.py \
  --query "cancer AND therapy" \
  --source pubmed \
  --limit 5 \
  --verbose
```

### Query aus Datei

```bash
# Erstelle eine Query-Datei
cat > test_query.txt << 'EOF'
(cancer OR tumor) AND (therapy OR treatment)
EOF

# Führe Suche durch
python main.py \
  --query-file test_query.txt \
  --source pubmed \
  --limit 10 \
  --output results.csv
```

## ❌ Fehlerbehandlung

### Fehler: "ModuleNotFoundError: No module named 'requests'"

```bash
# Stelle sicher, dass venv aktiv ist
# (venv) sollte am Anfang der Zeile stehen

# Falls nicht:
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Installiere Dependencies neu
pip install -r requirements.txt
```

### Fehler: "python: command not found" (macOS/Linux)

```bash
# Versuche python3 statt python
python3 main.py --query "test"

# Oder erstelle einen Alias
alias python=python3
```

### Fehler: "Permission denied" (Linux/macOS)

```bash
# Gib dem Script Ausführungsrechte
chmod +x main.py

# Oder starte mit python
python main.py --help
```

### Fehler: "cannot open file 'venv\Scripts\activate.bat'" (Windows)

```powershell
# Prüfe ob venv existiert
dir venv

# Falls nicht, erstelle neu
python -m venv venv

# Und aktiviere
venv\Scripts\Activate.ps1
```

## 🔄 Venv deaktivieren/wieder aktivieren

```bash
# Deaktivieren (alle Systeme)
deactivate

# Prompt sollte jetzt kein "(venv)" zeigen
$ _

# Wieder aktivieren
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

## 🔨 Entwicklungs-Setup

Falls du das Projekt weiterentwickeln möchtest:

```bash
# Installiere zusätzliche Dev-Tools
pip install -r requirements-dev.txt

# Das Paket im Edit-Modus installieren
pip install -e .

# Tests laufen lassen
pytest tests/ -v
```

## 📚 Weitere Ressourcen

- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)
- [PubMed API Dokumentation](https://www.ncbi.nlm.nih.gov/books/NBK25498/)
- [Europe PMC API Docs](https://europepmc.org/api)
- [Requests Library](https://requests.readthedocs.io/)

## 💡 Tipps

1. **Immer venv aktivieren** bevor du pip oder python nutzt
2. **requirements.txt aktuell halten**: `pip freeze > requirements.txt`
3. **config.env nicht committen**: Schützt deine API-Keys
4. **Logs überprüfen** bei Problemen: `tail -f logs/search_*.log`
