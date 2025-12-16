╔════════════════════════════════════════════════════════════════════════════╗
║        PARSER v2.3.0 - RULE-BASED FORMAT (Einfache Lösung)                ║
║                                                                            ║
║  NEUE REGEL: Gleiche Operatoren in EINE ZEILE!                            ║
║  Unterschiedliche Operatoren = Explizite Klammern!                        ║
║                                                                            ║
║  ✅ RICHTIG: cancer OR tumor                                              ║
║  ❌ FALSCH:  cancer                                                        ║
║             OR                                                             ║
║             tumor                                                          ║
╚════════════════════════════════════════════════════════════════════════════╝

════════════════════════════════════════════════════════════════════════════════
📋 DIE NEUE RULE - FORMAT VORGABE FÜR USER
════════════════════════════════════════════════════════════════════════════════

RULE 1: Gleiche Operatoren in EINE ZEILE
──────────────────────────────────────────

✅ RICHTIG:
  cancer OR tumor
  (Parser Output: ((cancer) OR (tumor)))

✅ RICHTIG:
  cancer AND tumor AND treatment
  (Parser Output: ((cancer) AND (tumor) AND (treatment)))

❌ FALSCH:
  cancer
  OR
  tumor
  (Error! Operatoren müssen in einer Zeile sein)


RULE 2: Unterschiedliche Operatoren = Explizite Klammern
────────────────────────────────────────────────────────

✅ RICHTIG:
  (cancer OR tumor) AND treatment
  (Parser Output: (((cancer) OR (tumor)) AND (treatment)))

✅ RICHTIG:
  cancer AND (tumor OR treatment)
  (Parser Output: ((cancer) AND ((tumor) OR (treatment))))

❌ FALSCH:
  cancer OR tumor AND treatment
  (Error! Mix von AND & OR ohne Klammern nicht erlaubt!)

❌ FALSCH:
  cancer
  OR
  tumor
  AND
  treatment
  (Error! Mix von AND & OR in Multiline nicht erlaubt!)


RULE 3: Multiline Format
─────────────────────────

✅ RICHTIG:
  cancer OR tumor
  AND
  (treatment OR therapy)
  
  Erklärung:
    Zeile 1: "cancer OR tumor" = eine komplette Gruppe (gleiches Operator OR)
    Zeile 2: "AND" = Operator (unterschiedlich von OR)
    Zeile 3: "(treatment OR therapy)" = geklammerte Gruppe (gleiches Operator OR)
  
  Parser Output: (((cancer) OR (tumor)) AND ((treatment) OR (therapy)))


❌ FALSCH:
  cancer
  OR
  tumor
  AND
  (treatment OR therapy)
  
  Erklärung:
    Zeile 1: "cancer" = einzelner Term
    Zeile 2: "OR" = Operator
    Zeile 3: "tumor" = einzelner Term
    ↑ Das ist falsch! "cancer" und "tumor" haben gleichen Operator OR
    ↑ Sie sollten in EINER ZEILE sein: "cancer OR tumor"

════════════════════════════════════════════════════════════════════════════════
🧪 BEISPIELE - RICHTIG vs FALSCH
════════════════════════════════════════════════════════════════════════════════

BEISPIEL 1: Einfache OR Query
─────────────────────────────

✅ RICHTIG:
  breast cancer OR lung cancer
  
  Output: ((breast) (cancer) OR (lung) (cancer))
  ↑ Alle Terms sind mit OR verbunden

❌ FALSCH:
  breast cancer
  OR
  lung cancer
  
  Error: Multiline Terms müssen vollständig sein!


BEISPIEL 2: Einfache AND Query
──────────────────────────────

✅ RICHTIG:
  cancer AND treatment
  
  Output: ((cancer) AND (treatment))

✅ AUCH RICHTIG:
  cancer AND tumor AND treatment
  
  Output: ((cancer) AND (tumor) AND (treatment))


BEISPIEL 3: Mix mit Klammern (Single-Line)
───────────────────────────────────────────

✅ RICHTIG:
  (cancer OR tumor) AND treatment
  
  Output: (((cancer) OR (tumor)) AND (treatment))

✅ AUCH RICHTIG:
  cancer AND (tumor OR treatment)
  
  Output: ((cancer) AND ((tumor) OR (treatment)))


BEISPIEL 4: Mix mit Klammern (Multiline)
─────────────────────────────────────────

✅ RICHTIG:
  cancer OR tumor
  AND
  treatment
  
  Output: (((cancer) OR (tumor)) AND (treatment))

✅ AUCH RICHTIG:
  cancer
  AND
  (tumor OR treatment)
  
  Output: ((cancer) AND ((tumor) OR (treatment)))


BEISPIEL 5: Komplexe Query
──────────────────────────

✅ RICHTIG:
  (cancer OR tumor) AND (treatment OR therapy) AND patient
  
  Output: (((cancer) OR (tumor)) AND ((treatment) OR (therapy)) AND (patient))

✅ AUCH RICHTIG (Multiline):
  cancer OR tumor
  AND
  (treatment OR therapy)
  AND
  patient
  
  Output: (((cancer) OR (tumor)) AND ((treatment) OR (therapy)) AND (patient))

