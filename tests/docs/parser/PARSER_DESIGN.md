╔════════════════════════════════════════════════════════════════════════════╗
║                    QUERY PARSER v2.2 - DESIGN GUIDE                        ║
║                  Ausführlich kommentiert für Laien                          ║
║                                                                            ║
║  Ein Leitfaden zum Verstehen, wie der Query Parser funktioniert            ║
╚════════════════════════════════════════════════════════════════════════════╝

════════════════════════════════════════════════════════════════════════════════
INHALTSVERZEICHNIS
════════════════════════════════════════════════════════════════════════════════

1. EINLEITUNG - Was ist der Query Parser?
2. GROSSES KONZEPT - Überblick
3. PHASE 1 - Cleaning & Format Detection (Bereinigung & Formatererkennung)
4. PHASE 2 - Operator Precedence Validation (Operatoren-Vorrang-Validierung)
5. PHASE 3 - Parsing & Parenthesization (Parsing & Klammerung)
6. PHASE 4 - Date Formatting & Source Conversion (Datumformat & Quellenkonvertierung)
7. ZUSAMMENFASSUNG - Alles zusammen
8. BEISPIELE - Praktische Anwendung

════════════════════════════════════════════════════════════════════════════════
1. EINLEITUNG - Was ist der Query Parser?
════════════════════════════════════════════════════════════════════════════════

Stell dir vor, du möchtest in einer medizinischen Datenbank nach "Krebs" UND
"Tumor" suchen. Du gibst ein:

  cancer AND tumor

Der Query Parser macht aus dieser einfachen Eingabe etwas, das die Datenbank
wirklich verstehen kann:

  ((cancer) AND (tumor))

Aber der Parser macht VIEL mehr als nur Klammern hinzufügen. Er:
  1. Bereinigt deine Eingabe (entfernt Kommentare, Leerzeilen)
  2. Prüft ob deine Query mehrdeutig ist (z.B. "A OR B AND C")
  3. Fügt intelligente Klammern hinzu
  4. Konvertiert Datumsformate für verschiedene Datenbanken
  5. Formatiert die Query für PubMed oder Europe PMC

ANALOGE ERKLÄRUNG:
─────────────────
Stell dir vor, ein Schüler schreibt eine Hausaufgabe auf:

  Input: "Find cancer OR tumor AND (treatment OR therapy)
          # with 2015-2020 date range"

Der Parser ist wie ein Lehrer, der:
  1. Die Hausaufgabe korrigiert (entfernt Kommentare)
  2. Prüft ob die Anfrage sinnvoll ist (keine Widersprüche)
  3. Macht die Struktur klar (Klammern)
  4. Konvertiert für verschiedene Formate (PubMed vs Europe PMC)

════════════════════════════════════════════════════════════════════════════════
2. GROSSES KONZEPT - Überblick
════════════════════════════════════════════════════════════════════════════════

DER PARSER FUNKTIONIERT NACH DEM "PIPELINE"-PRINZIP:

  Rohe Eingabe
       ↓
   [PHASE 1] Cleaning & Format Detection
       ↓ (Bereinigte Query + Format erkannt)
   [PHASE 2] Operator Precedence Validation
       ↓ (Validierung: Mehrdeutig oder OK?)
   [PHASE 3] Parsing & Parenthesization
       ↓ (Gekammerte, strukturierte Query)
   [PHASE 4] Date Formatting & Source Conversion
       ↓
  Finale Query (PubMed oder Europe PMC Format)


WAS JEDE PHASE MACHT:
─────────────────────

PHASE 1: Aufräumen
  Input:  "cancer OR tumor  # this is a comment
           
           another query"
  Output: "cancer OR tumor\nanother query"
  
  Warum? → Datenbanken verstehen Kommentare nicht

PHASE 2: Sicherheitsprüfung
  Input:  "cancer OR tumor AND treatment"
  Output: ❌ FEHLER! (Mehrdeutig - weiß nicht ob (A OR B) AND C oder A OR (B AND C))
  
  Input:  "(cancer OR tumor) AND treatment"
  Output: ✅ OK! (Klammern machen es eindeutig)
  
  Warum? → Verhindert dass die Datenbank falsch versteht

