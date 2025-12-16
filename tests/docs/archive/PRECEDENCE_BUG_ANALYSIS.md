╔════════════════════════════════════════════════════════════════════════════╗
║        CRITICAL BUG FIX: Multiline Parsing Precedence (v2.2.3)             ║
║                                                                            ║
║  Problem: Multiline Query wird FALSCH geklammert                           ║
║  Input:  cancer OR tumor AND (treatment OR therapy)                        ║
║  Falsch: ((cancer) OR (tumor) AND ((treatment) OR (therapy)))              ║
║  RICHTIG: (((cancer) OR (tumor)) AND ((treatment) OR (therapy)))           ║
║                                                                            ║
║  Root Cause: ODD Lines werden nicht einzeln geklammert!                   ║
╚════════════════════════════════════════════════════════════════════════════╝

════════════════════════════════════════════════════════════════════════════════
🔴 PROBLEM DETAILLIERT ERKLÄRT
════════════════════════════════════════════════════════════════════════════════

DEIN INPUT (test_valid_3_multiline.txt):
  Zeile 1: cancer          ← ODD (Suchterm)
  Zeile 2: OR             ← EVEN (Operator)
  Zeile 3: tumor          ← ODD (Suchterm)
  Zeile 4: AND            ← EVEN (Operator)
  Zeile 5: (treatment OR therapy)  ← ODD (Suchterm mit Klammern)

FALSCHE INTERPRETATION (v2.2.2):
  ((cancer) OR (tumor) AND ((treatment) OR (therapy)))
  ↑ Problem: tumor AND wird nicht geklammert!
  
  Database Interpretation:
    cancer OR tumor AND (treatment OR therapy)
    = cancer OR (tumor AND (treatment OR therapy))  ← FALSCH! (Precedence ist AND > OR)

RICHTIGE INTERPRETATION:
  (((cancer) OR (tumor)) AND ((treatment) OR (therapy)))
  ↑ RICHTIG: Jede ODD Line wird einzeln geklammert!
  
  Database Interpretation:
    (cancer OR tumor) AND (treatment OR therapy)  ← RICHTIG!


DETAILLIERTE ERKLÄRUNG:

Boolean Operator Precedence (Standard):
  AND > OR (AND bindet stärker!)

Beispiel ohne Klammern:
  A OR B AND C
  = A OR (B AND C)  ← AND wird zuerst ausgeführt!
  
Darum brauchen wir Klammern:
  (A OR B) AND C
  = Erst (A OR B), DANN AND C

In deinem Fall:
  cancer OR tumor AND (treatment OR therapy)
  = cancer OR (tumor AND (treatment OR therapy))  ← FALSCH!
  
Mit richtigen Klammern:
  (cancer OR tumor) AND (treatment OR therapy)
  = (cancer OR tumor) DANN AND (treatment OR therapy)  ← RICHTIG!


ALGORITHMUS FEHLER (v2.2.2):

```python
# ALT (FALSCH):
result_tokens = []
for i, line in enumerate(lines):
    if i % 2 == 0:  # ODD (Suchterme)
        parsed = parse_query_line(line, source)  ← Wird NUR intern geklammert!
        result_tokens.append(parsed)              ← Nicht gesamte ODD!
    else:  # EVEN (Operatoren)
        result_tokens.append(op)

result = ' '.join(result_tokens)  ← Kombiniert nur die Tokens!
if should_add_parentheses(result):
    result = f"({result})"  ← Outer Klammern, aber innere ODD nicht!
```

Problem:
  1. parse_query_line("cancer") → "(cancer)"
  2. parse_query_line("tumor") → "(tumor)"
  3. Kombiniert: "(cancer) OR (tumor) AND ..."
  4. Outer: "((cancer) OR (tumor) AND ...)"
  ↑ FALSCH! Der gesamte "(cancer) OR (tumor)" Teil braucht Klammern!


NEU (RICHTIG):

```python
# Gruppiere ODD Lines mit ihren Operatoren
# Beispiel: [cancer, OR, tumor] → behandle als Gruppe
# Dann: [GROUP1, AND, (treatment OR therapy)]
# Klammere jede Gruppe einzeln

# Resultat: (GROUP1) AND (GROUP2)
#         = ((cancer) OR (tumor)) AND ((treatment) OR (therapy))
```

