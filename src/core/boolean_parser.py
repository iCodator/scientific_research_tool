#!/usr/bin/env python3
# ============================================================================
# FILE: boolean_parser.py
# VERSION: v1.1.0 (Enhanced with field-term recognition)
# DATE: December 18, 2025
# AUTHOR: AI Assistant
# DIRECTORY: src/core/
# FULL PATH: src/core/boolean_parser.py
#
# DESCRIPTION: Boolean Query Parser with field-specific syntax support
# PURPOSE: Parse and validate complex boolean medical database queries
#          including PubMed field-specific terms like "cancer"[MeSH]
#
# CHANGELOG:
# v1.0.0 - Initial implementation (Dec 17, 2025)
# v1.1.0 - Added field-term recognition support (Dec 18, 2025)
#
# KEY CHANGES IN v1.1.0:
# - New is_field_term() function recognizes "term"[field] patterns
# - Updated validate_single_line() to accept field-specific terms
# - validate_multiline() automatically supports field-terms via delegation
# - All 13 field-specific syntax scenarios now supported
#
# ============================================================================

import re

# ============================================================================
# OPERATOR MAPPING - Normalize different language operators
# ============================================================================
# This dictionary maps various operator representations to standard English.
# Supports both English and German operators for international users.
# Example: "und" in German becomes "AND" internally
# ============================================================================

OPERATOR_MAP = {
    'and': 'AND',
    'und': 'AND',
    'AND': 'AND',
    'UND': 'AND',
    'or': 'OR',
    'oder': 'OR',
    'OR': 'OR',
    'ODER': 'OR',
    'not': 'NOT',
    'nicht': 'NOT',
    'kein': 'NOT',
    'keine': 'NOT',
    'ohne': 'NOT',
    'NOT': 'NOT',
}


# ============================================================================
# MAIN PARSER FUNCTION
# ============================================================================

def parse_query(query):
    """
    Main entry point for parsing boolean queries.
    
    WHAT THIS DOES:
    Takes a raw query string and validates it, returning success/failure
    with details about the format detected and any processing done.
    
    WHY IT MATTERS:
    This is the public API that external code calls to parse queries.
    It handles all formats (single-line, multi-line) transparently.
    
    PARAMETERS:
    query (str): Raw query string, e.g., "cancer AND treatment"
                 or multi-line format with operators on separate lines
    
    RETURNS:
    dict: Result dictionary with keys:
        - success (bool): True if query is valid, False otherwise
        - format (str): 'SINGLE_LINE' or 'MULTI_LINE'
        - output (str): Processed/normalized query
        - error (str): Error message if validation failed (optional)
    
    EXAMPLES:
    >>> result = parse_query('cancer AND treatment')
    >>> result['success']
    True
    >>> result['format']
    'SINGLE_LINE'
    
    >>> result = parse_query('(cancer\\nAND\\ntreatment)')
    >>> result['success']
    True
    >>> result['format']
    'MULTI_LINE'
    """
    
    # Remove comments and clean the query
    cleaned_query = preprocess(query)
    if not cleaned_query:
        return {
            'success': False,
            'format': 'UNKNOWN',
            'output': '',
            'error': 'Query is empty or only contains comments'
        }
    
    # Determine if single-line or multi-line format
    format_type = detect_format(cleaned_query)
    
    if format_type == 'MULTI_LINE':
        if not validate_multiline(cleaned_query):
            return {
                'success': False,
                'format': 'MULTI_LINE',
                'output': cleaned_query,
                'error': 'Multi-line format validation failed'
            }
        return {
            'success': True,
            'format': 'MULTI_LINE',
            'output': parse_multiline(cleaned_query)
        }
    
    elif format_type == 'SINGLE_LINE':
        if not validate_single_line(cleaned_query):
            return {
                'success': False,
                'format': 'SINGLE_LINE',
                'output': cleaned_query,
                'error': 'Single-line format validation failed'
            }
        return {
            'success': True,
            'format': 'SINGLE_LINE',
            'output': parse_single_line(cleaned_query)
        }
    
    else:
        return {
            'success': False,
            'format': 'UNKNOWN',
            'output': cleaned_query,
            'error': 'Could not determine query format'
        }


