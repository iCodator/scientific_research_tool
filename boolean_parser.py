#!/usr/bin/env python3
"""
Boolean Query Parser v1.2.1 - Enhanced with CLI & File Support

================================================================================
WHAT THIS SCRIPT DOES (Version: v1.2.1)
================================================================================
This is a complete boolean query validator for PubMed and Cochrane searches.
It can:
  • Validate single boolean queries (like "cancer"[MeSH])
  • Read and validate multiple queries from a text file
  • Recognize field-specific terms like "cancer"[MeSH], "tumor"[TIAB]
  • Support single-line and multi-line queries
  • Generate detailed, easy-to-understand reports
  • Create automatic logs in tests/logs/ directory

WHY THIS MATTERS
================================================================================
Researchers need valid boolean search syntax to find studies in databases like
PubMed. This tool helps catch syntax errors BEFORE searching the database.

USAGE EXAMPLES
================================================================================
# Show help text
python src/core/boolean_parser.py --help

# Check a single query
python src/core/boolean_parser.py '"cancer"[MeSH]'

# Check multiple queries from a file
python src/core/boolean_parser.py queries.txt

# Show detailed output
python src/core/boolean_parser.py queries.txt --verbose

# Save results as JSON
python src/core/boolean_parser.py queries.txt --format json
"""

import re
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# VERSION INFORMATION
VERSION = "v1.2.1"
LAST_UPDATED = "2025-12-22"


# ============================================================================
# SECTION 1: CORE PARSING FUNCTIONS
# ============================================================================
# These functions validate and analyze boolean queries
# VERSION: v1.2.1

def is_field_term(token):
    """
    WHAT THIS FUNCTION DOES:
    Checks if a single token is a field-specific term (like "cancer"[MeSH])
    
    WHY IT MATTERS:
    Field-terms are special in PubMed. They restrict searches to specific
    database fields (like Medical Subject Headings, Title/Abstract, etc.)
    
    HOW IT WORKS:
    Uses a pattern to check: must have quotes, content, and brackets
    
    EXAMPLES OF VALID FIELD-TERMS:
    ✅ "cancer"[MeSH]       → True (double quotes + field code)
    ✅ 'tumor'[TIAB]        → True (single quotes + field code)
    ✅ "2020-2025"[pdat]    → True (date range + field code)
    
    EXAMPLES OF INVALID FIELD-TERMS:
    ❌ cancer               → False (no quotes, no brackets)
    ❌ cancer[MeSH]         → False (not quoted!)
    ❌ "cancer"             → False (no brackets/field code)
    ❌ "cancer"[]           → False (empty field code)
    
    PARAMETERS:
    token (str): A single word/token from the query
    
    RETURNS:
    bool: True if this is a valid field-term, False otherwise
    
    VERSION: v1.2.1
    """
    # Pattern explanation:
    # ([\"\'])     = Start with either " or '
    # (.+?)        = Content in the middle (at least 1 character)
    # \1           = Same quote type as the start
    # \[           = Opening bracket [
    # ([A-Za-z0-9_]+) = Field code (letters, numbers, underscore)
    # \]           = Closing bracket ]
    pattern = r'^([\"\'])(.+?)\1\[([A-Za-z0-9_]+)\]$'
    return bool(re.match(pattern, token))


def tokenize(query):
    """
    WHAT THIS FUNCTION DOES:
    Breaks a query into individual tokens (words, operators, brackets, etc.)
    Special: keeps field-terms together as single units
    
    WHY IT MATTERS:
    The parser needs to work with individual parts of the query.
    Field-terms like "cancer"[MeSH] must stay together as one unit.
    
    HOW IT WORKS:
    1. Reads through the query character by character
    2. Groups characters into tokens
    3. Special handling for quoted content and field-codes
    
    EXAMPLES:
    Input:  "cancer"[MeSH] AND treatment
    Output: ['"cancer"[MeSH]', 'AND', 'treatment']
    
    Input:  ("cancer"[MeSH] OR "tumor"[TIAB])
    Output: ['(', '"cancer"[MeSH]', 'OR', '"tumor"[TIAB]', ')']
    
    PARAMETERS:
    query (str): A complete boolean query string
    
    RETURNS:
    list: List of tokens
    
    VERSION: v1.2.1
    """
    tokens = []
    i = 0
    
    # Loop through each character in the query
    while i < len(query):
        # Skip whitespace (spaces, tabs, newlines)
        if query[i].isspace():
            i += 1
        # Parentheses are individual tokens
        elif query[i] in '()':
            tokens.append(query[i])
            i += 1
        # Handle quoted strings (with optional field codes)
        elif query[i] in '"\'':
            quote = query[i]
            quoted_part = quote
            i += 1
            
            # Collect characters until closing quote
            while i < len(query) and query[i] != quote:
                quoted_part += query[i]
                i += 1
            
            # Add the closing quote
            if i < len(query):
                quoted_part += query[i]
                i += 1
            
            # Check for field code after the quote (like [MeSH])
            if i < len(query) and query[i] == '[':
                bracket_part = '['
                i += 1
                # Collect field code content
                while i < len(query) and query[i] != ']':
                    bracket_part += query[i]
                    i += 1
                # Add closing bracket
                if i < len(query):
                    bracket_part += query[i]
                    i += 1
                quoted_part += bracket_part
            
            tokens.append(quoted_part)
        # Handle regular words (operators, plain terms)
        else:
            word = ''
            # Collect characters until whitespace or special char
            while i < len(query) and not query[i].isspace() and query[i] not in '()':
                word += query[i]
                i += 1
            if word:
                tokens.append(word)
    
    return tokens