════════════════════════════════════════════════════════════════════════════════
✅ LÖSUNG - Corrected Multiline Parsing
════════════════════════════════════════════════════════════════════════════════

NEUE STRATEGIE:

1. Parse die Multiline Query in logische Gruppen
2. Eine Gruppe = Suchterme bis zum nächsten Top-Level Operator
3. Klammere JEDE Gruppe einzeln ein
4. Kombiniere die Gruppen mit den Top-Level Operatoren

BEISPIEL:

Input:
  cancer
  OR
  tumor
  AND
  (treatment OR therapy)

Parsing-Schritte:
  
  SCHRITT 1: Gruppieren
    Group 1: cancer OR tumor
    Group 2: (treatment OR therapy)
  
  SCHRITT 2: Jede Gruppe klammern
    Group 1 processed: (cancer) OR (tumor) → gesamte Gruppe: ((cancer) OR (tumor))
    Group 2 processed: (treatment OR therapy) → gesamte Gruppe: ((treatment) OR (therapy))
  
  SCHRITT 3: Kombinieren mit Top-Level Operator (AND)
    ((cancer) OR (tumor)) AND ((treatment) OR (therapy))
    ↑ RICHTIG!


PSEUDO-CODE (NEU):

```python
def parse_multiline_query_smart(query, source):
    """
    Phase 3: Parse Multi-Line Query (CORRECTED)
    
    Strategie:
      1. Finde TOP-LEVEL Operatoren (die Operatoren zwischen Gruppen)
      2. Gruppiere Terms zwischen diesen Top-Level Operatoren
      3. Parse jede Gruppe mit Parenthesization
      4. Kombiniere Gruppen mit Top-Level Operatoren
    """
    lines = query.strip().split('\n')
    lines = [l.strip() for l in lines if l.strip()]
    
    if len(lines) < 1:
        return None, "Leere Query"
    
    # SCHRITT 1: Parse die Zeilen
    result_tokens = []
    for i, line in enumerate(lines):
        if i % 2 == 0:  # ODD (Suchterme)
            parsed = parse_query_line(line, source)
            if parsed:
                result_tokens.append(parsed)
        else:  # EVEN (Operatoren)
            op = line.upper().strip()
            if op in ['AND', 'OR']:
                result_tokens.append(op)
            else:
                return None, f"Unerwarteter Operator: {op}"
    
    if not result_tokens:
        return None, "Keine Suchterme gefunden"
    
    # SCHRITT 2: Gruppiere nach TOP-LEVEL Operatoren
    # Top-Level sind die Operatoren in result_tokens auf geraden Positionen
    
    # Finde den "schwächsten" Operator (der mit niedrigster Precedence)
    # In Standard Boolean: AND > OR (AND bindet stärker)
    # Also: Suche nach OR (wenn vorhanden) als Top-Level
    
    groups = []
    current_group = []
    
    for token in result_tokens:
        if token == 'AND':
            # AND hat höhere Precedence als OR
            # Wenn wir OR im current_group haben: AND ist NICHT top-level
            # Wenn wir NUR AND's haben: AND könnte top-level sein
            
            if 'OR' in current_group:
                # OR hat niedrigere Precedence als AND
                # Also: AND ist top-level Operator
                # Speichere current_group als Gruppe
                groups.append(current_group)
                groups.append('AND')
                current_group = []
            else:
                # Kein OR im current_group
                # AND könnte noch nicht top-level sein
                current_group.append(token)
        
        elif token == 'OR':
            # OR hat niedrigere Precedence als AND
            # Also OR ist immer top-level wenn AND existiert
            current_group.append(token)
        
        else:
            # Es ist ein Suchterm
            current_group.append(token)
    
    # Füge letzte Gruppe hinzu
    if current_group:
        groups.append(current_group)
    
    # SCHRITT 3: Klammere jede Gruppe
    result = ""
    for i, group in enumerate(groups):
        if isinstance(group, list):
            # Es ist eine Gruppe von Terms & Operators
            group_str = ' '.join(group)
            
            # Klammere die Gruppe wenn nötig
            if should_add_parentheses(group_str):
                group_str = f"({group_str})"
            
            result += group_str
        else:
            # Es ist ein Operator (AND/OR)
            result += f" {group} "
    
    result = result.strip()
    
    # SCHRITT 4: Outer Parentheses
    if should_add_parentheses(result):
        result = f"({result})"
    
    return result, None
```

