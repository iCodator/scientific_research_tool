#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Boolean Query Parser v7.0 - Comprehensive Test Suite

Tests für die neu entwickelte Parser-Architektur mit:
- Phase 1: Preprocess (Kommentare, Leerzeilen, Whitespace)
- Phase 2: Format Detection (SINGLE_LINE vs MULTI_LINE)
- Phase 3: Validation & Parsing (FORMAT-spezifische Regeln)

VERWENDUNG:
    python -m pytest tests/test_parser_v7.py -v
    python -m pytest tests/test_parser_v7.py::TestPreprocessing -v
    python -m pytest tests/test_parser_v7.py::TestFormatDetection::test_detect_single_line_simple -v
"""

import pytest
from tests.src.core.boolean_parser import (
    parse_query,
    preprocess,
    detect_format,
    normalize_op,
    is_balanced_parens,
    parse_single_line,
    parse_multiline,
    validate_single_line,
    validate_multiline,
    tokenize,
    ParseError,
)


# ════════════════════════════════════════════════════════════════════════════
# PHASE 1: PREPROCESSING TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestPreprocessing:
    """Test Phase 1: Preprocess (comments, blank lines, whitespace)"""

    def test_preprocess_removes_comments(self):
        """Test that comments are removed"""
        query = '"cancer" AND "treatment" # this is a comment'
        result = preprocess(query)
        assert result == ['"cancer" AND "treatment"']

    def test_preprocess_removes_blank_lines(self):
        """Test that blank lines are removed"""
        query = '"cancer"\n\n"treatment"'
        result = preprocess(query)
        assert result == ['"cancer"', '"treatment"']

    def test_preprocess_trims_whitespace(self):
        """Test that whitespace is trimmed"""
        query = '  "cancer"   AND   "treatment"  '
        result = preprocess(query)
        assert result == ['"cancer"   AND   "treatment"']

    def test_preprocess_empty_query(self):
        """Test empty query preprocessing"""
        query = ""
        result = preprocess(query)
        assert result == []

    def test_preprocess_only_comments(self):
        """Test query with only comments"""
        query = "# this is only a comment\n# another comment"
        result = preprocess(query)
        assert result == []

    def test_preprocess_multiline_with_comments(self):
        """Test multiline query with comments"""
        query = '"cancer"\nAND # joining two terms\n"treatment"'
        result = preprocess(query)
        assert result == ['"cancer"', 'AND', '"treatment"']


# ════════════════════════════════════════════════════════════════════════════
# OPERATOR NORMALIZATION TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestOperatorNormalization:
    """Test operator normalization to English"""

    def test_normalize_english_and(self):
        """Test English AND remains AND"""
        assert normalize_op("AND") == "AND"

    def test_normalize_german_und(self):
        """Test German UND -> AND"""
        assert normalize_op("UND") == "AND"

    def test_normalize_english_or(self):
        """Test English OR remains OR"""
        assert normalize_op("OR") == "OR"

    def test_normalize_german_oder(self):
        """Test German ODER -> OR"""
        assert normalize_op("ODER") == "OR"

    def test_normalize_english_not(self):
        """Test English NOT remains NOT"""
        assert normalize_op("NOT") == "NOT"

    def test_normalize_german_nicht(self):
        """Test German NICHT -> NOT"""
        assert normalize_op("NICHT") == "NOT"

    def test_normalize_german_kein(self):
        """Test German KEIN -> NOT"""
        assert normalize_op("KEIN") == "NOT"

    def test_normalize_german_keine(self):
        """Test German KEINE -> NOT"""
        assert normalize_op("KEINE") == "NOT"

    def test_normalize_german_ohne(self):
        """Test German OHNE -> NOT"""
        assert normalize_op("OHNE") == "NOT"

    def test_normalize_case_insensitive(self):
        """Test case insensitive normalization"""
        assert normalize_op("and") == "AND"
        assert normalize_op("And") == "AND"
        assert normalize_op("und") == "AND"

    def test_normalize_invalid_operator(self):
        """Test invalid operator returns None"""
        assert normalize_op("XYZ") is None


# ════════════════════════════════════════════════════════════════════════════
# PARENTHESES VALIDATION TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestParenthesesValidation:
    """Test parentheses balancing and detection"""

    def test_balanced_parens_simple(self):
        """Test simple balanced parentheses"""
        assert is_balanced_parens("()") is True

    def test_balanced_parens_nested(self):
        """Test nested balanced parentheses"""
        assert is_balanced_parens("(())") is True

    def test_balanced_parens_with_content(self):
        """Test balanced parentheses with content"""
        assert is_balanced_parens('("cancer")') is True

    def test_unbalanced_parens_too_many_open(self):
        """Test unbalanced parentheses (too many open)"""
        assert is_balanced_parens("(()") is False

    def test_unbalanced_parens_too_many_close(self):
        """Test unbalanced parentheses (too many close)"""
        assert is_balanced_parens("())") is False

    def test_balanced_parens_ignores_quoted(self):
        """Test that quotes inside don't affect balance check"""
        assert is_balanced_parens('("(not paren)")') is True

    def test_multiple_pairs_balanced(self):
        """Test multiple balanced pairs"""
        assert is_balanced_parens("()()()") is True