def validate_single_line(query):
    """
    WHAT THIS FUNCTION DOES:
    Checks if a single-line query follows correct boolean syntax
    
    WHY IT MATTERS:
    Invalid queries will either fail in the database or give wrong results.
    This catches errors before they happen.
    
    VALIDATION RULES:
    1. Cannot start with AND or OR (what would it search?)
    2. Cannot end with AND or OR (incomplete thought)
    3. Cannot have AND AND or OR OR (double operators)
    4. Every ( must have matching ) (balanced parentheses)
    5. Operators and operands must alternate
    
    HOW IT WORKS:
    • Tokenizes the query
    • Checks each rule one by one
    • Returns True only if ALL rules pass
    
    EXAMPLES:
    ✅ "cancer"[MeSH]                         → Valid
    ✅ "cancer"[MeSH] AND treatment           → Valid
    ✅ ("cancer"[MeSH] OR "tumor"[TIAB])      → Valid
    ✅ (cancer OR tumor) AND therapy          → Valid
    
    ❌ AND cancer                             → Invalid (starts with AND)
    ❌ cancer AND                             → Invalid (ends with AND)
    ❌ cancer AND AND treatment               → Invalid (double AND)
    ❌ (cancer AND tumor                      → Invalid (unbalanced parens)
    
    PARAMETERS:
    query (str): A single-line query string
    
    RETURNS:
    bool: True if valid, False if invalid
    
    VERSION: v1.2.1
    """
    tokens = tokenize(query)
    
    # Rule 1: Must have at least one token
    if not tokens:
        return False
    
    # Rule 2: Cannot start with operator
    if tokens[0] in ['AND', 'OR']:
        return False
    
    # Rule 3: Cannot end with operator
    if tokens[-1] in ['AND', 'OR']:
        return False
    
    # Rule 4 & 5: Check token sequence
    prev_token_type = None
    paren_depth = 0
    
    for token in tokens:
        if token == '(':
            # Parenthesis must not follow an operand directly
            if prev_token_type == 'operand':
                return False
            paren_depth += 1
            prev_token_type = None
        elif token == ')':
            # Parenthesis must follow an operand or nothing
            if prev_token_type not in ['operand', None]:
                return False
            paren_depth -= 1
            # Check for unbalanced parentheses
            if paren_depth < 0:
                return False
            prev_token_type = 'operand'
        elif token in ['AND', 'OR']:
            # Operator must follow an operand
            if prev_token_type != 'operand':
                return False
            prev_token_type = 'operator'
        else:
            # This is an operand (term)
            # Operand must not follow another operand directly
            if prev_token_type == 'operand':
                return False
            # Check if it's a field-term, quoted phrase, or plain term
            if is_field_term(token):
                prev_token_type = 'operand'
            elif token.startswith('"') and token.endswith('"'):
                prev_token_type = 'operand'
            elif token.startswith("'") and token.endswith("'"):
                prev_token_type = 'operand'
            else:
                prev_token_type = 'operand'
    
    # Final checks: parentheses must be balanced, must end with operand
    return paren_depth == 0 and prev_token_type == 'operand'