PHASE 3: Strukturieren
  Input:  "cancer AND tumor"
  Output: "((cancer) AND (tumor))"
  
  Warum? → Datenbanken mögen klare Struktur

PHASE 4: Konvertierung
  Input:  "((cancer) AND (tumor)) mit Datum 2015-2020"
  Output (PubMed):      "((cancer) AND (tumor)) AND (2015:2020[pdat])"
  Output (Europe PMC):  "((cancer) AND (tumor)) AND (FIRST_PDATE:[2015 TO 2020])"
  
  Warum? → Verschiedene Datenbanken sprechen verschiedene "Sprachen"

════════════════════════════════════════════════════════════════════════════════
3. PHASE 1 - CLEANING & FORMAT DETECTION
   (Bereinigung & Formatererkennung)
════════════════════════════════════════════════════════════════════════════════

AUFGABE: Aufräumen und Format erkennen

Die rohe Eingabe kann messy sein:
  • Kommentare (# Das ist unwichtig)
  • Leerzeilen
  • Zu viele Abstände
  • Verschiedene Formate (Single-Line vs Multi-Line)

Die Phase räumt auf und erkennt das Format.

BEISPIEL 1: Single-Line Format
──────────────────────────────

Input:
  cancer OR tumor AND treatment

Phase 1 Prozess:
  1. Lese Zeile für Zeile
  2. Entferne Kommentare (Text nach #)
  3. Entferne leere Zeilen
  4. Zähle wie viele Zeilen übrig sind
  
Ergebnis:
  ✓ Format erkannt: "single-line"
  ✓ Bereinigte Query: "cancer OR tumor AND treatment"

BEISPIEL 2: Multi-Line Format mit Kommentaren
──────────────────────────────────────────────

Input:
  cancer       # Was wir suchen
  OR
  tumor        # Synonym
  AND
  treatment    # Therapie

Phase 1 Prozess:
  1. Lese jede Zeile
  2. Entferne "# Was wir suchen" → "cancer"
  3. Entferne "# Synonym" → "tumor"
  4. Entferne "# Therapie" → "treatment"
  5. Entferne leere Zeilen
  6. Zähle übrige Zeilen: 5 (ODD + EVEN Format erkannt)

Ergebnis:
  ✓ Format erkannt: "multi-line"
  ✓ Bereinigte Query:
      cancer
      OR
      tumor
      AND
      treatment

ODD/EVEN FORMAT ERKLÄRUNG:
─────────────────────────

Multi-Line muss einem bestimmten Muster folgen:

  Zeile 1 (ODD):   cancer        ← Ein Such-Begriff
  Zeile 2 (EVEN):  OR            ← Ein Operator
  Zeile 3 (ODD):   tumor         ← Ein Such-Begriff
  Zeile 4 (EVEN):  AND           ← Ein Operator
  Zeile 5 (ODD):   treatment     ← Ein Such-Begriff

Die Regel ist:
  • UNGERADE Zeilen (1, 3, 5) = Such-Begriffe (Queries)
  • GERADE Zeilen (2, 4, 6) = Operatoren (AND, OR, NOT)

WARUM dieses Muster?
  → Macht klar was Operator ist und was Query
  → Keine mehrdeutigen Strukturen möglich
  → Parser weiß immer: Zeile 5 = nächster Operator kommt

CODE-BEISPIEL:
──────────────

def clean_query(raw_query: str) -> str:
    """Entfernt Kommentare und Leerzeilen"""
    
    lines = raw_query.split('\n')      # Teile in Zeilen
    cleaned_lines = []
    
    for line in lines:
        # Entferne Kommentare (alles nach #)
        if '#' in line:
            line = line[:line.index('#')]   # Schneide ab bei #
        
        line = line.strip()             # Entferne Anfangs-/Endleerzeichen
        
        if line:                        # Nur nicht-leere Zeilen
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)     # Verbinde zurück

════════════════════════════════════════════════════════════════════════════════
4. PHASE 2 - OPERATOR PRECEDENCE VALIDATION
   (Operatoren-Vorrang-Validierung)
════════════════════════════════════════════════════════════════════════════════

AUFGABE: Sicherstellen dass die Query eindeutig ist

PROBLEM DAS WIR VERHINDERN:
──────────────────────────

Stell dir vor dein Mathelehrer schreibt:

  2 + 3 * 4

Ist das:
  (2 + 3) * 4 = 5 * 4 = 20  ?  ODER
  2 + (3 * 4) = 2 + 12 = 14  ?

Das ist MEHRDEUTIG! Deshalb gibt es Regeln für Operatoren-Vorrang (Precedence).

GLEICHES PROBLEM BEI QUERIES:
────────────────────────────

cancer OR tumor AND treatment

Ist das:
  (cancer OR tumor) AND treatment  ?  ODER
  cancer OR (tumor AND treatment)  ?

→ Das ist MEHRDEUTIG!

LÖSUNG: KLAMMERN ERZWINGEN
──────────────────────────

Wenn die Query mehrdeutig ist, sagen wir:

  ❌ FALSCH: "cancer OR tumor AND treatment"
  
  ✅ RICHTIG: "(cancer OR tumor) AND treatment"
  ODER
  ✅ RICHTIG: "cancer OR (tumor AND treatment)"

ERLAUBTE MUSTER:
────────────────

✅ NUR AND:
   cancer AND tumor AND treatment
   → Kein Mehrdeutig-Problem (ANDs sind alle gleich)

✅ NUR OR:
   cancer OR tumor OR treatment
   → Kein Mehrdeutig-Problem (ORs sind alle gleich)

✅ GEMISCHT ABER GEKLAMMERT:
   (cancer OR tumor) AND treatment
   → Klammern lösen die Mehrdeutigkeit

✅ MULTI-LINE:
   cancer
   OR
   tumor
   AND
   treatment
   → Multi-Line Format ERZWINGT Eindeutigkeit!

❌ GEMISCHT OHNE KLAMMERN:
   cancer OR tumor AND treatment
   → FEHLER! Mehrdeutig!

CODE-BEISPIEL:
──────────────

def has_mixed_operators(query: str) -> bool:
    """Prüft ob Query mehrdeutige Operatoren hat"""
    
    # Entferne alle geklammerten Teile
    # z.B. "A OR (B AND C)" → "A OR "
    cleaned = re.sub(r'\([^)]+\)', '', query)
    
    # Prüfe welche Operatoren noch vorhanden sind
    has_and = 'AND' in cleaned.upper()
    has_or = 'OR' in cleaned.upper()
    has_not = 'NOT' in cleaned.upper()
    
    # Wenn mehr als 1 Operator-Typ: MEHRDEUTIG!
    operator_count = sum([has_and, has_or, has_not])
    
    return operator_count > 1  # True = Fehler!

════════════════════════════════════════════════════════════════════════════════
5. PHASE 3 - PARSING & PARENTHESIZATION
   (Parsing & Klammerung)
════════════════════════════════════════════════════════════════════════════════

AUFGABE: Die Query in eine strukturierte Form bringen (mit Klammern)

SCHRITT-FÜR-SCHRITT ERKLÄRUNG:
───────────────────────────────

Input Query:
  cancer AND tumor AND treatment

Schritt 1: Tokenisieren (in Teile aufteilen)
  
  Query = "cancer AND tumor AND treatment"
  
  Split nach Operatoren:
    Terms:     ["cancer", "tumor", "treatment"]
    Operators: ["AND", "AND"]

Schritt 2: Jeden Term in Klammern wickeln
  
  cancer       → (cancer)
  tumor        → (tumor)
  treatment    → (treatment)

Schritt 3: Mit Operatoren wieder zusammenbauen
  
  (cancer) AND (tumor) AND (treatment)

Schritt 4: Alles in äußere Klammern wickeln
  
  ((cancer) AND (tumor) AND (treatment))

VISUELL:
────────

Input:  cancer AND tumor
        ↓
        Tokenize:
        Terms: ["cancer", "tumor"]
        Operators: ["AND"]
        ↓
        Wrap terms:
        ["(cancer)", "(tumor)"]
        ↓
        Combine:
        (cancer) AND (tumor)
        ↓
        Final:
        ((cancer) AND (tumor))

WARUM DOPPELTE KLAMMERN?
────────────────────────

Äußere Klammern = Parser-Wrapping (sagt "das ist eine komplette Query")
Innere Klammern = Term-Wrapping (sagt "das ist ein einzelner Suchbegriff")

((cancer) AND (tumor))
│└─ Innere: Jeden Term schützen
└──── Äußere: Ganze Query schützen

KOMPLEXERES BEISPIEL - Multi-Line:
───────────────────────────────────

Input:
  cancer
  OR
  tumor

Schritt 1: Parse Zeile 1 (ODD)
  Line = "cancer"
  Result = "(cancer)"

Schritt 2: Operator Zeile 2 (EVEN)
  Line = "OR"
  Result = " OR "

Schritt 3: Parse Zeile 3 (ODD)
  Line = "tumor"
  Result = "(tumor)"

Schritt 4: Zusammenbauen
  (cancer) OR (tumor)

Schritt 5: Final wrapping
  ((cancer) OR (tumor))

CODE-BEISPIEL:
──────────────

def parse_simple_query(query: str) -> str:
    """Parst Single-Line Query"""
    
    # Schritt 1: Tokenisieren
    terms, operators = tokenize_by_operators(query)
    # terms = ["cancer", "tumor"]
    # operators = ["AND"]
    
    # Schritt 2: Jeden Term wickeln
    wrapped_terms = [f"({term})" for term in terms]
    # wrapped_terms = ["(cancer)", "(tumor)"]
    
    # Schritt 3: Wieder zusammenbauen
    result = wrapped_terms[0]
    for i, operator in enumerate(operators):
        result += f" {operator} {wrapped_terms[i + 1]}"
    # result = "(cancer) AND (tumor)"
    
    # Schritt 4: Äußere Klammern
    return f"({result})"
    # return "((cancer) AND (tumor))"

════════════════════════════════════════════════════════════════════════════════
6. PHASE 4 - DATE FORMATTING & SOURCE CONVERSION
   (Datumformat & Quellenkonvertierung)
════════════════════════════════════════════════════════════════════════════════

AUFGABE: Datumsangaben konvertieren und für verschiedene Datenbanken formatieren

PROBLEM:
────────

Verschiedene Datenbanken sprechen verschiedene "Sprachen":

PubMed möchte: (2015:2020[pdat])
Europe PMC möchte: (FIRST_PDATE:[2015 TO 2020])

Der Parser muss dasselbe Datum für beide übersetzen können!

SCHRITT 1: DATUMSBEREICH ERKENNEN
──────────────────────────────────

Die Query könnte enthalten:
  "cancer 2015-2020"
  
Der Parser sucht nach diesem Muster:
  YYYY-YYYY
  
Also: 4-stellige Zahl, Bindestrich, 4-stellige Zahl

BEISPIEL:
  Input: "cancer with 2015-2020 data"
  Erkannt: Datumsbereich = "2015-2020"
  Übrig: "cancer with data"

CODE:
  pattern = r'(\d{4})-(\d{4})'  # Regex: 4 Ziffern - 4 Ziffern
  match = re.search(pattern, query)
  if match:
      start_year = match.group(1)  # 2015
      end_year = match.group(2)    # 2020

SCHRITT 2: KONVERTIEREN FÜR VERSCHIEDENE QUELLEN
──────────────────────────────────────────────────

Wenn wir "2015-2020" erkannt haben:

FÜR PubMed:
  (2015:2020[pdat])
  
  Logik:
    • Start:Endjahr Doppelpunkt)
    • [pdat] = "publication date" (PubMed Syntax)