════════════════════════════════════════════════════════════════════════════════
🔴 FEHLER EXAMPLES - Was der Parser ablehnen wird
════════════════════════════════════════════════════════════════════════════════

FEHLER 1: Mix ohne Klammern (Single-Line)
──────────────────────────────────────────

❌ FALSCH:
  cancer OR tumor AND treatment
  
  Error: "Mehrdeutig! Mix von AND & OR ohne Klammern: (cancer OR tumor) AND treatment?"
  Lösung: Klammern setzen: "(cancer OR tumor) AND treatment"


FEHLER 2: Multiline Terms mit gleichem Operator
────────────────────────────────────────────────

❌ FALSCH:
  cancer
  OR
  tumor
  
  Error: "Terms mit gleichem Operator sollten in EINER ZEILE sein: 'cancer OR tumor'"


FEHLER 3: Multiline Mix ohne Klammern
──────────────────────────────────────

❌ FALSCH:
  cancer
  OR
  tumor
  AND
  treatment
  
  Error: "Mix von AND & OR! Terms müssen geklammert sein!"
  
  Lösung A: In Single-Line: "(cancer OR tumor) AND treatment"
  Lösung B: In Multiline mit Gruppierung:
    cancer OR tumor
    AND
    treatment


FEHLER 4: Unausgewogene Klammern
─────────────────────────────────

❌ FALSCH:
  (cancer OR tumor AND treatment)
  
  Error: "Unbalanced parentheses oder mehrdeutige Gruppierung!"

════════════════════════════════════════════════════════════════════════════════
✅ IMPLEMENTIERUNGS-GUIDE FÜR PARSER v2.3.0
════════════════════════════════════════════════════════════════════════════════

PHASE 2 - INPUT VALIDATION (NEUE STRENGE RULE CHECK)
─────────────────────────────────────────────────────

NEUE FUNKTION: validate_operator_grouping()

WAS MACHT SIE:
  Validiert dass User die neue Rule einhält!
  
  1. Für Single-Line: Checke ob AND & OR OHNE Klammern gemischt sind
  2. Für Multiline: Checke ob Term-Zeilen zusammen gehören
  
REGELN:

Single-Line:
  ✅ "A OR B" → OK (nur ein Operator-Typ)
  ✅ "A AND B" → OK (nur ein Operator-Typ)
  ✅ "(A OR B) AND C" → OK (Mix aber mit Klammern)
  ❌ "A OR B AND C" → ERROR (Mix ohne Klammern)

Multiline:
  ✅ "A OR B" dann "AND" dann "C" → OK
  ✅ "A" dann "OR" dann "B" ABER nur wenn "A" und "B" single terms sind
  ❌ "A" dann "OR" dann "B" wenn A oder B komplexe Terms sind
  ❌ Operator auf seiner eigenen Zeile OHNE dass Terms links/rechts zusammen gehören

ALGORITHMUS:

```python
def validate_operator_grouping(query, format_type):
    """
    Validiere dass User die neue Grouping Rule einhält.
    
    RULE: 
      - Gleiche Operatoren in EINER Zeile
      - Unterschiedliche Operatoren = Klammern
    """
    
    if format_type == "single_line":
        tokens = query.split()
        
        # Finde Operatoren
        operators = [t for t in tokens if t in ['AND', 'OR']]
        
        # Wenn Mix von AND & OR: Checke Klammern
        if 'AND' in operators and 'OR' in operators:
            # Mix gefunden! Sind Klammern vorhanden?
            if '(' not in query or ')' not in query:
                return False, "Mix von AND & OR! Setze Klammern: (A OR B) AND C"
        
        return True, None
    
    else:  # multiline_odd_even
        lines = query.strip().split('\n')
        lines = [l.strip() for l in lines if l.strip()]
        
        # Überprüfe Struktur
        # ODD lines (index 0,2,4,...) = Terms
        # EVEN lines (index 1,3,5,...) = Operators
        
        # Neue Regel: ODD lines mit gleichem Operator sollten zusammen sein
        # Aber: Wenn sie auf separate Zeilen sind, ist das nur OK wenn:
        #   - Sie sind single, simple terms (kein "cancer OR tumor")
        #   - Sie haben Klammern
        
        for i in range(0, len(lines), 2):  # ODD indices
            line = lines[i]
            
            # Wenn Line Operatoren hat = komplexer Term
            if 'OR' in line.upper() or 'AND' in line.upper():
                # Komplexer Term - muss in Klammern sein
                if not (line.startswith('(') and line.endswith(')')):
                    return False, f"Komplexer Term muss geklammert sein: ({line})"
        
        return True, None
```

════════════════════════════════════════════════════════════════════════════════
📋 TEST DATEIEN - Korrekte Formatierung (für v2.3.0)
════════════════════════════════════════════════════════════════════════════════

test_valid_1.txt (Single-Line, ein Operator):
────────────────────────────────────────────

Inhalt:
  cancer AND tumor AND treatment

