# QUERY PARSER v2.3 - Entwicklungsplan
**Datum:** 10. Dezember 2025, 19:40 CET  
**Status:** READY FOR IMPLEMENTATION  
**Version:** 2.3 (Planning Phase)

---

## 🎯 Ziel v2.3

**Phase 3 & 4 fertigstellen + Unified Interface implementieren**

- ✅ Multi-Line Parsing (Phase 3) vollständig
- ✅ DateFormatConverter (Phase 4) funktional
- ✅ SourceFormatter für PubMed & Europe PMC
- ✅ parse_query_full() als Einstiegspunkt
- ✅ Erweiterte Test-Suite

---

## 📋 Prioritäre Tasks

### PRIORITY 1: Phase 3 Multi-Line Parsing (Deadline: sofort)

#### Task 1.1: `parse_query_line()` fertigstellen
```python
def parse_query_line(line: str) -> Dict:
    """
    Parsee eine einzelne Query-Zeile (ODD-Position).
    
    Input:  "Term1 OR Term2"
    Output: {
        'type': 'query',
        'terms': ['Term1', 'Term2'],
        'operator': 'OR',
        'raw': 'Term1 OR Term2'
    }
    """
```

**Anforderungen:**
- [ ] Terme extrahieren (alles außer Operatoren)
- [ ] Hauptoperator identifizieren
- [ ] Klammern respektieren
- [ ] Geklammerte Subexpressions als einzelne Terme behandeln

**Testcases:**
```
"Term1 OR Term2"                 → terms: ['Term1', 'Term2'], op: 'OR'
"(A OR B) AND C"                 → terms: ['(A OR B)', 'C'], op: 'AND'
"NOT (cancer AND cells)"         → terms: ['NOT', '(cancer AND cells)']
"coenzyme Q10"                   → terms: ['coenzyme Q10'] (kein op)
```

#### Task 1.2: `parse_complex_query()` fertigstellen
```python
def parse_complex_query(cleaned_query: str) -> Dict:
    """
    Parsee Multi-Line Query im ODD/EVEN Format.
    
    Input:
    ```
    Term1 OR Term2
    AND
    Term3 AND Term4
    ```
    
    Output: {
        'format': 'complex',
        'lines': [
            {'line': 1, 'type': 'query', ...},
            {'line': 2, 'type': 'operator', 'op': 'AND'},
            {'line': 3, 'type': 'query', ...}
        ],
        'structure': '(Term1 OR Term2) AND (Term3 AND Term4)'
    }
    """
```

**Anforderungen:**
- [ ] Alle ODD-Zeilen (Queries) parsen
- [ ] Alle EVEN-Zeilen (Operatoren) extrahieren
- [ ] Struktur als verschachtelter Baum aufbauen
- [ ] Finale Single-Line Struktur generieren

**Testcases:**
```
2.txt:
  Line 1 (ODD):  "Term1 OR Term2"     → Query
  Line 2 (EVEN): "NOT"                → Operator
  Line 3 (ODD):  "Term3 AND Term4 OR Term5"  → Query (MIXED!)
  Line 4 (EVEN): "AND"                → Operator
  Line 5 (ODD):  "Term6 OR Term7"     → Query

Expected: FEHLER (Line 3 hat mixed operators!)
```

---

### PRIORITY 2: Phase 4 DateFormatConverter (Deadline: +2 Tage)

#### Task 2.1: `detect_date_format()` implementieren
```python
def detect_date_format(query: str) -> Optional[Dict]:
    """
    Detektiert Datumsformate in Queries.
    
    Unterstützte Formate:
    - "2020-2024"          → {from: 2020, to: 2024, format: 'YYYY-YYYY'}
    - "2020:2024"          → {from: 2020, to: 2024, format: 'YYYY:YYYY'}
    - "2020 TO 2024"       → {from: 2020, to: 2024, format: 'YYYY TO YYYY'}
    - "[2020 TO 2024]"     → {from: 2020, to: 2024, format: '[YYYY TO YYYY]'}
    
    Return: None wenn kein Datum gefunden
    """
```