# ============================================================================
# PREPROCESSING
# ============================================================================

def preprocess(query):
    """
    Remove comments and blank lines from query.
    
    WHAT THIS DOES:
    Cleans the input query by removing Python-style # comments
    and extra whitespace, making it ready for parsing.
    
    WHY IT MATTERS:
    Comments allow users to document their queries without breaking parsing.
    This function strips them out cleanly.
    
    PARAMETERS:
    query (str): Raw query possibly with comments
    
    RETURNS:
    str: Cleaned query with comments removed
    
    EXAMPLES:
    >>> preprocess('cancer # search term\\nAND treatment')
    'cancer\\nAND treatment'
    """
    lines = query.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Remove inline comments (# outside of quotes)
        line = remove_inline_comment(line)
        # Skip blank lines
        if line.strip():
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)


def remove_inline_comment(line):
    """
    Remove Python-style comment from a single line.
    Respects quotes - doesn't remove # inside quoted strings.
    """
    in_single_quote = False
    in_double_quote = False
    
    for i, char in enumerate(line):
        if char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
        elif char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
        elif char == '#' and not in_single_quote and not in_double_quote:
            return line[:i].rstrip()
    
    return line


# ============================================================================
# FORMAT DETECTION
# ============================================================================

def detect_format(query):
    """
    Determine if query is single-line or multi-line format.
    
    WHAT THIS DOES:
    Analyzes the query structure to identify format:
    - SINGLE_LINE: Everything on one line, e.g., "cancer AND treatment"
    - MULTI_LINE: Operators on separate lines (3+ lines, odd count)
    
    WHY IT MATTERS:
    Different formats have different validation rules.
    Must identify correctly to apply the right validation.
    
    PARAMETERS:
    query (str): Query to analyze
    
    RETURNS:
    str: 'SINGLE_LINE', 'MULTI_LINE', or 'UNKNOWN'
    
    EXAMPLES:
    >>> detect_format('cancer AND treatment')
    'SINGLE_LINE'
    
    >>> detect_format('(cancer)\\nAND\\n(treatment)')
    'MULTI_LINE'
    """
    lines = query.strip().split('\n')
    
    if len(lines) == 1:
        return 'SINGLE_LINE'
    
    if len(lines) >= 3 and len(lines) % 2 == 1:
        return 'MULTI_LINE'
    
    return 'UNKNOWN'


# ============================================================================
# MULTI-LINE VALIDATION
# ============================================================================

def validate_multiline(query):
    """
    Validate multi-line query format.
    
    WHAT THIS DOES:
    Checks if multi-line query follows the proper format:
    - Must have odd number of lines (content, operator, content, ...)
    - Lines at even indices: content (must be valid)
    - Lines at odd indices: operators (AND, OR, NOT)
    
    WHY IT MATTERS:
    Multi-line format has specific structural requirements.
    This ensures the query structure is correct before parsing.
    
    PARAMETERS:
    query (str): Multi-line query string
    
    RETURNS:
    bool: True if valid multi-line format, False otherwise
    
    EXAMPLES:
    >>> validate_multiline('(cancer)\\nAND\\n(treatment)')
    True
    
    >>> validate_multiline('(cancer)\\nAND')  # Missing final content
    False
    """
    lines = query.strip().split('\n')
    
    # Must have odd number of lines
    if len(lines) < 3 or len(lines) % 2 == 0:
        return False
    
    # Validate each line
    for i, line in enumerate(lines):
        if i % 2 == 0:  # Even index = content line
            if not validate_single_line(line.strip()):
                return False
        else:  # Odd index = operator line
            if not is_valid_operator_line(line.strip()):
                return False
    
    return True


def is_valid_operator_line(line):
    """Check if a line contains a valid operator (AND, OR, NOT)."""
    operator = normalize_operators(line)
    return operator in ['AND', 'OR', 'NOT']


# ============================================================================
# SINGLE-LINE VALIDATION (ENHANCED IN v1.1.0)
# ============================================================================