def validate_multiline(query):
    """
    WHAT THIS FUNCTION DOES:
    Validates multi-line queries by combining lines and checking syntax
    
    WHY IT MATTERS:
    Researchers often write queries across multiple lines for readability.
    This validator treats them like single-line queries.
    
    HOW IT WORKS:
    1. Takes each non-empty line
    2. Joins them with spaces
    3. Validates as a single-line query
    
    EXAMPLES:
    Input:
      ("cancer"[MeSH])
      AND
      (treatment)
    
    Becomes: ("cancer"[MeSH]) AND (treatment)
    Then validated as single-line
    
    PARAMETERS:
    query (str): A multi-line query string
    
    RETURNS:
    bool: True if valid, False if invalid
    
    VERSION: v1.2.1
    """
    # Combine all non-empty lines with spaces
    combined = ' '.join(line.strip() for line in query.split('\n') if line.strip())
    # Validate the combined result
    return validate_single_line(combined)


def parse_query(query):
    """
    WHAT THIS FUNCTION DOES:
    Complete end-to-end query parsing and validation
    This is the main function you'll use most often
    
    WHY IT MATTERS:
    Gives you all information about your query in one function call
    
    HOW IT WORKS:
    1. Checks if query is empty
    2. Determines if single-line or multi-line
    3. Validates the syntax
    4. Returns detailed results
    
    EXAMPLE USAGE:
    result = parse_query('"cancer"[MeSH] AND treatment')
    if result['success']:
        print("Valid query!")
        print(f"Tokens: {result['tokens']}")
    else:
        print(f"Error: {result['error']}")
    
    PARAMETERS:
    query (str): A boolean query string
    
    RETURNS:
    dict with keys:
    - 'success' (bool): Is the query valid?
    - 'format' (str): 'SINGLE_LINE' or 'MULTI_LINE'
    - 'query' (str): The original query
    - 'tokens' (list): List of tokens
    - 'error' (str or None): Error message if invalid
    
    VERSION: v1.2.1
    """
    # Check for empty query
    if not query or not query.strip():
        return {
            'success': False,
            'format': 'SINGLE_LINE',
            'query': query,
            'tokens': [],
            'error': 'Empty query'
        }
    
    # Determine if multi-line
    is_multiline = '\n' in query
    query_format = 'MULTI_LINE' if is_multiline else 'SINGLE_LINE'
    
    try:
        # Validate appropriate to query type
        if is_multiline:
            is_valid = validate_multiline(query)
        else:
            is_valid = validate_single_line(query)
        
        if is_valid:
            # Query is valid - extract tokens
            combined = ' '.join(line.strip() for line in query.split('\n') if line.strip())
            tokens = tokenize(combined)
            return {
                'success': True,
                'format': query_format,
                'query': query,
                'tokens': tokens,
                'error': None
            }
        else:
            # Query is invalid - generate error message
            tokens = tokenize(query)
            error = get_validation_error(query, tokens)
            return {
                'success': False,
                'format': query_format,
                'query': query,
                'tokens': tokens,
                'error': error
            }
    except Exception as e:
        # Unexpected error
        return {
            'success': False,
            'format': query_format,
            'query': query,
            'tokens': [],
            'error': str(e)
        }


def get_validation_error(query, tokens):
    """
    WHAT THIS FUNCTION DOES:
    Determines the specific validation error for a failing query
    
    WHY IT MATTERS:
    Users need to know WHAT is wrong with their query to fix it
    
    HOW IT WORKS:
    Checks each possible error type and returns the first one found
    
    RETURNS:
    str: Human-readable error message
    
    VERSION: v1.2.1
    """
    if not tokens:
        return 'Empty query'
    
    if tokens[0] in ['AND', 'OR']:
        return f'Cannot start with operator: {tokens[0]}'
    
    if tokens[-1] in ['AND', 'OR']:
        return f'Cannot end with operator: {tokens[-1]}'
    
    # Check for double operators
    for i in range(len(tokens) - 1):
        if tokens[i] in ['AND', 'OR'] and tokens[i + 1] in ['AND', 'OR']:
            return f'Double operator: {tokens[i]} {tokens[i + 1]}'
    
    # Check for unbalanced parentheses
    paren_depth = 0
    for token in tokens:
        if token == '(':
            paren_depth += 1
        elif token == ')':
            paren_depth -= 1
            if paren_depth < 0:
                return 'Unbalanced parentheses'
    
    if paren_depth != 0:
        return 'Unbalanced parentheses'
    
    return 'Invalid query syntax'