# ════════════════════════════════════════════════════════════════════════════
# TOKENIZATION TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestTokenization:
    """Test tokenization of queries"""

    def test_tokenize_simple_and(self):
        """Test simple AND tokenization"""
        tokens = tokenize('"cancer" AND "treatment"')
        assert tokens == ['"cancer"', 'AND', '"treatment"']

    def test_tokenize_with_parens(self):
        """Test tokenization with parentheses"""
        tokens = tokenize('("cancer" AND "treatment")')
        assert tokens == ['(', '"cancer"', 'AND', '"treatment"', ')']

    def test_tokenize_nested_parens(self):
        """Test tokenization with nested parentheses"""
        tokens = tokenize('(("cancer") AND ("treatment"))')
        assert tokens == ['(', '(', '"cancer"', ')', 'AND', '(', '"treatment"', ')', ')']

    def test_tokenize_ignores_parens_in_quotes(self):
        """Test that parentheses inside quotes are not split"""
        tokens = tokenize('"can(cer)" AND "treat)ment"')
        assert tokens == ['"can(cer)"', 'AND', '"treat)ment"']

    def test_tokenize_multiple_spaces(self):
        """Test that multiple spaces are normalized"""
        tokens = tokenize('"cancer"    AND    "treatment"')
        assert tokens == ['"cancer"', 'AND', '"treatment"']


# ════════════════════════════════════════════════════════════════════════════
# PHASE 2: FORMAT DETECTION TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestFormatDetection:
    """Test Phase 2: Format detection (SINGLE_LINE vs MULTI_LINE)"""

    def test_detect_single_line_simple(self):
        """Test simple single line detection"""
        lines = ['"cancer" AND "treatment"']
        assert detect_format(lines) == "SINGLE_LINE"

    def test_detect_multiline_three_lines(self):
        """Test multi-line detection with 3 lines"""
        lines = ['"cancer"', 'AND', '"treatment"']
        assert detect_format(lines) == "MULTI_LINE"

    def test_detect_multiline_five_lines(self):
        """Test multi-line detection with 5 lines"""
        lines = ['"cancer"', 'AND', '"tumor"', 'AND', '"treatment"']
        assert detect_format(lines) == "MULTI_LINE"

    def test_detect_single_line_two_lines(self):
        """Test that two-line format is single-line (not valid multiline)"""
        lines = ['"cancer"', '"treatment"']
        assert detect_format(lines) == "SINGLE_LINE"

    def test_detect_multiline_german_operators(self):
        """Test multiline detection with German operators"""
        lines = ['"Krebs"', 'UND', '"Behandlung"']
        assert detect_format(lines) == "MULTI_LINE"


# ════════════════════════════════════════════════════════════════════════════
# SINGLE-LINE PARSING TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestSingleLineParsing:
    """Test SINGLE_LINE format parsing"""

    def test_parse_simple_and(self):
        """Test simple AND query"""
        result = parse_query('"cancer" AND "treatment"')
        assert result['success'] is True
        assert result['format'] == 'SINGLE_LINE'

    def test_parse_simple_or(self):
        """Test simple OR query"""
        result = parse_query('"cancer" OR "tumor"')
        assert result['success'] is True

    def test_parse_german_operators(self):
        """Test German operators in single-line"""
        result = parse_query('"Krebs" UND "Behandlung"')
        assert result['success'] is True
        assert 'AND' in result['output']

    def test_parse_with_parentheses(self):
        """Test single-line with parentheses"""
        result = parse_query('("cancer" OR "tumor") AND "treatment"')
        assert result['success'] is True

    def test_parse_unquoted_term_fails(self):
        """Test that unquoted terms fail"""
        result = parse_query('cancer AND treatment')
        assert result['success'] is False

    def test_parse_mixed_operators_fails(self):
        """Test that mixed operators at depth 0 fail"""
        result = parse_query('"cancer" AND "treatment" OR "tumor"')
        assert result['success'] is False

    def test_parse_mixed_operators_with_parens_succeeds(self):
        """Test that mixed operators with proper parens succeed"""
        result = parse_query('("cancer" AND "treatment") OR "tumor"')
        assert result['success'] is True


