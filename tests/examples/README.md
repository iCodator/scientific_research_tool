# Boolean Query Parser - Example Queries

**Deutsch:** Siehe unten / **English:** See above

---

## English

### Overview

This directory contains example queries for learning and testing the Boolean Query Parser.

### Simple Examples

These examples demonstrate the basic operators:

#### 1. simple_and.txt
```
"cancer" AND "treatment"
```
**Output:** `((cancer) AND (treatment))`  
**Meaning:** Both "cancer" AND "treatment" must appear

#### 2. simple_or.txt
```
"cancer" OR "tumor"
```
**Output:** `((cancer) OR (tumor))`  
**Meaning:** Either "cancer" OR "tumor" (or both) must appear

#### 3. simple_not.txt
```
"cancer" NOT "benign"
```
**Output:** `((cancer) NOT (benign))`  
**Meaning:** "cancer" must appear, but NOT "benign"

### Multi-Line Examples

These examples show how to use the multi-line format for better readability:

#### 4. multiline_simple.txt
```
"cancer"
OR
"tumor"
OR
"neoplasm"
```
**Output:** `(((cancer) OR (tumor)) OR (neoplasm))`  
**Meaning:** Search for synonyms - any of these terms can appear

**Use Case:** Searching for different names of the same medical condition

#### 5. multiline_complex.txt
```
("cancer" OR "tumor" OR "neoplasm")
AND
("treatment" OR "therapy" OR "intervention")
```
**Output:** `((((cancer) OR (tumor)) OR (neoplasm))) AND ((((treatment) OR (therapy)) OR (intervention))))`  
**Meaning:** Must have a cancer term AND a treatment term

**Use Case:** Searching for studies about treating cancer with various approaches

### Language Examples

#### 6. german_operators.txt
```
"Krebs" UND "Behandlung" ODER "Krebs" UND "Therapie"
```
**Output:** `((((Krebs) AND (Behandlung))) OR (((Krebs) AND (Therapie))))`  
**Meaning:** German operators work the same way as English

**Note:** Mix English and German operators freely - both are supported

### Complex Examples

#### 7. complex_nested.txt
```
(("cancer" OR "tumor") AND ("treatment" OR "therapy")) NOT ("benign" OR "non-malignant")
```
**Output:** `((((((cancer) OR (tumor))) AND (((treatment) OR (therapy))))) NOT (((benign) OR (non-malignant))))`  
**Meaning:** 
1. Must have a cancer term AND a treatment term
2. But CANNOT have a benign term

**Use Case:** Find studies about malignant cancer treatments, excluding benign cases

### Running Examples

```bash
# Run a single example
python ../boolean_parser_v7_0.py simple_and.txt

# Run all examples
for file in *.txt; do
    echo "Running: $file"
    python ../boolean_parser_v7_0.py "$file"
    echo ""
done
```

### Creating Your Own Examples

To create a new example:

1. Create a file with `.txt` extension
2. Write your query following the rules
3. Add comments with `#` to explain
4. Run with the parser

**Template:**
```
# My Example Query
# Description of what this query does
"term1" AND "term2"
```

### Tips

- ✅ Start with simple examples
- ✅ Use comments to explain your queries
- ✅ Test single-line format first, then multi-line
- ✅ Use parentheses to make complex queries clear
- ❌ Don't forget to quote your terms
- ❌ Don't mix operators without parentheses

---

---

## Deutsch

### Übersicht

Dieses Verzeichnis enthält Beispiel-Anfragen zum Lernen und Testen des Boolean Query Parsers.

### Einfache Beispiele

Diese Beispiele zeigen die grundlegenden Operatoren:

#### 1. simple_and.txt
```
"Krebs" UND "Behandlung"
```
**Ausgabe:** `((Krebs) AND (Behandlung))`  
**Bedeutung:** Sowohl "Krebs" ALS AUCH "Behandlung" müssen vorkommen

