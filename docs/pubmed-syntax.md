# PubMed Search Syntax - Vollständige Dokumentation

## Übersicht

**PubMed** ist die offizielle Suchmaschine der National Library of Medicine (NLM) für MEDLINE und kostenlos verfügbare Artikel. Im Gegensatz zu Europe PMC nutzt PubMed eine **Automatic Term Mapping (ATM)** Technologie für intelligente Suchergebnisse.

---

## 1. Direkte Suche (Ohne Feldtags)

### Einfache Suchbegriffe

```
cancer
diabetes
malaria
```

**Verhalten:** Automatische Term Mapping (ATM) ist aktiv. PubMed sucht den Begriff in:
- MeSH-Begriffen
- Text in Titel & Abstract
- Autorennamen
- Journal-Namen (wenn relevant)

**Beispiel:**
```
cancer
→ Findet "cancer", "carcinoma", "neoplasm" (Synonyme)
```

---

### Phrasensuche mit Anführungszeichen

```
"kidney allograft"
"systematic review"
"breast cancer"
```

**Wichtig:** Nur **doppelte** Anführungszeichen! Einfache (`'`) funktionieren NICHT!

**Verhalten:**
- Deaktiviert Automatic Term Mapping (ATM)
- Sucht exakte Wortfolge
- Zerlegt Phrase nicht in Einzelteile

**Richtig vs. Falsch:**
| ✅ Richtig | ❌ Falsch |
|-----------|----------|
| `"kidney allograft"` | `'kidney allograft'` |
| `"systematic review"` | `'systematic review'` |

---

## 2. Boolean-Operatoren

**Wichtig:** Alle Operatoren MÜSSEN **großgeschrieben** sein!

### AND (Beide Begriffe nötig)

```
diabetes AND exercise
"kidney allograft" AND transplant
cancer AND 2020[pdat]
```

Artikel müssen ALLE Begriffe enthalten.

---

### OR (Mindestens ein Begriff)

```
cancer OR tumor
diabetes OR "glucose intolerance"
```

Artikel müssen mindestens EINEN der Begriffe enthalten.

---

### NOT (Ausschluss)

```
cancer NOT mouse
diabetes NOT animal study
```

Schließt Artikel mit dem Term aus.

---

## 3. Klammern und Priorisierung

```
(diabetes OR "metabolic syndrome") AND exercise
(cancer OR tumor) AND therapy
```

**Wichtig:** Klammern müssen balanciert sein!

---

## 4. Wildcard-Suche (Trunkierung)

**Symbol:** `*` (Asterisk)

**Regeln:**
- Minimum **4 Zeichen** vor dem Wildcard
- Verursacht maximal **600 Expansionen**
- Deaktiviert Automatic Term Mapping
- **Nicht** am Wortanfang möglich

**Beispiele:**

| Query | Matches |
|-------|---------|
| `diabet*` | diabetes, diabetic, diabetics |
| `carcino*` | carcinoma, carcinogenic, carcinogenesis |
| `vaccin* schedul*` | vaccine schedule, vaccination schedules |
| `tumo*r associated macrophage*` | tumor/tumour + associated + macrophage/macrophages |

**Falsch:**
```
❌ dia*       (zu kurz! braucht min. 4 Zeichen)
❌ *betes     (Wildcard nicht am Anfang)
```

---

## 5. Proximity-Suche

**Syntax:** `"term1 term2"[field:~N]`

**Bedeutung:** Beide Terme erscheinen maximal N Wörter voneinander entfernt (beliebige Reihenfolge)

**Verfügbare Felder:**
- `[Title:~N]` oder `[ti:~N]` - Nur Titel
- `[Title/Abstract:~N]` oder `[tiab:~N]` - Titel oder Abstract
- `[Affiliation:~N]` oder `[ad:~N]` - Affiliationen

**Beispiele:**

```
"asthma treatment"[Title:~3]
→ "asthma treatment", "asthma and treatment", 
→ "asthma-related treatment", etc.

"patient physician relationship"[tiab:~0]
→ Wörter müssen direkt nebeneinander stehen (keine Wörter dazwischen)

"rationing healthcare"[ti:~2]
→ "rationing healthcare", "rationing of healthcare",
→ "healthcare rationing", etc.
```

