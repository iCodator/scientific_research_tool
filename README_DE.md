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

### Aus Anfrage-Datei

```bash
# Anfrage-Datei erstellen
echo "(female OR woman) AND (masturbation OR self-stimulation) NOT animal" > my_query.txt

# Suche ausführen
python main.py --query-file my_query.txt --source pubmed --output results.csv
```

---

## 🗄️ Unterstützte Datenbanken

| Datenbank   | Quelle       | Größe             | Syntax                                                          |
|-------------|--------------|-------------------|-----------------------------------------------------------------|
| **PubMed**  | NCBI (USA)   | 34 Mio.+ Artikel  | [NCBI Query](https://www.ncbi.nlm.nih.gov/books/NBK3827/)      |
| **Europe PMC** | EBI (Europa) | 42 Mio.+ Artikel | [Europe PMC](https://europepmc.org/api)                        |
| **Cochrane** | Cochrane Org | Systematische Reviews | [Cochrane API](https://data.cochrane.org/)                |

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
"Tumor Mechanism","Brown B",2023,"Cell","https://...","..."
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

# Debug-Modus
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

Alle Suchen werden automatisch in `logs/search_*.log` protokolliert.

### Wo speichere ich config.env?

Im Projekt-Root-Verzeichnis:

```text
scientific_research/
├── config.env          ← HIER (nicht auf GitHub!)
├── main.py
├── requirements.txt
└── ...
```

### Kann ich mehrere Datenbanken gleichzeitig durchsuchen?

Nein, momentan nur eine Datenbank pro Aufruf. Aber du kannst mit Bash-Scripts mehrere Aufrufe hintereinander ausführen:

```bash
python main.py --query "cancer" --source pubmed --output results_pubmed.csv
python main.py --query "cancer" --source europepmc --output results_europepmc.csv
python main.py --query "cancer" --source cochrane --output results_cochrane.csv
```

---

## 🐛 Fehlerbehandlung

### "Query validation failed"

Deine Anfrage ist nicht strukturiert. Nutze AND, OR, NOT Operatoren.

```text
❌ "Welche Rolle spielt Coenzym Q10?"
✅ "(Coenzym Q10) AND role"
```

### "No results found"

1. Anfrage vereinfachen (weniger AND-Bedingungen)
2. Synonyme nutzen: `(cancer OR carcinoma OR tumor)`
3. Rechtschreibung prüfen
4. `--limit` erhöhen

### "Connection timeout"

Die Datenbank antwortet nicht. Später erneut versuchen oder einen API-Key nutzen.

### "ModuleNotFoundError: No module named 'src'"

Stelle sicher, dass du vom **Projekt-Root** aus startest:

```bash
# RICHTIG:
cd scientific_research
python main.py --query "cancer" --source pubmed

# FALSCH:
cd src
python ../main.py --query "cancer" --source pubmed  # ❌
```

---

## 📁 Projekt-Struktur

```text
scientific_research/
├── README.md                    # Englische Hauptdoku
├── README_DE.md                 # Diese Datei (Deutsche Doku)
├── INSTALL.md                   # Installationsanleitung
├── QUERIES.md                   # Anfrage-Syntax Referenz
├── CONTRIBUTING.md              # Beitrags-Richtlinien
├── GITHUB_SETUP.md              # GitHub Einrichtung
├── PROJECT_OVERVIEW.md          # Datei-Struktur Übersicht
├── LICENSE                      # MIT Lizenz
├── requirements.txt             # Python Dependencies
├── main.py                      # Hauptskript
├── config.env.template          # API-Key Template
├── config.env                   # ← DEINE API-Keys (NICHT auf Git!)
├── .gitignore                   # Git Konfiguration
│
├── src/
│   ├── __init__.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── query_detector.py    # Anfrage-Typ Erkennung
│   │   └── query_validator.py   # Anfrage-Validierung
│   │
│   ├── databases/
│   │   ├── __init__.py
│   │   ├── database_adapter.py  # Basis-Klasse (Abstract)
│   │   ├── pubmed.py            # PubMed Adapter
│   │   ├── europe_pmc.py        # Europe PMC Adapter
│   │   └── cochrane.py          # Cochrane Adapter
│   │
│   └── config/
│       ├── __init__.py
│       └── settings.py          # Zentrale Konfiguration
│
├── logs/                        # ← Generierte Logdateien (NICHT auf Git!)
│   └── search_2025-12-08.log
│
└── output/                      # ← Exportierte Ergebnisse (NICHT auf Git!)
    ├── results.csv
    └── results.json
```

Siehe [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) für detaillierte Datei-Beschreibungen.

---

## 🤝 Mitwirken

Beiträge sind willkommen!

1. Fork das Repository
2. Feature-Branch erstellen: `git checkout -b feature/neue-funktion`
3. Änderungen committen: `git commit -am "Feature hinzugefügt"`
4. Push: `git push origin feature/neue-funktion`
5. Pull Request erstellen

Weitere Informationen: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 Lizenz

MIT Lizenz - siehe [LICENSE](LICENSE) Datei für Details.

```
Copyright (c) 2025 Arnulf Bultmann

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 📞 Support & Kontakt

- **GitHub Issues**: https://github.com/yourusername/scientific_research/issues
- **Diskussionen**: https://github.com/yourusername/scientific_research/discussions
- **Email**: arnulf.bultmann@example.com

---

## 🙏 Danksagungen

Gebaut mit:
- [NCBI PubMed API](https://pubmed.ncbi.nlm.nih.gov/)
- [Europe PMC API](https://europepmc.org/)
- [Cochrane Library](https://www.cochranelibrary.com/)

---

## 🔗 Weitere Ressourcen

### Dokumentation
- [PubMed Query Language](https://www.ncbi.nlm.nih.gov/books/NBK3827/)
- [Europe PMC Query Syntax](https://europepmc.org/QueryTipsFAQ)
- [Advanced PubMed Search](https://pubmed.ncbi.nlm.nih.gov/advanced/)

### Python
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Requests Library](https://requests.readthedocs.io/)
- [BioPython](https://biopython.org/)

### Tools
- [Git & GitHub](https://github.com/)
- [Python Package Manager (pip)](https://pip.pypa.io/)

---

## 💡 Tipps & Best Practices

### Anfragen-Tipps

1. **Spezifisch sein**: Je präziser die Anfrage, desto bessere Ergebnisse
   ```bash
   # Gut:
   python main.py --query "cancer AND immunotherapy AND clinical trial" --limit 50
   
   # Weniger gut:
   python main.py --query "cancer" --limit 50
   ```

2. **Synonyme nutzen**: Nutze OR um verschiedene Begriffe zu kombinieren
   ```bash
   # Besser:
   python main.py --query "(cancer OR carcinoma OR tumor) AND (therapy OR treatment)"
   ```

3. **Testen mit kleinem Limit**: Teste erst mit `--limit 5`
   ```bash
   python main.py --query "deine-anfrage" --source pubmed --limit 5
   ```

### Performance-Tipps

1. **API-Keys nutzen**: Mit Keys sind Anfragen schneller
2. **Kein zu großes Limit**: Sehr große Anfragen können lange dauern
3. **Logs überprüfen**: Bei Problemen `logs/` überprüfen

### Datenschutz-Tipps

1. **config.env schützen**: Niemals auf GitHub pushen
2. **Sensitive Daten**: Keine API-Keys in Code schreiben
3. **.gitignore nutzen**: Schützt automatisch vor Versehentlichem Upload

---

## 🚀 Fortgeschrittene Verwendung

### Mit Bash-Script

```bash
#!/bin/bash

# search.sh - Suchen mit Logging

cd scientific_research

QUERIES=(
  "(cancer OR tumor) AND immunotherapy"
  "covid 19 AND vaccine"
  "machine learning AND medicine"
)

for query in "${QUERIES[@]}"; do
  echo "Searching: $query"
  python main.py \
    --query "$query" \
    --source pubmed \
    --limit 100 \
    --output "output/results_${query// /_}.csv"
done
```

### Mit Python-Script

```python
import subprocess
import os

os.chdir('scientific_research')

queries = [
    "(cancer OR tumor) AND immunotherapy",
    "covid 19 AND vaccine",
    "machine learning AND medicine"
]

for query in queries:
    cmd = [
        'python', 'main.py',
        '--query', query,
        '--source', 'pubmed',
        '--limit', '100',
        '--output', f"output/results_{query.replace(' ', '_')}.csv"
    ]
    subprocess.run(cmd)
```

### Mit Docker (optional zukünftig)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
```

---

## 📈 Roadmap

Geplante Features:
- [ ] Web-Interface (Flask/Django)
- [ ] Datenbank-Integration (SQLite/PostgreSQL)
- [ ] Automatisierte Searches (Cron-Jobs)
- [ ] Machine Learning für Query-Optimization
- [ ] Advanced Filtering & Ranking
- [ ] Multi-Language Support (DE, FR, ES)
- [ ] REST API
- [ ] Docker-Support

---

## 🐞 Bekannte Probleme

| Problem | Ursache | Lösung |
|---------|--------|--------|
| Keine Ergebnisse | Zu spezifische Anfrage | Anfrage vereinfachen, OR nutzen |
| Timeout | Server antwortet nicht | Später erneut versuchen |
| Memory Error | Zu großes Limit | Limit reduzieren (max 1000) |
| API Error | Ungültiger Key | Key überprüfen |
| Import Error | Falsches Verzeichnis | Von `scientific_research/` starten |

---

## 📊 Statistiken

| Metrik | Wert |
|--------|------|
| Unterstützte Datenbanken | 3 |
| Artikel in PubMed | 34 Mio.+ |
| Artikel in Europe PMC | 42 Mio.+ |
| Minimale Python Version | 3.8 |
| Lizenz | MIT |
| Code Lines | ~1500 |
| Dokumentation | ~2500 Zeilen |
| Unterstützte APIs | 3 (NCBI, EBI, Cochrane) |

---

## ✅ Checkliste für erste Nutzung

- [ ] Repository geklont
- [ ] Verzeichnis: `cd scientific_research`
- [ ] Python 3.8+ installiert
- [ ] Virtuelle Umgebung erstellt: `python3 -m venv venv`
- [ ] venv aktiviert: `source venv/bin/activate`
- [ ] Requirements installiert: `pip install -r requirements.txt`
- [ ] config.env.template kopiert: `cp config.env.template config.env`
- [ ] config.env mit API-Keys gefüllt (optional)
- [ ] Erste Test-Anfrage: `python main.py --query "cancer" --source pubmed --limit 5`
- [ ] Logs überprüft: `ls logs/`
- [ ] Dokumentation gelesen: README.md, INSTALL.md
- [ ] Alle Tests bestanden

---

## 🎉 Gratulationen!

Du hast das **Scientific Research Tool** erfolgreich eingerichtet! 

### Nächste Schritte:

1. **Erste Suche starten**:
   ```bash
   python main.py --query "your topic here" --source pubmed --limit 10
   ```

2. **Mit Export arbeiten**:
   ```bash
   python main.py --query "your topic" --source pubmed --limit 100 --output my_results.csv
   ```

3. **Logs überprüfen**:
   ```bash
   tail -f logs/search_*.log
   ```

4. **Weitere Datenbanken ausprobieren**:
   ```bash
   python main.py --query "your topic" --source europepmc --limit 50
   ```

Viel Erfolg bei deiner Forschung! 🔬

---

**Letzte Aktualisierung**: 2025-12-08 | **Version**: 1.0.0 | **Sprache**: Deutsch 🇩🇪 | **Project Root**: `scientific_research`

Entwickelt mit ❤️ für wissenschaftliche Forschung