#### 2. simple_or.txt
```
"Krebs" ODER "Tumor"
```
**Ausgabe:** `((Krebs) OR (Tumor))`  
**Bedeutung:** Entweder "Krebs" ODER "Tumor" (oder beide) müssen vorkommen

#### 3. simple_not.txt
```
"Krebs" NICHT "gutartig"
```
**Ausgabe:** `((Krebs) NOT (gutartig))`  
**Bedeutung:** "Krebs" muss vorkommen, aber NICHT "gutartig"

### Mehrzeilige Beispiele

Diese Beispiele zeigen, wie man das mehrzeilige Format für bessere Lesbarkeit nutzt:

#### 4. multiline_simple.txt
```
"Krebs"
ODER
"Tumor"
ODER
"Neoplasma"
```
**Ausgabe:** `(((Krebs) OR (Tumor)) OR (Neoplasma))`  
**Bedeutung:** Suche nach Synonymen - einer dieser Begriffe kann vorkommen

**Anwendungsfall:** Suche nach verschiedenen Namen desselben medizinischen Zustands

#### 5. multiline_complex.txt
```
("Krebs" ODER "Tumor" ODER "Neoplasma")
UND
("Behandlung" ODER "Therapie" ODER "Intervention")
```
**Ausgabe:** `((((Krebs) OR (Tumor)) OR (Neoplasma))) AND ((((Behandlung) OR (Therapie)) OR (Intervention))))`  
**Bedeutung:** Muss einen Krebsbegriff UND einen Behandlungsbegriff haben

**Anwendungsfall:** Suche nach Studien über die Behandlung von Krebs mit verschiedenen Ansätzen

### Sprachbeispiele

#### 6. german_operators.txt
```
"Krebs" UND "Behandlung" ODER "Krebs" UND "Therapie"
```
**Ausgabe:** `((((Krebs) AND (Behandlung))) OR (((Krebs) AND (Therapie))))`  
**Bedeutung:** Deutsche Operatoren funktionieren genauso wie englische

**Hinweis:** Englische und deutsche Operatoren können frei gemischt werden - beide werden unterstützt

### Komplexe Beispiele

#### 7. complex_nested.txt
```
(("Krebs" ODER "Tumor") UND ("Behandlung" ODER "Therapie")) NICHT ("gutartig" ODER "nicht-bösartig")
```
**Ausgabe:** `((((((Krebs) OR (Tumor))) AND (((Behandlung) OR (Therapie))))) NOT (((gutartig) OR (nicht-bösartig))))`  
**Bedeutung:**
1. Muss einen Krebsbegriff UND einen Behandlungsbegriff haben
2. Kann aber KEINEN gutartigen Begriff haben

**Anwendungsfall:** Suche nach Studien über die Behandlung von bösartigem Krebs, ohne gutartige Fälle

### Beispiele Ausführen

```bash
# Ein einzelnes Beispiel ausführen
python ../boolean_parser_v7_0.py simple_and.txt

# Alle Beispiele ausführen
for file in *.txt; do
    echo "Führe aus: $file"
    python ../boolean_parser_v7_0.py "$file"
    echo ""
done
```

### Eigene Beispiele Erstellen

Um ein neues Beispiel zu erstellen:

1. Erstelle eine Datei mit der Erweiterung `.txt`
2. Schreibe Ihre Anfrage nach den Regeln
3. Fügen Sie Kommentare mit `#` hinzu, um zu erklären
4. Führen Sie mit dem Parser aus

**Vorlage:**
```
# Meine Beispiel-Anfrage
# Beschreibung, was diese Anfrage tut
"Begriff1" UND "Begriff2"
```

### Tipps

- ✅ Beginnen Sie mit einfachen Beispielen
- ✅ Verwenden Sie Kommentare, um Ihre Anfragen zu erklären
- ✅ Testen Sie zuerst das einzeilige Format, dann mehrzeilig
- ✅ Verwenden Sie Klammern, um komplexe Anfragen klar zu machen
- ❌ Vergessen Sie nicht, Ihre Begriffe in Anführungszeichen zu setzen
- ❌ Mischen Sie nicht Operatoren ohne Klammern