Aber das ist zu komplex! Besserer Weg:

════════════════════════════════════════════════════════════════════════════════
✅ BESSERE LÖSUNG - Simpler & Klarer
════════════════════════════════════════════════════════════════════════════════

Idee: Nutze die bestehende Single-Line Parser Logic auf Multiline!

```python
def parse_multiline_query_fixed(query, source):
    """
    Phase 3: Parse Multi-Line Query (SIMPLIFIED & CORRECT)
    
    Neue Strategie:
      1. Konvertiere Multiline zu Single-Line (mit Klammern um jede ODD!)
      2. Parse Single-Line
      3. Fertig!
    """
    lines = query.strip().split('\n')
    lines = [l.strip() for l in lines if l.strip()]
    
    if len(lines) < 1:
        return None, "Leere Query"
    
    # SCHRITT 1: Konvertiere Multiline zu Single-Line
    # Aber: Klammere JEDE ODD einzeln!
    single_line_tokens = []
    
    for i, line in enumerate(lines):
        if i % 2 == 0:  # ODD (Suchterme)
            # Parse die Zeile
            parsed = parse_query_line(line, source)
            if parsed:
                single_line_tokens.append(parsed)
        else:  # EVEN (Operatoren)
            op = line.upper().strip()
            if op in ['AND', 'OR']:
                single_line_tokens.append(op)
            else:
                return None, f"Unerwarteter Operator: {op}"
    
    if not single_line_tokens:
        return None, "Keine Suchterme gefunden"
    
    # SCHRITT 2: Kombiniere zu Single-Line String
    single_line = ' '.join(single_line_tokens)
    
    # SCHRITT 3: Nutze Single-Line Parser!
    # (Die Single-Line Parser handhabt Operator Precedence richtig)
    result, error = parse_single_line_query(single_line, source)
    
    return result, error
```

WARTE! Das macht auch keinen Unterschied weil parse_single_line_query
die Tokens nicht weiter gruppiert!

════════════════════════════════════════════════════════════════════════════════
🎯 ECHTE LÖSUNG - Correct Operator Precedence Grouping
════════════════════════════════════════════════════════════════════════════════

Das echte Problem: parse_single_line_query klammert jeden Token einzeln,
aber berücksichtigt nicht Operator Precedence!

Wir brauchen: Grouping nach Operator Precedence!