FÜR Europe PMC:
  (FIRST_PDATE:[2015 TO 2020])
  
  Logik:
    • FIRST_PDATE = Feld für Veröffentlichungsdatum
    • [2015 TO 2020] = Range Syntax

CODE-BEISPIEL:
──────────────

class DateFormatConverter:
    def __init__(self, source: str):
        self.source = source  # "pubmed" oder "europepmc"
    
    def convert_date_format(self, date_range: str) -> str:
        """Konvertiert "2015-2020" zu source-spezifischem Format"""
        
        start_year, end_year = date_range.split('-')
        
        if self.source == "pubmed":
            # PubMed Format
            return f"({start_year}:{end_year}[pdat])"
        
        elif self.source == "europepmc":
            # Europe PMC Format
            return f"(FIRST_PDATE:[{start_year} TO {end_year}])"

KOMPLETTES BEISPIEL:
───────────────────

Input Query:
  cancer AND tumor 2015-2020

Phase 4 Prozess:
  
  1. Erkenne Datum: "2015-2020"
  2. Entferne Datum aus Query: "cancer AND tumor"
  
  3. Konvertiere für PubMed:
     ((cancer) AND (tumor)) AND (2015:2020[pdat])
  
  4. Konvertiere für Europe PMC:
     ((cancer) AND (tumor)) AND (FIRST_PDATE:[2015 TO 2020])

