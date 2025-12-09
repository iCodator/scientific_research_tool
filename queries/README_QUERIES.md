# 📂 Abfrage-Bibliothek (Query Files)

In diesem Ordner kannst du deine komplexen Suchanfragen als Textdateien speichern. 
Das hat den Vorteil, dass du komplizierte Logik (viele Klammern, OR/AND Verknüpfungen) nicht jedes Mal neu in die Kommandozeile tippen musst.

## 📝 Wie erstelle ich eine Query-Datei?

Erstelle einfach eine `.txt` Datei (z.B. `meine_suche.txt`) und schreibe deine Suchanfrage hinein.

**Regeln:**
- Keine Anführungszeichen um die gesamte Query nötig.
- Zeilenumbrüche sind erlaubt (werden vom Tool automatisch zu Leerzeichen umgewandelt).
- Kommentare sind (noch) nicht unterstützt, nur die reine Query.
- **Nutze die korrekte Syntax für deine Zieldatenbank** (siehe unten).

## 🚀 Wie nutze ich die Dateien?

Nutze das Flag `--query-file` (oder `-qf` falls implementiert) beim Starten des Tools:

```bash
# Aus dem Hauptverzeichnis des Projekts:
python main.py --query-file queries/cancer_immunotherapy.txt --source pubmed
```

---

## 🗂 Datenbank-spezifische Syntax

**WICHTIG**: Die Query-Syntax unterscheidet sich je nach Datenbank. Wähle das richtige Format!

### PubMed Queries

Nutze **PubMed Field-Tags** in `[...]` Format:

**Beispiel-Datei: `queries/pubmed/cancer_immunotherapy.txt`**
```text
((cancer OR tumor OR neoplasm) 
 AND 
 (immunotherapy OR "immune checkpoint inhibitor")) 
 AND 
 (2023:2025[pdat]))
```

**Häufige Tags:**
- `[TitleAbstract]` - Nur Titel/Abstract
- `[Title]` - Nur Titel
- `[pdat]` - Publikationsdatum (Format: `YYYY:YYYY`)
- `[Author]` - Autor
- `[Journal]` - Journalname
- `[MeSH Terms]` - MeSH-Deskriptoren

**Weitere Beispiele:**

`queries/pubmed/covid_vaccines.txt`:
```text
(COVID-19[Title] OR coronavirus[Title]) 
AND 
(vaccine* OR vaccination)
AND
(2020:2025[pdat])
```

---

### Europe PMC Queries

Nutze **Europe PMC Field-Format**: `FIELD:value`

**Beispiel-Datei: `queries/europepmc/covid_open_access.txt`**
```text
((covid OR coronavirus) 
 AND 
 (vaccine OR vaccination)) 
 AND 
 PUBYEAR:2020-2025 
 AND 
 ISOPENACCESSY:Y
```

**Häufige Fields:**
- `TITLE_ABSTRACT:` - Titel & Abstract
- `TITLE:` - Nur Titel
- `ABSTRACT:` - Nur Abstract
- `PUBYEAR:` - Publikationsjahr (Format: `YYYY-YYYY`)
- `AUTH:` - Autor
- `JOURNAL:` - Journalname
- `ISOPENACCESSY:Y` - Nur Open Access

**Weitere Beispiele:**

`queries/europepmc/diabetes_treatment.txt`:
```text
TITLE_ABSTRACT:(diabetes OR glucose intolerance)
AND
TITLE_ABSTRACT:(exercise OR physical activity)
AND
PUBYEAR:2021-2025
AND
ISOPENACCESSY:Y
```

---

### Cochrane Queries

**Wichtig:** Cochrane akzeptiert **KEINE Field-Tags** wie `[pdat]` oder `PUBYEAR:`.
Nutze normale **AND/OR/NOT Syntax** ohne spezielle Formatierung.

**Beispiel-Datei: `queries/cochrane/cancer_treatment.txt`**
```text
(cancer OR tumor OR malignancy) 
AND 
(immunotherapy OR checkpoint inhibitor)
```

**Hinweise zu Cochrane:**
- Keine Field-Tags (`[TitleAbstract]`, `PUBYEAR:` funktionieren nicht)
- Normale AND/OR/NOT Operatoren verwenden
- Automatische Filterung auf Systematic Reviews
- Keine Datumfilterung über Query-Syntax (wird ignoriert)