def get_query_info(query):
    """
    WHAT THIS FUNCTION DOES:
    Extracts detailed information about a valid query
    
    WHY IT MATTERS:
    Users want to understand what their query contains
    
    EXAMPLE:
    query = '"cancer"[MeSH] AND "treatment"[TIAB]'
    info = get_query_info(query)
    # info['field_terms'] = ['"cancer"[MeSH]', '"treatment"[TIAB]']
    # info['num_field_terms'] = 2
    # info['operators'] = ['AND']
    
    PARAMETERS:
    query (str): A valid query string
    
    RETURNS:
    dict with:
    - 'tokens': List of all tokens
    - 'field_terms': List of field-specific terms
    - 'num_field_terms': Count of field-terms
    - 'operators': List of operators (AND, OR)
    - 'operands': List of plain terms (non-field-terms)
    - 'num_tokens': Total token count
    
    VERSION: v1.2.1
    """
    tokens = tokenize(query)
    field_terms = [t for t in tokens if is_field_term(t)]
    operators = [t for t in tokens if t in ['AND', 'OR']]
    operands = [t for t in tokens if t not in ['AND', 'OR', '(', ')'] and not is_field_term(t)]
    
    return {
        'tokens': tokens,
        'field_terms': field_terms,
        'num_field_terms': len(field_terms),
        'operators': operators,
        'operands': operands,
        'num_tokens': len(tokens)
    }


# ============================================================================
# SECTION 2: FILE INPUT & OUTPUT FUNCTIONS
# ============================================================================
# These functions handle reading queries from files and creating logs
# VERSION: v1.2.1

def read_queries_from_file(filepath):
    """
    WHAT THIS FUNCTION DOES:
    Reads boolean queries from a text file (one per line)
    
    WHY IT MATTERS:
    Researchers often have many queries to test. This reads them all at once.
    
    FILE FORMAT:
    • One query per line
    • Lines starting with # are comments (ignored)
    • Empty lines are ignored
    
    EXAMPLE FILE (queries.txt):
      # My cancer search queries
      "cancer"[MeSH]
      "cancer"[MeSH] AND treatment
      
      # This is invalid (will be caught)
      cancer AND
    
    PARAMETERS:
    filepath (str): Path to the text file
    
    RETURNS:
    list: List of dicts with 'line' number and 'query' text
    
    VERSION: v1.2.1
    """
    queries = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    queries.append({'line': i, 'query': line})
        return queries
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found")
        sys.exit(1)
    except IOError as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def create_log_filename(log_dir='tests/logs'):
    """
    WHAT THIS FUNCTION DOES:
    Creates meaningful log filenames with date/time stamps
    
    WHY IT MATTERS:
    Each test run gets a unique filename so you can keep all results
    
    HOW IT WORKS:
    • Creates tests/logs/ directory if needed
    • Uses current date and time in filename
    
    EXAMPLE FILENAMES:
    PARSER_RESULTS_20251222_105700.txt    (text format)
    PARSER_RESULTS_20251222_105700.json   (JSON format)
    
    PARAMETERS:
    log_dir (str): Directory to save logs (default: tests/logs)
    
    RETURNS:
    dict: {'txt': filename, 'json': filename}
    
    VERSION: v1.2.1
    """
    # Create directory if it doesn't exist
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    # Generate timestamp (YYYYMMDD_HHMMSS)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return {
        'txt': f"{log_dir}/PARSER_RESULTS_{timestamp}.txt",
        'json': f"{log_dir}/PARSER_RESULTS_{timestamp}.json"
    }