**Anforderungen:**
- [ ] Regex für alle Formate
- [ ] Validierung (from < to, sinnvolle Jahre)
- [ ] Case-insensitive matching

**Testcases:**
```python
detect_date_format("cancer AND 2020:2024")
→ {'from': 2020, 'to': 2024, 'format': 'YYYY:YYYY', 'position': (12, 21)}

detect_date_format("2019-2023 AND diabetes")
→ {'from': 2019, 'to': 2023, 'format': 'YYYY-YYYY', 'position': (0, 9)}

detect_date_format("no dates here")
→ None
```

#### Task 2.2: `convert_date_format()` implementieren
```python
def convert_date_format(
    detected: Dict, 
    target_format: str  # 'pubmed' | 'europe_pmc' | 'google_scholar'
) -> str:
    """
    Konvertiert erkanntes Datum in Zielformat.
    
    PubMed Format:        AND (2020:2024[pdat])
    Europe PMC Format:    AND (FIRST_PDATE:[2020 TO 2024])
    Google Scholar Format: pubdate:[2020 TO 2024]
    """
```

**Anforderungen:**
- [ ] Quellformat extrahieren
- [ ] Zielformat-spezifische Syntax
- [ ] Datum in Query einfügen

**Beispiele:**
```python
# PubMed
convert_date_format({from: 2020, to: 2024}, 'pubmed')
→ "AND (2020:2024[pdat])"

# Europe PMC
convert_date_format({from: 2020, to: 2024}, 'europe_pmc')
→ "AND (FIRST_PDATE:[2020 TO 2024])"

# Google Scholar
convert_date_format({from: 2020, to: 2024}, 'google_scholar')
→ "pubdate:[2020 TO 2024]"
```

---

### PRIORITY 3: Source-Formatter (Deadline: +3 Tage)

#### Task 3.1: `SourceFormatter` erweitern
```python
class SourceFormatter:
    """Formatiert Output für verschiedene Datenquellen."""
    
    SOURCES = {
        'pubmed': {
            'wrapper': '({})',
            'date_format': '{}[pdat]',
            'operator_style': 'UPPERCASE'
        },
        'europe_pmc': {
            'wrapper': '{}',  # ohne Außen-Klammern (v2.1 Bugfix)
            'date_format': 'FIRST_PDATE:[{}]',
            'operator_style': 'UPPERCASE'
        },
        'google_scholar': {
            'wrapper': '{}',
            'date_format': 'pubdate:[{}]',
            'operator_style': 'MIXED'
        },
        'scopus': {
            'wrapper': '{}',
            'date_format': 'PUBYEAR({})',
            'operator_style': 'UPPERCASE'
        }
    }
```

**Anforderungen:**
- [ ] SCOPUS-Format hinzufügen
- [ ] CrossRef-Format
- [ ] ArXiv-Format
- [ ] Datenbank-agnostische Syntax-Konvertierung

---

### PRIORITY 4: Unified Interface (Deadline: +4 Tage)

#### Task 4.1: `parse_query_full()` implementieren
```python
def parse_query_full(
    raw_query: str,
    source: str = 'pubmed',  # Target-Datenquelle
    output_format: str = 'formatted'  # 'structured' | 'formatted' | 'debug'
) -> Dict:
    """
    Unified Einstiegspunkt für alle 4 Phasen.
    
    Phase 1: Cleaning
    Phase 2: Validierung (Operator Precedence)
    Phase 3: Parsing (Single/Multi-Line)
    Phase 4: Formatierung + Datumkonvertierung
    """
```