**Weitere Beispiele:**

`queries/cochrane/diabetes_exercise.txt`:
```text
(diabetes OR glucose intolerance)
AND
(exercise OR physical activity OR fitness)
AND
(intervention OR treatment)
```

`queries/cochrane/heart_disease_therapy.txt`:
```text
((heart disease OR cardiac disease OR cardiovascular disease)
 AND
 (drug therapy OR pharmacological treatment OR medication))
NOT
animal
```

---

## 🗂 Empfohlene Verzeichnis-Struktur

Organisiere deine Queries nach Datenbank:

```
queries/
├── pubmed/
│   ├── cancer_immunotherapy.txt
│   ├── covid_vaccines.txt
│   └── README.md (für deine Notizen)
│
├── europepmc/
│   ├── covid_open_access.txt
│   ├── diabetes_treatment.txt
│   └── README.md
│
├── cochrane/
│   ├── cancer_treatment.txt
│   ├── diabetes_exercise.txt
│   └── README.md
│
└── temp/
    └── experimental_queries.txt
```

---

## 💡 Tipps & Tricks

### 1. Query-Komplexität schrittweise aufbauen

Starte einfach, erweitere dann:

`queries/pubmed/simple.txt`:
```text
cancer
```

Dann erweitern zu:
```text
cancer AND immunotherapy
```

Dann zu:
```text
(cancer OR tumor) AND (immunotherapy OR checkpoint)
```

### 2. Multi-Zeilen Queries für bessere Lesbarkeit

Statt:
```text
(cancer OR tumor) AND (immunotherapy OR checkpoint) AND (2023:2025[pdat]) AND NOT animal
```

Besser:
```text
(cancer OR tumor)
AND
(immunotherapy OR checkpoint)
AND
(2023:2025[pdat])
AND
NOT animal
```

Das Tool konvertiert Zeilenumbrüche automatisch zu Leerzeichen!

### 3. Verwende aussagekräftige Dateinamen

❌ `q1.txt`, `query_old.txt`
✅ `cancer_immunotherapy_2023_2025.txt`, `covid_vaccines_pubmed.txt`

### 4. Speichere erfolgreiche Queries

Wenn eine Query gute Ergebnisse liefert, speicher sie ab für später:

```bash
# Suche mit Export
python main.py --query-file queries/pubmed/cancer_immunotherapy.txt \
  --source pubmed \
  --output results_2025-12-09.csv

# Speichern mit Datum
cp queries/pubmed/cancer_immunotherapy.txt \
   queries/pubmed/archived/cancer_immunotherapy_2025-12-09.txt
```

---

## 🔍 Fehlerbehandlung

### Fehler: "Query validation failed"

**Grund:** Query-Syntax falsch für diese Datenbank.

**Lösung:**
1. Überprüfe, welche Datenbank du nutzt (`--source pubmed` vs `--source europepmc` vs `--source cochrane`)
2. Überprüfe die korrekte Syntax oben
3. Besonders: Field-Tags (`[pdat]`) sind nur für PubMed, nicht für Cochrane!

### Beispiel - Falsch/Richtig:

❌ **FALSCH für Cochrane** (PubMed Syntax):
```text
cancer[TitleAbstract] AND 2023:2025[pdat]
```

✅ **RICHTIG für Cochrane**:
```text
cancer AND therapy
```

✅ **RICHTIG für PubMed**:
```text
cancer[TitleAbstract] AND 2023:2025[pdat]
```

---

## 📚 Weitere Ressourcen

- **[QUERIES.md](../QUERIES.md)** - Vollständige Syntax-Referenz mit detaillierten Beispielen
- **[README.md](../README.md)** - Hauptdokumentation
- **PubMed Help**: https://www.ncbi.nlm.nih.gov/books/NBK3827/
- **Europe PMC API**: https://europepmc.org/api
- **Cochrane Suche**: https://www.cochrane.org/

---

**💡 Tipp**: Speichere deine häufigsten Queries hier ab und verwende sie immer wieder! Macht alles etwas einfacher!