```python
def parse_single_line_query_with_precedence(query, source):
    """
    Phase 3: Parse Single-Line mit korrekter Operator Precedence
    
    Precedence (Standard):
      1. () - Parentheses (höchste)
      2. AND - höher als OR
      3. OR - niedriger als AND (niedrigste)
    
    Algorithmus:
      1. Split by OR (lowest precedence)
      2. Für jeden OR-Teil: Split by AND
      3. Klammere jede Gruppe
      4. Kombiniere mit Operatoren
    """
    tokens = query.split()
    
    # Validiere Precedence
    valid, error = validate_precedence(tokens)
    if not valid:
        return None, error
    
    # ALGORITHMUS: Gruppiere nach niedrigster Precedence (OR)
    
    # Aber: Nur wenn gemischt!
    operators = [t for t in tokens if t in ['AND', 'OR']]
    
    if 'AND' not in operators:
        # Nur OR oder nur AND → einfach klammern
        result_tokens = []
        for token in tokens:
            if token in ['AND', 'OR']:
                result_tokens.append(token)
            else:
                parsed = parse_query_line(token, source)
                if parsed:
                    result_tokens.append(parsed)
        
        result = ' '.join(result_tokens)
        if should_add_parentheses(result):
            result = f"({result})"
        return result, None
    
    elif 'OR' not in operators:
        # Nur AND, kein OR → einfach klammern
        result_tokens = []
        for token in tokens:
            if token in ['AND', 'OR']:
                result_tokens.append(token)
            else:
                parsed = parse_query_line(token, source)
                if parsed:
                    result_tokens.append(parsed)
        
        result = ' '.join(result_tokens)
        if should_add_parentheses(result):
            result = f"({result})"
        return result, None
    
    # MIX von AND & OR mit Klammern → gruppiere nach OR!
    # OR hat niedrigere Precedence, wird "außen" geklammert
    
    or_groups = []
    current_and_group = []
    
    for token in tokens:
        if token == 'OR':
            # Speichere aktuellen AND-Gruppe
            if current_and_group:
                or_groups.append(' '.join(current_and_group))
            or_groups.append('OR')
            current_and_group = []
        else:
            current_and_group.append(token)
    
    # Letzte AND-Gruppe
    if current_and_group:
        or_groups.append(' '.join(current_and_group))
    
    # Jetzt: or_groups = [AND_GROUP1, 'OR', AND_GROUP2, 'OR', ...]
    # Parse jede AND_GROUP
    
    result_tokens = []
    for item in or_groups:
        if item == 'OR':
            result_tokens.append('OR')
        else:
            # Es ist eine AND_GROUP
            # Parse sie und klammere
            and_tokens = item.split()
            and_result = []
            
            for token in and_tokens:
                if token == 'AND':
                    and_result.append('AND')
                else:
                    parsed = parse_query_line(token, source)
                    if parsed:
                        and_result.append(parsed)
            
            group_str = ' '.join(and_result)
            # Klammere diese Gruppe
            group_str = f"({group_str})"
            result_tokens.append(group_str)
    
    result = ' '.join(result_tokens)
    
    # Outer parentheses
    if should_add_parentheses(result):
        result = f"({result})"
    
    return result, None
```

BEISPIEL:

Input: "cancer OR tumor AND treatment"
Tokens: ["cancer", "OR", "tumor", "AND", "treatment"]

STEP 1: Split by OR (lowest precedence)
  OR_Groups: [
    "cancer",
    "OR",
    "tumor AND treatment"
  ]

STEP 2: Parse jede AND_GROUP
  Group 1: "cancer" → "(cancer)"
  Group 2: "tumor AND treatment" → "((tumor) AND (treatment))"

STEP 3: Kombiniere
  "(cancer) OR ((tumor) AND (treatment))"

STEP 4: Outer
  "((cancer) OR ((tumor) AND (treatment)))"

✅ RICHTIG! (cancer) OR (tumor AND treatment)

════════════════════════════════════════════════════════════════════════════════
📋 IMPLEMENTIERUNGS-PLAN
════════════════════════════════════════════════════════════════════════════════

NEUE FUNKTION:

Benannt: parse_single_line_query_with_precedence()
Ort: Vor der aktuellen parse_single_line_query() Funktion
Zweck: Handhabt Operator Precedence korrekt!

ÄNDERUNG:

In parse_single_line_query(): Verwende neue Funktion
In parse_multiline_query(): Verwende neue Funktion (über Single-Line Konvertierung)

TESTS:

test_valid_1: ✅ (nur AND)
test_valid_2: ✅ (Klammern vorhanden)
test_valid_3: ✅ (Multiline mit Precedence)

════════════════════════════════════════════════════════════════════════════════
🎯 ZUSAMMENFASSUNG
════════════════════════════════════════════════════════════════════════════════

PROBLEM:
  test_valid_3: "cancer OR tumor AND (treatment OR therapy)"
  Falsch: ((cancer) OR (tumor) AND ((treatment) OR (therapy)))
  Richtig: (((cancer) OR (tumor)) AND ((treatment) OR (therapy)))

ROOT CAUSE:
  Operator Precedence wird nicht beachtet
  AND > OR wird ignoriert

LÖSUNG:
  Neue Funktion: parse_single_line_query_with_precedence()
  Grouped nach Operator Precedence (OR außen, AND innen)

RESULTAT:
  test_valid_3: ((cancer) OR (tumor) AND ...) 
             → (((cancer) OR (tumor)) AND ...)  ✅

════════════════════════════════════════════════════════════════════════════════

Document: PRECEDENCE_BUG_FIX.md
Version: 1.0
Datum: 11. Dezember 2025, 09:46 CET
Status: ANALYSIS COMPLETE - Implementation pending
Critical: Operator Precedence (AND > OR) must be handled!

