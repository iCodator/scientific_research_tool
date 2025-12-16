# Boolean Query Parser - Benutzerhandbuch

## Übersicht

Der Boolean Query Parser wandelt menschenlesbare boolesche Suchanfragen in ein standardisiertes, vollständig geklammertes Format um. Er unterstützt sowohl englische als auch deutsche Operatoren und liefert klare Fehlermeldungen, wenn Anfragen mehrdeutig oder ungültig sind.

---

## Inhaltsverzeichnis

1. [Schnellstart](#schnellstart)
2. [Unterstützte Operatoren](#unterstützte-operatoren)
3. [Anfrage-Formate](#anfrage-formate)
4. [Anfragen Schreiben](#anfragen-schreiben)
5. [Beispiele](#beispiele)
6. [Fehlermeldungen](#fehlermeldungen)
7. [Best Practices](#best-practices)

---

## Schnellstart

### Installation

```bash
# Keine Installation erforderlich - nur Python 3.6+
python boolean_parser_v7_0.py
```

### Grundlegende Verwendung

```bash
# Interaktiver Modus
python boolean_parser_v7_0.py

# Aus Datei
python boolean_parser_v7_0.py meine_anfrage.txt
```

### Ihre Erste Anfrage

```
"Krebs" UND "Behandlung"
```

Ausgabe: `((Krebs) AND (Behandlung))`

---

## Unterstützte Operatoren

Der Parser unterstützt englische und deutsche Operatoren:

| Englisch | Deutsche Entsprechungen | Beschreibung |
|----------|------------------------|--------------|
| **AND** | und | Beide Begriffe müssen vorkommen |
| **OR** | oder | Einer der Begriffe muss vorkommen |
| **NOT** | nicht, kein, keine, ohne | Begriff darf NICHT vorkommen |

**Hinweis:** Operatoren sind nicht groß-/kleinschreibungsempfindlich. `UND`, `und`, `Und` funktionieren alle gleich.

---

## Anfrage-Formate

Der Parser unterstützt zwei Formate:

### 1. Einzeiliges Format

Alles in einer Zeile. Verwenden Sie dies für komplexe verschachtelte Anfragen.

**Beispiel:**
```
"Krebs" UND "Tumor" ODER "Neoplasma"
```

**Wann verwenden:**
- Einfache Anfragen
- Anfragen mit komplexer Verschachtelung über Operatoren hinweg
- Anfragen mit gemischten Operatoren in Klammern

---

### 2. Mehrzeiliges Format

Anfragen über mehrere Zeilen verteilt mit Operatoren in separaten Zeilen.

**Beispiel:**
```
"Krebs" ODER "Tumor"
UND
"Behandlung"
```

**Regeln für Mehrzeiliges Format:**
1. Muss mindestens 3 Zeilen haben
2. Muss eine ungerade Anzahl von Zeilen haben (3, 5, 7, ...)
3. Geradzahlige Zeilen (2., 4., 6., ...) enthalten NUR Operatoren
4. Alle Operatoren müssen gleich sein (alle UND, oder alle ODER, oder alle NICHT)
5. Jede ungerade Zeile muss ausgeglichene Klammern haben (keine Klammern, die über Operatorzeilen hinweggehen)

**Wann verwenden:**
- Lange Listen von Begriffen mit demselben Operator
- Bessere Lesbarkeit für einfache Anfragen
- Wenn Sie die Struktur klar sehen möchten

---

## Anfragen Schreiben

### Regel 1: Setzen Sie Ihre Suchbegriffe Immer in Anführungszeichen

✅ **Richtig:**
```
"Krebs" UND "Behandlung"
```

❌ **Falsch:**
```
Krebs UND Behandlung
```

### Regel 2: Verwenden Sie Klammern für Komplexe Anfragen

Beim Mischen von Operatoren verwenden Sie Klammern, um Ihre Absicht klar zu machen:

✅ **Richtig:**
```
("Krebs" ODER "Tumor") UND "Behandlung"
```

❌ **Mehrdeutig:**
```
"Krebs" ODER "Tumor" UND "Behandlung"
```
*Ist dies: (Krebs ODER Tumor) UND Behandlung? Oder: Krebs ODER (Tumor UND Behandlung)?*

### Regel 3: Mehrzeilige Anfragen Benötigen Denselben Operator

✅ **Richtig:**
```
"Krebs"
ODER
"Tumor"
ODER
"Neoplasma"
```

❌ **Falsch:**
```
"Krebs"
ODER
"Tumor"
UND
"Behandlung"
```
*Gemischte Operatoren erfordern einzeiliges Format mit Klammern*

### Regel 4: Jede Zeile Muss Ausgeglichen Sein (Mehrzeilig)

✅ **Richtig:**
```
("Krebs" ODER "Tumor")
UND
("Behandlung" ODER "Therapie")
```

❌ **Falsch:**
```
(("Krebs" ODER "Tumor")
UND
("Behandlung" ODER "Therapie"))
```
*Erste Zeile hat unausgeglichene Klammern - verwenden Sie stattdessen einzeiliges Format*

---

## Beispiele

### Grundlegende Suchen

**Einfaches UND:**
```
"Krebs" UND "Behandlung"
```
→ `((Krebs) AND (Behandlung))`

**Einfaches ODER:**
```
"Krebs" ODER "Tumor"
```
→ `((Krebs) OR (Tumor))`

**Einfaches NICHT:**
```
"Krebs" NICHT "gutartig"
```
→ `((Krebs) NOT (gutartig))`

---

### Mehrere Begriffe

**Mehrzeiliges ODER:**
```
"Krebs"
ODER
"Tumor"
ODER
"Neoplasma"
ODER
"Karzinom"
```
→ `((((Krebs) OR (Tumor)) OR (Neoplasma)) OR (Karzinom))`

**Einzeilig mit Klammern:**
```
("Krebs" ODER "Tumor" ODER "Neoplasma")
```
→ `(((Krebs) OR (Tumor)) OR (Neoplasma))`

---

### Gemischte Operatoren

**Zwei verschiedene Operatoren (erfordert Klammern):**
```
("Krebs" ODER "Tumor") UND "Behandlung"
```
→ `((((Krebs) OR (Tumor))) AND (Behandlung))`

**Komplexe Verschachtelung:**
```
(("Krebs" ODER "Tumor") UND ("Behandlung" ODER "Therapie")) NICHT "gutartig"
```
→ `(((((Krebs) OR (Tumor))) AND (((Behandlung) OR (Therapie)))) NOT (gutartig))`

---

### Englische Operatoren

```
"cancer" AND "treatment"
```
→ `((cancer) AND (treatment))`

```
"tumor" OR "neoplasm"
```
→ `((tumor) OR (neoplasm))`

```
"cancer" NOT "benign"
```
→ `((cancer) NOT (benign))`

---

### Mehrzeilig Komplex

```
("Krebs" ODER "Tumor" ODER "Neoplasma")
UND
("Behandlung" ODER "Therapie" ODER "Intervention")
OHNE
("gutartig" ODER "nicht-bösartig")
```
→ `((((((Krebs) OR (Tumor)) OR (Neoplasma))) AND ((((Behandlung) OR (Therapie)) OR (Intervention)))) NOT (((gutartig) OR (nicht-bösartig))))`

---

## Fehlermeldungen

Der Parser liefert klare, hilfreiche Fehlermeldungen:

### Begriffe Ohne Anführungszeichen

**Anfrage:**
```
Krebs UND Behandlung
```

**Fehler:**
```
SINGLE-LINE: Unquoted term 'Krebs'
```

**Lösung:** Setzen Sie alle Suchbegriffe in Anführungszeichen: `"Krebs" UND "Behandlung"`

---

### Gemischte Operatoren Ohne Klammern

**Anfrage:**
```
"Krebs" ODER "Tumor" UND "Behandlung"
```

**Fehler:**
```
SINGLE-LINE: Mixed operators {'OR', 'AND'} without parens
```

**Lösung:** Fügen Sie Klammern hinzu: `("Krebs" ODER "Tumor") UND "Behandlung"`

---

### Unausgeglichene Klammern in Mehrzeilig

**Anfrage:**
```
(("Krebs" ODER "Tumor")
UND
("Behandlung"))
```

**Fehler:**
```
MULTI-LINE: Line 1 has unbalanced parentheses.
  (("Krebs" ODER "Tumor")
  Use SINGLE-LINE format for cross-line nesting.
```

**Lösung:** Verwenden Sie einzeiliges Format: `(("Krebs" ODER "Tumor") UND ("Behandlung"))`

---

### Gemischte Operatoren in Mehrzeilig

**Anfrage:**
```
"Krebs"
ODER
"Tumor"
UND
"Behandlung"
```

**Fehler:**
```
MULTI-LINE: Mixed operators {'OR', 'AND'}
```

**Lösung:** Entweder:
1. Verwenden Sie durchgehend denselben Operator (alle ODER oder alle UND)
2. Verwenden Sie einzeilig mit Klammern: `("Krebs" ODER "Tumor") UND "Behandlung"`

---

## Best Practices

### 1. Beginnen Sie Einfach

Beginnen Sie mit einfachen Anfragen und fügen Sie schrittweise Komplexität hinzu:
```
"Krebs"                                     # Schritt 1
"Krebs" UND "Behandlung"                    # Schritt 2
("Krebs" ODER "Tumor") UND "Behandlung"     # Schritt 3
```

### 2. Verwenden Sie Mehrzeilig für Lesbarkeit

Wenn Sie viele Begriffe mit demselben Operator haben:

**Anstatt:**
```
"A" ODER "B" ODER "C" ODER "D" ODER "E"
```

**Verwenden Sie:**
```
"A"
ODER
"B"
ODER
"C"
ODER
"D"
ODER
"E"
```

### 3. Verwenden Sie Kommentare

Fügen Sie Kommentare hinzu, um Ihre Anfragelogik zu erklären:

```
# Suche nach Krebs-bezogenen Begriffen
"Krebs" ODER "Tumor" ODER "Neoplasma"
UND
# Kombiniert mit Behandlungsbegriffen
"Behandlung" ODER "Therapie"
OHNE
# Aber gutartige Fälle ausschließen
"gutartig"
```

### 4. Testen Sie Schrittweise

Wenn Sie einen Fehler erhalten:
1. Vereinfachen Sie Ihre Anfrage
2. Testen Sie jeden Teil separat
3. Kombinieren Sie Teile nacheinander

### 5. Speichern Sie Komplexe Anfragen

Speichern Sie Ihre funktionierenden Anfragen in `.txt`-Dateien:

```bash
python boolean_parser_v7_0.py meine_komplexe_anfrage.txt
```

---

## Häufige Muster

### Muster 1: Synonyme

Suche nach mehreren Synonymen desselben Konzepts:

```
"Krebs" ODER "Tumor" ODER "Neoplasma" ODER "Karzinom"
```

### Muster 2: Erforderlich + Optional

Suche nach erforderlichen Begriffen UND optionalen Variationen:

```
"Krebs" UND ("Behandlung" ODER "Therapie" ODER "Intervention")
```

### Muster 3: Einschließen + Ausschließen

Suche nach Begriffen, aber bestimmte Typen ausschließen:

```
("Krebs" ODER "Tumor") NICHT ("gutartig" ODER "nicht-bösartig")
```

### Muster 4: Kombinationssuche

Mehrere Konzepte kombinieren:

```
("Krebs" ODER "Tumor")
UND
("Behandlung" ODER "Therapie")
UND
("effektiv" ODER "erfolgreich")
```

---

## Fehlerbehebung

### Meine Anfrage funktioniert, aber die Ausgabe sieht anders aus

Der Parser wandelt Ihre Anfrage in eine vollständig geklammerte Form um. Das ist normal und gewährleistet eine eindeutige Interpretation.

**Ihre Eingabe:**
```
"A" UND "B" UND "C"
```

**Parser-Ausgabe:**
```
(((A) AND (B)) AND (C))
```

Beide bedeuten dasselbe - der Parser macht die Gruppierung nur explizit.

---

### Ich muss nach Anführungszeichen in meinem Begriff suchen

Verwenden Sie maskierte Anführungszeichen innerhalb Ihrer Suchbegriffe:

```
"die \"beste\" Behandlung"
```

---

### Meine mehrzeilige Anfrage schlägt fehl

Prüfen Sie:
1. Haben Sie eine ungerade Anzahl von Zeilen? (3, 5, 7...)
2. Sind geradzahlige Zeilen NUR Operatoren?
3. Sind alle Operatoren gleich?
4. Hat jede ungerade Zeile ausgeglichene Klammern?

Wenn Sie es nicht beheben können, verwenden Sie stattdessen das einzeilige Format.

---

## Hilfe Erhalten

Wenn Sie auf Probleme stoßen:

1. Überprüfen Sie die Fehlermeldung - sie sagt Ihnen normalerweise genau, was falsch ist
2. Vereinfachen Sie Ihre Anfrage und testen Sie Teile separat
3. Überprüfen Sie die Beispiele in diesem Handbuch
4. Prüfen Sie, ob Ihre Anfrage alle Regeln befolgt

---

## Zusammenfassung

### ✅ Tun Sie:
- Setzen Sie alle Suchbegriffe in Anführungszeichen: `"Begriff"`
- Verwenden Sie Klammern für komplexe Anfragen
- Verwenden Sie denselben Operator im mehrzeiligen Format
- Halten Sie ungerade Zeilen im mehrzeiligen Format ausgeglichen
- Fügen Sie Kommentare hinzu, um Ihre Logik zu erklären

### ❌ Tun Sie nicht:
- Lassen Sie Begriffe ohne Anführungszeichen: `Begriff` ❌
- Mischen Sie Operatoren ohne Klammern
- Verwenden Sie verschiedene Operatoren im mehrzeiligen Format
- Spannen Sie Klammern über Operatorzeilen im mehrzeiligen Format
- Vergessen Sie nicht, komplexe Anfragen zu testen

---

## Schnellreferenzkarte

```
OPERATOREN (nicht groß-/kleinschreibungsempfindlich)
Englisch: AND, OR, NOT
Deutsch:  UND, ODER, NICHT/KEIN/KEINE/OHNE

FORMATE
Einzeilig:   "A" UND "B" ODER "C"
Mehrzeilig:  "A"
             UND
             "B"

REGELN
✓ Begriffe immer in Anführungszeichen setzen
✓ Klammern für gemischte Operatoren verwenden
✓ Mehrzeilig = nur gleicher Operator
✓ Jede Zeile ausgeglichen im mehrzeiligen Format

BEISPIELE
Einfach:     "Krebs" UND "Behandlung"
Mehrere:     "A" ODER "B" ODER "C"
Komplex:     ("A" ODER "B") UND ("C" ODER "D")
Ausschließen: "Krebs" NICHT "gutartig"
```

---

*Für technische Details siehe die Entwicklerdokumentation.*
