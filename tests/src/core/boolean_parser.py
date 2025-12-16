#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Boolean Query Parser v7.0 - Simplified
Unambiguous boolean query parser with strict multiline format rules

SPECIFICATION v7.0:

PHASE 1: PREPROCESS
  - Remove comments (# to end of line)
  - Remove blank lines
  - Trim whitespace

PHASE 2: DETECT FORMAT
  - MULTI_LINE: 3+ lines (odd count), even lines are operators
  - SINGLE_LINE: everything else

PHASE 3: VALIDATE & PARSE

  MULTI-LINE:
    Rule 1: Odd count, min 3 lines
    Rule 2: All even lines = same operator (normalized)
    Rule 3: Each odd line must be balanced expression
    Rule 4: Each odd line must have balanced parentheses (no cross-line)
    Assembly: Left-to-right (top-to-bottom)
    
  SINGLE-LINE:
    Rule 1: Normalize German operators to English
    Rule 2: Validate balanced parentheses
    Rule 3: Unfold nested parentheses recursively
    Rule 4: Validate each term is quoted (or TERM_N)
    Rule 5: No mixed operators at depth 0

OPERATORS:
  AND: and, und
  OR:  or, oder
  NOT: not, nicht, kein, keine, ohne
"""

# ════════════════════════════════════════════════════════════════════════════

OPERATOR_MAP = {
    'AND': 'AND', 'UND': 'AND',
    'OR': 'OR', 'ODER': 'OR',
    'NOT': 'NOT', 'NICHT': 'NOT', 'KEIN': 'NOT', 'KEINE': 'NOT', 'OHNE': 'NOT',
}

class ParseError(Exception):
    pass

# ════════════════════════════════════════════════════════════════════════════
# PHASE 1: PREPROCESS
# ════════════════════════════════════════════════════════════════════════════

def preprocess(query):
    """Remove comments, blank lines, trim whitespace"""
    lines = []
    for line in query.split('\n'):
        line = line.split('#')[0].strip()  # Remove comments and trim
        if line:
            lines.append(line)
    return lines

# ════════════════════════════════════════════════════════════════════════════
# UTILITIES
# ════════════════════════════════════════════════════════════════════════════

def normalize_op(token):
    """Normalize operator token to English (AND/OR/NOT)"""
    return OPERATOR_MAP.get(token.upper())

def is_balanced_parens(text):
    """Check if parentheses are balanced (ignore inside quotes)"""
    depth, in_quotes = 0, False
    for char in text:
        if char == '"':
            in_quotes = not in_quotes
        elif not in_quotes:
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
                if depth < 0:
                    return False
    return depth == 0

def find_innermost_parens(text):
    """Find innermost (start, end) indices, or None"""
    depth, in_quotes = 0, False
    start = None
    for i, char in enumerate(text):
        if char == '"':
            in_quotes = not in_quotes
        elif not in_quotes:
            if char == '(':
                if depth == 0:
                    start = i
                depth += 1
            elif char == ')':
                depth -= 1
                if depth == 0 and start is not None:
                    return (start, i + 1)
    return None

def normalize_operators(expr):
    """Replace German operators with English in expression"""
    result = expr
    for german, english in OPERATOR_MAP.items():
        if german != english:
            result = result.replace(' ' + german + ' ', ' ' + english + ' ')
    return result

# ════════════════════════════════════════════════════════════════════════════
# PHASE 2: DETECT FORMAT
# ════════════════════════════════════════════════════════════════════════════

def detect_format(lines):
    """Detect MULTI_LINE or SINGLE_LINE format"""
    if len(lines) == 1:
        return 'SINGLE_LINE'
    
    # Multi-line: 3+ lines, odd count, even lines are operators
    if len(lines) >= 3 and len(lines) % 2 == 1:
        all_ops = all(normalize_op(lines[i].upper()) for i in range(1, len(lines), 2))
        if all_ops:
            return 'MULTI_LINE'
    
    return 'SINGLE_LINE'

# ════════════════════════════════════════════════════════════════════════════
# MULTI-LINE PARSING
# ════════════════════════════════════════════════════════════════════════════

def validate_multiline(lines):
    """Validate multi-line format"""
    # Rule 1: Odd count, min 3
    if len(lines) < 3:
        raise ParseError(f"MULTI-LINE: Need 3+ lines, got {len(lines)}")
    if len(lines) % 2 == 0:
        raise ParseError(f"MULTI-LINE: Need odd count, got {len(lines)}")
    
    # Rule 4: Each odd line must have balanced parens (check FIRST)
    for i in range(0, len(lines), 2):
        if not is_balanced_parens(lines[i]):
            raise ParseError(
                f"MULTI-LINE: Line {i+1} has unbalanced parentheses.\n"
                f"  {lines[i]}\n"
                f"  Use SINGLE-LINE format for cross-line nesting."
            )
    
    # Rule 2: All operators identical
    ops = [normalize_op(lines[i].upper()) for i in range(1, len(lines), 2)]
    if len(set(ops)) > 1:
        raise ParseError(f"MULTI-LINE: Mixed operators {set(ops)}")
    
    # Rule 3: Each odd line is valid
    for i in range(0, len(lines), 2):
        validate_single_line(lines[i])

def parse_multiline(lines):
    """Parse multi-line to fully parenthesized form"""
    validate_multiline(lines)
    
    # Parse each odd line
    parsed = [parse_single_line(lines[i]) for i in range(0, len(lines), 2)]
    
    # Combine with operator
    op = normalize_op(lines[1].upper())
    result = parsed[0]
    for p in parsed[1:]:
        result += f" {op} {p}"
    
    return f"({result})"

# ════════════════════════════════════════════════════════════════════════════
# SINGLE-LINE PARSING
# ════════════════════════════════════════════════════════════════════════════

def tokenize(line):
    """Split line into tokens (parens separate)"""
    tokens = []
    current = ""
    in_quotes = False
    
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
            current += char
        elif char in '()' and not in_quotes:
            if current:
                tokens.append(current)
                current = ""
            tokens.append(char)
        elif char == ' ' and not in_quotes:
            if current:
                tokens.append(current)
                current = ""
        else:
            current += char
    
    if current:
        tokens.append(current)
    
    return tokens

def validate_single_line(line):
    """Validate single-line format"""
    line = ' '.join(line.split())  # Normalize whitespace
    tokens = tokenize(line)
    
    # All terms must be quoted or TERM_N
    for t in tokens:
        if t not in '()' and not normalize_op(t):
            if not (t.startswith('"') and t.endswith('"')) and not t.startswith('TERM_'):
                raise ParseError(f"SINGLE-LINE: Unquoted term '{t}'")
    
    # No mixed operators at depth 0
    ops, depth = set(), 0
    for t in tokens:
        if t == '(':
            depth += 1
        elif t == ')':
            depth -= 1
        elif normalize_op(t) and depth == 0:
            ops.add(normalize_op(t))
    
    if len(ops) > 1:
        raise ParseError(f"SINGLE-LINE: Mixed operators {ops} without parens")

def unfold_parens(line):
    """Unfold nested parentheses, return (unfolded, term_map, order)"""
    term_map = {}
    order = []
    counter = [0]
    
    while True:
        pos = find_innermost_parens(line)
        if not pos:
            break
        
        start, end = pos
        counter[0] += 1
        term_name = f"TERM_{counter[0]}"
        
        term_map[term_name] = line[start:end]
        order.append(term_name)
        line = line[:start] + term_name + line[end:]
    
    return line, term_map, order

def parse_single_line(line):
    """Parse single-line to fully parenthesized form"""
    line = ' '.join(line.split())  # Normalize whitespace
    validate_single_line(line)
    
    # Unfold nested parentheses
    line, term_map, order = unfold_parens(line)
    
    # Validate each term (bottom-up)
    for term_name in order:
        term_expr = term_map[term_name]
        inner = term_expr[1:-1] if term_expr.startswith('(') and term_expr.endswith(')') else term_expr
        validate_single_line(inner)
    
    # Tokenize and rebuild
    tokens = tokenize(line)
    result = []
    
    for t in tokens:
        if t == '(' or t == ')':
            result.append(t)
        elif normalize_op(t):
            result.append(normalize_op(t))
        elif t.startswith('TERM_'):
            result.append(t)
        elif t.startswith('"') and t.endswith('"'):
            result.append(f"({t[1:-1]})")  # Unquote and wrap
        else:
            result.append(t)
    
    output = ' '.join(result)
    if not (output.startswith('(') and output.endswith(')')):
        output = f"({output})"
    
    # Expand terms
    for term_name in reversed(order):
        term_expr = normalize_operators(term_map[term_name])
        output = output.replace(term_name, term_expr)
    
    return output

# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════

def parse_query(query):
    """Main parser function"""
    try:
        # Phase 1: Preprocess
        lines = preprocess(query)
        
        if not lines:
            return {'success': False, 'error': 'Empty query'}
        
        # Phase 2: Detect format
        fmt = detect_format(lines)
        
        # Phase 3: Parse
        if fmt == 'MULTI_LINE':
            lines_upper = [line.upper() for line in lines]
            output = parse_multiline(lines_upper)
        else:
            output = parse_single_line(lines[0].upper())
        
        output = normalize_operators(output)
        
        return {
            'success': True,
            'output': output,
            'format': fmt,
        }
    
    except ParseError as e:
        return {'success': False, 'error': str(e)}
    except Exception as e:
        return {'success': False, 'error': f'ERROR: {str(e)}'}

# ════════════════════════════════════════════════════════════════════════════
# CLI
# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        print("=" * 80)
        print("Boolean Query Parser v7.0 - Simplified")
        print("=" * 80)
        
        while True:
            try:
                print("\nEnter query (empty line to finish, 'exit' to quit):")
                query_lines = []
                while True:
                    line = input()
                    if not line:
                        break
                    query_lines.append(line)
                
                query = '\n'.join(query_lines)
                if query.lower() in ['exit', 'quit']:
                    break
                
                result = parse_query(query)
                print("\n" + "=" * 80)
                print(f"Success: {result['success']}")
                if result.get('format'):
                    print(f"Format: {result['format']}")
                if result.get('output'):
                    print(f"Output: {result['output']}")
                if result.get('error'):
                    print(f"Error: {result['error']}")
                print("=" * 80)
            
            except KeyboardInterrupt:
                print("\nExiting...")
                break
    
    else:
        input_file = sys.argv[1]
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                query = f.read()
            
            result = parse_query(query)
            
            print("=" * 80)
            print(f"File: {input_file}")
            print("=" * 80)
            print(f"Success: {result['success']}")
            if result.get('format'):
                print(f"Format: {result['format']}")
            if result.get('output'):
                print(f"Output: {result['output']}")
            if result.get('error'):
                print(f"Error: {result['error']}")
            print("=" * 80)
        
        except FileNotFoundError:
            print(f"Error: File '{input_file}' not found")
            sys.exit(1)
