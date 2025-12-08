# Query-Syntax Referenz 📋

Detaillierte Anleitung für die richtige Query-Syntax.

## Grundkonzepte

Das Tool akzeptiert **strukturierte Queries** mit logischen Operatoren.

### Die 3 Basis-Operatoren

| Operator | Bedeutung | Beispiel |
|----------|-----------|----------|
| **AND** | Alle Begriffe müssen vorkommen | `cancer AND therapy` |
| **OR** | Mindestens einer der Begriffe | `cancer OR tumor` |
| **NOT** | Schließt einen Begriff aus | `cancer AND NOT animal` |

## Syntax-Regeln

### 1. Klammern für Gruppen

Nutze Klammern um mehrere Begriffe zu gruppieren:

```
✅ (cancer OR tumor) AND (therapy OR treatment)
❌ cancer OR tumor AND therapy (mehrdeutig - keine Klammern)
```

Warum Klammern wichtig sind:
- `(A OR B) AND C` = (A AND C) ODER (B AND C)
- `A OR (B AND C)` = A ODER (B AND C)

### 2. Mehrwort-Begriffe

Mehrwort-Begriffe können mit oder ohne Anführungszeichen verwendet werden:

```
✅ Coenzym Q10 AND mitochondria
✅ "Coenzym Q10" AND mitochondria
✅ "covid 19" OR coronavirus
✅ covid 19 OR coronavirus
```

### 3. Groß-/Kleinschreibung

Die meisten Datenbanken sind **case-insensitive** (ignorieren Groß-/Kleinschreibung):

```
✅ cancer AND THERAPY
✅ Cancer AND Therapy
✅ CANCER AND THERAPY
(Alle sind äquivalent)
```

### 4. Spezial-Zeichen

Nur diese Zeichen sind erlaubt:

```
Erlaubt:
  - Buchstaben (a-z, A-Z)
  - Zahlen (0-9)
  - Leerzeichen
  - Klammern: ( )
  - Anführungszeichen: " "
  - Bindestrich: - (in Begriffen wie "self-stimulation")
  - Sternchen: * (Wildcard, optional)

Nicht erlaubt:
  - Fragezeichen: ?
  - Ausrufezeichen: !
  - Kommas: , (außer in Listen)
  - Punkte: . (außer als Dezimalzahl)
```

## Query-Beispiele

### Einfache Queries

```bash
# Ein Begriff
python main.py --query "cancer" --source pubmed

# Zwei Begriffe
python main.py --query "cancer therapy" --source pubmed
# (wird als "cancer AND therapy" interpretiert)
```

### AND-Operationen

```bash
# Alle Begriffe müssen vorkommen
python main.py --query "cancer AND therapy AND 2023" --source pubmed

# Mit Klammern
python main.py --query "cancer AND (surgery OR chemotherapy)" --source pubmed
```

### OR-Operationen

```bash
# Mindestens einer der Begriffe
python main.py --query "cancer OR carcinoma OR malignancy" --source pubmed

# Synonym-Suche
python main.py --query "(masturbation OR self-stimulation)" --source pubmed
```

### NOT-Operationen

```bash
# Schließt Begriffe aus
python main.py --query "cancer AND NOT animal" --source pubmed

# Mehrfach ausschließen
python main.py --query "cancer AND NOT animal AND NOT in-vitro" --source pubmed
```

### Komplexe Kombinationen

```bash
# Multiple Gruppen
python main.py --query "(cancer OR tumor) AND (therapy OR treatment) AND NOT animal" --source pubmed

# Mit Mehrwort-Begriffen
python main.py --query "(Coenzym Q10 OR ubiquinone) AND (heart disease OR cardiac)" --source pubmed

# Verschachtelte Gruppen
python main.py --query "((female OR woman) AND (masturbation OR self-stimulation)) AND NOT animal" --source pubmed
```

## PubMed Field-Syntax

PubMed akzeptiert optionale **Field-Tags** für präzisere Suche:

### Häufig verwendete Tags

| Tag | Bedeutung | Beispiel |
|-----|-----------|----------|
| `[TitleAbstract]` | Nur in Titel/Abstract | `cancer[TitleAbstract]` |
| `[Title]` | Nur im Titel | `cancer[Title]` |
| `[Abstract]` | Nur im Abstract | `cancer[Abstract]` |
| `[Author]` | Autorenname | `Smith[Author]` |
| `[Journal]` | Journalname | `Nature[Journal]` |
| `[pdat]` | Publikationsdatum | `2020:2025[pdat]` |
| `[MeSH Terms]` | MeSH-Deskriptoren | `cancer[MeSH Terms]` |

### Beispiele mit Tags

```bash
# Nur im Titel/Abstract
python main.py --query "cancer[TitleAbstract] AND therapy[TitleAbstract]" --source pubmed

# Mit Datumbereich
python main.py --query "cancer AND 2020:2025[pdat]" --source pubmed

# Mit Autor
python main.py --query "Smith[Author] AND cancer" --source pubmed

# Mit Journal
python main.py --query "Nature[Journal] AND cancer" --source pubmed

# Mit MeSH-Terms
python main.py --query "cancer[MeSH Terms]" --source pubmed
```