**Workflow:**
```
1. Phase 1: clean_query()
   └─ Output: bereinigte Query
   
2. Phase 1: Format erkennen
   ├─ is_multiline() → True/False
   ├─ is_complex_format() → True/False
   └─ Output: Format-Info
   
3. Phase 2: Validierung
   ├─ has_mixed_operators() → Fehler?
   └─ Output: Validation-Result
   
4. Phase 3: Parsing
   ├─ parse_simple_query() ODER parse_complex_query()
   └─ Output: Parse-Tree
   
5. Phase 4: Formatierung
   ├─ detect_date_format()
   ├─ convert_date_format()
   ├─ apply_source_formatting()
   └─ Output: Formatted Query
   
6. Return: Vollständig verarbeitete Query
```

**Rückgabeformat:**
```python
{
    'status': 'success' | 'error',
    'input': {
        'raw': '...',
        'format': 'single-line' | 'multi-line'
    },
    'processing': {
        'phase1_cleaned': '...',
        'phase2_valid': True,
        'phase3_parsed': {...},
        'phase4_formatted': '...'
    },
    'output': {
        'query': '...',
        'source': 'pubmed',
        'has_dates': True,
        'date_range': {'from': 2020, 'to': 2024}
    },
    'error': None | 'Error message'
}
```

---

## 🧪 Erweiterte Test-Suite (v2.3)

### Test-Kategorien

#### Kategorie 1: Parsing Tests
```python
test_parse_query_line_simple()
test_parse_query_line_with_brackets()
test_parse_query_line_mixed_operators()  # Sollte FEHLER sein
test_parse_complex_query_valid()
test_parse_complex_query_invalid_format()
```

#### Kategorie 2: DateFormat Tests
```python
test_detect_date_yyyy_yyyy()
test_detect_date_yyyy_colon_yyyy()
test_detect_date_yyyy_to_yyyy()
test_detect_date_bracketed()
test_convert_date_to_pubmed()
test_convert_date_to_europe_pmc()
test_convert_date_to_google_scholar()
```

#### Kategorie 3: Source-Format Tests
```python
test_format_for_pubmed()
test_format_for_europe_pmc()
test_format_for_scopus()
test_format_for_crossref()
```

#### Kategorie 4: Integration Tests
```python
test_full_workflow_simple()
test_full_workflow_complex()
test_full_workflow_with_dates()
test_full_workflow_error_recovery()
```

---

## 📊 Testdateien für v2.3

### Neue Testdateien erstellen:

1. **date_format_tests.txt**
   ```
   cancer AND 2020:2024
   OR
   diabetes AND [2019 TO 2023]
   ```

2. **complex_valid.txt**
   ```
   (Term1 OR Term2)
   AND
   (Term3 AND Term4)
   AND
   Term5
   ```

3. **multiline_error.txt**
   ```
   A OR B AND C
   (sollte FEHLER sein: mixed operators)
   ```

---

## 🔧 Implementierungs-Reihenfolge

```
Week 1:
  ├─ Task 1.1: parse_query_line() 
  ├─ Task 1.2: parse_complex_query()
  └─ Task 2.1: detect_date_format()

Week 2:
  ├─ Task 2.2: convert_date_format()
  ├─ Task 3.1: SourceFormatter erweitern
  └─ Task 4.1: parse_query_full()

Week 3:
  ├─ Erweiterte Test-Suite
  ├─ Bug-Fixes & Optimierung
  └─ v2.3 Release
```

---

## 📈 Success Criteria v2.3

- [ ] Phase 3 zu 100% implementiert
- [ ] Phase 4 zu 100% implementiert
- [ ] Alle 5 Test-Dateien bestehen
- [ ] Mindestens 20 Unit-Tests
- [ ] Dokumentation aktualisiert
- [ ] Keine regression vs v2.2
- [ ] Performance < 100ms pro Query

---

## 🚀 v2.4+ Geplant

- [ ] Error Recovery & Auto-Fix
- [ ] Query Optimization
- [ ] SQL/Elasticsearch Generation
- [ ] Natural Language Output
- [ ] Cloud API Integration
- [ ] Web UI Prototype

---

**Status:** Ready for implementation  
**Next Step:** Task 1.1 beginnen (parse_query_line)