---

## 6. Hyphenated Phrases (Mit Bindestrich)

```
kidney-allograft
heart-attack
```

**Hinweis:** Falls nicht im Phrase Index, keine Ergebnisse. Mit Anführungszeichen umgehen:
```
"heart-attack"
```

---

## 7. Field Tags (Feldspezifische Suche)

**Format:** `term[tag]`

**Wichtig:** 
- Kein Leerzeichen zwischen Term und Tag!
- Tags deaktivieren Automatic Term Mapping
- Case-insensitive

### Title-Feld

```
cancer[ti]  oder  cancer[title]
"systematic review"[ti]
```

---

### Author-Feld

```
smith j[au]          (Nachname + Initials)
smith ja[au]         (Nachname + alle Initials)
julia s wong[au]     (Vorname + Nachname)
wong julia s[au]     (Nachname + Vorname + Initials)

smith j[1au]         (Erster Autor)
smith j[lastau]      (Letzter Autor)
```

**Hinweise:**
- Keine Punkte nach Initials: `smith ja` (nicht `smith j.a.`)
- Full Author Names nur ab 2002
- Auto-Trunkation (mit `"smith j"[au]` deaktivierbar)

---

### Journal-Feld

```
Nature[ta]
"The Lancet"[ta]
mol biol cell[ta]     (Abkürzung)
1059-1524[ta]         (ISSN)
```

---

### MeSH-Felder

```
asthma[mh]            (Mit Explosion - alle Unterterme)
asthma[majr]          (Nur Haupt-MeSH-Begriffe)
asthma[mh:noexp]      (Nur dieser Term, keine Unterterme)

diabetes[mh]/drug therapy    (Mit Subheading)
cytokines[majr]
```

---

### Title/Abstract-Feld

```
diabetes[tiab]
"kidney disease"[tiab]
```

---

### Text Words-Feld

```
malaria[tw]
```

Sucht in Title, Abstract, MeSH Terms, und weiteren Feldern.

---

### Affiliation-Feld

```
UCLA[ad]
harvard[ad]
```

Mit Proximity möglich: `"harvard department"[ad:~2]`

---

### All Fields

```
cancer[all]
```

---

## 8. Datums-Filter

### Publikationsjahr - Einfach

```
cancer AND 2020[pdat]
```

Nur Jahr 2020.

---

### Publikationsjahr - Bereich

```
diabetes AND 2015:2020[pdat]
```

Jahre 2015 bis 2020 (inklusiv).

**Wichtig:** 
- `:` (Doppelpunkt) zwischen Jahren, **NICHT** `TO` oder `-`
- **KEINE** Klammern um den Bereich

---

### Publikationsdatum - Spezifisch

```
cancer AND 2020/06/15[pdat]
cancer AND 2020/06[pdat]     (Monat optional)
cancer AND 2020[pdat]        (Jahr nur)
```

**Format:** `YYYY/MM/DD` (mit `/`, nicht `-`)

---

### Datumsbereich

```
heart disease AND 2019/01/01:2019/12/01[dp]
```

---

### Relative Daten

```
cancer AND "last 60 days"[edat]
cancer AND "last 5 years"[edat]
```

---

### Datum-Felder (Tags)

| Tag | Bedeutung |
|-----|-----------|
| `[pdat]` | **Publication Date** (Print + Electronic) |
| `[dp]` | **Date of Publication** (alle Publikationsdaten) |
| `[epdat]` | **Electronic Publication Date** |
| `[ppdat]` | **Print Publication Date** |
| `[edat]` | **Entry Date** (PubMed Aufnahmedatum) |
| `[mhda]` | **MeSH Date** (Indexierungsdatum) |

---

## 9. Publication Type Filter

```
cancer AND review[pt]
diabetes AND "clinical trial"[pt]
NOT preprint[pt]
```

**Häufige Publication Types:**
- `review[pt]` - Review
- `systematic[sb]` - Systematic Review
- `clinical trial[pt]`
- `case report[pt]`
- `editorial[pt]`
- `letter[pt]`