## Europe PMC Syntax

Europe PMC nutzt eine andere Syntax als PubMed:

### Field-Format

```
FIELD:value
```

### Häufige Fields

| Field | Beispiel |
|-------|----------|
| `TITLE_ABSTRACT` | `TITLE_ABSTRACT:cancer` |
| `TITLE` | `TITLE:cancer` |
| `ABSTRACT` | `ABSTRACT:cancer` |
| `AUTH` | `AUTH:Smith` |
| `JOURNAL` | `JOURNAL:Nature` |
| `PUBYEAR` | `PUBYEAR:2020-2025` |
| `ISOPENACCESSY` | Open Access nur | `ISOPENACCESSY:Y` |

### Beispiele für Europe PMC

```bash
# Einfache Suche
python main.py --query "cancer AND therapy" --source europepmc

# Mit Fields
python main.py --query "TITLE_ABSTRACT:cancer AND PUBYEAR:2020-2025" --source europepmc

# Mit Autor
python main.py --query "AUTH:Smith AND TITLE_ABSTRACT:cancer" --source europepmc

# Open Access nur
python main.py --query "cancer AND ISOPENACCESSY:Y" --source europepmc

# Kombiniert
python main.py --query "TITLE_ABSTRACT:(covid OR coronavirus) AND PUBYEAR:2020-2025 AND ISOPENACCESSY:Y" --source europepmc
```

## Wildcards (Optional)

Manche Datenbanken unterstützen Wildcards für Wort-Varianten:

| Wildcard | Bedeutung | Beispiel |
|----------|-----------|----------|
| `*` | 0 oder mehr Zeichen | `carcinom*` (cancer, carcinoma) |
| `?` | Genau 1 Zeichen | `tum?r` (tumor, tumor) |

### Wildcard-Beispiele

```bash
# Catch all Varianten von "cancer"
python main.py --query "cancer* AND therapy" --source pubmed

# Britische/Amerikanische Schreibweise
python main.py --query "(tumour OR tum?r) AND therapy" --source pubmed
```

## Häufige Fehler

### ❌ Falsch

```
query = "Welche Therapien sind am wirksamsten gegen Krebs?"
# → Natürlichsprachige Frage (nicht erlaubt)

query = "cancer"  "therapy"
# → Doppelte Anführungszeichen (nicht erlaubt)

query = (cancer AND therapy
# → Klammern nicht balanciert

query = cancer & therapy
# → & statt AND (nicht erkannt)
```

### ✅ Richtig

```
query = "(cancer OR carcinoma) AND therapy"
# → Klammern, Operatoren korrekt

query = "cancer therapy"
# → Mehrwort-Begriff in Anführungszeichen

query = cancer AND therapy AND 2020:2025[pdat]
# → Mit PubMed Field-Tags

query = (cancer[TitleAbstract]) AND (therapy[TitleAbstract])
# → Vollständig formatiert
```

## Tipps für bessere Suchergebnisse

### 1. Synonyme nutzen

```bash
# Schlechte Suche
python main.py --query "cancer" --source pubmed

# Bessere Suche
python main.py --query "(cancer OR carcinoma OR tumor OR malignancy)" --source pubmed
```

### 2. Englische Begriffe

Wissenschaftliche Datenbanken nutzen meist Englisch:

```bash
# Nicht: Krebs, Geschwulst
# Sondern:
python main.py --query "cancer" --source pubmed

# Nicht: Behandlung, Therapie
# Sondern:
python main.py --query "treatment OR therapy" --source pubmed
```

### 3. Breite vs. enge Suche

```bash
# Breite Suche (viele Ergebnisse)
python main.py --query "cancer" --source pubmed --limit 1000

# Enge Suche (wenige, relevante Ergebnisse)
python main.py --query "(cancer[TitleAbstract]) AND (immunotherapy[TitleAbstract]) AND (human) AND 2023:2025[pdat]" --source pubmed --limit 50
```

### 4. Ausschlüsse für Präzision

```bash
# Schließe unwanted Ergebnisse aus
python main.py --query "cancer AND therapy AND NOT animal AND NOT cell AND NOT in-vitro" --source pubmed
```

## Testing deiner Query

Vor dem großen Export, teste die Query mit kleinem Limit:

```bash
# Test mit 5 Ergebnissen
python main.py \
  --query "deine-query-hier" \
  --source pubmed \
  --limit 5 \
  --verbose

# Wenn Ergebnisse sehen gut aus:
python main.py \
  --query "deine-query-hier" \
  --source pubmed \
  --limit 100 \
  --output results.csv
```

## Weitere Ressourcen

- [PubMed Query Language](https://www.ncbi.nlm.nih.gov/books/NBK3827/)
- [Europe PMC Query Syntax](https://europepmc.org/QueryTipsFAQ)
- [Advanced PubMed Search](https://pubmed.ncbi.nlm.nih.gov/advanced/)
