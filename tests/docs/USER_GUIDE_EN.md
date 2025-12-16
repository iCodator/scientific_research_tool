# Boolean Query Parser - User Guide

## Overview

The Boolean Query Parser converts human-readable boolean search queries into a standardized, fully parenthesized format. It supports both English and German operators and provides clear error messages when queries are ambiguous or invalid.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Supported Operators](#supported-operators)
3. [Query Formats](#query-formats)
4. [Writing Queries](#writing-queries)
5. [Examples](#examples)
6. [Error Messages](#error-messages)
7. [Best Practices](#best-practices)

---

## Quick Start

### Installation

```bash
# No installation needed - just Python 3.6+
python boolean_parser_v7_0.py
```

### Basic Usage

```bash
# Interactive mode
python boolean_parser_v7_0.py

# From file
python boolean_parser_v7_0.py my_query.txt
```

### Your First Query

```
"cancer" AND "treatment"
```

Output: `((cancer) AND (treatment))`

---

## Supported Operators

The parser supports both English and German operators:

| English | German Equivalents | Description |
|---------|-------------------|-------------|
| **AND** | und | Both terms must appear |
| **OR** | oder | Either term must appear |
| **NOT** | nicht, kein, keine, ohne | Term must NOT appear |

**Note:** Operators are case-insensitive. `AND`, `and`, `And` all work the same.

---

## Query Formats

The parser supports two formats:

### 1. Single-Line Format

Everything on one line. Use this for complex nested queries.

**Example:**
```
"cancer" AND "tumor" OR "neoplasm"
```

**When to use:**
- Simple queries
- Queries with complex nesting across operators
- Queries with mixed operators in parentheses

---

### 2. Multi-Line Format

Queries spread across multiple lines with operators on separate lines.

**Example:**
```
"cancer" OR "tumor"
AND
"treatment"
```

**Rules for Multi-Line:**
1. Must have at least 3 lines
2. Must have an odd number of lines (3, 5, 7, ...)
3. Even-numbered lines (2nd, 4th, 6th...) contain ONLY operators
4. All operators must be the same (all AND, or all OR, or all NOT)
5. Each odd line must have balanced parentheses (no parentheses spanning across operator lines)

**When to use:**
- Long lists of terms with the same operator
- Better readability for simple queries
- When you want to see the structure clearly

---

## Writing Queries

### Rule 1: Always Quote Your Search Terms

✅ **Correct:**
```
"cancer" AND "treatment"
```

❌ **Incorrect:**
```
cancer AND treatment
```

### Rule 2: Use Parentheses for Complex Queries

When mixing operators, use parentheses to make your intent clear:

✅ **Correct:**
```
("cancer" OR "tumor") AND "treatment"
```

❌ **Ambiguous:**
```
"cancer" OR "tumor" AND "treatment"
```
*Is this: (cancer OR tumor) AND treatment? Or: cancer OR (tumor AND treatment)?*

### Rule 3: Multi-Line Queries Need Same Operator

✅ **Correct:**
```
"cancer"
OR
"tumor"
OR
"neoplasm"
```

❌ **Incorrect:**
```
"cancer"
OR
"tumor"
AND
"treatment"
```
*Mixed operators require single-line format with parentheses*

### Rule 4: Each Line Must Be Balanced (Multi-Line)

✅ **Correct:**
```
("cancer" OR "tumor")
AND
("treatment" OR "therapy")
```

❌ **Incorrect:**
```
(("cancer" OR "tumor")
AND
("treatment" OR "therapy"))
```
*First line has unbalanced parentheses - use single-line format instead*

---

## Examples

### Basic Searches

**Simple AND:**
```
"cancer" AND "treatment"
```
→ `((cancer) AND (treatment))`

**Simple OR:**
```
"cancer" OR "tumor"
```
→ `((cancer) OR (tumor))`

**Simple NOT:**
```
"cancer" NOT "benign"
```
→ `((cancer) NOT (benign))`

---

### Multiple Terms

**Multi-Line OR:**
```
"cancer"
OR
"tumor"
OR
"neoplasm"
OR
"carcinoma"
```
→ `((((cancer) OR (tumor)) OR (neoplasm)) OR (carcinoma))`

**Single-Line with parentheses:**
```
("cancer" OR "tumor" OR "neoplasm")
```
→ `(((cancer) OR (tumor)) OR (neoplasm))`

---

### Mixed Operators

**Two different operators (requires parentheses):**
```
("cancer" OR "tumor") AND "treatment"
```
→ `((((cancer) OR (tumor))) AND (treatment))`

**Complex nesting:**
```
(("cancer" OR "tumor") AND ("treatment" OR "therapy")) NOT "benign"
```
→ `(((((cancer) OR (tumor))) AND (((treatment) OR (therapy)))) NOT (benign))`

---

### German Operators

```
"Krebs" UND "Behandlung"
```
→ `((Krebs) AND (Behandlung))`

```
"Tumor" ODER "Neoplasma"
```
→ `((Tumor) OR (Neoplasma))`

```
"Krebs" OHNE "gutartig"
```
→ `((Krebs) NOT (gutartig))`

---

### Multi-Line Complex

```
("cancer" OR "tumor" OR "neoplasm")
AND
("treatment" OR "therapy" OR "intervention")
NOT
("benign" OR "non-malignant")
```
→ `((((((cancer) OR (tumor)) OR (neoplasm))) AND ((((treatment) OR (therapy)) OR (intervention)))) NOT (((benign) OR (non-malignant))))`

---

## Error Messages

The parser provides clear, helpful error messages:

### Unquoted Terms

**Query:**
```
cancer AND treatment
```

**Error:**
```
SINGLE-LINE: Unquoted term 'cancer'
```

**Fix:** Add quotes around all search terms: `"cancer" AND "treatment"`

---

### Mixed Operators Without Parentheses

**Query:**
```
"cancer" OR "tumor" AND "treatment"
```

**Error:**
```
SINGLE-LINE: Mixed operators {'OR', 'AND'} without parens
```

**Fix:** Add parentheses: `("cancer" OR "tumor") AND "treatment"`

---

### Unbalanced Parentheses in Multi-Line

**Query:**
```
(("cancer" OR "tumor")
AND
("treatment"))
```

**Error:**
```
MULTI-LINE: Line 1 has unbalanced parentheses.
  (("cancer" OR "tumor")
  Use SINGLE-LINE format for cross-line nesting.
```

**Fix:** Use single-line format: `(("cancer" OR "tumor") AND ("treatment"))`

---

### Mixed Operators in Multi-Line

**Query:**
```
"cancer"
OR
"tumor"
AND
"treatment"
```

**Error:**
```
MULTI-LINE: Mixed operators {'OR', 'AND'}
```

**Fix:** Either:
1. Use same operator throughout (all OR or all AND)
2. Use single-line with parentheses: `("cancer" OR "tumor") AND "treatment"`

---

## Best Practices

### 1. Start Simple

Begin with simple queries and add complexity gradually:
```
"cancer"                                    # Step 1
"cancer" AND "treatment"                    # Step 2
("cancer" OR "tumor") AND "treatment"       # Step 3
```

### 2. Use Multi-Line for Readability

When you have many terms with the same operator:

**Instead of:**
```
"A" OR "B" OR "C" OR "D" OR "E"
```

**Use:**
```
"A"
OR
"B"
OR
"C"
OR
"D"
OR
"E"
```

### 3. Use Comments

Add comments to explain your query logic:

```
# Search for cancer-related terms
"cancer" OR "tumor" OR "neoplasm"
AND
# Combined with treatment terms
"treatment" OR "therapy"
NOT
# But exclude benign cases
"benign"
```

### 4. Test Incrementally

If you get an error:
1. Simplify your query
2. Test each part separately
3. Combine parts one at a time

### 5. Save Complex Queries

Save your working queries in `.txt` files:

```bash
python boolean_parser_v7_0.py my_complex_query.txt
```

---

## Common Patterns

### Pattern 1: Synonyms

Search for multiple synonyms of the same concept:

```
"cancer" OR "tumor" OR "neoplasm" OR "carcinoma"
```

### Pattern 2: Required + Optional

Search for required terms AND optional variations:

```
"cancer" AND ("treatment" OR "therapy" OR "intervention")
```

### Pattern 3: Include + Exclude

Search for terms but exclude certain types:

```
("cancer" OR "tumor") NOT ("benign" OR "non-malignant")
```

### Pattern 4: Combination Search

Combine multiple concepts:

```
("cancer" OR "tumor")
AND
("treatment" OR "therapy")
AND
("effective" OR "successful")
```

---

## Troubleshooting

### My query works but output looks different

The parser converts your query to a fully parenthesized form. This is normal and ensures unambiguous interpretation.

**Your input:**
```
"A" AND "B" AND "C"
```

**Parser output:**
```
(((A) AND (B)) AND (C))
```

Both mean the same thing - the parser just makes the grouping explicit.

---

### I need to search for quotes in my term

Use escaped quotes inside your search terms:

```
"the \"best\" treatment"
```

---

### My multi-line query fails

Check:
1. Do you have an odd number of lines? (3, 5, 7...)
2. Are even lines ONLY operators?
3. Are all operators the same?
4. Does each odd line have balanced parentheses?

If you can't fix it, use single-line format instead.

---

## Getting Help

If you encounter issues:

1. Check the error message - it usually tells you exactly what's wrong
2. Simplify your query and test parts separately
3. Review the examples in this guide
4. Check if your query follows all the rules

---

## Summary

### ✅ Do:
- Quote all search terms: `"term"`
- Use parentheses for complex queries
- Use same operator in multi-line format
- Keep odd lines balanced in multi-line format
- Add comments to explain your logic

### ❌ Don't:
- Leave terms unquoted: `term` ❌
- Mix operators without parentheses
- Use different operators in multi-line format
- Span parentheses across operator lines in multi-line
- Forget to test complex queries

---

## Quick Reference Card

```
OPERATORS (case-insensitive)
English: AND, OR, NOT
German:  UND, ODER, NICHT/KEIN/KEINE/OHNE

FORMATS
Single-line: "A" AND "B" OR "C"
Multi-line:  "A"
             AND
             "B"

RULES
✓ Always quote terms
✓ Use parentheses for mixed operators
✓ Multi-line = same operator only
✓ Each line balanced in multi-line

EXAMPLES
Simple:    "cancer" AND "treatment"
Multiple:  "A" OR "B" OR "C"
Complex:   ("A" OR "B") AND ("C" OR "D")
Exclude:   "cancer" NOT "benign"
```

---

*For technical details, see the Developer Documentation.*