# ════════════════════════════════════════════════════════════════════════════
# MULTI-LINE PARSING TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestMultiLineParsing:
    """Test MULTI_LINE format parsing"""

    def test_parse_multiline_and_three_lines(self):
        """Test basic 3-line AND query"""
        query = '"cancer"\nAND\n"treatment"'
        result = parse_query(query)
        assert result['success'] is True
        assert result['format'] == 'MULTI_LINE'

    def test_parse_multiline_and_five_lines(self):
        """Test 5-line AND query"""
        query = '"cancer"\nAND\n"tumor"\nAND\n"treatment"'
        result = parse_query(query)
        assert result['success'] is True

    def test_parse_multiline_or_three_lines(self):
        """Test basic 3-line OR query"""
        query = '"cancer"\nOR\n"tumor"'
        result = parse_query(query)
        assert result['success'] is True

    def test_parse_multiline_german_und(self):
        """Test multiline with German UND operator"""
        query = '"Krebs"\nUND\n"Behandlung"'
        result = parse_query(query)
        assert result['success'] is True

    def test_parse_multiline_even_count_fails(self):
        """Test that even count fails"""
        query = '"cancer"\nAND\n"tumor"\nAND'
        result = parse_query(query)
        assert result['success'] is False

    def test_parse_multiline_mixed_operators_fails(self):
        """Test that mixed operators fail"""
        query = '"cancer"\nAND\n"tumor"\nOR\n"treatment"'
        result = parse_query(query)
        assert result['success'] is False


# ════════════════════════════════════════════════════════════════════════════
# EDGE CASES & ERROR HANDLING
# ════════════════════════════════════════════════════════════════════════════

class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_query(self):
        """Test empty query"""
        result = parse_query("")
        assert result['success'] is False

    def test_only_whitespace(self):
        """Test query with only whitespace"""
        result = parse_query("   \n  \n  ")
        assert result['success'] is False

    def test_single_term_quoted(self):
        """Test single quoted term"""
        result = parse_query('"cancer"')
        assert result['success'] is True

    def test_single_term_not_quoted(self):
        """Test single unquoted term"""
        result = parse_query('cancer')
        assert result['success'] is False

    def test_long_query(self):
        """Test long complex query"""
        query = '(("cancer" OR "tumor" OR "malignancy") AND ("treatment" OR "therapy") NOT "animal")'
        result = parse_query(query)
        assert result['success'] is True

    def test_deep_nesting(self):
        """Test deeply nested parentheses"""
        query = '((((("cancer"))))'
        result = parse_query(query)
        assert result['success'] is True


# ════════════════════════════════════════════════════════════════════════════
# LANGUAGE SUPPORT TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestLanguageSupport:
    """Test English and German language support"""

    def test_german_und_operator(self):
        """Test German UND operator"""
        result = parse_query('"Krebs" UND "Behandlung"')
        assert result['success'] is True
        assert 'AND' in result['output']

    def test_german_oder_operator(self):
        """Test German ODER operator"""
        result = parse_query('"Krebs" ODER "Tumor"')
        assert result['success'] is True
        assert 'OR' in result['output']

    def test_mixed_languages(self):
        """Test mixing English and German operators"""
        result = parse_query('"cancer" UND "treatment" NOT "animal"')
        assert result['success'] is True
        assert 'AND' in result['output']
        assert 'NOT' in result['output']


# ════════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestIntegration:
    """Integration tests combining multiple features"""

    def test_full_workflow_single_line(self):
        """Test full workflow for single-line query"""
        query = '("cancer" OR "tumor") AND "treatment"'
        result = parse_query(query)
        assert result['success'] is True
        assert result['format'] == 'SINGLE_LINE'

    def test_full_workflow_multi_line(self):
        """Test full workflow for multi-line query"""
        query = '"cancer"\nAND\n"treatment"\nAND\n"therapy"'
        result = parse_query(query)
        assert result['success'] is True
        assert result['format'] == 'MULTI_LINE'

    def test_comment_removal_integration(self):
        """Test that comments are properly removed"""
        query = '"cancer" # search for cancer\nAND\n"treatment"'
        result = parse_query(query)
        assert result['success'] is True

    def test_operator_normalization_integration(self):
        """Test that operators are normalized"""
        query = '"cancer" UND "treatment" NICHT "animal"'
        result = parse_query(query)
        assert result['success'] is True
        assert 'AND' in result['output']
        assert 'NOT' in result['output']


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