def format_layperson_log(queries_data):
    """
    WHAT THIS FUNCTION DOES:
    Creates a detailed, easy-to-understand report for non-technical users
    
    WHY IT MATTERS:
    Users need to understand results in plain English, not technical jargon
    
    HOW IT WORKS:
    Formats query results with:
    • Clear status indicators (✅ VALID / ❌ INVALID)
    • Plain English explanations
    • Examples of correct/incorrect syntax
    • Tips for better searches
    
    PARAMETERS:
    queries_data (list): Results from parse_query() for each query
    
    RETURNS:
    str: Formatted report text
    
    VERSION: v1.2.1
    """
    log = []
    
    # ========== REPORT HEADER ==========
    log.append("=" * 80)
    log.append("BOOLEAN QUERY PARSER - RESULTS REPORT")
    log.append("=" * 80)
    log.append("")
    log.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.append(f"Version: {VERSION}")
    log.append("")
    
    # ========== STATISTICS SUMMARY ==========
    passed = sum(1 for q in queries_data if q['result']['success'])
    failed = len(queries_data) - passed
    
    log.append("=" * 80)
    log.append("SUMMARY")
    log.append("=" * 80)
    log.append(f"Total Queries Tested: {len(queries_data)}")
    log.append(f"✅ Valid Queries: {passed}")
    log.append(f"❌ Invalid Queries: {failed}")
    if len(queries_data) > 0:
        success_rate = (passed / len(queries_data)) * 100
        log.append(f"Success Rate: {success_rate:.1f}%")
    log.append("")
    
    # ========== DETAILED RESULTS FOR EACH QUERY ==========
    log.append("=" * 80)
    log.append("DETAILED RESULTS")
    log.append("=" * 80)
    log.append("")
    
    for q_data in queries_data:
        query = q_data['query']
        result = q_data['result']
        info = q_data['info']
        
        status = "✅ VALID" if result['success'] else "❌ INVALID"
        log.append(f"Query #{q_data.get('line', '?')}: {status}")
        log.append(f"  Query: {query}")
        
        if result['success']:
            # Show details for valid queries
            log.append(f"  Format: {result['format']}")
            log.append(f"  Tokens: {', '.join(result['tokens'])}")
            
            if info['field_terms']:
                log.append(f"  Field-Specific Terms Found: {len(info['field_terms'])}")
                for ft in info['field_terms']:
                    log.append(f"    • {ft}")
            
            if info['operators']:
                log.append(f"  Operators Used: {', '.join(info['operators'])}")
        else:
            # Show error explanation for invalid queries
            log.append(f"  Error: {result['error']}")
            log.append(f"  Explanation:")
            
            error = result['error']
            if 'Cannot start with operator' in error:
                log.append(f"    A query cannot begin with AND or OR.")
                log.append(f"    Example: ❌ AND cancer")
                log.append(f"    Fix: ✅ cancer AND treatment")
            elif 'Cannot end with operator' in error:
                log.append(f"    A query cannot end with AND or OR.")
                log.append(f"    Example: ❌ cancer AND")
                log.append(f"    Fix: ✅ cancer AND treatment")
            elif 'Double operator' in error:
                log.append(f"    Two operators cannot appear next to each other.")
                log.append(f"    Example: ❌ cancer AND AND treatment")
                log.append(f"    Fix: ✅ cancer AND treatment")
            elif 'Unbalanced parentheses' in error:
                log.append(f"    Every opening parenthesis must have a closing one.")
                log.append(f"    Example: ❌ (cancer AND tumor")
                log.append(f"    Fix: ✅ (cancer AND tumor)")
        
        log.append("")
    
    # ========== EXPLANATIONS ==========
    log.append("=" * 80)
    log.append("WHAT DO THESE RESULTS MEAN?")
    log.append("=" * 80)
    log.append("")
    log.append("VALID QUERY (✅)")
    log.append("  Your query follows proper boolean search syntax.")
    log.append("  It can be used to search PubMed or other databases.")
    log.append("")
    log.append("INVALID QUERY (❌)")
    log.append("  Your query has a syntax error (see explanation above).")
    log.append("  Fix the error before using it in a database search.")
    log.append("")
    log.append("FIELD-SPECIFIC TERMS")
    log.append("  Terms like \"cancer\"[MeSH] restrict searches to specific fields.")
    log.append("  [MeSH] searches the Medical Subject Headings")
    log.append("  [TIAB] searches Title and Abstract")
    log.append("  [pdat] searches publication date")
    log.append("")
    
    # ========== TIPS ==========
    log.append("=" * 80)
    log.append("TIPS FOR BETTER SEARCHES")
    log.append("=" * 80)
    log.append("")
    log.append("• Use quotes around multi-word terms: \"lung cancer\"")
    log.append("• Use AND to require multiple terms: cancer AND treatment")
    log.append("• Use OR to include alternative terms: cancer OR tumor")
    log.append("• Use parentheses to group: (cancer OR tumor) AND treatment")
    log.append("• Use field codes for precise searches: \"cancer\"[MeSH]")
    log.append("")
    
    log.append("=" * 80)
    log.append("END OF REPORT")
    log.append("=" * 80)
    
    return '\n'.join(log)


# ============================================================================
# SECTION 3: COMMAND-LINE INTERFACE
# ============================================================================
# This section handles command-line arguments and main program flow
# VERSION: v1.2.1

