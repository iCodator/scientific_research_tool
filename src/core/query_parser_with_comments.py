"""
═══════════════════════════════════════════════════════════════════════════
ERWEITERTE QUERY-PARSER MIT COMMENT-SUPPORT
═══════════════════════════════════════════════════════════════════════════

Feature: Query-Textdateien können jetzt Python-ähnliche Kommentare enthalten!

Beispiel (queries/coenzym_q10.txt):

    # Das ist ein Kommentar - wird ignoriert
    'Coenzym Q10'  # Inline-Kommentar
    AND
    # Zeitraum-Filter
    (2015:2025[pdat])  # Nur Artikel ab 2015

Ausgabe-Query (nach Parsing):
    'Coenzym Q10' AND (2015:2025[pdat])

═══════════════════════════════════════════════════════════════════════════
"""

import re
from pathlib import Path
from typing import Tuple

def load_query_with_comments(filepath: str) -> Tuple[str, str]:
    """
    Lädt eine Query aus einer Textdatei mit Comment-Support.
    
    Features:
    =========
    1. Unterstützt Python-ähnliche Kommentare (#)
    2. Entfernt Kommentare am Ende von Zeilen (inline comments)
    3. Ignoriert Zeilen, die nur aus Kommentaren bestehen
    4. Behält Zeilenumbrüche aber entfernt überflüssige Leerzeichen
    5. Gibt auch die Original-Datei zurück (für Debugging)
    
    Args:
        filepath (str): Pfad zur Query-Datei
        
    Returns:
        Tuple[str, str]: (bereinigte_query, original_inhalt)
        
    Raises:
        FileNotFoundError: Wenn Datei nicht existiert
        IOError: Wenn Datei nicht lesbar ist
        
    Beispiele:
    =========
    
    # Datei: queries/coenzym.txt
    # ----------
    # # Suche nach Coenzym Q10
    # 'Coenzym Q10'  # Hauptterm
    # AND
    # (2015:2025[pdat])  # Datumbereich
    # 
    # query, original = load_query_with_comments("queries/coenzym.txt")
    # 
    # query wäre dann:
    # 'Coenzym Q10' AND (2015:2025[pdat])
    # 
    # original wäre die komplette Originaldatei mit Kommentaren
    """
    try:
        file_path = Path(filepath)
        
        # Falls relativer Pfad, versuche relativ zu Projekt-Root
        if not file_path.exists():
            from pathlib import Path as PathlibPath
            PROJECT_ROOT = PathlibPath(__file__).parent.parent.parent
            file_path = PROJECT_ROOT / filepath
        
        if not file_path.exists():
            raise FileNotFoundError(f"Query-Datei nicht gefunden: {filepath}")
        
        # Lese Original-Inhalt
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Starte Parsing
        cleaned_lines = []
        
        for line in original_content.split('\n'):
            # SCHRITT 1: Entferne Inline-Kommentare (Text nach #)
            # Aber Vorsicht: # in Strings sollten ignoriert werden!
            line_without_comment = _remove_inline_comment(line)
            
            # SCHRITT 2: Entferne führende/nachfolgende Whitespace
            line_stripped = line_without_comment.strip()
            
            # SCHRITT 3: Ignoriere leere Zeilen
            if line_stripped:
                cleaned_lines.append(line_stripped)
        
        # SCHRITT 4: Verbinde alle Zeilen mit Leerzeichen
        # (Zeilenumbrüche werden zu Leerzeichen, wie in read-file tradition)
        cleaned_query = ' '.join(cleaned_lines)
        
        # SCHRITT 5: Cleanup: Mehrfache Leerzeichen zu einzelnem Leerzeichen
        cleaned_query = re.sub(r'\s+', ' ', cleaned_query).strip()
        
        return cleaned_query, original_content
        
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Datei nicht gefunden: {filepath}") from e
    except Exception as e:
        raise IOError(f"Fehler beim Lesen der Query-Datei: {e}") from e


