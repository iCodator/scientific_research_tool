# Query Format Guide - USER REGELN

Ein umfassender Guide für die korrekte Formatierung von Suchanfragen (Boolean Queries) für medizinische Datenbanken wie PubMed und Europe PMC.

---

## 📋 Inhaltsverzeichnis

1. [Grundprinzipien](#grundprinzipien)
2. [Die 3 Hauptregeln](#die-3-hauptregeln)
3. [Einzelne Operatoren verstehen](#einzelne-operatoren-verstehen)
4. [Korrekte Query-Struktur](#korrekte-query-struktur)
5. [Häufige Fehler](#häufige-fehler)
6. [Beispiele (Richtig vs. Falsch)](#beispiele-richtig-vs-falsch)
7. [Quick Reference](#quick-reference)

---

## Grundprinzipien

Eine **Boolean Query** kombiniert Suchbegriffe (Terms) mit logischen Operatoren, um präzise Suchergebnisse zu definieren.

### Komponenten einer Query

```
Suchbegriffe (Terms):   CANCER, TUMOR, TREATMENT, PATIENT
Operatoren:              AND, OR, NOT
Klammern:                ( ) zur Gruppierung
```

### Ziel

**Eindeutigkeit:** Deine Query darf nicht mehrdeutig sein. Der Parser muss genau verstehen können, wie deine Begriffe logisch zusammenhängen.

---

## Die 3 Hauptregeln

### RULE 1: Logisch zusammengehörige Gruppen in EINER ZEILE

Eine logische Gruppe besteht aus mehreren Begriffen, die durch **denselben Operator** verbunden sind und zusammen eine Bedeutungseinheit bilden.

**Beispiel:** Synonyme mit OR verbunden
- `CANCER OR TUMOR` ist eine Gruppe (Synonyme)
- Sie gehören zusammen und sollten in EINER ZEILE stehen

#### ✅ RICHTIG

```
CANCER OR TUMOR
```
- Output: `((CANCER) OR (TUMOR))`

#### ❌ FALSCH

```
CANCER
OR
TUMOR
```
- **Fehler:** Die OR-Gruppe wurde zerlegt!
- **Fehlermeldung:** "Logische Gruppen müssen in einer Zeile stehen oder geklammert werden"

---

### RULE 2: Unterschiedliche Operatoren brauchen Klammern (oder korrekte Multiline-Struktur)

Sobald du **AND** und **OR** vermischst (oder andere Kombinationen), musst du eindeutig machen, wie die Begriffe gruppiert sind.

#### ✅ RICHTIG - Inline mit Klammern

```
(CANCER OR TUMOR) AND TREATMENT
```
- Output: `(((CANCER) OR (TUMOR)) AND (TREATMENT))`
- Klammern machen clear: `(OR-Gruppe) AND (einzelner Begriff)`

#### ✅ AUCH RICHTIG - Multiline mit klarer Gruppierung

```
CANCER OR TUMOR
AND
TREATMENT
```
- Zeile 1: `CANCER OR TUMOR` ist eine zusammenhängende Gruppe
- Zeile 2: `AND` ist der Operator zwischen den Gruppen
- Zeile 3: `TREATMENT` ist ein einzelner Begriff
- Output: `(((CANCER) OR (TUMOR)) AND (TREATMENT))`

#### ❌ FALSCH - Mehrdeutig (mix ohne Klammern)

```
CANCER OR TUMOR AND TREATMENT
```
- **Fehler:** Mehrdeutig! Könnte bedeuten:
  - `CANCER OR (TUMOR AND TREATMENT)` (ODER zuerst)
  - `(CANCER OR TUMOR) AND TREATMENT` (AND zuerst)
  - Der Parser weiß nicht, welches richtig ist!
- **Fehlermeldung:** "Mix von AND & OR ohne Klammern! Setze Klammern."

#### ❌ AUCH FALSCH - Zerlegt + mehrdeutig

```
CANCER
OR
TUMOR
AND
TREATMENT
```
- **Fehler:** 
  1. Gruppe `CANCER OR TUMOR` wurde zerlegt
  2. Mix von AND & OR ohne klare Struktur
- **Fehlermeldung:** "Ambige Multiline-Struktur! Logische Gruppen dürfen nicht zerlegt werden."

---

### RULE 3: Multiline nur bei klarer Gruppierungsstruktur

Multiline ist nur OK, wenn **jede Zeile eine komplette logische Einheit darstellt**.

#### ✅ RICHTIG

```
CANCER OR TUMOR
AND
TREATMENT OR THERAPY
```
- Zeile 1: `CANCER OR TUMOR` (komplette Gruppe)
- Zeile 2: `AND` (Operator zwischen Gruppen)
- Zeile 3: `TREATMENT OR THERAPY` (komplette Gruppe)
- Output: `(((CANCER) OR (TUMOR)) AND ((TREATMENT) OR (THERAPY)))`

#### ❌ FALSCH

```
CANCER OR TUMOR
AND
(TREATMENT OR THERAPY)
```
- **Hinweis:** Das IST eigentlich OK, wenn...
- Nein, warte! Das ist tatsächlich auch OK, weil jede Zeile eine komplette Gruppe ist!

#### ❌ WIRKLICH FALSCH

```
CANCER
OR
TUMOR
AND
TREATMENT OR THERAPY
```
- **Fehler:** `CANCER OR TUMOR` wurde zerlegt über 3 Zeilen
- **Was Parser sieht:** Mehrdeutige Struktur
- **Fehlermeldung:** "Ambige Multiline-Struktur!"

---

## Einzelne Operatoren verstehen

### AND - Alle Begriffe müssen vorkommen

```
CANCER AND TREATMENT
```
- Suchergebnisse MÜSSEN sowohl CANCER als auch TREATMENT enthalten
- Output: `((CANCER) AND (TREATMENT))`

#### Multiline-Variante

```
CANCER
AND
TREATMENT
```
- Äquivalent zu obiger Zeile
- Output: `((CANCER) AND (TREATMENT))`

---

### OR - Mindestens ein Begriff muss vorkommen

```
CANCER OR TUMOR
```
- Suchergebnisse können CANCER, TUMOR oder beides enthalten
- **Wichtig:** Das ist eine Gruppe! Sie gehört in EINER Zeile!
- Output: `((CANCER) OR (TUMOR))`

#### Mehrfach OR

```
CANCER OR TUMOR OR CARCINOMA
```
- Alle in EINER Zeile, da sie durch denselben Operator verbunden sind
- Output: `((CANCER) OR (TUMOR) OR (CARCINOMA))`

---

### NOT - Ausschluss eines Begriffs

```
CANCER NOT PEDIATRIC
```
- Suchergebnisse MÜSSEN CANCER enthalten, dürfen aber NICHT PEDIATRIC enthalten
- Output: `((CANCER) NOT (PEDIATRIC))`

#### Kombination mit anderen Operatoren

```
(CANCER OR TUMOR) NOT PEDIATRIC
```
- Suchergebnisse müssen CANCER ODER TUMOR enthalten, aber nicht PEDIATRIC
- Output: `(((CANCER) OR (TUMOR)) NOT (PEDIATRIC))`

---

## Korrekte Query-Struktur

### Single-Line Queries

Eine Zeile, alle Operatoren + Begriffe zusammen.

#### Format

```
[TERM1] [OPERATOR] [TERM2] [OPERATOR] [TERM3] ...
```

#### Regeln

- Alle Begriffe mit **gleichen Operatoren** können unbesorgt gemischt werden
- Sobald du **unterschiedliche Operatoren** hast, **brauchst du Klammern**

#### Beispiele

✅ **Alle AND** (keine Klammern nötig):
```
CANCER AND TUMOR AND TREATMENT
```

✅ **Alle OR** (keine Klammern nötig):
```
CANCER OR TUMOR OR LYMPHOMA
```

✅ **Mix mit Klammern**:
```
(CANCER OR TUMOR) AND TREATMENT
(CANCER AND TUMOR) OR LYMPHOMA
(BREAST OR LUNG) NOT PEDIATRIC
```

❌ **Mix ohne Klammern** (ERROR):
```
CANCER OR TUMOR AND TREATMENT
```

---

### Multiline Queries

Mehrere Zeilen: jede ODD-Zeile ein Term/Gruppe, jede EVEN-Zeile ein Operator.

#### Format

```
[TERM_ODER_GRUPPE_1]
[OPERATOR]
[TERM_ODER_GRUPPE_2]
[OPERATOR]
[TERM_ODER_GRUPPE_3]
```

#### Regeln

- **ODD Zeilen (1, 3, 5, ...):** Terms oder geklammerte Gruppen
- **EVEN Zeilen (2, 4, 6, ...):** Operatoren (AND, OR, NOT)
- Jede Gruppe muss **zusammenhängend** sein (nicht zerlegt)

#### Beispiel 1: Einfach

```
CANCER
AND
TUMOR
```

#### Beispiel 2: Mit Gruppen

```
CANCER OR TUMOR
AND
TREATMENT OR THERAPY
```

#### Beispiel 3: Mit Klammern (für Sicherheit)

```
(CANCER OR TUMOR)
AND
(TREATMENT OR THERAPY)
```

---

## Häufige Fehler

### Fehler 1: OR-Gruppe zerlegt

❌ **FALSCH**
```
CANCER
OR
TUMOR
AND
TREATMENT
```

**Problem:** 
- `CANCER OR TUMOR` wurde zerlegt (sollte in einer Zeile sein)
- Mix von AND & OR ist mehrdeutig

✅ **RICHTIG - Option A (Inline)**
```
(CANCER OR TUMOR) AND TREATMENT
```

✅ **RICHTIG - Option B (Multiline)**
```
CANCER OR TUMOR
AND
TREATMENT
```

---

### Fehler 2: AND & OR ohne Klammern (Single-Line)

❌ **FALSCH**
```
CANCER OR TUMOR AND TREATMENT
```

**Problem:** Mehrdeutig
- Könnte `CANCER OR (TUMOR AND TREATMENT)` bedeuten
- Könnte `(CANCER OR TUMOR) AND TREATMENT` bedeuten

✅ **RICHTIG**
```
(CANCER OR TUMOR) AND TREATMENT
```
oder
```
CANCER OR (TUMOR AND TREATMENT)
```

---

### Fehler 3: Komplexer Term nicht geklammert (Multiline)

❌ **FALSCH**
```
CANCER
AND
TUMOR OR TREATMENT
```

**Problem:** `TUMOR OR TREATMENT` ist eine Gruppe, sollte geklammert sein

✅ **RICHTIG**
```
CANCER
AND
(TUMOR OR TREATMENT)
```

---

### Fehler 4: Unbalanced Parentheses

❌ **FALSCH**
```
(CANCER OR TUMOR AND TREATMENT
```

**Problem:** Schließende Klammer fehlt

✅ **RICHTIG**
```
(CANCER OR TUMOR) AND TREATMENT
```

---

## Beispiele (Richtig vs. Falsch)

### Beispiel 1: Einfache Synonyme

**Frage:** Ich suche nach Krebs (Synonyme: Cancer, Tumor, Carcinoma)

✅ **RICHTIG**
```
CANCER OR TUMOR OR CARCINOMA
```
Output: `((CANCER) OR (TUMOR) OR (CARCINOMA))`

❌ **FALSCH**
```
CANCER
OR
TUMOR
OR
CARCINOMA
```

---

### Beispiel 2: Und-Verknüpfung

**Frage:** Ich suche nach Krebsbehandlung

✅ **RICHTIG**
```
CANCER AND TREATMENT
```
Output: `((CANCER) AND (TREATMENT))`

✅ **AUCH RICHTIG**
```
CANCER
AND
TREATMENT
```

---

### Beispiel 3: Komplexe Query mit Ausschluss

**Frage:** Ich suche nach Brustkrebs-Behandlung, aber nicht bei Kindern

✅ **RICHTIG - Inline**
```
(BREAST OR LUNG) AND CANCER AND TREATMENT NOT PEDIATRIC
```

✅ **RICHTIG - Multiline**
```
BREAST OR LUNG
AND
CANCER
AND
TREATMENT
NOT
PEDIATRIC
```

Output (beide): `(((BREAST) OR (LUNG)) AND (CANCER) AND (TREATMENT) NOT (PEDIATRIC))`

---

### Beispiel 4: Mehrdeutige Query (FALSCH)

❌ **FALSCH - Mehrdeutig**
```
CANCER OR TUMOR AND TREATMENT AND THERAPY
```

**Problem:** Unklar ob:
- `CANCER OR (TUMOR AND TREATMENT AND THERAPY)` oder
- `(CANCER OR TUMOR) AND TREATMENT AND THERAPY` oder
- Andere Interpretationen?

✅ **RICHTIG - Klammern klären es**

Option A:
```
CANCER OR (TUMOR AND TREATMENT AND THERAPY)
```

Option B:
```
(CANCER OR TUMOR) AND TREATMENT AND THERAPY
```

---

### Beispiel 5: Sehr komplexe Query

**Frage:** 
- Brustkrebs oder Lungenkrebs
- Mit Chemotherapie oder Strahlentherapie
- Aber nicht bei Kindern

✅ **RICHTIG - Inline**
```
(BREAST OR LUNG) AND CANCER AND (CHEMOTHERAPY OR RADIATION) NOT PEDIATRIC
```

✅ **RICHTIG - Multiline**
```
BREAST OR LUNG
AND
CANCER
AND
CHEMOTHERAPY OR RADIATION
NOT
PEDIATRIC
```

Output: `(((BREAST) OR (LUNG)) AND (CANCER) AND ((CHEMOTHERAPY) OR (RADIATION)) NOT (PEDIATRIC))`

---

## Quick Reference

### Die 3 Goldenen Regeln

| Regel | Beispiel | Status |
|-------|----------|--------|
| **Gleiche Operatoren in EINER Zeile** | `A OR B` ✅ / `A / OR / B` ❌ | Mandatory |
| **Mix von AND & OR = Klammern** | `(A OR B) AND C` ✅ / `A OR B AND C` ❌ | Mandatory |
| **Multiline nur bei klaren Gruppen** | `A OR B / AND / C` ✅ / `A / OR / B / AND / C` ❌ | Mandatory |

### Operator-Spickzettel

| Operator | Bedeutung | Beispiel |
|----------|-----------|----------|
| **AND** | Alle müssen vorkommen | `CANCER AND TREATMENT` |
| **OR** | Min. eines muss vorkommen | `CANCER OR TUMOR` |
| **NOT** | Ausschluss | `CANCER NOT PEDIATRIC` |

### Format-Spickzettel

| Format | Struktur | Beispiel |
|--------|----------|----------|
| **Single-Line** | Ein Satz | `(CANCER OR TUMOR) AND TREATMENT` |
| **Multiline** | Abwechselnd Terms/Ops | `A OR B` / `AND` / `C OR D` |

---

## Fehlerbehandlung

Wenn deine Query einen ERROR vom Parser erhält, prüfe:

1. **Sind Klammern balanced?** → Zähle `(` und `)` auf beiden Seiten
2. **Hast du AND & OR gemischt (ohne Klammern)?** → Setze Klammern
3. **Hast du logische Gruppen zerlegt?** → Schreibe sie in EINER Zeile
4. **Sind komplexe Terms geklammert?** → `(A OR B)` statt `A OR B` in Multiline

---

## Zusammenfassung

- **RULE 1:** Logische Gruppen bleiben zusammen (eine Zeile oder geklammert)
- **RULE 2:** AND & OR Mix braucht Klammern oder korrekte Multiline-Struktur
- **RULE 3:** Multiline nur wenn jede Zeile eine komplette Einheit ist
- **ZIEL:** Eindeutigkeit! Der Parser darf nicht raten müssen!

---

**Fragen?** Überprüfe die Beispiele oder die Fehlermeldung des Parsers!