════════════════════════════════════════════════════════════════════════════════
7. ZUSAMMENFASSUNG - Alles zusammen
════════════════════════════════════════════════════════════════════════════════

DIE 4 PHASEN ALS METAPHER:
──────────────────────────

Stell dir vor, du möchtest eine Brief an verschiedene Länder schreiben:

PHASE 1 - Aufräumen (Handschrift verbessern)
  Dein Brief:  "Find cancer
                # ignore this
                OR tumor"
  Resultat:    "Find cancer OR tumor"
  
PHASE 2 - Validierung (Grammatik prüfen)
  Dein Brief:  "Find cancer OR tumor AND treatment"
  Parser:      "Das ist mehrdeutig! Setze Klammern!"
  
PHASE 3 - Strukturieren (Struktur klären)
  Dein Brief:  "cancer OR tumor"
  Resultat:    "((cancer) OR (tumor))"
  
PHASE 4 - Übersetzung (für verschiedene Länder)
  Für USA:       "((cancer) OR (tumor)) with dates 2015-2020"
  Für England:   "((cancer) OR (tumor)) dated between 2015 and 2020"

DATENFLUSS:
───────────

Rohe Input
    ↓
PHASE 1: Cleaning
    Input: "cancer # comment\n\nOR tumor"
    Output: "cancer OR tumor"
    ↓
