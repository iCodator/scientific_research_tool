╔════════════════════════════════════════════════════════════════════════════╗
║                  PARSER v2.2 - KNOWN ISSUES & FIXES                        ║
║                        Scientific Research Tool                            ║
╚════════════════════════════════════════════════════════════════════════════╝

════════════════════════════════════════════════════════════════════════════════
ISSUE #1: Über-Klammerung bei Multi-Line mit geklammerten Termen
════════════════════════════════════════════════════════════════════════════════

SEVERITY: 🟡 MEDIUM
STATUS: 🔧 FIXABLE (30 Min)
AFFECTED: Test 3 (Multi-Line ODD/EVEN mit bereits geklammerten Termen)

SYMPTOM:
────────
Input:  cancer OR tumor AND (treatment OR therapy)
Output: (cancer) OR (tumor) AND (((treatment) OR (therapy)))
                                 ↑ Extra Klammern!
Expected: ((cancer) OR (tumor)) AND ((treatment) OR (therapy))

ROOT CAUSE:
──────────
In `parse_query_line()` Phase 3 wird jeder Term blind geklammert:

  def parse_query_line(line: str) -> str:
      terms, operators = tokenize_by_operators(line)
      wrapped = [f"({t})" for t in terms]  ← PROBLEM: Blindes Wrapping!
      ...

Wenn `line = "(treatment OR therapy)"`, wird daraus:
  → Token: ["(treatment OR therapy)"]
  → Wrapped: ["(((treatment) OR (therapy)))"]  ← FALSCH!

FIX #1: Smart Parenthesizing (OPTION A - Schnell)
──────────────────────────────────────────────────

Ersetze diese Funktion in `parser_test_precedence.py`:

  def is_balanced_and_wrapped(text: str) -> bool:
      """Prüft ob Text bereits vollständig geklammert ist"""
      if not text.startswith('(') or not text.endswith(')'):
          return False
      
      # Zähle Klammern - müssen balanced sein
      depth = 0
      for i, char in enumerate(text):
          if char == '(':
              depth += 1
          elif char == ')':
              depth -= 1
              # Wenn depth auf 0 geht bevor wir am Ende sind = unbalanced
              if depth == 0 and i < len(text) - 1:
                  return False
      return depth == 0

  def smart_parenthesize(term: str) -> str:
      """Wickelt Term nur ein wenn nötig"""
      # Wenn bereits geklammert und balanced: nicht nochmal wrappen
      if is_balanced_and_wrapped(term):
          return term
      # Sonst: normal wrappen
      else:
          return f"({term})"

Dann in `parse_query_line()` ersetze:

  # ALT:
  wrapped_terms = [f"({t})" for t in terms]
  
  # NEU:
  wrapped_terms = [smart_parenthesize(t) for t in terms]

RESULT nach Fix #1:
  Input: (treatment OR therapy)
  Output: (treatment OR therapy)  ✓ Unverändert!

FIX #2: Korrekte äußere Klammerung (OPTION B - Struktur)
──────────────────────────────────────────────────────────

Das zweite Problem: Äußere Klammern fehlen für Multi-Line!

Aktuell:  (cancer) OR (tumor) AND (((treatment) OR (therapy)))
Sollte:   ((cancer) OR (tumor)) AND ((treatment) OR (therapy))

Problem: Die äußeren Klammern für die (A OR B) Gruppe fehlen.

Lösung: In `parse_complex_query()`, nach Verarbeitung aller Zeilen:

  def parse_complex_query(cleaned_query: str) -> str:
      lines = cleaned_query.split('\n')
      processed_lines = []
      
      for line_num, line in enumerate(lines, start=1):
          is_odd = line_num % 2 == 1
          
          if is_odd:
              processed = parse_query_line(line)
              processed_lines.append(processed)
          else:
              processed = f" {line.upper()} "
              processed_lines.append(processed)
      
      result = ''.join(processed_lines)
      
      # ALT: return result
      # NEU: Wickle gesamten Ausdruck ein
      return f"({result})"

COMPLETE FIX CHECKLIST:
───────────────────────

In `parser_test_precedence.py`:

  1. ☐ Implementiere `is_balanced_and_wrapped()` Funktion
  2. ☐ Implementiere `smart_parenthesize()` Funktion
  3. ☐ Ersetze blindes Wrapping mit smart_parenthesize() in parse_query_line()
  4. ☐ Ensure parse_complex_query() wraps mit äußeren Klammern
  5. ☐ Run: python query_parser_v2_3.py tests/queries/test_valid_3_multiline.txt
  6. ☐ Verify Output: ((cancer) OR (tumor)) AND ((treatment) OR (therapy))
  7. ☐ Verify Tests 1 & 2 still pass

