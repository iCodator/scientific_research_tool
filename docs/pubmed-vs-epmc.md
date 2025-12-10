# PubMed vs. Europe PMC - Vollständiger Syntax-Vergleich

## Schnellreferenz

| Aufgabe | PubMed | Europe PMC |
|---------|--------|-----------|
| **Einfache Suche** | `cancer` | `cancer` |
| **Phrase** | `"kidney allograft"` | `"kidney allograft"` |
| **AND** | `cancer AND therapy` | `cancer AND therapy` |
| **OR** | `cancer OR tumor` | `cancer OR tumor` |
| **NOT** | `cancer NOT mouse` | `cancer NOT mouse` |
| **Jahresbereich** | `2015:2020[pdat]` | `PUB_YEAR:(2015-2020)` |
| **Einzelnes Jahr** | `2020[pdat]` | `PUB_YEAR:2020` |
| **Titel-Suche** | `cancer[ti]` | `TITLE:cancer` |
| **Autor-Suche** | `smith j[au]` | `AUTH:smith j` |
| **Journal-Suche** | `Nature[ta]` | `JOURNAL:Nature` |
| **Wildcard** | `diabet*` | `diabet*` |
| **Proximity** | `"cancer therapy"[tiab:~5]` | `"cancer therapy"~5` |
| **MeSH-Terms** | `asthma[mh]` | Limited |

---

## Detaillierter Vergleich

### 1. Datumsformate

#### PubMed

**Einfaches Jahr:**
```
cancer AND 2020[pdat]
```

**Jahresbereich:**
```
cancer AND 2015:2020[pdat]
→ Doppelpunkt (:) als Separator
```

**Spezifisches Datum:**
```
cancer AND 2020/06/15[pdat]
→ Format: YYYY/MM/DD
```

**Relative Daten:**
```
cancer AND "last 60 days"[edat]
```

#### Europe PMC

**Einfaches Jahr:**
```
cancer AND PUB_YEAR:2020
```

**Jahresbereich:**
```
cancer AND PUB_YEAR:(2015-2020)
→ Bindestrich (-) als Separator
→ Runde Klammern erforderlich
```

**Spezifisches Datum:**
```
cancer AND FIRST_PDATE:[2020-01-01 TO 2020-12-31]
→ Format: YYYY-MM-DD
→ 'TO' als Range-Operator
→ ECKIGE Klammern
```

---

### 2. Feldformate

#### PubMed: `term[tag]`

```
cancer[ti]                    (Title)
smith j[au]                   (Author)
Nature[ta]                    (Journal)
asthma[mh]                    (MeSH)
2020[pdat]                    (Publication Year)
diabetes[tiab]                (Title/Abstract)
```

**Besonderheiten:**
- Kein Leerzeichen zwischen Term und Tag
- Case-insensitive
- Tags deaktivieren Automatic Term Mapping (ATM)

#### Europe PMC: `FIELDNAME:value`

```
TITLE:cancer                  (Title)
AUTH:smith j                  (Author)
JOURNAL:Nature                (Journal)
ESSN:1234-5678               (Electronic ISSN)
PUB_YEAR:2020                (Publication Year)
SRC:MED                       (Source: PubMed/MEDLINE)
OPEN_ACCESS:Y                 (Open Access nur)
```

**Besonderheiten:**
- Feldnamen sind CASE-SENSITIVE
- Kein Leerzeichen vor Doppelpunkt
- Feldnamen müssen genau bekannt sein

---

### 3. Autor-Suche

#### PubMed

```
smith j[au]                   (Nachname + Initial)
smith ja[au]                  (Nachname + Initials)
julia s wong[au]              (Vorname + Nachname)
smith j[1au]                  (First Author)
smith j[lastau]               (Last Author)
"smith j"[au]                 (Exakt - keine Trunkation)
```

#### Europe PMC

```
AUTH:smith
AUTH:smith j
AUTH:"smith j"                (Exakt)
AUTH:"smith ja"
```

---

### 4. Journal-Suche

#### PubMed