---

## 10. Subset Filter

### Systematic Reviews

```
diabetes AND systematic[sb]
```

Nutzt zusätzlich zu Publication Type auch eine Search-Strategie!

---

### MEDLINE

```
cancer AND medline[sb]
```

Nur MEDLINE-indexierte Artikel.

---

### Free Full Text

```
cancer AND free full text[sb]
cancer AND free fulltext[sb]
```

---

### Full Text

```
cancer AND full text[sb]
```

---

### PubMed Central

```
cancer AND "pubmed pmc"[sb]
```

---

### Has Abstract

```
cancer AND hasabstract
```

Kein Field Tag nötig!

---

## 11. Komplexe Queries

### Beispiel 1: Fokussierte Suche

```
(diabetes OR "glucose intolerance") AND (exercise OR "physical activity") 
AND systematic[sb] AND 2015:2025[pdat] AND free full text[sb]
```

---

### Beispiel 2: MeSH + Autor + Datum

```
asthma[mh] AND smith j[1au] AND review[pt] AND 2020:2025[pdat]
```

---

### Beispiel 3: Proximity + Exclusion

```
"patient physician relationship"[tiab:~0] AND NOT preprint[pt]
```

---

## Häufige Fehler

| ❌ Falsch | ✅ Richtig | Problem |
|----------|----------|---------|
| `'kidney allograft'` | `"kidney allograft"` | Einfache statt doppelte Anführungszeichen |
| `cancer and exercise` | `cancer AND exercise` | Operator kleingeschrieben |
| `cancer (2015-2025)[pdat]` | `cancer AND 2015:2025[pdat]` | Falsches Datumsformat |
| `cancer (2015 TO 2025)[pdat]` | `cancer AND 2015:2025[pdat]` | TO statt Doppelpunkt |
| `cancer [ti]` | `cancer[ti]` | Leerzeichen vor Tag |
| `dia*` | `diabet*` | Zu kurzer Term vor Wildcard |
| `*betes` | `diabet*` | Wildcard am Anfang |
| `"cancer therapy"[abstract:~5]` | `"cancer therapy"[tiab:~5]` | Proximity nur in [ti], [tiab], [ad] |

---

## Conversion Table: Allgemein → PubMed

| Format | Allgemein | PubMed | Konvertierung |
|--------|-----------|--------|--------------|
| **Jahr** | 2020 | `2020[pdat]` | Füge [pdat] hinzu |
| **Jahresbereich** | 2015-2020 | `2015:2020[pdat]` | `:` statt `-` |
| **Monat** | 2020-06 | `2020/06[pdat]` | `/` statt `-` |
| **Vollständiges Datum** | 2020-06-15 | `2020/06/15[pdat]` | `/` + [pdat] |
| **Phrase** | title:"kidney disease" | `"kidney disease"[ti]` | `[ti]` statt `title:` |

---

## API-Integration (E-utilities)

### ESearch URL

```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cancer+AND+2020[pdat]&usehistory=y&retmax=100
```

### EFetch URL

```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=19393038&retmode=xml&rettype=abstract
```

---

## Wichtige Unterschiede zu Europe PMC

| Feature | PubMed | Europe PMC |
|---------|--------|-----------|
| **Datumsformat** | `2015:2025[pdat]` | `PUB_YEAR:(2015-2025)` |
| **Feldformat** | `cancer[ti]` | `TITLE:cancer` |
| **Automatic Term Mapping** | ✅ Standard | ❌ Nicht vorhanden |
| **MeSH Support** | ✅ Volles Support | ⚠️ Begrenzt |
| **Wildcards** | Min. 4 Zeichen | Min. 3 Zeichen |
| **Proximity** | `[field:~N]` | `"phrase"~N` |

---

## Weitere Ressourcen

- **PubMed Help:** https://pubmed.ncbi.nlm.nih.gov/help/
- **NCBI E-utilities:** https://www.ncbi.nlm.nih.gov/books/NBK25499/
- **MeSH Browser:** https://www.ncbi.nlm.nih.gov/mesh/
- **PubMed Citation Sensor:** Automatische Erkennung von Autorentiteln, Daten, etc.