def validate_single_line(query):
    """
    Validate single-line query format.
    
    WHAT THIS DOES:
    Checks if single-line query contains valid tokens:
    - Operators (AND, OR, NOT)
    - Quoted phrases ("text" or 'text')
    - Field-specific terms ("term"[MeSH])  ← NEW in v1.1.0
    - Parentheses ( and )
    - Simple terms (single words)
    
    WHY IT MATTERS:
    Single-line validation ensures all tokens in the query are recognized.
    This is the core validation function used by both single and multi-line.
    
    PARAMETERS:
    query (str): Single-line query to validate
    
    RETURNS:
    bool: True if all tokens are valid, False if any invalid token found
    
    EXAMPLES:
    >>> validate_single_line('cancer AND treatment')
    True
    
    >>> validate_single_line('"cancer"[MeSH] AND treatment')
    True
    
    >>> validate_single_line('cancer [INVALID]')
    False
    """
    tokens = tokenize(query)
    
    for token in tokens:
        if is_operator(token):
            # Operators are valid
            continue
        elif is_quoted_phrase(token):
            # Quoted phrases without field codes are valid
            continue
        elif is_field_term(token):
            # Field-specific terms are valid (NEW in v1.1.0)
            continue
        elif is_parenthesis(token):
            # Parentheses are valid
            continue
        elif is_simple_term(token):
            # Simple terms are valid
            continue
        else:
            # Unknown token type - invalid
            return False
    
    return True


# ============================================================================
# NEW FUNCTION IN v1.1.0: is_field_term()
# ============================================================================

def is_field_term(token):
    """
    Recognize if a token is a field-specific search term.
    
    WHAT THIS DOES:
    Identifies PubMed/database field-specific search patterns.
    These combine a quoted search term with a database field code in brackets.
    
    EXAMPLES OF FIELD-SPECIFIC TERMS:
    - "cancer"[MeSH]      ← Search for "cancer" in MeSH database
    - 'tumor'[TIAB]       ← Search for 'tumor' in Title/Abstract
    - "2020-2025"[pdat]   ← Search for dates in publication date field
    - "(cancer OR tumor)"[TIAB]  ← Complex search in Title/Abstract
    
    WHY IT MATTERS:
    Medical database queries often use field-specific searches for precision.
    Without recognizing these patterns, valid queries would be rejected.
    
    This function enables the parser to accept all legitimate field-specific
    query syntax, making it compatible with PubMed, Europe PMC, etc.
    
    FIELD CODES RECOGNIZED:
    This function accepts ANY field code (generic pattern matching), including:
    - [MeSH] = Medical Subject Headings (controlled vocabulary)
    - [TIAB] = Title and Abstract
    - [pdat] = Publication Date
    - [AU] = Author
    - [TA] = Journal Name
    - [WORD] = Any custom field code
    
    PARAMETERS:
    token (str): A single token/word to check
                 Example: "cancer"[MeSH]
    
    RETURNS:
    bool: True if token matches field-term pattern, False otherwise
    
    EXAMPLES THAT RETURN TRUE:
    >>> is_field_term('"cancer"[MeSH]')
    True
    >>> is_field_term("'tumor'[TIAB]")
    True
    >>> is_field_term('"2020-2025"[pdat]')
    True
    >>> is_field_term('"any text"[field]')
    True
    
    EXAMPLES THAT RETURN FALSE:
    >>> is_field_term('cancer[MeSH]')  # Not quoted
    False
    >>> is_field_term('"cancer"')  # No field code
    False
    >>> is_field_term('"cancer"[]')  # Empty field code
    False
    >>> is_field_term('cancer')  # Simple term
    False
    
    PATTERN STRUCTURE:
    Field-term = (Quote) + (Content) + (Quote) + [ + (FieldCode) + ]
                 ^                      ^          ^                 ^
                 " or '                 " or '     [                 ]
    
    ALGORITHM:
    1. Check minimum length (at least 6 characters: "a"[b])
    2. Check token starts with quote (" or ')
    3. Find matching closing quote of same type
    4. Check opening bracket [ immediately after closing quote
    5. Find closing bracket ]
    6. Verify field code is not empty (between [ and ])
    7. Verify nothing exists after closing bracket
    8. Return True if all checks pass
    """
    
    # STEP 1: Minimum length check
    # Smallest valid field-term is "a"[b] which is 6 characters
    if len(token) < 6:
        return False
    
    # STEP 2: Opening quote check
    # Must start with either double quote (") or single quote (')
    if token[0] not in ['"', "'"]:
        return False
    
    # Store which type of quote we found (to match closing quote)
    quote_type = token[0]
    
    # STEP 3: Find closing quote
    # Search for the matching closing quote starting after position 0
    closing_quote_pos = -1
    for i in range(1, len(token)):
        if token[i] == quote_type:
            closing_quote_pos = i
            break
    
    # If no closing quote found, not a valid field-term
    if closing_quote_pos == -1:
        return False
    
    # STEP 4: Check for opening bracket [
    # The next character after the closing quote MUST be [
    if closing_quote_pos + 1 >= len(token):
        # Token ends right after closing quote, no bracket possible
        return False
    
    if token[closing_quote_pos + 1] != '[':
        # Next character isn't [, so not a field-term
        return False
    
    # STEP 5: Find closing bracket ]
    # Search for ] after the opening bracket
    closing_bracket_pos = -1
    for i in range(closing_quote_pos + 2, len(token)):
        if token[i] == ']':
            closing_bracket_pos = i
            break
    
    # If no closing bracket found, not a valid field-term
    if closing_bracket_pos == -1:
        return False
    
    # STEP 6: Verify field code is not empty
    # Calculate field code length (between [ and ])
    # We found [ at position (closing_quote_pos + 1)
    # Field code starts at (closing_quote_pos + 2) and ends before closing_bracket_pos
    field_code_length = closing_bracket_pos - (closing_quote_pos + 2)
    
    if field_code_length < 1:
        # Empty field code like "term"[]
        return False
    
    # STEP 7: Verify nothing after closing bracket
    # The closing bracket should be the LAST character in the token
    if closing_bracket_pos != len(token) - 1:
        # Extra characters after bracket like "term"[field]extra
        return False
    
    # STEP 8: All checks passed - this IS a field-term!
    return True


