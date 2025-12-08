# Scientific Research Tool

English version: [README.md](README.md)

Ein Python-Tool zur Durchsuchung großer wissenschaftlicher Datenbanken (PubMed, Europe PMC, Cochrane) mit **strukturierten Suchanfragen**.

## 🎯 Was ist dieses Tool?

Stellt dir vor, du möchtest wissenschaftliche Artikel zum Thema "Cancer Immunotherapy" finden. Anstatt auf der PubMed-Website zu suchen, kannst du mit diesem Tool eine **strukturierte Abfrage** schreiben:

```bash
python main.py --query "(cancer OR tumor) AND (immunotherapy OR immune checkpoint)" --limit 100 --output results.csv
```

Das Tool:
- ✅ Durchsucht PubMed, Europe PMC und Cochrane
- ✅ Validiert deine Query automatisch
- ✅ Exportiert Ergebnisse in CSV oder JSON
- ✅ Speichert alle Suchen in Logs

## 🚀 Schnelleinstieg (5 Minuten)

### 1. Installation

```bash
# Repository klonen
git clone https://github.com/yourusername/scientific-research-tool.git
cd scientific-research-tool

# Virtuelle Umgebung
python3 -m venv venv
source venv/bin/activate  # oder: venv\Scripts\activate (Windows)

# Dependencies
pip install -r requirements.txt
```

### 2. Erste Suche

```bash
# Einfache Test-Query
python main.py --query "cancer AND therapy" --source pubmed --limit 10

# Mit Export
python main.py --query "cancer AND therapy" --source pubmed --limit 50 --output results.csv
```

### 3. Query aus Datei

```bash
# Erstelle eine Query-Datei
echo "(cancer OR tumor) AND (immunotherapy OR immune)" > my_query.txt

# Führe Suche durch
python main.py --query-file my_query.txt --source pubmed --output results.json
```

## 📚 Dokumentation

- **[README.md](README.md)** - Ausführliche Dokumentation (Features, Fehlerbehandlung)
- **[INSTALL.md](INSTALL.md)** - Detaillierte Installationsanleitung für alle Systeme
- **[QUERIES.md](QUERIES.md)** - Query-Syntax Referenz mit vielen Beispielen

## 🔧 Query-Syntax

### Erlaubte Formate ✅

```bash
# Einfache Suche
cancer AND therapy

# Mit OR
(cancer OR tumor) AND therapy

# Mit NOT
cancer AND NOT animal

# Mehrwort-Begriffe
"Coenzym Q10" AND mitochondria

# Komplexe Kombinationen
((cancer OR carcinoma) AND (therapy OR treatment)) NOT animal

# Mit PubMed Field-Tags
cancer[TitleAbstract] AND 2020:2025[pdat]

# Europe PMC Syntax
TITLE_ABSTRACT:cancer AND PUBYEAR:2020-2025
```

### NICHT erlaubte Formate ❌

```
# Natürlichsprachige Fragen
"Welche Rolle spielt Coenzym Q10?"

# Aussagesätze
"Auswirkungen von Akupunktur auf Rückenschmerzen"

# Vergleiche
"Ist Therapie A erfolgreicher als Therapie B?"
```

## 📖 Verwendungsbeispiele

### Beispiel 1: Einfache Suche

```bash
python main.py \
  --query "cancer" \
  --source pubmed \
  --limit 25
```

### Beispiel 2: Mit Export

```bash
python main.py \
  --query "(cancer OR tumor) AND therapy" \
  --source pubmed \
  --limit 100 \
  --output cancer_therapy_results.csv
```

### Beispiel 3: Komplexe Query

```bash
python main.py \
  --query "((female OR woman) AND (masturbation OR self-stimulation)) NOT animal" \
  --source pubmed \
  --limit 50 \
  --output female_sexuality_study.json \
  --verbose
```

### Beispiel 4: PubMed Field-Tags

```bash
python main.py \
  --query "cancer[TitleAbstract] AND immunotherapy[TitleAbstract] AND 2023:2025[pdat]" \
  --source pubmed \
  --limit 200 \
  --output recent_cancer_immunotherapy.csv
```

### Beispiel 5: Europe PMC durchsuchen

```bash
python main.py \
  --query "TITLE_ABSTRACT:(covid OR coronavirus) AND PUBYEAR:2020-2025 AND ISOPENACCESSY:Y" \
  --source europepmc \
  --limit 100 \
  --output open_access_covid.csv
```

## 📊 Output-Format

### CSV-Export (Standard)

Öffnet in: Excel, Google Sheets, LibreOffice, Python

```csv
title,authors,year,journal,url,abstract
"Cancer Immunotherapy","Smith J, Jones A",2024,"Nature","https://...",
"Mechanism of Tumor","Brown B",2023,"Cell","https://...",...
```

### JSON-Export

Öffnet in: VS Code, Online JSON Viewer, Python

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