PHASE 2: Validierung
    Input: "cancer OR tumor"
    Output: ✅ Valid (nur OR)
    ↓
PHASE 3: Parsing
    Input: "cancer OR tumor"
    Output: "((cancer) OR (tumor))"
    ↓
PHASE 4: Konvertierung
    Input: "((cancer) OR (tumor)) 2015-2020"
    Output (PubMed): "((cancer) OR (tumor)) AND (2015:2020[pdat])"
    Output (Europe PMC): "((cancer) OR (tumor)) AND (FIRST_PDATE:[2015 TO 2020])"

════════════════════════════════════════════════════════════════════════════════
8. BEISPIELE - Praktische Anwendung
════════════════════════════════════════════════════════════════════════════════

BEISPIEL 1: Einfache Single-Line Query
───────────────────────────────────────

Input:
  cancer AND tumor

Phase 1 Output:
  Format: "single-line"
  Query: "cancer AND tumor"

Phase 2 Output:
  Status: ✅ Valid (nur AND Operatoren)

Phase 3 Output:
  ((cancer) AND (tumor))

Phase 4 Output (PubMed):
  ((cancer) AND (tumor))

Phase 4 Output (Europe PMC):
  ((cancer) AND (tumor))


BEISPIEL 2: Geklammerte Query mit mehreren Operatoren
──────────────────────────────────────────────────────

Input:
  (cancer OR tumor) AND treatment

Phase 1 Output:
  Format: "single-line"
  Query: "(cancer OR tumor) AND treatment"

Phase 2 Output:
  Status: ✅ Valid (geklammert, eindeutig)

Phase 3 Output:
  (((cancer) OR (tumor)) AND (treatment))
  
  Erklärung:
    (cancer) OR (tumor)          ← Inner-Klammern für Begriffe
    │└────────────────────┘
    └─ Äußere Klammern für Gruppe
    
    ((cancer) OR (tumor)) AND (treatment)
    │  │└──── Innere Begriffe
    │  └────── Gruppe-Klammern
    └────────── Final-Klammern

Phase 4 Output (PubMed):
  (((cancer) OR (tumor)) AND (treatment))


BEISPIEL 3: Multi-Line mit Datum
─────────────────────────────────

Input:
  cancer
  OR
  tumor
  AND
  (treatment OR therapy)
  2015-2020

Phase 1 Output:
  Format: "multi-line"
  Query: 
    cancer
    OR
    tumor
    AND
    (treatment OR therapy)

Phase 2 Output:
  Status: ✅ Valid (ODD/EVEN Format)