def create_parser():
    """
    WHAT THIS FUNCTION DOES:
    Creates the command-line argument parser with help text
    
    WHY IT MATTERS:
    Users need to know how to use the program from the command line
    
    PARAMETERS:
    None
    
    RETURNS:
    ArgumentParser: Configured argument parser
    
    VERSION: v1.2.1
    """
    parser = argparse.ArgumentParser(
        prog='boolean_parser.py',
        description='''
Boolean Query Parser v1.2.1 - Validate PubMed/Cochrane search queries

This tool checks if your search queries follow proper boolean search syntax.
It can validate single queries or read from a file.

WHAT IT DOES:
  • Validates boolean search syntax
  • Identifies field-specific terms like "cancer"[MeSH]
  • Generates detailed reports
  • Creates logs for record-keeping

EXAMPLES:

  1. Check a single query:
     python src/core/boolean_parser.py '"cancer"[MeSH]'

  2. Check queries from a file:
     python src/core/boolean_parser.py queries.txt

  3. Save results to JSON:
     python src/core/boolean_parser.py queries.txt --output results.json

  4. Verbose output:
     python src/core/boolean_parser.py queries.txt --verbose

FILE FORMAT:
  Create a text file with one query per line:
  
  "cancer"[MeSH]
  "cancer"[MeSH] AND treatment
  ("cancer"[MeSH] OR "tumor"[TIAB]) AND 2020:2025[pdat]
  
  Lines starting with # are treated as comments and ignored.
  Empty lines are also ignored.

OUTPUT:
  Results are automatically saved to tests/logs/ with a timestamp.
  Example: PARSER_RESULTS_20251222_105700.txt
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'query',
        nargs='?',
        help='A boolean query or path to a file containing queries'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Save results to a file (txt or json)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['txt', 'json'],
        default='txt',
        help='Output format (default: txt)'
    )
    
    return parser


def main():
    """
    WHAT THIS FUNCTION DOES:
    Main program entry point - handles all command-line operations
    
    WHY IT MATTERS:
    This is what runs when you execute the script from command line
    
    HOW IT WORKS:
    1. Parses command-line arguments
    2. Reads queries (from file or command line)
    3. Validates each query
    4. Creates log files
    5. Shows results to user
    
    PARAMETERS:
    None (reads from sys.argv)
    
    RETURNS:
    None
    
    VERSION: v1.2.1
    """
    # Parse command-line arguments
    parser = create_parser()
    args = parser.parse_args()
    
    # Check if user provided input
    if not args.query:
        parser.print_help()
        return
    
    # Determine if input is a file or a single query
    input_path = Path(args.query)
    
    if input_path.exists() and input_path.is_file():
        # Input is a file - read queries from it
        queries_list = read_queries_from_file(args.query)
    else:
        # Input is a single query string
        queries_list = [{'line': 1, 'query': args.query}]
    
    # ========== PROCESS EACH QUERY ==========
    queries_data = []
    for q_data in queries_list:
        # Parse and validate the query
        result = parse_query(q_data['query'])
        # Extract information if query is valid
        info = get_query_info(q_data['query']) if result['success'] else {}
        
        # Store results
        queries_data.append({
            'line': q_data['line'],
            'query': q_data['query'],
            'result': result,
            'info': info
        })
        
        # Show console output
        status = "✅" if result['success'] else "❌"
        print(f"{status} [{q_data['line']}] {q_data['query'][:60]}")
        if args.verbose and not result['success']:
            print(f"   Error: {result['error']}")
    
    # ========== GENERATE LOG FILES ==========
    log_files = create_log_filename()
    
    # Create text log (human-readable)
    txt_log = format_layperson_log(queries_data)
    with open(log_files['txt'], 'w', encoding='utf-8') as f:
        f.write(txt_log)
    print(f"\n✅ Text log saved to: {log_files['txt']}")
    
    # Create JSON log (machine-readable)
    json_data = {
        'timestamp': datetime.now().isoformat(),
        'version': VERSION,
        'summary': {
            'total': len(queries_data),
            'passed': sum(1 for q in queries_data if q['result']['success']),
            'failed': sum(1 for q in queries_data if not q['result']['success'])
        },
        'results': [
            {
                'line': q['line'],
                'query': q['query'],
                'success': q['result']['success'],
                'format': q['result']['format'],
                'tokens': q['result']['tokens'],
                'error': q['result']['error'],
                'field_terms': q['info'].get('field_terms', [])
            }
            for q in queries_data
        ]
    }
    
    with open(log_files['json'], 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2)
    print(f"✅ JSON log saved to: {log_files['json']}")
    
    # Show detailed output if requested
    if args.verbose or not input_path.exists():
        print("\n" + txt_log)


# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================
# This runs when you execute the script from command line
# VERSION: v1.2.1

if __name__ == '__main__':
    main()