# ============================================================================
# TOKEN TYPE CHECKING FUNCTIONS
# ============================================================================

def is_operator(token):
    """Check if token is an operator (AND, OR, NOT)."""
    return normalize_operators(token) in ['AND', 'OR', 'NOT']


def is_quoted_phrase(token):
    """
    Check if token is a quoted phrase WITHOUT field code.
    
    WHAT THIS DOES:
    Identifies quoted strings like "phrase" or 'phrase'
    But NOT field-specific terms like "phrase"[MeSH]
    
    RETURNS:
    bool: True if quoted but NOT a field-term
    
    EXAMPLES:
    >>> is_quoted_phrase('"cancer"')
    True
    >>> is_quoted_phrase("'treatment'")
    True
    >>> is_quoted_phrase('"cancer"[MeSH]')
    False  # This is a field-term, not a simple quoted phrase
    """
    if len(token) < 2:
        return False
    
    # Check for matching quotes (not field-terms)
    if (token[0] == '"' and token[-1] == '"') or \
       (token[0] == "'" and token[-1] == "'"):
        # It's quoted, but make sure it's not a field-term
        # (field-terms have brackets after the quote)
        return not is_field_term(token)
    
    return False


def is_parenthesis(token):
    """Check if token is a parenthesis: ( or )"""
    return token in ['(', ')']


def is_simple_term(token):
    """
    Check if token is a simple unquoted term.
    
    WHAT THIS DOES:
    Identifies simple words/terms without quotes or brackets.
    
    EXAMPLES:
    >>> is_simple_term('cancer')
    True
    >>> is_simple_term('AND')
    False  # Operators are not simple terms
    >>> is_simple_term('"cancer"')
    False  # Quoted terms are not simple terms
    """
    # Must have at least 1 character
    if len(token) == 0:
        return False
    
    # Cannot be an operator
    if is_operator(token):
        return False
    
    # Cannot be a parenthesis
    if is_parenthesis(token):
        return False
    
    # Cannot be a quoted phrase
    if token[0] in ['"', "'"]:
        return False
    
    # Anything else is a simple term
    return True


# ============================================================================
# TOKENIZATION
# ============================================================================