```
Nature[ta]                    (Journal Name)
mol biol cell[ta]             (Abkürzung)
1059-1524[ta]                 (ISSN)
```

#### Europe PMC

```
JOURNAL:Nature
JOURNAL:"The Lancet"
ISSN:1234-5678
ESSN:1234-5678                (Electronic ISSN)
```

---

### 5. Wildcard-Suche

#### PubMed

```
diabet*                       (Min. 4 Zeichen vor *)
vaccin* schedul*              (Multiple Wildcards)
"breast feed*"                (In Phrasen)
```

**Limitierungen:**
- Nicht am Wortanfang: `❌ *betes`
- Minimum 4 Zeichen: `❌ dia*`
- Max 600 Expansionen

#### Europe PMC

```
diabet*                       (Min. 3 Zeichen vor *)
vaccin* schedul*              (Multiple Wildcards)
```

**Limitierungen:**
- Nicht am Wortanfang
- Minimum 3 Zeichen

---

### 6. Proximity-Suche

#### PubMed

```
"asthma treatment"[Title:~3]
"patient physician relationship"[tiab:~0]
```

**Format:** `"term1 term2"[field:~N]`
**N=0:** Direkt nebeneinander
**Verfügbare Felder:** Title [ti], Title/Abstract [tiab], Affiliation [ad]

#### Europe PMC

```
"asthma treatment"~5
```

**Format:** `"term1 term2"~N`
**Keine Feldangabe möglich**

---

### 7. MeSH-Begriffe

#### PubMed (Vollständig unterstützt)

```
asthma[mh]                    (Mit Explosion - alle Unterterme)
asthma[majr]                  (Haupt-MeSH-Begriffe)
asthma[mh:noexp]              (Kein Explosion)
diabetes[mh]/drug therapy     (Mit Subheading)
```

#### Europe PMC (Begrenzt)

```
asthma                        (Automatische Zuordnung)
```

**Hinweis:** Europe PMC hat nicht die volle MeSH-Integration wie PubMed

---

### 8. Publication Type

#### PubMed

```
review[pt]
"systematic review"[pt]
"clinical trial"[pt]
case report[pt]
editorial[pt]
```

Oder mit Subset:
```
systematic[sb]                (Systematic Review + Search-Strategie)
```

#### Europe PMC

```
Limitierte Publication Type Filter
(über OPEN_ACCESS, HAS_ABSTRACT, etc.)
```

---

### 9. Komplexe Queries

#### PubMed

```
(diabetes OR "glucose intolerance") AND (exercise OR "physical activity") 
AND systematic[sb] AND 2015:2025[pdat]
```

**Parsing:** Left-to-right mit Klammer-Priorität

#### Europe PMC

```
(diabetes OR "glucose intolerance") AND (exercise OR "physical activity") 
AND PUB_YEAR:(2015-2025)
```

**Parsing:** Left-to-right mit Klammer-Priorität

---

## Konvertierungs-Checkliste

### Wenn Sie PubMed-Query zu Europe PMC konvertieren:

- [ ] **Datumsformat:** `YYYY:YYYY[pdat]` → `PUB_YEAR:(YYYY-YYYY)`
- [ ] **Feldformat:** `term[tag]` → `FIELD:term`
- [ ] **Anführungszeichen:** Bleiben gleich (doppelte)
- [ ] **Operatoren:** Bleiben gleich (AND, OR, NOT)
- [ ] **Wildcard:** Gleich (aber nur min. 3 Zeichen nötig)
- [ ] **Proximity:** `[field:~N]` → `~N` (ohne Feldangabe)
- [ ] **MeSH:** Vollständige MeSH-Queries können nicht konvertiert werden

---

### Wenn Sie Europe PMC-Query zu PubMed konvertieren:

- [ ] **Datumsformat:** `PUB_YEAR:(YYYY-YYYY)` → `YYYY:YYYY[pdat]`
- [ ] **Feldformat:** `FIELD:term` → `term[tag]`
  - `TITLE:cancer` → `cancer[ti]`
  - `AUTH:smith` → `smith[au]`
  - `JOURNAL:Nature` → `Nature[ta]`