## 🛠️ Befehle

```bash
# Hilfe anzeigen
python main.py --help

# Einfache Suche
python main.py --query "cancer" --source pubmed

# Mit Datei
python main.py --query-file queries/my_search.txt --source pubmed

# Mit Export
python main.py --query "cancer" --source pubmed --output results.csv

# Debug-Modus
python main.py --query "cancer" --source pubmed --verbose

# Maximale Anzahl Ergebnisse
python main.py --query "cancer" --source pubmed --limit 1000
```

## 🗄️ Unterstützte Datenbanken

| Datenbank | Quelle | Größe | Syntax |
|-----------|--------|-------|--------|
| **PubMed** | NCBI (USA) | 34M+ Artikel | [NCBI Query](https://www.ncbi.nlm.nih.gov/books/NBK3827/) |
| **Europe PMC** | EBI (Europa) | 42M+ Artikel | [Europe PMC](https://europepmc.org/api) |
| **Cochrane** | Cochrane Org | Systematische Reviews | [Cochrane API](https://data.cochrane.org/) |

## ❓ Häufig gestellte Fragen

### Kann ich natürlichsprachige Fragen stellen?

**Nein.** Das Tool akzeptiert nur **strukturierte Queries** mit AND, OR, NOT Operatoren. Das schützt die Qualität und Konsistenz der Suchergebnisse.

### Wie viele Artikel kann ich maximal downloaden?

Das hängt von der Datenbank ab:
- **PubMed**: Bis zu 100.000 über API
- **Europe PMC**: Bis zu 1.000 Standard, mehr mit API Key
- **Cochrane**: Bis zu 10.000

### Muss ich API-Keys konfigurieren?

**Nein.** Das Tool funktioniert auch ohne API-Keys, aber:
- Suchen sind langsamer
- Du erreichst schneller die Rate Limits
- Manche erweiterten Features sind nicht verfügbar

### Kann ich meine Suchen zeitplanen?

Aktuell nicht, aber du kannst mit `cron` (Linux/macOS) oder Task Scheduler (Windows) automatisieren:

```bash
# Linux/macOS - Täglich um 8 Uhr suchen
0 8 * * * /home/user/scientific-research-tool/venv/bin/python /home/user/scientific-research-tool/main.py --query-file /home/user/queries/daily_search.txt --output /home/user/results/daily_$(date +\%Y\%m\%d).csv
```

## 🐛 Fehlerbehandlung

### "Query-Validierung fehlgeschlagen"

**Problem**: Deine Query ist nicht strukturiert

```
❌ "Welche Rolle spielt Coenzym Q10?"
```

**Lösung**: Nutze AND, OR, NOT Operatoren

```
✅ "Coenzym Q10 AND role"
```

### "Keine Ergebnisse gefunden"

**Problem**: Die Query liefert keine Treffer

**Lösungen**:
1. Vereinfache die Query (zu viele AND-Bedingungen)
2. Nutze Synonyme: `(cancer OR carcinoma OR tumor)`
3. Überprüfe die Schreibweise
4. Setze ein größeres `--limit`

### "Connection timeout"

**Problem**: Datenbank antwortet nicht

**Lösungen**:
```bash
# Versuche es später nochmal
sleep 300 && python main.py --query "cancer" --source pubmed

# Oder nutze einen API-Key für höhere Limits
```

## 📝 Logs

Alle Suchen werden automatisch geloggt:

```bash
# Letzte Suche anschauen
tail -f logs/search_*.log

# Alle Logs der heutigen Suche
cat logs/search_2025-12-08.log | grep cancer
```

## 🔐 Sicherheit

- **API-Keys**: Bitte in `config.env` speichern (wird automatisch ignoriert)
- **Daten**: Alle Suchen sind lokal und privat
- **Abhängigkeiten**: Nur sichere, weit verbreitete Pakete

## 📄 Lizenz

MIT License - siehe [LICENSE](LICENSE)

## 🤝 Beiträge

Beiträge sind willkommen! Bitte:

1. Fork das Repository
2. Feature-Branch erstellen: `git checkout -b feature/neue-funktion`
3. Changes committen: `git commit -am "Feature hinzugefügt"`
4. Push: `git push origin feature/neue-funktion`
5. Pull Request erstellen

## 📞 Support

- **GitHub Issues**: https://github.com/yourusername/scientific-research-tool/issues
- **Diskussionen**: https://github.com/yourusername/scientific-research-tool/discussions
- **Email**: support@example.com

## 🙏 Credits

Entwickelt von: [Your Name](https://github.com/yourusername)

Datenquellen:
- [NCBI PubMed](https://pubmed.ncbi.nlm.nih.gov/)
- [Europe PMC](https://europepmc.org/)
- [Cochrane Library](https://www.cochranelibrary.com/)

---

**Letzte Aktualisierung**: 2025-12-08 | **Version**: 1.0.0
