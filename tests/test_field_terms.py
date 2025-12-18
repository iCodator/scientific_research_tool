#!/usr/bin/env python3
# ============================================================================
# FILE: test_field_terms.py
# VERSION: v1.0.0 (Field-term recognition test suite)
# DATE: December 18, 2025
# AUTHOR: AI Assistant
# DIRECTORY: tests/
# FULL PATH: tests/test_field_terms.py
#
# DESCRIPTION: Comprehensive test suite for field-specific syntax support
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
#
# ============================================================================

import sys
import os

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
# TEST SETUP
# ============================================================================

class TestResults:
    """Simple test result tracking."""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, test_name):
        self.passed += 1
        print(f"  ✅ {test_name}")
    
    def add_fail(self, test_name, expected, actual, reason=""):
        self.failed += 1
        msg = f"  ❌ {test_name}\n     Expected: {expected}\n     Actual: {actual}"
        if reason:
            msg += f"\n     Reason: {reason}"
        self.errors.append(msg)
        print(msg)
    
    def print_summary(self):
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

def test_group_1_field_term_recognition(results):
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
    
    # Test valid field-terms (should return True)
    print("\n✓ Valid field-terms (should return TRUE):")
    assert_is_field_term('"cancer"[MeSH]', True, 
                        "Double-quoted field-term with MeSH code", results)
    assert_is_field_term("'tumor'[TIAB]", True, 
                        "Single-quoted field-term with TIAB code", results)
    assert_is_field_term('"2020-2025"[pdat]', True, 
                        "Numbers in quotes with date field code", results)
    assert_is_field_term('"(cancer OR tumor)"[TIAB]', True, 
                        "Complex content in quotes with field code", results)
    assert_is_field_term('"Smith J"[AU]', True, 
                        "Author name with AU field code", results)
    
    # Test invalid field-terms (should return False)
    print("\n✗ Invalid field-terms (should return FALSE):")
    assert_is_field_term('cancer[MeSH]', False, 
                        "Term not quoted - not a field-term", results)
    assert_is_field_term('"cancer"', False, 
                        "Quoted term without field code", results)
    assert_is_field_term('"cancer"[]', False, 
                        "Quoted term with empty field code", results)
    assert_is_field_term('cancer', False, 
                        "Simple term without quotes or brackets", results)
    assert_is_field_term('[MeSH]', False, 
                        "Just brackets without quoted term", results)
    assert_is_field_term('"cancer"[MeSH]extra', False, 
                        "Extra characters after bracket", results)


# ============================================================================
# TEST GROUP 2: SINGLE-LINE SCENARIO VALIDATION (7 scenarios)
# ============================================================================