Phase 3 Output:
  (cancer) OR (tumor) AND (((treatment) OR (therapy)))
  
  ⚠️  Hinweis: Das ist über-geklammert!
  Sollte sein: ((cancer) OR (tumor)) AND ((treatment) OR (therapy))
  (Siehe KNOWN_ISSUES.md für Fix)

Phase 4 Output (PubMed):
  (cancer) OR (tumor) AND (((treatment) OR (therapy))) AND (2015:2020[pdat])

Phase 4 Output (Europe PMC):
  (cancer) OR (tumor) AND (((treatment) OR (therapy))) AND (FIRST_PDATE:[2015 TO 2020])


BEISPIEL 4: ❌ FEHLER - Mehrdeutige Query
──────────────────────────────────────────

Input:
  cancer OR tumor AND treatment

Phase 1 Output:
  Format: "single-line"
  Query: "cancer OR tumor AND treatment"

Phase 2 Output:
  ❌ FEHLER!
  
  Message:
    "Mehrdeutige Operatoren: AND + OR
    
    Problem: Gemischte Operatoren ohne Klammern!
    
    Beispiele für Lösungen:
    ✓ (cancer OR tumor) AND treatment
    ✓ cancer OR (tumor AND treatment)"

Der Parser stoppt hier und gibt Fehler aus!

════════════════════════════════════════════════════════════════════════════════
SCHNELLE REFERENZ - Die wichtigsten Konzepte
════════════════════════════════════════════════════════════════════════════════

TERM (Suchbegriff):
  Einzelne Wörter wie "cancer", "tumor", "(treatment OR therapy)"

OPERATOR:
  Verknüpfungswörter: AND, OR, NOT
  
PRECEDENCE (Vorrang):
  AND hat höheren Vorrang als OR in Mathematik
  Aber: Wir verhindern Mehrdeutigkeit durch Klammern!

PARENTHESES (Klammern):
  () macht Struktur deutlich und verhindert Mehrdeutigkeit

SINGLE-LINE:
  Alles in einer Zeile: "cancer AND tumor"

MULTI-LINE (ODD/EVEN):
  Mehrere Zeilen mit alternierenden Queries und Operatoren:
    Zeile 1: cancer    (ODD - Query)
    Zeile 2: AND       (EVEN - Operator)
    Zeile 3: tumor     (ODD - Query)

════════════════════════════════════════════════════════════════════════════════
HÄUFIG GESTELLTE FRAGEN
════════════════════════════════════════════════════════════════════════════════

F: Warum so viele Klammern?
A: Klammern machen die Struktur eindeutig. Die Datenbank kann nicht
   raten, was gemeint ist. Mit Klammern ist alles klar!

F: Warum NOT "A AND B"?
A: Das ist mehrdeutig! Ist NOT(A AND B) oder (NOT A) AND B?
   Besser: NOT (A AND B) oder (NOT A) AND B mit Klammern.

F: Warum verschiedene Formate für verschiedene Datenbanken?
A: Jede Datenbank hat ihre eigene "Sprache". PubMed und Europe PMC
   sprechen unterschiedliche Syntax. Phase 4 macht die Übersetzung.

F: Was passiert wenn ich etwas Falsches eingebe?
A: Der Parser gibt eine klare Fehlermeldung und stoppt.
   Er verarbeitet keine mehrdeutigen Queries.

════════════════════════════════════════════════════════════════════════════════
ZUSAMMENFASSUNG FÜR EILIGE
════════════════════════════════════════════════════════════════════════════════

Der Query Parser hat 4 Aufgaben:

1️⃣  PUTZEN → Kommentare entfernen, Format erkennen
2️⃣  PRÜFEN → Ist die Query eindeutig? (Keine "A OR B AND C" ohne Klammern!)
3️⃣  STRUKTURIEREN → Klammern hinzufügen für Klarheit
4️⃣  ÜBERSETZEN → Datum konvertieren, für verschiedene Datenbanken formatieren

Das Ziel: Eine rohe Query → Eine klare, strukturierte Query die die 
Datenbank perfekt versteht!

════════════════════════════════════════════════════════════════════════════════

Document: PARSER_DESIGN.md
Version: 1.0
Datum: 10. Dezember 2025
Zielgruppe: Alle (auch Laien)
Schwierigkeitsgrad: Anfänger-freundlich mit technischen Details
