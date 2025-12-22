#!/usr/bin/env python3
# ============================================================================
# FILE: test_field_terms.py
# VERSION: v1.1.0 (Field-term recognition test suite with logging)
# DATE: December 18, 2025
# AUTHOR: AI Assistant
# DIRECTORY: tests/
# FULL PATH: tests/test_field_terms.py
#
# DESCRIPTION: Comprehensive test suite for field-specific syntax support
#              with detailed logging to tests/logs/
# PURPOSE: Verify that all 13 field-specific syntax scenarios are correctly
#          recognized and validated by the enhanced boolean_parser
#
# TEST COVERAGE: 13 scenarios
#   - Single-line scenarios: 7 tests (1.1 through 1.7)
#   - Multi-line scenarios: 4 tests (2.1 through 2.4)
#   - Quote variation scenarios: 2 tests (3.1 and 3.2)
#
# CHANGELOG:
# v1.0.0 - Initial test suite (Dec 18, 2025)
# v1.1.0 - Added detailed logging to tests/logs/ (Dec 18, 2025)
#
# LOGGING FEATURE:
# - All tests saved with meaningful names in tests/logs/
# - Detailed logs for each test group
# - Timestamp included in log filenames
# - Test results summary in each log
# - JSON export for machine-readability
#
# ============================================================================

import sys
import os
import json
from datetime import datetime

# Add src directory to path so we can import from src.core
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.boolean_parser import (
    parse_query,
    validate_single_line,
    validate_multiline,
    is_field_term,
    tokenize,
)


# ============================================================================
# LOGGING SETUP
# ============================================================================