- [ ] **Anführungszeichen:** Bleiben gleich
- [ ] **Operatoren:** Bleiben gleich
- [ ] **Proximity:** `~N` → `[tiab:~N]` (Feldangabe hinzufügen)
- [ ] **Spezielle Filter:** `SRC:MED` → Keine direkte Äquivalenz

---

## Praktische Beispiele

### Beispiel 1: Einfache Suche

**Szenario:** Suche nach "Koenzym Q10" und verwandten Themen aus den Jahren 2020-2025

**PubMed:**
```
("Coenzyme Q10" OR ubiquinone) AND 2020:2025[pdat]
```

**Europe PMC:**
```
("Coenzyme Q10" OR ubiquinone) AND PUB_YEAR:(2020-2025)
```

---

### Beispiel 2: Autor + Spezifisches Feld

**Szenario:** Artikel von Smith, J. in Nature über Mitochondrien

**PubMed:**
```
smith j[1au] AND mitochondria AND Nature[ta]
```

**Europe PMC:**
```
AUTH:smith AND mitochondria AND JOURNAL:Nature
```

---

### Beispiel 3: Systematic Review mit Datum

**Szenario:** Systematic Reviews über Diabetes von 2015-2025

**PubMed:**
```
diabetes AND systematic[sb] AND 2015:2025[pdat]
```

**Europe PMC:**
```
diabetes AND PUB_YEAR:(2015-2025)
(Kein Systematic Review Filter verfügbar)
```

---

### Beispiel 4: Proximity + Exclusion

**Szenario:** "Patient physician relationship" aber nicht bei Tieren

**PubMed:**
```
"patient physician relationship"[tiab:~0] NOT animal[mh]
```

**Europe PMC:**
```
"patient physician relationship"~0 NOT animal
```

---

## Wichtige Unterschiede in der Philosophie

### PubMed

✅ **Automatic Term Mapping (ATM)**
- Intelligente Synonymfindung
- MeSH-Integration
- Flexiblere Suche

✅ **Einfache Anfragen funktionieren auch ohne Syntax**
```
cancer              (Findet auch "carcinoma", "tumor")
```

✅ **Rich Field Support**
- MeSH Major Topics
- Publication Types
- Entry Date, MeSH Date, etc.

### Europe PMC

✅ **Explizite Query-Struktur**
- Keine "versteckte" Synonymfindung
- Was Sie sehen ist was Sie bekommen

✅ **Multi-Database Support**
- PubMed, PMC, Preprints, Patents, etc.
- Filter nach Quelle möglich

✅ **Open Access fokussiert**
- OPEN_ACCESS Filter
- FREE_FULLTEXT Filter

---

## Query-Compiler Adapter (Pseudocode)

```python
# Konvertierung PubMed → Europe PMC
def pubmed_to_europepmc(query):
    # Datumsformat
    query = re.sub(r'(\d{4}):(\d{4})\[pdat\]', 
                   r'PUB_YEAR:(\1-\2)', query)
    
    # Feldtags
    query = query.replace('[ti]', ' mit TITLE:')
    query = query.replace('[au]', ' mit AUTH:')
    query = query.replace('[ta]', ' mit JOURNAL:')
    
    # Proximity (vereinfacht)
    query = re.sub(r'\[tiab:~(\d+)\]', r'~\1', query)
    
    return query
```

---

## Troubleshooting

| Problem | PubMed | Europe PMC |
|---------|--------|-----------|
| Zu viele Ergebnisse | Nutze [majr] statt [mh] | Füge spezifische Feldtags hinzu |
| Zu wenig Ergebnisse | Entferne Anführungszeichen für ATM | Nutze Wildcard * |
| Synonym nicht gefunden | Nutze einfache Suche für ATM | Explizit alle Varianten eingeben |
| Datum funktioniert nicht | Nutze [pdat] statt [dp] | Nutze PUB_YEAR:(YYYY-YYYY) |