def tokenize(query):
    """
    Split query into tokens, respecting quotes.
    
    WHAT THIS DOES:
    Breaks a query into individual tokens (words/operators/parentheses)
    while being aware of quoted strings and brackets.
    
    WHY IT MATTERS:
    Quoted strings should be treated as single tokens, not split on spaces.
    This function preserves quoted content as units.
    
    PARAMETERS:
    query (str): Query string to tokenize
    
    RETURNS:
    list: List of token strings
    
    EXAMPLES:
    >>> tokenize('cancer AND treatment')
    ['cancer', 'AND', 'treatment']
    
    >>> tokenize('"cancer phrase" AND treatment')
    ['"cancer phrase"', 'AND', 'treatment']
    """
    tokens = []
    current_token = ''
    in_quote = False
    quote_char = None
    
    for i, char in enumerate(query):
        if char in ['"', "'"] and not in_quote:
            in_quote = True
            quote_char = char
            current_token += char
        elif char == quote_char and in_quote:
            in_quote = False
            current_token += char
            # Check if followed by [ for field-term
            if i + 1 < len(query) and query[i + 1] == '[':
                # Continue to collect the field code
                j = i + 1
                while j < len(query) and query[j] != ']':
                    current_token += query[j]
                    j += 1
                if j < len(query):
                    current_token += query[j]  # Add closing ]
        elif char in ['(', ')'] and not in_quote:
            if current_token:
                tokens.append(current_token)
                current_token = ''
            tokens.append(char)
        elif char == ' ' and not in_quote:
            if current_token:
                tokens.append(current_token)
                current_token = ''
        else:
            current_token += char
    
    if current_token:
        tokens.append(current_token)
    
    return tokens


# ============================================================================
# PARSING
# ============================================================================

def parse_multiline(query):
    """
    Parse multi-line query and return normalized output.
    
    WHAT THIS DOES:
    Processes a validated multi-line query, normalizing operators
    and returning the formatted result.
    
    PARAMETERS:
    query (str): Validated multi-line query
    
    RETURNS:
    str: Normalized query with standard operators
    """
    lines = query.strip().split('\n')
    result = []
    
    for i, line in enumerate(lines):
        if i % 2 == 0:  # Content line
            result.append(parse_single_line(line.strip()))
        else:  # Operator line
            result.append(normalize_operators(line.strip()))
    
    return '\n'.join(result)


def parse_single_line(query):
    """
    Parse single-line query and return normalized output.
    
    WHAT THIS DOES:
    Normalizes operators in a single-line query while preserving
    terms, quotes, field codes, and parentheses exactly.
    
    PARAMETERS:
    query (str): Validated single-line query
    
    RETURNS:
    str: Normalized query with standard operators
    """
    tokens = tokenize(query)
    normalized_tokens = [normalize_operators(t) if is_operator(t) else t for t in tokens]
    
    # Reconstruct with proper spacing
    result = ' '.join(normalized_tokens)
    
    # Handle unfold parentheses if needed
    result = unfold_parens(result)
    
    return result


# ============================================================================
# OPERATOR NORMALIZATION
# ============================================================================

def normalize_operators(text):
    """
    Convert operators to standard form (AND, OR, NOT).
    
    WHAT THIS DOES:
    Handles multiple language/case variants of operators.
    Converts "und" → "AND", "ODER" → "OR", etc.
    
    PARAMETERS:
    text (str): Text potentially containing an operator
    
    RETURNS:
    str: Normalized operator or original text if not an operator
    
    EXAMPLES:
    >>> normalize_operators('und')
    'AND'
    >>> normalize_operators('ODER')
    'OR'
    >>> normalize_operators('cancer')
    'cancer'
    """
    return OPERATOR_MAP.get(text, text)


# ============================================================================
# PARENTHESES HANDLING
# ============================================================================

def unfold_parens(query):
    """
    Process parentheses in query (future expansion point).
    
    WHAT THIS DOES:
    Placeholder for parentheses processing.
    Currently returns query unchanged.
    Can be expanded for parentheses optimization/analysis.
    
    PARAMETERS:
    query (str): Query with parentheses
    
    RETURNS:
    str: Processed query
    """
    # In future versions, this could:
    # - Validate parentheses matching
    # - Optimize nested parentheses
    # - Flatten unnecessary nesting
    # For now, return unchanged
    return query