def _remove_inline_comment(line: str) -> str:
    """
    Entfernt Inline-Kommentare (# bis Zeilenende) aus einer Zeile.
    
    Besonderheiten:
    ===============
    1. Ignoriert # innerhalb von Anführungszeichen (' oder ")
    2. Ignoriert # innerhalb von eckigen Klammern [...]
    3. Entfernt nur Kommentare außerhalb dieser Strukturen
    
    Args:
        line (str): Die zu verarbeitende Zeile
        
    Returns:
        str: Zeile ohne Inline-Kommentar
        
    Beispiele:
    ==========
    >>> _remove_inline_comment("'Coenzym Q10'  # Hauptterm")
    "'Coenzym Q10'"
    
    >>> _remove_inline_comment("NOT animal[MeSH Terms]  # Filtern")
    "NOT animal[MeSH Terms]"
    
    >>> _remove_inline_comment("# Das ist ein Kommentar")
    ""
    
    >>> _remove_inline_comment("(2015:2025[pdat])  # Datumbereich")
    "(2015:2025[pdat])"
    
    >>> _remove_inline_comment("term with 'quoted # string' after")
    "term with 'quoted # string' after"
    """
    
    # Wenn keine # vorhanden, direkt zurückgeben
    if '#' not in line:
        return line
    
    in_single_quote = False
    in_double_quote = False
    in_brackets = False
    bracket_depth = 0
    
    result = []
    i = 0
    
    while i < len(line):
        char = line[i]
        
        # VERWALTUNG VON QUOTING/BRACKETS
        # ================================
        
        # Single-Quote aktivieren/deaktivieren
        if char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
            result.append(char)
            i += 1
            continue
        
        # Double-Quote aktivieren/deaktivieren  
        if char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
            result.append(char)
            i += 1
            continue
        
        # Eckige Klammern zählen (nur außerhalb von Quotes)
        if not in_single_quote and not in_double_quote:
            if char == '[':
                bracket_depth += 1
                in_brackets = bracket_depth > 0
            elif char == ']':
                bracket_depth -= 1
                in_brackets = bracket_depth > 0
        
        # KOMMENTAR-DETEKTION
        # ===================
        
        # Wenn # außerhalb aller Strukturen → Kommentar gefunden!
        if (char == '#' and 
            not in_single_quote and 
            not in_double_quote and 
            not in_brackets):
            # Rest der Zeile ist Kommentar → Breche ab
            break
        
        result.append(char)
        i += 1
    
    return ''.join(result)


# ═══════════════════════════════════════════════════════════════════════════
# ALTERNATIVE IMPLEMENTIERUNG (RegEx-basiert, einfacher aber weniger robust)
# ═══════════════════════════════════════════════════════════════════════════

def _remove_inline_comment_regex(line: str) -> str:
    """
    RegEx-basierte Alternative (schneller, aber weniger robust).
    
    Entfernt Kommentare, ignoriert aber # in Strings nicht perfekt.
    Nutze diese nur, wenn die Character-basierte Version zu langsam ist.
    
    Args:
        line (str): Die zu verarbeitende Zeile
        
    Returns:
        str: Zeile ohne Kommentar
    """
    # Einfacher RegEx: Alles von # bis Ende (außer in einfachen Quotes)
    # Warnung: Das hier ist NICHT perfekt für komplexe Queries!
    # Besser: Character-basierte Version nutzen
    
    match = re.search(r"(?<!['\"\\])#.*$", line)
    if match:
        return line[:match.start()]
    return line


# ═══════════════════════════════════════════════════════════════════════════
# INTEGRATION IN main.py
# ═══════════════════════════════════════════════════════════════════════════

# Ersetze in main.py die alte load_query Funktion mit dieser neuen Version:

# ALTE FUNKTION (veraltet):
"""
def load_query(filepath: str) -> str:
    try:
        file_path = Path(filepath)
        if not file_path.exists():
            file_path = PROJECT_ROOT / filepath
        with open(file_path, 'r', encoding='utf-8') as f:
            query = f.read().strip()
        logger.info(f"📂 Query aus Datei geladen: {file_path}")
        return query
    except FileNotFoundError:
        logger.error(f"❌ Datei nicht gefunden: {filepath}")
        sys.exit(1)
"""

# NEUE FUNKTION (mit Comment-Support):
"""
def load_query(filepath: str) -> str:
    try:
        query, original = load_query_with_comments(filepath)
        file_path = Path(filepath)
        if not file_path.exists():
            file_path = PROJECT_ROOT / filepath
        logger.info(f"📂 Query aus Datei geladen: {file_path}")
        logger.debug(f"Original-Inhalt mit Kommentaren:\\n{original}")
        logger.debug(f"Bereinigte Query: {query}")
        return query
    except (FileNotFoundError, IOError) as e:
        logger.error(f"❌ {e}")
        sys.exit(1)
"""

# ═══════════════════════════════════════════════════════════════════════════
# BEISPIEL-QUERY-DATEIEN MIT KOMMENTAREN
# ═══════════════════════════════════════════════════════════════════════════