def test_group_2_single_line_scenarios(results):
    """
    Test all 7 single-line field-specific syntax scenarios.
    
    WHAT WE'RE TESTING:
    The validate_single_line() function should accept queries
    with field-specific terms in various combinations.
    
    SCENARIO 1.1: Simple field-term
    SCENARIO 1.2: Multiple field-terms with operator
    SCENARIO 1.3: Mixed - field-term and simple term
    SCENARIO 1.4: Field-terms inside parentheses
    SCENARIO 1.5: Single quotes instead of double quotes
    SCENARIO 1.6: Complex nesting
    SCENARIO 1.7: Numbers in field-term
    """
    print("\n" + "=" * 70)
    print("GROUP 2: SINGLE-LINE SCENARIO TESTS (7 scenarios)")
    print("Testing validate_single_line() function")
    print("=" * 70)
    
    # Scenario 1.1: Simple field-term
    print("\n[Scenario 1.1] Simple field-term:")
    assert_validates_single_line(
        '"cancer"[MeSH]',
        True,
        "1.1 - Simple field-term passes validation",
        results
    )
    
    # Scenario 1.2: Multiple field-terms with AND
    print("\n[Scenario 1.2] Multiple field-terms with operator:")
    assert_validates_single_line(
        '"cancer"[MeSH] AND "treatment"[TIAB]',
        True,
        "1.2 - Multiple field-terms with AND passes validation",
        results
    )
    
    # Scenario 1.3: Mixed - field-term and simple term
    print("\n[Scenario 1.3] Mixed field-term and simple term:")
    assert_validates_single_line(
        '"cancer"[MeSH] AND treatment',
        True,
        "1.3 - Field-term with simple term passes validation",
        results
    )
    
    # Scenario 1.4: Field-terms in parentheses
    print("\n[Scenario 1.4] Field-terms in parentheses:")
    assert_validates_single_line(
        '("cancer"[MeSH] OR "tumor"[TIAB])',
        True,
        "1.4 - Field-terms in parentheses passes validation",
        results
    )
    
    # Scenario 1.5: Single quotes
    print("\n[Scenario 1.5] Single-quoted field-term:")
    assert_validates_single_line(
        "'cancer'[MeSH]",
        True,
        "1.5 - Single-quoted field-term passes validation",
        results
    )
    
    # Scenario 1.6: Complex nesting
    print("\n[Scenario 1.6] Complex nesting:")
    assert_validates_single_line(
        '("cancer"[MeSH] OR treatment) AND "therapy"[TIAB]',
        True,
        "1.6 - Complex nesting with field-terms passes validation",
        results
    )
    
    # Scenario 1.7: Numbers in field-term
    print("\n[Scenario 1.7] Numbers in field-term:")
    assert_validates_single_line(
        '"2020-2025"[pdat]',
        True,
        "1.7 - Date range in field-term passes validation",
        results
    )


# ============================================================================
# TEST GROUP 3: MULTI-LINE SCENARIO VALIDATION (4 scenarios)
# ============================================================================

def test_group_3_multi_line_scenarios(results):
    """
    Test all 4 multi-line field-specific syntax scenarios.
    
    WHAT WE'RE TESTING:
    The validate_multiline() function should accept queries where
    field-specific terms appear on content lines (even-numbered lines).
    
    SCENARIO 2.1: Basic multi-line with field-term
    SCENARIO 2.2: Multiple field-terms on same line
    SCENARIO 2.3: Mixed field-terms and simple terms
    SCENARIO 2.4: Complex nesting in multi-line
    """
    print("\n" + "=" * 70)
    print("GROUP 3: MULTI-LINE SCENARIO TESTS (4 scenarios)")
    print("Testing validate_multiline() function")
    print("=" * 70)
    
    # Scenario 2.1: Basic multi-line
    print("\n[Scenario 2.1] Basic multi-line with field-term:")
    query_2_1 = '("cancer"[MeSH])\nAND\n(treatment)'
    assert_parses_query(
        query_2_1,
        True,
        "2.1 - Basic multi-line with field-term parses successfully",
        results
    )
    
    # Scenario 2.2: Multiple field-terms on same line
    print("\n[Scenario 2.2] Multiple field-terms on same line:")
    query_2_2 = '("cancer"[MeSH] OR "tumor"[TIAB])\nAND\n("treatment"[TIAB])'
    assert_parses_query(
        query_2_2,
        True,
        "2.2 - Multiple field-terms on same line parses successfully",
        results
    )
    
    # Scenario 2.3: Mixed field-terms and simple terms
    print("\n[Scenario 2.3] Mixed field-terms and simple terms:")
    query_2_3 = '("cancer"[MeSH])\nAND\n(treatment OR therapy)'
    assert_parses_query(
        query_2_3,
        True,
        "2.3 - Mixed field-terms and simple terms parses successfully",
        results
    )
    
    # Scenario 2.4: Complex nesting
    print("\n[Scenario 2.4] Complex nesting in multi-line:")
    query_2_4 = '(("cancer"[MeSH] OR "tumor"[TIAB]) AND "2020-2025"[pdat])\nOR\n(therapy)'
    assert_parses_query(
        query_2_4,
        True,
        "2.4 - Complex nesting with field-terms parses successfully",
        results
    )


