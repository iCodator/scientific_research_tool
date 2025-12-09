# 📘 Scientific Research Tool - Dokumentation

Willkommen zur offiziellen Dokumentation des Scientific Research Tools! 
Diese Anleitung erklärt dir genau, wie das Tool funktioniert, wie du es benutzt und wie es aufgebaut ist.

---

## 📑 Inhaltsverzeichnis
1. [Was ist das?](#-was-ist-das)
2. [Schnellstart](#-schnellstart)
3. [Bedienungsanleitung (Befehle)](#-bedienungsanleitung)
4. [Suchbeispiele](#-suchbeispiele-copy--paste)
5. [Die Ergebnisse (Output)](#-die-ergebnisse)
6. [Projektstruktur](#-projektstruktur)
7. [Fehlerbehebung](#-fehlerbehebung)

---

## 🌟 Was ist das?

Dieses Tool ist eine **Kommandozeilen-Suchmaschine** für wissenschaftliche Artikel. Anstatt manuell auf verschiedenen Webseiten zu suchen, kannst du mit **einem Befehl** mehrere Datenbanken abfragen und die Ergebnisse sauber gespeichert bekommen.

### Unterstützte Datenbanken:
- **PubMed:** Die größte Datenbank für Medizin & Life Sciences (NIH).
- **Europe PMC:** Europäisches Pendant mit Fokus auf Open Access und Biomedizin.
- **Cochrane Library:** Goldstandard für systematische Reviews und klinische Studien.

---

## 🚀 Schnellstart

Voraussetzung: Du hast Python installiert und das Terminal geöffnet.

### 1. Installation (einmalig)
```bash
# Erstelle eine virtuelle Umgebung (Isolation für das Projekt)
python3 -m venv venv

# Aktiviere die Umgebung
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Installiere die benötigten Pakete
pip install -r requirements.txt
```

### 2. Der erste Test
```bash
python main.py --query "aspirin" --source pubmed --limit 5
```
Wenn du Ergebnisse auf dem Bildschirm siehst: Glückwunsch! Es funktioniert. 🎉

---

## 🎮 Bedienungsanleitung

Das Tool wird über die Datei `main.py` gesteuert. Du gibst verschiedene "Flaggen" (Optionen) an, um zu steuern, was passiert.

### Die wichtigsten Befehle

| Flag | Abkürzung | Beschreibung | Beispiel |
|------|-----------|--------------|----------|
| `--query` | - | **(Pflicht)** Wonach suchst du? Bei Leerzeichen in Anführungszeichen setzen! | `--query "cancer treatment"` |
| `--source` | - | Welche Datenbank? (`pubmed`, `europepmc`, `cochrane`) | `--source europepmc` |
| `--limit` | - | Wie viele Artikel max.? (Standard: 25) | `--limit 100` |
| `--output` | - | Speichern als Datei. Name angeben (`.csv` oder `.json`) | `--output results.csv` |
| `--verbose` | - | "Gesprächiger Modus" – Zeigt technische Details (gut bei Fehlern) | `--verbose` |

---

## 🔍 Suchbeispiele (Copy & Paste)

### Szenario 1: Einfache Suche in PubMed
Ich will schnell wissen, was es Neues zu "Diabetes" gibt.
```bash
python main.py --query "diabetes" --source pubmed --limit 10
```

### Szenario 2: Datenexport für Excel
Ich brauche 100 Artikel über COVID-Impfstoffe aus Europe PMC für eine Tabelle.
```bash
python main.py --query "covid vaccine" --source europepmc --limit 100 --output my_data.csv
```
👉 **Ergebnis:** Die Datei liegt dann unter `output/europepmc_my_data.csv`.

### Szenario 3: Komplexere Suche
Ich suche Artikel über Krebs (Cancer) ODER Tumore, aber nur aus den Jahren 2023 bis 2025.
```bash
python main.py --query "(cancer OR tumor) AND 2023:2025" --source pubmed --output current_cancer_research.json
```

---

## 📂 Die Ergebnisse

Das Tool speichert Ergebnisse automatisch im Ordner `output/`.
Der Dateiname wird intelligent angepasst, damit du weißt, woher die Daten kommen.

**Beispiel:**
- Befehl: `--output studien.csv`
- Quelle: `--source cochrane`
- **Tatsächliche Datei:** `output/cochrane_studien.csv`

### Formate:

1. **CSV (.csv):**
   - Perfekt für Excel, Google Sheets oder LibreOffice Calc.
   - Spalten: ID, Titel, Autoren, Jahr, Journal, DOI, Link, Abstract.

2. **JSON (.json):**
   - Perfekt für Programmierer oder Datenanalyse (Python/R).
   - Enthält die gleichen Daten, aber strukturiert als Text-Objekte.

---

## 🏗 Projektstruktur

Hier ist eine Übersicht, wo du welche Dateien findest:

```text
scientific_research_tool/
├── docs/                   # 📄 Hier liegt diese Dokumentation
├── logs/                   # 📝 Log-Dateien (Fehlerprotokolle & Historie)
├── output/                 # 📊 Hier landen deine Suchergebnisse (CSV/JSON)
├── src/                    # 🧠 Der Quellcode (die "Intelligenz")
│   ├── config/             # Einstellungen (.env laden)
│   ├── core/               # Hauptlogik (Validierung, Datentypen)
│   └── databases/          # Adapter für PubMed, Cochrane, etc.
├── main.py                 # 🚀 Das Start-Skript (Hier tippst du deine Befehle)
├── requirements.txt        # Liste der benötigten Python-Pakete
└── README.md               # Kurze Übersicht für GitHub
```

---

## 🔧 Fehlerbehebung

### Problem: `ModuleNotFoundError: No module named 'src'`
**Lösung:** Das wurde in der neuesten Version (`main.py`) behoben! Stelle sicher, dass du die aktuellste `main.py` nutzt. Sie fügt den Projektpfad automatisch hinzu.

### Problem: `command not found: python`
**Lösung:** Auf manchen Systemen (Linux/Mac) musst du `python3` statt `python` schreiben.

### Problem: Exportierte CSV ist leer
**Lösung:**
1. Hast du `--limit` zu niedrig gesetzt?
2. Gab es für deine Suchanfrage überhaupt Ergebnisse? (Prüfe die Schreibweise!)
3. Schau in den `logs/` Ordner, dort steht oft der genaue Grund.

### Problem: "API Limit reached"
**Lösung:** Manche Datenbanken erlauben nur eine bestimmte Anzahl an Anfragen pro Sekunde. Warte kurz und versuche es erneut oder reduziere das `--limit`.

---

**Viel Erfolg bei deiner Recherche! 🔬**