EXAMPLE_QUERIES = {
    "coenzym_q10_with_comments.txt": """
# ============================================================================
# Suche nach Coenzym Q10 (auch Ubiquinon genannt)
# ============================================================================

# Hauptsuchterm mit Alternativen (| = OR)
(
  'Coenzym Q10'  # Moderner Name
  OR 'CoQ10'     # Abkürzung
  OR Ubiquinone  # Wissenschaftlicher Name
)

# UND kombiniert mit einem Datumbereich
AND

# Nur Artikel aus den letzten 10 Jahren
(2015:2025[pdat])

# Ausschluss: Wir wollen keine Tier-Versuche
NOT animal
    """,
    
    "diabetes_exercise.txt": """
# Diabetes-Forschung mit Bewegungstherapie
# =========================================

# Main terms
(
  diabetes            # Diabetes mellitus
  OR 'glucose intolerance'  # Verwandte Condition
  OR 'metabolic syndrome'   # Related condition
)

# AND kombiniert mit
AND

# Intervention-Typ
(
  exercise     # Bewegung
  OR 'physical activity'  # Körperliche Aktivität
  OR fitness   # Fitness
)

# Zusätzliche Filterung
AND
(2020:2025[pdat])  # Nur neuere Forschung
    """,
    
    "cochrane_cancer_immunotherapy.txt": """
# ============================================================================
# Cochrane Review: Krebsbehandlung mit Immunotherapie
# ============================================================================
# Hinweis: Cochrane akzeptiert KEINE Field-Tags wie [pdat]
# Nutze nur normale AND/OR/NOT Syntax
# ============================================================================

(
  cancer       # Allgemeiner Suchterm
  OR tumor     # Synonym
  OR neoplasm  # Wissenschaftlicher Term
)

AND

(
  immunotherapy            # Hauptterm
  OR 'checkpoint inhibitor'  # Spezifischer Typ
  OR 'immune checkpoint'      # Alternative Formulierung
)

NOT

animal  # Ausschluß: Keine Tier-Versuche
    """
}


# ═══════════════════════════════════════════════════════════════════════════
# UNIT TESTS
# ═══════════════════════════════════════════════════════════════════════════

def test_remove_inline_comment():
    """Test-Funktion für Comment-Removal."""
    
    test_cases = [
        # (input, expected_output)
        ("'Coenzym Q10'  # Hauptterm", "'Coenzym Q10'"),
        ("NOT animal[MeSH Terms]  # Filtern", "NOT animal[MeSH Terms]"),
        ("# Das ist ein Kommentar", ""),
        ("(2015:2025[pdat])  # Datumbereich", "(2015:2025[pdat])"),
        ("term with 'quoted # string' after", "term with 'quoted # string' after"),
        ('term with "quoted # string" after', 'term with "quoted # string" after'),
        ("normal text without comment", "normal text without comment"),
        ("[Title/Abstract]  # Field Tag", "[Title/Abstract]"),
    ]
    
    print("Test-Lauf: _remove_inline_comment")
    print("=" * 70)
    
    all_passed = True
    for i, (input_text, expected) in enumerate(test_cases, 1):
        result = _remove_inline_comment(input_text)
        passed = result == expected
        all_passed = all_passed and passed
        
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"\nTest {i}: {status}")
        print(f"  Input:    {input_text!r}")
        print(f"  Expected: {expected!r}")
        print(f"  Got:      {result!r}")
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ Alle Tests bestanden!")
    else:
        print("✗ Einige Tests fehlgeschlagen!")
    
    return all_passed


if __name__ == "__main__":
    # Führe Tests aus
    test_remove_inline_comment()
    
    print("\n" + "=" * 70)
    print("Beispiel-Parsing:")
    print("=" * 70)
    
    # Beispiel mit inline-Test
    example = """
    # Suche nach Krebs und Immuntherapie
    (cancer OR tumor)  # Haupt-Suchterm
    AND
    (immunotherapy OR checkpoint)  # Interventionstyp
    AND
    (2020:2025[pdat])  # Neuere Forschung nur
    """
    
    # Lokale Test-Version (ohne Datei)
    cleaned_lines = []
    for line in example.split('\n'):
        line_clean = _remove_inline_comment(line).strip()
        if line_clean:
            cleaned_lines.append(line_clean)
    
    result = ' '.join(cleaned_lines)
    result = re.sub(r'\s+', ' ', result).strip()
    
    print(f"Original:\n{example}\n")
    print(f"Bereinigt:\n{result}\n")
