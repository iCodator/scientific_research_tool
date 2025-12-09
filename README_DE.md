# Scientific Research Tool 🔬

Ein Python-Werkzeug zur programmgesteuerten Suche in großen wissenschaftlichen Datenbanken (PubMed, Europe PMC, Cochrane) mit **strukturierten Anfragen**.

![Lizenz](https://img.shields.io/badge/Lizenz-MIT-yellow.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Status](https://img.shields.io/badge/Status-Aktiv-green.svg)

## 🎯 Was ist das?

Statt manuell in PubMed zu suchen, nutze dieses Tool zur programmatischen Suche in mehreren wissenschaftlichen Datenbanken mit **strukturierten Abfragen**:

```bash
python main.py --query "(cancer OR tumor) AND (immunotherapy OR immune checkpoint)" --source pubmed --limit 100 --output results.csv
```

## ✨ Features

- 🔍 **Mehrere Datenbanken**: PubMed (34 Mio.+ Artikel), Europe PMC (42 Mio.+ Artikel), Cochrane (Systematische Reviews)
- 📋 **Strukturierte Anfragen**: AND, OR, NOT Operatoren mit Syntax-Validierung
- 📊 **Mehrere Formate**: Export zu CSV oder JSON
- 🔐 **API-Integration**: Optionale API-Keys für höhere Rate Limits
- 📝 **Vollständiges Logging**: Alle Suchen werden automatisch protokolliert
- 🛡️ **Anfrage-Validierung**: Verhindert fehlerhafte Suchen vor dem API-Aufruf
- 🌍 **Multi-Sprachen-Support**: Deutsche und englische Dokumentation

---

## 🚀 Schnelleinstieg

### 1. Installation

```bash
# Repository klonen
git clone https://github.com/yourusername/scientific_research.git
cd scientific_research

# Virtuelle Umgebung erstellen
python3 -m venv venv
source venv/bin/activate  # oder: venv\Scripts\activate (Windows)

# Dependencies installieren
pip install -r requirements.txt
```

### 2. Erste Suche

```bash
# Einfache Test-Anfrage
python main.py --query "cancer AND therapy" --source pubmed --limit 10

# Mit Export
python main.py --query "cancer AND therapy" --source pubmed --limit 50 --output results.csv
```

### 3. Komplexe Anfrage

```bash
python main.py \
  --query "((cancer OR tumor) AND (therapy OR treatment)) NOT animal" \
  --source pubmed \
  --limit 100 \
  --output cancer_research.json
```

---

## 📚 Dokumentation

- **[INSTALL.md](INSTALL.md)** – Detaillierte Installationsanleitung für alle Systeme
- **[QUERIES.md](QUERIES.md)** – Vollständige Anfrage-Syntax-Referenz mit Beispielen
- **[CONTRIBUTING.md](CONTRIBUTING.md)** – Deutsche Kurzübersicht
- **[GITHUB_SETUP.md](GITHUB_SETUP.md)** – GitHub-Einrichtungsanleitung
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** – Datei-Struktur-Übersicht

---

## 📖 Verwendungsbeispiele

### Einfache Suche

```bash
python main.py --query "cancer" --source pubmed --limit 25
```

### Mit Field-Tags (PubMed)

```bash
python main.py \
  --query "cancer[TitleAbstract] AND 2023:2025[pdat]" \
  --source pubmed \
  --limit 100
```

### Europe PMC Suche

```bash
python main.py \
  --query "TITLE_ABSTRACT:covid AND PUBYEAR:2020-2025 AND ISOPENACCESSY:Y" \
  --source europepmc \
  --limit 100
```

### Cochrane Suche

```bash
python main.py --query "cancer AND immunotherapy" --source cochrane --limit 10
```

### Aus Anfrage-Datei

```bash
# Anfrage-Datei erstellen
echo "(female OR woman) AND (masturbation OR self-stimulation) NOT animal" > my_query.txt

# Suche ausführen
python main.py --query-file my_query.txt --source pubmed --output results.csv
```

---

## 🗄️ Unterstützte Datenbanken

| Datenbank   | Quelle       | Größe             | Zugang                                                          |
|-------------|--------------|-------------------|-----------------------------------------------------------------|
| **PubMed**  | NCBI (USA)   | 34 Mio.+ Artikel  | [NCBI Query](https://www.ncbi.nlm.nih.gov/books/NBK3827/) via JSON API |
| **Europe PMC** | EBI (Europa) | 42 Mio.+ Artikel | [Europe PMC API](https://europepmc.org/api)                        |
| **Cochrane** | Europe PMC¹ | Systematische Reviews | [Europe PMC](https://europepmc.org/api) mit Auto-Filter            |

¹ **Hinweis zu Cochrane**: Cochrane-Reviews werden über die Europe PMC API abgerufen für maximale Zuverlässigkeit. Anfragen nutzen breite Suche (`AND Cochrane`) mit automatischer clientseitiger Filterung für Präzision.

---

## 💡 Anfrage-Syntax

### Erlaubte Formate ✅

```bash
✅ cancer AND therapy
✅ (cancer OR tumor) AND (therapy OR treatment)
✅ cancer AND NOT animal
✅ "Coenzyme Q10" AND mitochondria
✅ cancer[TitleAbstract] AND 2020:2025[pdat]
✅ TITLE_ABSTRACT:cancer AND PUBYEAR:2020-2025
```

### NICHT erlaubt ❌

```bash
❌ "Welche Therapien sind am wirksamsten bei Krebs?"  # Natürlichsprachige Fragen
❌ "Vorteile von Akupunktur bei Rückenschmerzen"      # Natürlichsprachige Aussagen
❌ "Ist Therapie A wirksamer als Therapie B?"         # Vergleiche als Fragen
```

Siehe **[QUERIES.md](QUERIES.md)** für vollständige Syntax-Dokumentation.

---

## 🔐 API-Konfiguration (Optional)

Das Tool funktioniert auch ohne API-Keys, aber die Limits sind strenger.

### PubMed/NCBI

1. Gehe zu: https://www.ncbi.nlm.nih.gov/account/
2. Registriere dich / Melde dich an
3. Hole deinen API-Key vom Dashboard
4. Erstelle `config.env`:

```bash
PUBMED_API_KEY=dein_api_key_hier
PUBMED_EMAIL=deine_email@example.com
```

### Europe PMC

1. Key erhalten von: https://europepmc.org/api
2. Hinzufügen zu `config.env`:

```bash
EUROPEPMC_API_KEY=dein_key_hier
```

**Wichtig**: Committe `config.env` niemals auf GitHub! Nutze `config.env.template` als Vorlage.

---

## 📊 Export-Formate

### CSV-Export

```csv
title,authors,year,journal,url,abstract
"Cancer Immunotherapy","Smith J, Jones A",2024,"Nature","https://...",
"Tumor Mechanism","Brown B",2023,"Cell","https://...",
```

### JSON-Export

```json
[
  {
    "title": "Cancer Immunotherapy",
    "authors": ["Smith J", "Jones A"],
    "year": 2024,
    "journal": "Nature",
    "url": "https://...",
    "abstract": "..."
  }
]
```

---

## 🛠️ Befehle

```bash
# Hilfe anzeigen
python main.py --help

# Einfache Suche
python main.py --query "cancer" --source pubmed

# Aus Datei
python main.py --query-file my_query.txt --source pubmed

# Mit Export
python main.py --query "cancer" --source pubmed --output results.csv

# Debug-Modus (zeigt Logs im Terminal)
python main.py --query "cancer" --source pubmed --verbose

# Benutzerdefiniertes Limit
python main.py --query "cancer" --source pubmed --limit 1000
```

---

## ❓ Häufig gestellte Fragen

### Brauche ich API-Keys?

Nein, das Tool funktioniert auch ohne diese. Mit Keys erhältst du aber:
- Höhere Rate Limits
- Schnellere Suchen
- Zusätzliche Features

### Welche Anfrage-Formate sind erlaubt?

Nur **strukturierte Anfragen** mit AND, OR, NOT Operatoren. Natürlichsprachige Fragen sind NICHT erlaubt. Siehe [QUERIES.md](QUERIES.md) für Details.

### Wie viele Artikel kann ich herunterladen?

- PubMed: Bis zu 100.000 über API
- Europe PMC: Bis zu 1.000–10.000 je nach Account
- Cochrane: Bis zu 10.000

### Wo sind die Logs?

Alle Suchen werden automatisch in `logs/search_*.log` protokolliert. Nutze das `--verbose` Flag um auch Terminal-Output zu sehen.

### Wie unterscheidet sich Cochrane von Europe PMC?

- **Europe PMC**: Durchsucht alle Artikeltypen über 42 Mio.+ Artikel
- **Cochrane**: Gefiltert speziell auf **Systematische Reviews** via automatischer Erkennung (Journal-Name + DOI-Präfix + Titel-Keywords)

---

## 🐛 Fehlerbehandlung

### "Query validation failed"

Deine Anfrage ist nicht strukturiert. Nutze AND, OR, NOT Operatoren.

```text
❌ "Welche Rolle spielt Coenzym Q10?"
✅ "(Coenzym Q10) AND Rolle"
```

### "No results found"

Versuche:
1. Vereinfache die Anfrage (entferne zu viele AND Bedingungen)
2. Nutze Synonyme: `(cancer OR carcinoma OR tumor)`
3. Überprüfe Rechtschreibung
4. Erhöhe das `--limit`

### "Connection timeout"

Die Datenbank antwortet nicht. Versuche es später noch mal oder nutze einen API-Key.

---

## 📁 Projektstruktur

Siehe **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** für detaillierte Dateistruktur-Dokumentation.

## 🤝 Mitwirken

Wir freuen uns über Beiträge! Siehe **[CONTRIBUTING.md](CONTRIBUTING.md)** für Richtlinien.

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe **[LICENSE](LICENSE)** Datei für Details.

## 📞 Support

- 📖 Lies die [Dokumentation](https://github.com/yourusername/scientific_research#readme)
- 🐛 Berichte Bugs via GitHub Issues
- 💬 Diskutiere Features in GitHub Discussions

---

**Gebaut mit ❤️ für offene Wissenschaft** 🔬
