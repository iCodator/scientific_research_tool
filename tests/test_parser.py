#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Boolean Query Parser v4.0 - Extended Test Script
Tests the parser AND custom test files from tests/queries/

Usage:
    python test_parser.py                    # Run all tests (built-in + custom)
    python test_parser.py --verbose          # Verbose output
    python test_parser.py --category 2       # Run specific category (built-in only)
    python test_parser.py --quick             # Quick smoke test
    python test_parser.py --custom-only      # Only test files from queries/
    python test_parser.py --builtin-only     # Only built-in categories

Location: scientific_research_tool/tests/test_parser.py
Logs generated in: scientific_research_tool/tests/logs/
Test queries location: scientific_research_tool/tests/queries/valid/ or /invalid/
"""

import sys
import os
import json
import datetime
from pathlib import Path

# ════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ════════════════════════════════════════════════════════════════════════════

# Auto-detect tests/ directory and create logs/ subdirectory
TEST_ROOT = Path(__file__).parent
TEST_LOG_DIR = TEST_ROOT / "logs"
TEST_LOG_DIR.mkdir(parents=True, exist_ok=True)

# Paths for custom test queries
VALID_QUERIES_DIR = TEST_ROOT / "queries" / "valid"
INVALID_QUERIES_DIR = TEST_ROOT / "queries" / "invalid"

TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = TEST_LOG_DIR / f"test_run_{TIMESTAMP}.log"
RESULTS_FILE = TEST_LOG_DIR / f"test_results_{TIMESTAMP}.json"

# ════════════════════════════════════════════════════════════════════════════
# PARSER CODE (embedded)
# ════════════════════════════════════════════════════════════════════════════

def normalize_input(query):
    if not query:
        return ""
    query = query.strip()
    query = query.upper()
    lines = query.split('\n')
    lines = [' '.join(line.split()) for line in lines]
    query = '\n'.join(lines)
    return query

def detect_format(normalized_query):
    if '\n' in normalized_query:
        return 'MULTILINE'
    return 'SINGLE_LINE'

VALID_OPERATORS = {'AND', 'OR', 'NOT'}

def is_valid_operator(token):
    return token in VALID_OPERATORS

def has_balanced_parentheses(text):
    depth = 0
    for char in text:
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        if depth < 0:
            return False
    return depth == 0

def is_fully_wrapped(text):
    text = text.strip()
    if len(text) < 2 or not text.startswith('(') or not text.endswith(')'):
        return False
    depth = 0
    for i, char in enumerate(text):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        if depth == 0 and i < len(text) - 1:
            return False
    return depth == 0

def tokenize_line(line):
    tokens = []
    current_token = ""
    in_quotes = False
    i = 0
    while i < len(line):
        char = line[i]
        if char == '"':
            in_quotes = not in_quotes
            current_token += char
        elif char == ' ' and not in_quotes:
            if current_token:
                tokens.append(current_token)
                current_token = ""
        else:
            current_token += char
        i += 1
    if current_token:
        tokens.append(current_token)
    return tokens

def get_operator_types_in_line(line):
    tokens = tokenize_line(line)
    operators_found = set()
    for token in tokens:
        if token.startswith('"') and token.endswith('"'):
            continue
        if is_valid_operator(token):
            operators_found.add(token)
    return operators_found

def is_homogeneous_line(line):
    operators = get_operator_types_in_line(line)
    is_homo = len(operators) <= 1
    return is_homo, operators

class ParserError(Exception):
    pass

def validate_multiline(lines):
    if len(lines) % 2 == 0:
        raise ParserError(f"Invalid line count: must be ODD (got {len(lines)} lines)")
    for i in range(0, len(lines), 2):
        line = lines[i]
        is_homo, ops_found = is_homogeneous_line(line)
        if not is_homo:
            raise ParserError(f"Line {i + 1}: Mixed operators found! {ops_found}")
    for i in range(1, len(lines), 2):
        op_line = lines[i].strip()
        if not is_valid_operator(op_line):
            raise ParserError(f"Line {i + 1}: Invalid operator '{op_line}'")

def validate_single_line(query):
    if not has_balanced_parentheses(query):
        raise ParserError("Unbalanced parentheses!")
    tokens = tokenize_line(query)
    has_and = False
    has_or = False
    for token in tokens:
        if token == 'AND':
            has_and = True
        elif token == 'OR':
            has_or = True
    if has_and and has_or and '(' not in query:
        raise ParserError("Mixed operators (AND & OR) without parentheses!")

def parse_line(line):
    tokens = tokenize_line(line)
    result_tokens = []
    for token in tokens:
        if is_valid_operator(token):
            result_tokens.append(token)
        else:
            term = token
            if is_fully_wrapped(term):
                term = term[1:-1].strip()
            term = f"({term})"
            result_tokens.append(term)
    result = ' '.join(result_tokens)
    if not is_fully_wrapped(result):
        result = f"({result})"
    return result

def parse_multiline(lines):
    parsed_groups = []
    for i in range(0, len(lines), 2):
        group = parse_line(lines[i])
        parsed_groups.append(group)
    operators = []
    for i in range(1, len(lines), 2):
        operators.append(lines[i].strip())
    result = parsed_groups[0]
    for j, op in enumerate(operators):
        result += f" {op} " + parsed_groups[j + 1]
    result = f"({result})"
    return result

def parse_single_line(query):
    tokens = tokenize_line(query)
    result_tokens = []
    for token in tokens:
        if is_valid_operator(token):
            result_tokens.append(token)
        else:
            if is_fully_wrapped(token):
                result_tokens.append(token)
            else:
                result_tokens.append(f"({token})")
    result = ' '.join(result_tokens)
    if not is_fully_wrapped(result):
        result = f"({result})"
    return result

def parse_query(query):
    try:
        normalized = normalize_input(query)
        if not normalized:
            return {'success': False, 'error': 'Empty query', 'phase': 0}
        format_type = detect_format(normalized)
        try:
            if format_type == 'MULTILINE':
                lines = normalized.split('\n')
                lines = [line.strip() for line in lines if line.strip()]
                validate_multiline(lines)
                result = parse_multiline(lines)
            else:
                validate_single_line(normalized)
                result = parse_single_line(normalized)
            return {'success': True, 'output': result, 'format': format_type, 'phase': 4}
        except ParserError as e:
            return {'success': False, 'error': str(e), 'format': format_type, 'phase': 2}
    except Exception as e:
        return {'success': False, 'error': f'Internal error: {str(e)}', 'phase': 'unknown'}

# ════════════════════════════════════════════════════════════════════════════
# TEST LOGGING
# ════════════════════════════════════════════════════════════════════════════

class TestLogger:
    def __init__(self, log_file):
        self.log_file = log_file
        self.results = []
        self.verbose = '--verbose' in sys.argv
        
    def log(self, message):
        print(message)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(message + '\n')
    
    def log_test(self, test_id, name, query, expected_success, result, passed):
        entry = {
            'test_id': test_id,
            'name': name,
            'query': query,
            'expected_success': expected_success,
            'actual_success': result['success'],
            'output': result.get('output'),
            'error': result.get('error'),
            'passed': passed,
            'timestamp': datetime.datetime.now().isoformat()
        }
        self.results.append(entry)
        
        status = "✅ PASS" if passed else "❌ FAIL"
        self.log(f"{status} | {test_id}: {name}")
        
        if self.verbose or not passed:
            self.log(f"       Input: {query[:80]}")
            self.log(f"       Expected success: {expected_success}")
            self.log(f"       Actual success: {result['success']}")
            if result.get('output'):
                self.log(f"       Output: {result['output'][:80]}")
            if result.get('error'):
                self.log(f"       Error: {result['error'][:100]}")
    
    def save_results(self):
        with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

# ════════════════════════════════════════════════════════════════════════════
# BUILT-IN TEST CASES
# ════════════════════════════════════════════════════════════════════════════

TEST_CATEGORIES = {
    1: {
        'name': 'BASIC SINGLE-TERM QUERIES',
        'tests': [
            ('1.1', 'Single word', 'cancer', True),
            ('1.2', 'Single word lowercase', 'tumor', True),
            ('1.3', 'Quoted phrase', '"breast cancer"', True),
        ]
    },
    2: {
        'name': 'HOMOGENEOUS OPERATORS',
        'tests': [
            ('2.1', 'Two AND', 'cancer AND tumor', True),
            ('2.2', 'Three AND', 'cancer AND tumor AND lesion', True),
            ('2.3', 'Two OR', 'cancer OR tumor', True),
            ('2.4', 'Three OR', 'cancer OR tumor OR lesion', True),
            ('2.5', 'NOT operator', 'cancer NOT benign', True),
        ]
    },
    3: {
        'name': 'QUOTED PHRASES',
        'tests': [
            ('3.1', 'Phrase with AND', '"breast cancer" AND treatment', True),
            ('3.2', 'Multiple phrases', '"breast cancer" OR "lung cancer"', True),
            ('3.3', 'Mixed phrases and terms', '"clinical trial" AND outcome', True),
        ]
    },
    4: {
        'name': 'PARENTHESES & GROUPING',
        'tests': [
            ('4.1', 'Simple grouping', '(cancer OR tumor) AND treatment', True),
            ('4.2', 'Both sides grouped', '(cancer OR tumor) AND (treatment OR therapy)', True),
            ('4.3', 'Nested parentheses', '((cancer OR tumor) AND treatment) OR prevention', True),
        ]
    },
    5: {
        'name': 'MULTILINE FORMAT',
        'tests': [
            ('5.1', 'Basic multiline', 'cancer OR tumor\nAND\ntreatment', True),
            ('5.2', 'Multiline both sides', 'cancer OR tumor\nAND\ntreatment OR therapy', True),
            ('5.3', 'Five-line multiline', 'cancer OR tumor\nAND\ntreatment OR therapy\nOR\nprevention', True),
        ]
    },
    6: {
        'name': 'ERROR DETECTION - MIXED OPERATORS',
        'tests': [
            ('6.1', 'Mixed AND/OR', 'cancer OR tumor AND treatment', False),
            ('6.2', 'Mixed OR/AND', 'cancer AND tumor OR treatment', False),
            ('6.3', 'Three mixed', 'cancer OR tumor AND lesion OR treatment', False),
        ]
    },
    7: {
        'name': 'ERROR DETECTION - UNBALANCED PARENS',
        'tests': [
            ('7.1', 'Missing closing', '(cancer OR tumor AND treatment', False),
            ('7.2', 'Missing opening', 'cancer OR tumor) AND treatment', False),
            ('7.3', 'Extra closing', '(cancer OR tumor)) AND treatment', False),
        ]
    },
    8: {
        'name': 'ERROR DETECTION - MULTILINE',
        'tests': [
            ('8.1', 'Even lines (2)', 'cancer OR tumor\nAND', False),
            ('8.2', 'Mixed in line', 'cancer OR tumor AND lesion\nOR\ntreatment', False),
            ('8.3', 'Invalid operator', 'cancer OR tumor\nXOR\ntreatment', False),
        ]
    },
    9: {
        'name': 'EDGE CASES - WHITESPACE',
        'tests': [
            ('9.1', 'Extra spaces', 'cancer   AND   tumor', True),
            ('9.2', 'Leading/trailing', '  cancer AND tumor  ', True),
            ('9.3', 'Multiline spaces', 'cancer  OR  tumor\nAND\ntreatment', True),
        ]
    },
    10: {
        'name': 'EDGE CASES - CASE SENSITIVITY',
        'tests': [
            ('10.1', 'Lowercase operators', 'cancer and tumor', True),
            ('10.2', 'Mixed with parens', '(cancer oR tumor) AnD treatment', True),
        ]
    },
    11: {
        'name': 'REAL-WORLD QUERIES',
        'tests': [
            ('11.1', 'Medical query', '("breast cancer" OR "lung cancer") AND (treatment OR therapy)', True),
            ('11.2', 'Exclusion query', '(cancer AND treatment) NOT benign', True),
            ('11.3', 'Complex multiline', '"breast cancer" OR "lung cancer"\nAND\ntreatment OR therapy\nNOT\nbenign', True),
        ]
    },
    12: {
        'name': 'EMPTY & NULL CASES',
        'tests': [
            ('12.1', 'Empty string', '', False),
            ('12.2', 'Only whitespace', '   ', False),
            ('12.3', 'Only newlines', '\n\n\n', False),
        ]
    },
}

# ════════════════════════════════════════════════════════════════════════════
# CUSTOM QUERY FILE LOADER
# ════════════════════════════════════════════════════════════════════════════

def load_custom_queries():
    """Load custom test queries from valid/ and invalid/ directories"""
    custom_tests = []
    
    # Load valid queries
    if VALID_QUERIES_DIR.exists():
        valid_files = sorted(VALID_QUERIES_DIR.glob('*.txt'))
        for i, file_path in enumerate(valid_files, 1):
            try:
                query = file_path.read_text().strip()
                test_id = f"C.V.{i}"
                test_name = file_path.stem
                custom_tests.append((test_id, test_name, query, True, 'valid'))
            except Exception as e:
                print(f"⚠️  Error reading {file_path}: {e}")
    
    # Load invalid queries
    if INVALID_QUERIES_DIR.exists():
        invalid_files = sorted(INVALID_QUERIES_DIR.glob('*.txt'))
        for i, file_path in enumerate(invalid_files, 1):
            try:
                query = file_path.read_text().strip()
                test_id = f"C.I.{i}"
                test_name = file_path.stem
                custom_tests.append((test_id, test_name, query, False, 'invalid'))
            except Exception as e:
                print(f"⚠️  Error reading {file_path}: {e}")
    
    return custom_tests

# ════════════════════════════════════════════════════════════════════════════
# MAIN TEST RUNNER
# ════════════════════════════════════════════════════════════════════════════

def run_tests():
    logger = TestLogger(LOG_FILE)
    
    # Header
    logger.log("=" * 100)
    logger.log("BOOLEAN QUERY PARSER v4.0 - COMPREHENSIVE TEST SUITE")
    logger.log("=" * 100)
    logger.log(f"Timestamp: {datetime.datetime.now()}")
    logger.log(f"Log file: {LOG_FILE}")
    logger.log(f"Working directory: {Path.cwd()}")
    logger.log("")
    
    # Determine which tests to run
    run_builtin = '--custom-only' not in sys.argv
    run_custom = '--builtin-only' not in sys.argv
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    # ─────────────────────────────────────────────────────────────────────
    # RUN BUILT-IN TESTS
    # ─────────────────────────────────────────────────────────────────────
    
    if run_builtin:
        logger.log("╔" + "═" * 98 + "╗")
        logger.log("║" + " SECTION 1: BUILT-IN TEST CATEGORIES ".center(98) + "║")
        logger.log("╚" + "═" * 98 + "╝")
        logger.log("")
        
        # Determine which categories to run
        if '--quick' in sys.argv:
            categories_to_run = [1, 6, 7, 8]  # Smoke test
        elif '--category' in sys.argv:
            idx = sys.argv.index('--category')
            categories_to_run = [int(sys.argv[idx + 1])]
        else:
            categories_to_run = list(TEST_CATEGORIES.keys())
        
        for category_num in categories_to_run:
            if category_num not in TEST_CATEGORIES:
                logger.log(f"⚠️  Category {category_num} not found\n")
                continue
            
            category = TEST_CATEGORIES[category_num]
            logger.log("─" * 100)
            logger.log(f"CATEGORY {category_num}: {category['name']}")
            logger.log("─" * 100)
            logger.log("")
            
            for test_id, name, query, expected_success in category['tests']:
                total_tests += 1
                result = parse_query(query)
                passed = result['success'] == expected_success
                
                if passed:
                    passed_tests += 1
                else:
                    failed_tests += 1
                
                logger.log_test(test_id, name, query, expected_success, result, passed)
            
            logger.log("")
    
    # ─────────────────────────────────────────────────────────────────────
    # RUN CUSTOM TESTS FROM FILES
    # ─────────────────────────────────────────────────────────────────────
    
    if run_custom:
        custom_tests = load_custom_queries()
        
        if custom_tests:
            logger.log("")
            logger.log("╔" + "═" * 98 + "╗")
            logger.log("║" + f" SECTION 2: CUSTOM TEST FILES ({len(custom_tests)} tests) ".center(98) + "║")
            logger.log("╚" + "═" * 98 + "╝")
            logger.log("")
            
            # Group by valid/invalid
            valid_tests = [t for t in custom_tests if t[4] == 'valid']
            invalid_tests = [t for t in custom_tests if t[4] == 'invalid']
            
            # Run valid tests
            if valid_tests:
                logger.log("─" * 100)
                logger.log(f"CUSTOM VALID TESTS ({len(valid_tests)} tests)")
                logger.log("─" * 100)
                logger.log("")
                
                for test_id, name, query, expected_success, _ in valid_tests:
                    total_tests += 1
                    result = parse_query(query)
                    passed = result['success'] == expected_success
                    
                    if passed:
                        passed_tests += 1
                    else:
                        failed_tests += 1
                    
                    logger.log_test(test_id, name, query, expected_success, result, passed)
                
                logger.log("")
            
            # Run invalid tests
            if invalid_tests:
                logger.log("─" * 100)
                logger.log(f"CUSTOM INVALID TESTS ({len(invalid_tests)} tests)")
                logger.log("─" * 100)
                logger.log("")
                
                for test_id, name, query, expected_success, _ in invalid_tests:
                    total_tests += 1
                    result = parse_query(query)
                    passed = result['success'] == expected_success
                    
                    if passed:
                        passed_tests += 1
                    else:
                        failed_tests += 1
                    
                    logger.log_test(test_id, name, query, expected_success, result, passed)
                
                logger.log("")
        else:
            if run_builtin:
                logger.log("")
            logger.log("⚠️  No custom test files found in:")
            logger.log(f"    - {VALID_QUERIES_DIR}")
            logger.log(f"    - {INVALID_QUERIES_DIR}")
            logger.log("")
    
    # ─────────────────────────────────────────────────────────────────────
    # SUMMARY
    # ─────────────────────────────────────────────────────────────────────
    
    logger.log("=" * 100)
    logger.log("TEST SUMMARY")
    logger.log("=" * 100)
    logger.log(f"Total Tests:  {total_tests}")
    logger.log(f"Passed:       {passed_tests} ✅")
    logger.log(f"Failed:       {failed_tests} ❌")
    if total_tests > 0:
        success_rate = 100 * passed_tests / total_tests
        logger.log(f"Success Rate: {success_rate:.1f}%")
    logger.log("=" * 100)
    logger.log("")
    
    if failed_tests == 0 and total_tests > 0:
        logger.log("🎉 ALL TESTS PASSED! Parser is production-ready! 🎉")
    elif failed_tests > 0:
        logger.log(f"⚠️  {failed_tests} test(s) failed. Check log file for details.")
    else:
        logger.log("⚠️  No tests were run.")
    
    logger.log("")
    logger.log(f"Log file: {LOG_FILE}")
    logger.log(f"Results: {RESULTS_FILE}")
    
    # Save results
    logger.save_results()
    
    return failed_tests == 0

# ════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