class TestLogger:
    """
    Handles test logging to tests/logs/ directory.
    
    WHAT THIS DOES:
    Creates detailed log files for every test, organized by test group.
    Each log file has a meaningful name with timestamp for easy reference.
    
    WHY IT MATTERS:
    Detailed logs help track test history, debug failures, and verify
    that all scenarios are being tested consistently over time.
    
    LOG FILE NAMING:
    GROUP_[N]_[GROUPNAME]_[TIMESTAMP].log
    TEST_SUMMARY_[TIMESTAMP].txt (human-readable)
    TEST_SUMMARY_[TIMESTAMP].json (machine-readable)
    """
    
    def __init__(self):
        self.log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        self.ensure_log_dir()
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.test_logs = []
        self.summary_data = {
            'timestamp': datetime.now().isoformat(),
            'test_groups': {},
            'total_passed': 0,
            'total_failed': 0,
            'total_tests': 0
        }
    
    def ensure_log_dir(self):
        """Create tests/logs directory if it doesn't exist."""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            print(f"📁 Created logs directory: {self.log_dir}")
    
    def log_test(self, group_name, test_name, status, details):
        """
        Log a single test result.
        
        WHAT THIS DOES:
        Records detailed information about a single test execution,
        including timestamp, group, name, status, and details.
        
        PARAMETERS:
        group_name (str): Name of test group (e.g., "Group 1: Field-term Recognition")
        test_name (str): Name of individual test (e.g., "Double-quoted field-term with MeSH code")
        status (str): "PASS" or "FAIL"
        details (dict): Test details including expected, actual, reason
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'group': group_name,
            'test_name': test_name,
            'status': status,
            'details': details
        }
        self.test_logs.append(log_entry)
    
    def save_group_log(self, group_name, group_number, tests_passed, tests_failed):
        """
        Save log file for a test group.
        
        WHAT THIS DOES:
        Creates a detailed log file with all test results for one group.
        Filename format: GROUP_[N]_[NAME]_[TIMESTAMP].log
        
        PARAMETERS:
        group_name (str): Name of the test group
        group_number (int): Number of the test group (1, 2, 3, etc.)
        tests_passed (int): Count of tests that passed
        tests_failed (int): Count of tests that failed
        
        RETURNS:
        str: Filename of saved log
        """
        # Create safe filename from group name
        safe_group_name = group_name.replace(':', '').replace(' ', '_').replace('-', '')
        filename = f"GROUP_{group_number}_{safe_group_name}_{self.timestamp}.log"
        filepath = os.path.join(self.log_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"{group_name}\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Tests Passed: {tests_passed}\n")
            f.write(f"Tests Failed: {tests_failed}\n")
            f.write(f"Success Rate: {(tests_passed / max(tests_passed + tests_failed, 1) * 100):.1f}%\n\n")
            
            # Write individual test results
            for log_entry in self.test_logs:
                if log_entry['group'] == group_name:
                    f.write("-" * 80 + "\n")
                    f.write(f"Test: {log_entry['test_name']}\n")
                    f.write(f"Status: {log_entry['status']}\n")
                    f.write(f"Time: {log_entry['timestamp']}\n\n")
                    
                    details = log_entry['details']
                    for key, value in details.items():
                        f.write(f"  {key}: {value}\n")
                    f.write("\n")
        
        print(f"  📝 Log saved: {filename}")
        return filename
    
    def save_summary_log(self, total_passed, total_failed):
        """
        Save overall summary log with JSON for machine-readability.
        
        WHAT THIS DOES:
        Creates comprehensive summary files after all tests complete.
        One file is human-readable text, one is machine-readable JSON.
        
        FILES CREATED:
        - tests/logs/TEST_SUMMARY_[TIMESTAMP].txt (human-readable)
        - tests/logs/TEST_SUMMARY_[TIMESTAMP].json (machine-readable)
        
        PARAMETERS:
        total_passed (int): Total tests that passed
        total_failed (int): Total tests that failed
        """
        self.summary_data['total_passed'] = total_passed
        self.summary_data['total_failed'] = total_failed
        self.summary_data['total_tests'] = total_passed + total_failed
        
        # Save human-readable summary
        summary_filename = f"TEST_SUMMARY_{self.timestamp}.txt"
        summary_filepath = os.path.join(self.log_dir, summary_filename)
        
        with open(summary_filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("FIELD-TERM RECOGNITION TEST SUITE - FINAL SUMMARY\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Timestamp: {self.summary_data['timestamp']}\n")
            f.write(f"Total Tests: {self.summary_data['total_tests']}\n")
            f.write(f"Passed: {total_passed}\n")
            f.write(f"Failed: {total_failed}\n")
            success_rate = (total_passed / max(self.summary_data['total_tests'], 1) * 100)
            f.write(f"Success Rate: {success_rate:.1f}%\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("TEST GROUPS\n")
            f.write("=" * 80 + "\n\n")
            
            for group_name, group_data in self.summary_data['test_groups'].items():
                f.write(f"{group_name}\n")
                f.write(f"  Passed: {group_data['passed']}\n")
                f.write(f"  Failed: {group_data['failed']}\n\n")
        
        # Save JSON summary for machine-readability
        json_filename = f"TEST_SUMMARY_{self.timestamp}.json"
        json_filepath = os.path.join(self.log_dir, json_filename)
        
        with open(json_filepath, 'w', encoding='utf-8') as f:
            json.dump(self.summary_data, f, indent=2)
        
        print(f"\n  📊 Summary saved: {summary_filename}")
        print(f"  📊 JSON saved: {json_filename}")


# ============================================================================
# TEST SETUP
# ============================================================================

class TestResults:
    """
    Simple test result tracking with logging support.
    
    WHAT THIS DOES:
    Tracks test results and integrates with TestLogger to save
    detailed logs for every test execution.
    """
    def __init__(self, logger=None):
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.logger = logger
        self.current_group = None
    
    def set_current_group(self, group_name):
        """Set the current test group for logging."""
        self.current_group = group_name
    
    def add_pass(self, test_name):
        """Record a passing test."""
        self.passed += 1
        print(f"  ✅ {test_name}")
        
        if self.logger:
            self.logger.log_test(
                self.current_group,
                test_name,
                "PASS",
                {"result": "Test passed successfully"}
            )
    
    def add_fail(self, test_name, expected, actual, reason=""):
        """Record a failing test."""
        self.failed += 1
        msg = f"  ❌ {test_name}\n     Expected: {expected}\n     Actual: {actual}"
        if reason:
            msg += f"\n     Reason: {reason}"
        self.errors.append(msg)
        print(msg)
        
        if self.logger:
            self.logger.log_test(
                self.current_group,
                test_name,
                "FAIL",
                {
                    "expected": str(expected),
                    "actual": str(actual),
                    "reason": reason if reason else "No additional reason provided"
                }
            )
    
    def print_summary(self):
        """Print test summary to console."""
        print("\n" + "=" * 70)
        print(f"TEST RESULTS: {self.passed} passed, {self.failed} failed")
        print("=" * 70)
        if self.failed == 0:
            print("✅ ALL TESTS PASSED!")
        return self.failed == 0


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def assert_is_field_term(token, expected, test_name, results):
    """Test is_field_term() function."""
    actual = is_field_term(token)
    if actual == expected:
        results.add_pass(test_name)
        return True
    else:
        results.add_fail(test_name, f"is_field_term({token}) = {expected}", f"got {actual}")
        return False


def assert_validates_single_line(query, expected, test_name, results):
    """Test validate_single_line() function."""
    actual = validate_single_line(query)
    if actual == expected:
        results.add_pass(test_name)
        return True
    else:
        results.add_fail(test_name, f"validate_single_line() = {expected}", f"got {actual}", 
                        f"Query: {query}")
        return False


def assert_parses_query(query, should_succeed, test_name, results):
    """Test parse_query() function."""
    result = parse_query(query)
    actual = result['success']
    if actual == should_succeed:
        results.add_pass(test_name)
        return True
    else:
        results.add_fail(test_name, f"parse_query success = {should_succeed}", 
                        f"got {actual}", f"Query: {query}")
        return False


# ============================================================================
# TEST GROUP 1: UNIT TESTS FOR is_field_term()
# ============================================================================

def test_group_1_field_term_recognition(results, logger):
    """
    Test the is_field_term() function directly.
    
    WHAT WE'RE TESTING:
    The new is_field_term() function should correctly identify
    tokens that match the field-specific term pattern.
    
    PATTERN: "text"[fieldcode] or 'text'[fieldcode]
    """
    print("\n" + "=" * 70)
    print("GROUP 1: FIELD-TERM RECOGNITION TESTS")
    print("Testing is_field_term() function")
    print("=" * 70)
    
    group_name = "Group 1: Field-term Recognition"
    results.set_current_group(group_name)
    group_passed = 0
    group_failed = 0
    
    # Test valid field-terms (should return True)
    print("\n✓ Valid field-terms (should return TRUE):")
    tests = [
        ('"cancer"[MeSH]', True, "Double-quoted field-term with MeSH code"),
        ("'tumor'[TIAB]", True, "Single-quoted field-term with TIAB code"),
        ('"2020-2025"[pdat]', True, "Numbers in quotes with date field code"),
        ('"(cancer OR tumor)"[TIAB]', True, "Complex content in quotes with field code"),
        ('"Smith J"[AU]', True, "Author name with AU field code"),
    ]
    
    for token, expected, name in tests:
        if assert_is_field_term(token, expected, name, results):
            group_passed += 1
        else:
            group_failed += 1
    
    # Test invalid field-terms (should return False)
    print("\n✗ Invalid field-terms (should return FALSE):")
    tests = [
        ('cancer[MeSH]', False, "Term not quoted - not a field-term"),
        ('"cancer"', False, "Quoted term without field code"),
        ('"cancer"[]', False, "Quoted term with empty field code"),
        ('cancer', False, "Simple term without quotes or brackets"),
        ('[MeSH]', False, "Just brackets without quoted term"),
        ('"cancer"[MeSH]extra', False, "Extra characters after bracket"),
    ]
    
    for token, expected, name in tests:
        if assert_is_field_term(token, expected, name, results):
            group_passed += 1
        else:
            group_failed += 1
    
    if logger:
        logger.summary_data['test_groups'][group_name] = {
            'passed': group_passed,
            'failed': group_failed
        }
        logger.save_group_log(group_name, 1, group_passed, group_failed)


# ============================================================================
# TEST GROUP 2: SINGLE-LINE SCENARIO VALIDATION (7 scenarios)
# ============================================================================

def test_group_2_single_line_scenarios(results, logger):
    """
    Test all 7 single-line field-specific syntax scenarios.
    """
    print("\n" + "=" * 70)
    print("GROUP 2: SINGLE-LINE SCENARIO TESTS (7 scenarios)")
    print("Testing validate_single_line() function")
    print("=" * 70)
    
    group_name = "Group 2: Single-line Scenarios"
    results.set_current_group(group_name)
    group_passed = 0
    group_failed = 0
    
    # Scenario 1.1: Simple field-term
    print("\n[Scenario 1.1] Simple field-term:")
    if assert_validates_single_line('"cancer"[MeSH]', True,
                                    "1.1 - Simple field-term passes validation", results):
        group_passed += 1
    else:
        group_failed += 1
    
    # Scenario 1.2: Multiple field-terms with AND
    print("\n[Scenario 1.2] Multiple field-terms with operator:")
    if assert_validates_single_line('"cancer"[MeSH] AND "treatment"[TIAB]', True,
                                    "1.2 - Multiple field-terms with AND passes validation", results):
        group_passed += 1
    else:
        group_failed += 1
    
    # Scenario 1.3: Mixed - field-term and simple term
    print("\n[Scenario 1.3] Mixed field-term and simple term:")
    if assert_validates_single_line('"cancer"[MeSH] AND treatment', True,
                                    "1.3 - Field-term with simple term passes validation", results):
        group_passed += 1
    else:
        group_failed += 1
    
    # Scenario 1.4: Field-terms in parentheses
    print("\n[Scenario 1.4] Field-terms in parentheses:")
    if assert_validates_single_line('("cancer"[MeSH] OR "tumor"[TIAB])', True,
                                    "1.4 - Field-terms in parentheses passes validation", results):
        group_passed += 1
    else:
        group_failed += 1
    
    # Scenario 1.5: Single quotes
    print("\n[Scenario 1.5] Single-quoted field-term:")
    if assert_validates_single_line("'cancer'[MeSH]", True,
                                    "1.5 - Single-quoted field-term passes validation", results):
        group_passed += 1
    else:
        group_failed += 1
    
    # Scenario 1.6: Complex nesting
    print("\n[Scenario 1.6] Complex nesting:")
    if assert_validates_single_line('("cancer"[MeSH] OR treatment) AND "therapy"[TIAB]', True,
                                    "1.6 - Complex nesting with field-terms passes validation", results):
        group_passed += 1
    else:
        group_failed += 1
    
    # Scenario 1.7: Numbers in field-term
    print("\n[Scenario 1.7] Numbers in field-term:")
    if assert_validates_single_line('"2020-2025"[pdat]', True,
                                    "1.7 - Date range in field-term passes validation", results):
        group_passed += 1
    else:
        group_failed += 1
    
    if logger:
        logger.summary_data['test_groups'][group_name] = {
            'passed': group_passed,
            'failed': group_failed
        }
        logger.save_group_log(group_name, 2, group_passed, group_failed)


# ============================================================================
# TEST GROUP 3: MULTI-LINE SCENARIO VALIDATION (4 scenarios)
# ============================================================================

def test_group_3_multi_line_scenarios(results, logger):
    """
    Test all 4 multi-line field-specific syntax scenarios.
    """
    print("\n" + "=" * 70)
    print("GROUP 3: MULTI-LINE SCENARIO TESTS (4 scenarios)")
    print("Testing validate_multiline() function")
    print("=" * 70)
    
    group_name = "Group 3: Multi-line Scenarios"
    results.set_current_group(group_name)
    group_passed = 0
    group_failed = 0
    
    # Scenario 2.1: Basic multi-line
    print("\n[Scenario 2.1] Basic multi-line with field-term:")
    query_2_1 = '("cancer"[MeSH])\nAND\n(treatment)'
    if assert_parses_query(query_2_1, True,
                          "2.1 - Basic multi-line with field-term parses successfully", results):
        group_passed += 1
    else:
        group_failed += 1
    
    # Scenario 2.2: Multiple field-terms on same line
    print("\n[Scenario 2.2] Multiple field-terms on same line:")
    query_2_2 = '("cancer"[MeSH] OR "tumor"[TIAB])\nAND\n("treatment"[TIAB])'
    if assert_parses_query(query_2_2, True,
                          "2.2 - Multiple field-terms on same line parses successfully", results):
        group_passed += 1
    else:
        group_failed += 1
    
    # Scenario 2.3: Mixed field-terms and simple terms
    print("\n[Scenario 2.3] Mixed field-terms and simple terms:")
    query_2_3 = '("cancer"[MeSH])\nAND\n(treatment OR therapy)'
    if assert_parses_query(query_2_3, True,
                          "2.3 - Mixed field-terms and simple terms parses successfully", results):
        group_passed += 1
    else:
        group_failed += 1
    
    # Scenario 2.4: Complex nesting
    print("\n[Scenario 2.4] Complex nesting in multi-line:")
    query_2_4 = '(("cancer"[MeSH] OR "tumor"[TIAB]) AND "2020-2025"[pdat])\nOR\n(therapy)'
    if assert_parses_query(query_2_4, True,
                          "2.4 - Complex nesting with field-terms parses successfully", results):
        group_passed += 1
    else:
        group_failed += 1
    
    if logger:
        logger.summary_data['test_groups'][group_name] = {
            'passed': group_passed,
            'failed': group_failed
        }
        logger.save_group_log(group_name, 3, group_passed, group_failed)


# ============================================================================
# TEST GROUP 4: QUOTE VARIATION SCENARIOS (2 scenarios)
# ============================================================================

def test_group_4_quote_variations(results, logger):
    """
    Test quote variation scenarios.
    """
    print("\n" + "=" * 70)
    print("GROUP 4: QUOTE VARIATION TESTS (2 scenarios)")
    print("Testing quote variations and field code variety")
    print("=" * 70)
    
    group_name = "Group 4: Quote Variations"
    results.set_current_group(group_name)
    group_passed = 0
    group_failed = 0
    
    # Scenario 3.1: Single vs double quotes
    print("\n[Scenario 3.1] Single vs double quotes mixed:")
    if assert_validates_single_line('"cancer"[MeSH] OR \'tumor\'[TIAB]', True,
                                    "3.1 - Mixed single and double quotes passes validation", results):
        group_passed += 1
    else:
        group_failed += 1
    
    # Scenario 3.2: Multiple different field codes
    print("\n[Scenario 3.2] Multiple different field codes:")
    if assert_validates_single_line('"term"[MeSH] AND "term"[TIAB] AND "term"[pdat]', True,
                                    "3.2 - Multiple different field codes passes validation", results):
        group_passed += 1
    else:
        group_failed += 1
    
    if logger:
        logger.summary_data['test_groups'][group_name] = {
            'passed': group_passed,
            'failed': group_failed
        }
        logger.save_group_log(group_name, 4, group_passed, group_failed)


# ============================================================================
# TEST GROUP 5: EDGE CASES AND ERROR HANDLING
# ============================================================================

def test_group_5_edge_cases(results, logger):
    """
    Test edge cases to ensure robust error handling.
    """
    print("\n" + "=" * 70)
    print("GROUP 5: EDGE CASES AND ERROR HANDLING")
    print("Testing invalid and boundary cases")
    print("=" * 70)
    
    group_name = "Group 5: Edge Cases"
    results.set_current_group(group_name)
    group_passed = 0
    group_failed = 0
    
    # Invalid: Not quoted
    print("\n✗ Invalid cases (should FAIL validation):")
    if assert_validates_single_line('cancer[MeSH]', False,
                                    "Edge case - Unquoted term with brackets should FAIL", results):
        group_passed += 1
    else:
        group_failed += 1
    
    # Invalid: Empty brackets
    if assert_validates_single_line('"cancer"[]', False,
                                    "Edge case - Empty field code should FAIL", results):
        group_passed += 1
    else:
        group_failed += 1
    
    # Valid: Nested parentheses with field-terms
    print("\n✓ Valid edge cases (should PASS validation):")
    if assert_validates_single_line('(("cancer"[MeSH] OR "tumor"[TIAB]) AND (treatment))', True,
                                    "Edge case - Deeply nested field-terms should PASS", results):
        group_passed += 1
    else:
        group_failed += 1
    
    # Valid: Field-term with special characters
    if assert_validates_single_line('"(cancer OR tumor)"[TIAB]', True,
                                    "Edge case - Field-term with parentheses inside should PASS", results):
        group_passed += 1
    else:
        group_failed += 1
    
    if logger:
        logger.summary_data['test_groups'][group_name] = {
            'passed': group_passed,
            'failed': group_failed
        }
        logger.save_group_log(group_name, 5, group_passed, group_failed)


# ============================================================================
# MAIN TEST EXECUTION
# ============================================================================

def main():
    """
    Run all test groups with logging.
    """
    
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  FIELD-TERM RECOGNITION TEST SUITE".center(68) + "║")
    print("║" + "  Testing Enhanced Boolean Parser v1.1.0".center(68) + "║")
    print("║" + "  With Detailed Logging to tests/logs/".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Initialize logger
    logger = TestLogger()
    results = TestResults(logger=logger)
    
    # Run all test groups
    test_group_1_field_term_recognition(results, logger)
    test_group_2_single_line_scenarios(results, logger)
    test_group_3_multi_line_scenarios(results, logger)
    test_group_4_quote_variations(results, logger)
    test_group_5_edge_cases(results, logger)
    
    # Save summary logs
    if logger:
        logger.save_summary_log(results.passed, results.failed)
    
    # Print summary and exit with appropriate code
    success = results.print_summary()
    
    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