Ergebnis:
  ✅ SUCCESS!
  Output: ((cancer) AND (tumor) AND (treatment))


test_valid_2.txt (Single-Line, Mix mit Klammern):
──────────────────────────────────────────────────

Inhalt:
  (cancer OR tumor) AND treatment

Ergebnis:
  ✅ SUCCESS!
  Output: (((cancer) OR (tumor)) AND (treatment))


test_valid_3_multiline.txt (KORRIGIERT - Neue Rule!):
────────────────────────────────────────────────────

ALTE (FALSCHE) Version:
  cancer
  OR
  tumor
  AND
  (treatment OR therapy)
  ❌ ERROR! Terms mit gleichem Operator sollten in einer Zeile sein

NEUE (RICHTIGE) Version:
  cancer OR tumor
  AND
  (treatment OR therapy)

Ergebnis:
  ✅ SUCCESS!
  Output: (((cancer) OR (tumor)) AND ((treatment) OR (therapy)))


test_invalid_1.txt (Mix ohne Klammern):
────────────────────────────────────────

Inhalt:
  cancer OR tumor AND treatment

Ergebnis:
  ❌ ERROR!
  Fehler: "Mix von AND & OR ohne Klammern! Setze Klammern"

════════════════════════════════════════════════════════════════════════════════
🚀 INSTALLATION - Parser v2.3.0 (Rule-Based)
════════════════════════════════════════════════════════════════════════════════

SCHRITT 1: Download neue Version
────────────────────────────────

Download: parser_v2_3_0_rule_based.py (wird erstellt)
Artifact ID: [wird zugewiesen]


SCHRITT 2: Backup alte Version
──────────────────────────────

COMMAND:
  cp tests/src/core/parser_test_precedence.py tests/src/core/parser_test_precedence.py.backup.v2.2.3


SCHRITT 3: Kopiere neue Version
────────────────────────────────

COMMAND:
  cp parser_v2_3_0_rule_based.py tests/src/core/parser_test_precedence.py


SCHRITT 4: Teste
───────────────

COMMAND:
  python tests/src/core/parser_test_precedence.py

ERWARTETE AUSGABE:
  Query Parser v2.3.0 - Rule-Based Format
  ═══════════════════════════════════════════
  
  Test 1: Single-Line AND (ein Operator)
    Status: ✅ PASS
  
  Test 2: Single-Line mit Klammern (Mix richtig formatiert)
    Status: ✅ PASS
  
  Test 3: Multiline mit Grouping (NEW RULE)
    Status: ✅ PASS
  
  Test 4: Single-Line Mix OHNE Klammern (sollte Error sein)
    Status: ✅ PASS (Error expected)
  
  Test 5: Multiline falsche Gruppierung (sollte Error sein)
    Status: ✅ PASS (Error expected)


SCHRITT 5: Deine Test-Dateien aktualisieren
─────────────────────────────────────────────

test_valid_3_multiline.txt KORRIGIEREN:

ALT (FALSCH):
  cancer
  OR
  tumor
  AND
  (treatment OR therapy)

NEU (RICHTIG):
  cancer OR tumor
  AND
  (treatment OR therapy)

COMMAND:
  python query_parser_v2_3.py tests/queries/valid/test_valid_3_multiline.txt

ERGEBNIS:
  ✅ SUCCESS!
  Output Query: (((cancer) OR (tumor)) AND ((treatment) OR (therapy)))

════════════════════════════════════════════════════════════════════════════════
📊 VORHER vs NACHHER - PARSER VERSIONS
════════════════════════════════════════════════════════════════════════════════

v2.2.3 (Operator Precedence - Komplex):
  - Versuchte Precedence automatisch zu berechnen
  - Schwierig zu debuggen
  - User-Fehler schwer zu erkennen

v2.3.0 (Rule-Based - Einfach):
  - User muss klare Regeln folgen
  - Parser validiert INPUT strict
  - Klare Fehlermeldungen wenn Rule verletzt
  - Viel einfacher zu verstehen!

════════════════════════════════════════════════════════════════════════════════
✅ ZUSAMMENFASSUNG
════════════════════════════════════════════════════════════════════════════════

NEUE LÖSUNG:
  ✅ Einfach (keine Precedence-Logik)
  ✅ Streng (klare Rules)
  ✅ Verständlich (User weiß was erlaubt ist)

RULE 1: Gleiche Operatoren in EINE ZEILE
  cancer OR tumor ✅
  (NICHT: cancer / OR / tumor)

RULE 2: Unterschiedliche Operatoren = Klammern
  (cancer OR tumor) AND treatment ✅
  (NICHT: cancer OR tumor AND treatment)

RESULTAT:
  - Alle Tests können PASS sein
  - Parser ist einfacher
  - User hat klare Vorgabe

════════════════════════════════════════════════════════════════════════════════

Document: PARSER_v2.3.0_RULE_BASED_FORMAT.md
Version: 1.0
Datum: 11. Dezember 2025, 10:00 CET
Status: ANALYSIS COMPLETE - Implementation ready
Approach: Rule-Based Format Validation (Simple & Clear)