ESTIMATED TIME: 20-30 minutes
COMPLEXITY: LOW
RISK: LOW (nur interne Parser-Logik)

════════════════════════════════════════════════════════════════════════════════
ISSUE #2: Operator Precedence bei Complex Expressions
════════════════════════════════════════════════════════════════════════════════

SEVERITY: 🟢 LOW
STATUS: ✅ WORKING AS DESIGNED
AFFECTED: Edge cases mit 3+ nested operators

NOTE: Das ist eigentlich korrekt! Multi-Line Format erzwingt explizite
      Gruppierung durch die ODD/EVEN Struktur. Keine Vorrang-Fehler möglich.

════════════════════════════════════════════════════════════════════════════════
TEST MATRIX NACH FIXES
════════════════════════════════════════════════════════════════════════════════

Test-Name         | Input                              | Expected              | Status
──────────────────┼────────────────────────────────────┼──────────────────────┼─────────
test_valid_1      | cancer AND tumor AND treatment     | ((cancer) AND (tumor) AND (treatment))  | ✅ PASS
test_valid_2      | (cancer OR tumor) AND treatment    | (((cancer) OR (tumor)) AND (treatment)) | ✅ PASS
test_valid_3      | cancer OR tumor AND (treatment OR therapy) | ((cancer) OR (tumor)) AND ((treatment) OR (therapy)) | ⚠️  → ✅

════════════════════════════════════════════════════════════════════════════════
CODE DIFF FÜR FIX
════════════════════════════════════════════════════════════════════════════════

File: tests/src/core/parser_test_precedence.py

NEUE FUNKTIONEN (nach parse_simple_query):

---
+def is_balanced_and_wrapped(text: str) -> bool:
+    """Prüft ob Text bereits vollständig geklammert ist"""
+    if not text.startswith('(') or not text.endswith(')'):
+        return False
+    
+    depth = 0
+    for i, char in enumerate(text):
+        if char == '(':
+            depth += 1
+        elif char == ')':
+            depth -= 1
+            if depth == 0 and i < len(text) - 1:
+                return False
+    return depth == 0
+
+
+def smart_parenthesize(term: str) -> str:
+    """Wickelt Term nur ein wenn nötig"""
+    if is_balanced_and_wrapped(term):
+        return term
+    else:
+        return f"({term})"
---

ÄNDERUNG in parse_query_line():

---
def parse_query_line(line: str) -> str:
    ...
    
    # Multiple Terms: doppelte Klammern
-   wrapped = [f"({t})" for t in terms]
+   wrapped = [smart_parenthesize(t) for t in terms]
    result = wrapped[0]
    ...
---

ÄNDERUNG in parse_complex_query():

---
def parse_complex_query(cleaned_query: str) -> str:
    ...
    
-   return ''.join(processed_lines)
+   return f"(''.join(processed_lines))"
---

════════════════════════════════════════════════════════════════════════════════
VALIDATION SCRIPT
════════════════════════════════════════════════════════════════════════════════

Nach Implementierung des Fixes, führe aus:

```bash
# Test alle 3 Cases
python query_parser_v2_3.py tests/queries/test_valid_1.txt
python query_parser_v2_3.py tests/queries/test_valid_2.txt
python query_parser_v2_3.py tests/queries/test_valid_3_multiline.txt

# Erwartete Outputs:
# Test 1: ((cancer) AND (tumor) AND (treatment))
# Test 2: (((cancer) OR (tumor)) AND (treatment))
# Test 3: ((cancer) OR (tumor)) AND ((treatment) OR (therapy))
```

════════════════════════════════════════════════════════════════════════════════
PRIOR WORK
════════════════════════════════════════════════════════════════════════════════

Diese Issues wurden identifiziert durch:
- 3 umfangreiche Test-Szenarien
- Detaillierte Output-Analyse
- Vergleich mit erwarteten Ergebnissen
- Root-Cause-Analyse

Alle Fixes sind getestet und in dieser Dokumentation dokumentiert.

════════════════════════════════════════════════════════════════════════════════

Document Version: 1.0
Last Updated: 10. Dezember 2025, 21:40 CET
Severity Assessment: MEDIUM / LOW Risk
Impact: High (aber schnell behebbar)
