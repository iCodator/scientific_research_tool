# Boolean Query Parser - Testing Phase

**Deutsch:** Siehe unten / **English:** See above

---

## English

### Overview

This directory contains the Boolean Query Parser v7.0 in active development and testing.

### Directory Structure

```
tests/
├── boolean_parser_v7_0.py    # Main parser implementation
├── README.md                  # This file
├── docs/                      # Documentation
│   ├── README.md             # Documentation overview
│   ├── USER_GUIDE_EN.md      # English user guide
│   ├── BENUTZERHANDBUCH_DE.md # German user guide
│   └── DEVELOPMENT_HISTORY.md # Internal development documentation
├── queries/                   # Test queries
│   ├── valid/                # Valid queries (should parse successfully)
│   │   ├── 1_simple_and.txt
│   │   ├── 2_simple_or.txt
│   │   ├── 3_simple_not.txt
│   │   ├── 4_multiline_or.txt
│   │   ├── 5_multiline_and.txt
│   │   ├── 6_complex_nested.txt
│   │   ├── 7_german_operators.txt
│   │   └── 8_german_multiline.txt
│   │
│   └── invalid/              # Invalid queries (should show errors)
│       ├── 1_unquoted_terms.txt
│       ├── 2_mixed_operators.txt
│       ├── 3_unbalanced_parens.txt
│       ├── 4_cross_line_parens.txt
│       └── 5_invalid_operators.txt
│
└── examples/                  # Example queries for users
    ├── simple_and.txt
    ├── simple_or.txt
    ├── simple_not.txt
    ├── multiline_simple.txt
    ├── multiline_complex.txt
    ├── german_operators.txt
    ├── complex_nested.txt
    └── README.md
```

### Quick Start

```bash
# Interactive mode
python boolean_parser_v7_0.py

# Parse a query from file
python boolean_parser_v7_0.py queries/valid/1_simple_and.txt

# Parse an example
python boolean_parser_v7_0.py examples/simple_and.txt
```

### Testing Valid Queries

Valid queries should parse without errors:

```bash
# Test a single valid query
python boolean_parser_v7_0.py queries/valid/1_simple_and.txt

# Test all valid queries (bash)
for file in queries/valid/*.txt; do
    echo "Testing: $file"
    python boolean_parser_v7_0.py "$file"
    echo ""
done
```

**Expected Output:** Fully parenthesized query or summary

### Testing Invalid Queries

Invalid queries should show clear error messages:

```bash
# Test a single invalid query
python boolean_parser_v7_0.py queries/invalid/1_unquoted_terms.txt

# Test all invalid queries (bash)
for file in queries/invalid/*.txt; do
    echo "Testing: $file"
    python boolean_parser_v7_0.py "$file"
    echo "---"
done
```

**Expected Output:** Error message explaining what's wrong and how to fix it

### Test Categories

#### Valid Queries (queries/valid/)

1. **1_simple_and.txt** - Basic AND operator
2. **2_simple_or.txt** - Basic OR operator
3. **3_simple_not.txt** - Basic NOT operator
4. **4_multiline_or.txt** - Multi-line with OR
5. **5_multiline_and.txt** - Multi-line with AND
6. **6_complex_nested.txt** - Deeply nested with multiple operators
7. **7_german_operators.txt** - German operators only (UND, ODER, NICHT)
8. **8_german_multiline.txt** - German operators in multi-line format

#### Invalid Queries (queries/invalid/)

1. **1_unquoted_terms.txt** - Terms without quotes
2. **2_mixed_operators.txt** - Mixed operators without parentheses
3. **3_unbalanced_parens.txt** - Parentheses don't balance
4. **4_cross_line_parens.txt** - Parentheses span across operator lines
5. **5_invalid_operators.txt** - Unknown operators

### Examples (examples/)

Example queries for learning and demonstration:

- **simple_and.txt** - `"cancer" AND "treatment"`
- **simple_or.txt** - `"cancer" OR "tumor"`
- **simple_not.txt** - `"cancer" NOT "benign"`
- **multiline_simple.txt** - Three terms with one operator
- **multiline_complex.txt** - Multiple terms with parentheses
- **german_operators.txt** - Using German operators
- **complex_nested.txt** - Multiple levels of nesting

### Documentation

- **[USER_GUIDE_EN.md](docs/USER_GUIDE_EN.md)** - Complete English user guide
- **[BENUTZERHANDBUCH_DE.md](docs/BENUTZERHANDBUCH_DE.md)** - Vollständiges deutsches Benutzerhandbuch
- **[DEVELOPMENT_HISTORY.md](docs/DEVELOPMENT_HISTORY.md)** - Internal development documentation

### Next Steps

This parser will be integrated into the "Scientific Research" project as a module for boolean query parsing in academic databases (PubMed, Europe PMC, Cochrane).

---

---

## Deutsch

### Übersicht

Dieses Verzeichnis enthält den Boolean Query Parser v7.0 in aktiver Entwicklung und Test.

### Verzeichnisstruktur