# ============================================================================
# TEST GROUP 4: QUOTE VARIATION SCENARIOS (2 scenarios)
# ============================================================================

def test_group_4_quote_variations(results):
    """
    Test quote variation scenarios.
    
    WHAT WE'RE TESTING:
    The parser should handle both single and double quotes,
    and support multiple different field codes in one query.
    
    SCENARIO 3.1: Single vs double quotes mixed
    SCENARIO 3.2: Multiple different field codes
    """
    print("\n" + "=" * 70)
    print("GROUP 4: QUOTE VARIATION TESTS (2 scenarios)")
    print("Testing quote variations and field code variety")
    print("=" * 70)
    
    # Scenario 3.1: Single vs double quotes
    print("\n[Scenario 3.1] Single vs double quotes mixed:")
    assert_validates_single_line(
        '"cancer"[MeSH] OR \'tumor\'[TIAB]',
        True,
        "3.1 - Mixed single and double quotes passes validation",
        results
    )
    
    # Scenario 3.2: Multiple different field codes
    print("\n[Scenario 3.2] Multiple different field codes:")
    assert_validates_single_line(
        '"term"[MeSH] AND "term"[TIAB] AND "term"[pdat]',
        True,
        "3.2 - Multiple different field codes passes validation",
        results
    )


# ============================================================================
# TEST GROUP 5: EDGE CASES AND ERROR HANDLING
# ============================================================================

def test_group_5_edge_cases(results):
    """
    Test edge cases to ensure robust error handling.
    
    WHAT WE'RE TESTING:
    The parser should correctly reject invalid syntax
    while accepting valid edge cases.
    """
    print("\n" + "=" * 70)
    print("GROUP 5: EDGE CASES AND ERROR HANDLING")
    print("Testing invalid and boundary cases")
    print("=" * 70)
    
    # Invalid: Not quoted
    print("\n✗ Invalid cases (should FAIL validation):")
    assert_validates_single_line(
        'cancer[MeSH]',
        False,
        "Edge case - Unquoted term with brackets should FAIL",
        results
    )
    
    # Invalid: Empty brackets
    assert_validates_single_line(
        '"cancer"[]',
        False,
        "Edge case - Empty field code should FAIL",
        results
    )
    
    # Valid: Nested parentheses with field-terms
    print("\n✓ Valid edge cases (should PASS validation):")
    assert_validates_single_line(
        '(("cancer"[MeSH] OR "tumor"[TIAB]) AND (treatment))',
        True,
        "Edge case - Deeply nested field-terms should PASS",
        results
    )
    
    # Valid: Field-term with special characters
    assert_validates_single_line(
        '"(cancer OR tumor)"[TIAB]',
        True,
        "Edge case - Field-term with parentheses inside should PASS",
        results
    )


# ============================================================================
# MAIN TEST EXECUTION
# ============================================================================

def main():
    """
    Run all test groups.
    
    WHAT THIS DOES:
    Executes the complete test suite in order, collecting results,
    and printing a summary at the end.
    
    TEST ORGANIZATION:
    - Group 1: Unit tests for is_field_term()
    - Group 2: Single-line scenarios (7 tests)
    - Group 3: Multi-line scenarios (4 tests)
    - Group 4: Quote variations (2 tests)
    - Group 5: Edge cases (4 tests)
    
    Total: 13+ comprehensive tests covering all 13 scenarios plus edge cases
    """
    
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  FIELD-TERM RECOGNITION TEST SUITE".center(68) + "║")
    print("║" + "  Testing Enhanced Boolean Parser v1.1.0".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    results = TestResults()
    
    # Run all test groups
    test_group_1_field_term_recognition(results)
    test_group_2_single_line_scenarios(results)
    test_group_3_multi_line_scenarios(results)
    test_group_4_quote_variations(results)
    test_group_5_edge_cases(results)
    
    # Print summary and exit with appropriate code
    success = results.print_summary()
    
    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