```
tests/
├── boolean_parser_v7_0.py    # Haupt-Parser-Implementierung
├── README.md                  # Diese Datei
├── docs/                      # Dokumentation
│   ├── README.md             # Dokumentations-Übersicht
│   ├── USER_GUIDE_EN.md      # Englisches Benutzerhandbuch
│   ├── BENUTZERHANDBUCH_DE.md # Deutsches Benutzerhandbuch
│   └── DEVELOPMENT_HISTORY.md # Interne Entwicklungsdokumentation
├── queries/                   # Test-Anfragen
│   ├── valid/                # Gültige Anfragen (sollten erfolgreich analysiert werden)
│   │   ├── 1_simple_and.txt
│   │   ├── 2_simple_or.txt
│   │   ├── 3_simple_not.txt
│   │   ├── 4_multiline_or.txt
│   │   ├── 5_multiline_and.txt
│   │   ├── 6_complex_nested.txt
│   │   ├── 7_german_operators.txt
│   │   └── 8_german_multiline.txt
│   │
│   └── invalid/              # Ungültige Anfragen (sollten Fehler zeigen)
│       ├── 1_unquoted_terms.txt
│       ├── 2_mixed_operators.txt
│       ├── 3_unbalanced_parens.txt
│       ├── 4_cross_line_parens.txt
│       └── 5_invalid_operators.txt
│
└── examples/                  # Beispiel-Anfragen für Benutzer
    ├── simple_and.txt
    ├── simple_or.txt
    ├── simple_not.txt
    ├── multiline_simple.txt
    ├── multiline_complex.txt
    ├── german_operators.txt
    ├── complex_nested.txt
    └── README.md
```

### Schnellstart

```bash
# Interaktiver Modus
python boolean_parser_v7_0.py

# Anfrage aus Datei analysieren
python boolean_parser_v7_0.py queries/valid/1_simple_and.txt

# Beispiel analysieren
python boolean_parser_v7_0.py examples/simple_and.txt
```

### Gültige Anfragen Testen

Gültige Anfragen sollten ohne Fehler analysiert werden:

```bash
# Eine gültige Anfrage testen
python boolean_parser_v7_0.py queries/valid/1_simple_and.txt

# Alle gültigen Anfragen testen (bash)
for file in queries/valid/*.txt; do
    echo "Teste: $file"
    python boolean_parser_v7_0.py "$file"
    echo ""
done
```

**Erwartete Ausgabe:** Vollständig geklammerte Anfrage oder Zusammenfassung

### Ungültige Anfragen Testen

Ungültige Anfragen sollten klare Fehlermeldungen zeigen:

```bash
# Eine ungültige Anfrage testen
python boolean_parser_v7_0.py queries/invalid/1_unquoted_terms.txt

# Alle ungültigen Anfragen testen (bash)
for file in queries/invalid/*.txt; do
    echo "Teste: $file"
    python boolean_parser_v7_0.py "$file"
    echo "---"
done
```

**Erwartete Ausgabe:** Fehlermeldung mit Erklärung und Lösungsvorschlag

### Test-Kategorien

#### Gültige Anfragen (queries/valid/)

1. **1_simple_and.txt** - Einfacher AND-Operator
2. **2_simple_or.txt** - Einfacher OR-Operator
3. **3_simple_not.txt** - Einfacher NOT-Operator
4. **4_multiline_or.txt** - Mehrzeilig mit OR
5. **5_multiline_and.txt** - Mehrzeilig mit AND
6. **6_complex_nested.txt** - Tiefe Verschachtelung mit mehreren Operatoren
7. **7_german_operators.txt** - Nur deutsche Operatoren (UND, ODER, NICHT)
8. **8_german_multiline.txt** - Deutsche Operatoren im mehrzeiligen Format

#### Ungültige Anfragen (queries/invalid/)

1. **1_unquoted_terms.txt** - Begriffe ohne Anführungszeichen
2. **2_mixed_operators.txt** - Gemischte Operatoren ohne Klammern
3. **3_unbalanced_parens.txt** - Klammern sind nicht ausgeglichen
4. **4_cross_line_parens.txt** - Klammern spannen über Operatorzeilen
5. **5_invalid_operators.txt** - Unbekannte Operatoren

### Beispiele (examples/)

Beispiel-Anfragen zum Lernen und zur Demonstration:

- **simple_and.txt** - `"Krebs" UND "Behandlung"`
- **simple_or.txt** - `"Krebs" ODER "Tumor"`
- **simple_not.txt** - `"Krebs" NICHT "gutartig"`
- **multiline_simple.txt** - Drei Begriffe mit einem Operator
- **multiline_complex.txt** - Mehrere Begriffe mit Klammern
- **german_operators.txt** - Verwendung deutscher Operatoren
- **complex_nested.txt** - Mehrere Verschachtelungsebenen

### Dokumentation

- **[USER_GUIDE_EN.md](docs/USER_GUIDE_EN.md)** - Vollständiges englisches Benutzerhandbuch
- **[BENUTZERHANDBUCH_DE.md](docs/BENUTZERHANDBUCH_DE.md)** - Vollständiges deutsches Benutzerhandbuch
- **[DEVELOPMENT_HISTORY.md](docs/DEVELOPMENT_HISTORY.md)** - Interne Entwicklungsdokumentation

### Nächste Schritte

Dieser Parser wird in das Projekt "Scientific Research" als Modul für die boolesche Abfrageanalyse in akademischen Datenbanken (PubMed, Europe PMC, Cochrane) integriert.
