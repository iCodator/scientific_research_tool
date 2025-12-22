# 📋 COMPLETE FILE ANALYSIS - Scientific Research Tool
## Detailed Overview for All Python & JSON Files
**Analysis Date:** December 22, 2025
**Project:** Scientific Research Tool - Multi-Database Query Compiler
**Framework:** Boolean Query Parser for PubMed, Europe PMC & Cochrane Library

---

## 📂 FILE STRUCTURE & DIRECTORY CLASSIFICATION

```
scientific_research_tool/
├── src/core/              ← CORE PARSING & COMPILATION
│   ├── boolean_parser.py
│   ├── query_compiler.py
│   ├── query_detector.py
│   ├── query_validator.py
│   ├── query_parser_with_comments.py
│   ├── logging_manager.py
│   └── database_adapter.py
├── src/config/            ← CONFIGURATION & SYNTAX RULES
│   ├── settings.py
│   ├── pubmed-syntax.json
│   └── europe-pmc-syntax.json
├── src/databases/         ← DATABASE API ADAPTERS
│   ├── pubmed.py
│   ├── europe_pmc.py
│   └── cochrane.py
└── main.py               ← ENTRY POINT (PROJECT ROOT)
```

---

# 🔍 DETAILED FILE ANALYSIS

## **1. BOOLEAN_PARSER.PY** (29,595 characters)
**Location:** `src/core/boolean_parser.py`
**Version:** v1.2.1 | **Last Updated:** December 22, 2025
**Purpose:** Validate and analyze boolean search queries with detailed reporting

### What It Does (In Simple Terms)
Think of this as a **grammar checker for database queries**. Just like a spell-checker validates English sentences, this tool validates scientific database queries to make sure they follow the correct syntax rules.

### Core Functions

| Function | Purpose | Key Feature |
|----------|---------|-------------|
| `is_field_term(token)` | Detects field-specific terms like `"cancer"[MeSH]` | Identifies quoted content with field tags |
| `tokenize(query)` | Breaks query into individual tokens/words | Keeps field-terms together as single units |
| `validate_single_line(query)` | Validates syntax of one-line queries | Checks operators, parentheses balance, token sequence |
| `validate_multiline(query)` | Validates multi-line formatted queries | Handles complex structures with newlines |

### Validation Rules

✅ **Valid Query Examples:**
- `"cancer"[MeSH] AND therapy` (field-specific search)
- `(cancer OR tumor) AND (2015:2025[pdat])` (complex with date range)
- Multi-line queries with proper formatting

❌ **Invalid Query Examples:**
- `AND cancer` (starts with operator)
- `cancer AND` (ends with operator)
- `(cancer AND tumor` (unbalanced parentheses)
- `cancer AND AND therapy` (double operator)

### Special Features
- **Field-term Recognition:** Automatically identifies PubMed-specific terms like `[MeSH]`, `[TIAB]`, `[pdat]`
- **Quoted String Handling:** Supports single `'` and double `"` quotes
- **Multiline Support:** Can validate queries split across multiple lines
- **Detailed Logging:** Provides comprehensive error messages with examples

---

## **2. QUERY_PARSER_WITH_COMMENTS.PY** (12,964 characters)
**Location:** `src/core/query_parser_with_comments.py`
**Purpose:** Load queries from files with Python-style comment support

### What It Does (In Simple Terms)
Allows you to write search queries with **helpful comments** (like code comments) that get automatically removed before processing. This makes complex queries more understandable.

### Core Functionality

**Main Function: `load_query_with_comments(filepath)`**
- Input: Text file with queries and comments
- Output: Cleaned query string + original content

**How Comments Work:**
```
# Full-line comment (entire line ignored)
'Coenzym Q10'      # Inline comment (rest of line ignored)
AND (2015:2025[pdat])  # Date range
```

After parsing → `'Coenzym Q10' AND (2015:2025[pdat])`

### Comment Processing Rules
1. **Full-line comments:** Lines starting with `#` are completely ignored
2. **Inline comments:** Text after `#` on a line is removed
3. **Smart detection:** Ignores `#` inside quotes or brackets
4. **Whitespace cleanup:** Multiple spaces collapsed to single space

---

## **3. QUERY_COMPILER.PY** (9,351 characters)
**Location:** `src/core/query_compiler.py`
**Purpose:** Translate universal queries to database-specific syntax

### What It Does (In Simple Terms)
Imagine a **translator** that converts a general search query into the specific language each database understands. The same user query works for PubMed, Europe PMC, and Cochrane—just automatically translated for each.

### The Translation Problem
Different databases have different syntax:

| Database | Format Example |
|----------|---|
| **User Input (Universal)** | `(cancer OR tumor) AND (2015:2025[pdat])` |
| **PubMed** | `(cancer OR tumor) AND (2015:2025[pdat])` ← Uses `[pdat]` |
| **Europe PMC** | `(cancer OR tumor) AND PUB_YEAR:(2015 TO 2025)` ← Uses `PUB_YEAR:` and `TO` |
| **Cochrane** | `(cancer OR tumor) AND (2015:2025)` ← Removes `[pdat]` tag |

### Core Compilation Methods

1. **`_compile_for_pubmed(query)`**
   - Input: Universal query
   - Keeps `[pdat]` format unchanged
   - Output: PubMed-ready query

2. **`_compile_for_europepmc(query)`**
   - Converts `(YYYY:YYYY[pdat])` → `PUB_YEAR:(YYYY TO YYYY)`
   - Output: Europe PMC REST API compatible

3. **`_compile_for_cochrane(query)`**
   - Removes `[pdat]` tags completely
   - Output: Cochrane Library compatible

---

## **4. QUERY_DETECTOR.PY** (11,825 characters)
**Location:** `src/core/query_detector.py`
**Purpose:** Auto-detect if query is already formatted or needs processing

### What It Does (In Simple Terms)
Acts as a **smart classifier** that looks at what the user typed and decides:
- "This looks like a pre-formatted database query" → Use it directly
- "This looks like plain English/German" → Send to LLM for processing

### Query Type Recognition

**PubMed-Formatted Query Detection**
- Looks for markers like `[Title/Abstract]`, `[MeSH Terms]`, `[pdat]`
- Minimum 2 markers needed for high confidence

**Europe PMC-Formatted Query Detection**
- Looks for markers like `TITLE_ABSTRACT:`, `PUB_YEAR:`, `AUTHOR:`
- Minimum 1 marker for confidence

**Natural Language Detection**
- German: Looks for umlauts (`ä`, `ö`, `ü`, `ß`) and German keywords
- English: Default if no German markers found

---

## **5. QUERY_VALIDATOR.PY** (2,702 characters)
**Location:** `src/core/query_validator.py`
**Purpose:** Validate query syntax for specific databases

### What It Does (In Simple Terms)
A **syntax checker** that verifies a query is valid for a specific database before sending it. Prevents wasted API calls with broken queries.

### Validation Checks

1. **Length Check**
   - ❌ Empty or less than 3 characters
   - ✅ Reasonable query length

2. **Format Detection**
   - PubMed: Looks for operators OR field tags
   - Europe PMC: Looks for operators OR field syntax

3. **Bracket Balance**
   - Must have equal number of `(` and `)`

---

## **6. LOGGING_MANAGER.PY** (8,226 characters)
**Location:** `src/core/logging_manager.py`
**Purpose:** Centralized logging for all database operations

### What It Does (In Simple Terms)
Creates a **comprehensive audit trail** of all search operations. Everything goes through one central system that:
- Creates separate log files per database
- Automatically includes timestamps
- Writes to both console AND file simultaneously
- Supports verbose/debug modes

### Singleton Pattern
Only **one LoggingManager instance per database** exists.

### Core Features

| Feature | What It Does |
|---------|---|
| **Automatic Setup** | Creates `logs/` directory if missing |
| **Database Prefix** | Log files named `pubmed_search_2025-12-22.log` |
| **Dual Output** | Logs to file AND console simultaneously |
| **Verbose Mode** | Toggle DEBUG-level logging on/off |
| **File Location** | Returns full path to log file |

---

## **7. DATABASE_ADAPTER.PY** (1,512 characters)
**Location:** `src/core/database_adapter.py`
**Purpose:** Abstract interface for all database implementations

### What It Does (In Simple Terms)
Defines a **contract** that all database adapters must follow. Like a recipe template—every database module must implement these exact methods.

### Why This Design?

✅ **Consistent Interface**
- All adapters implement `search()` the same way
- Main code doesn't care which database it's using

✅ **Plug-and-Play**
- Can add new databases easily
- Just inherit from DatabaseAdapter and implement `search()`

---

## **8. SETTINGS.PY** (9,612 characters)
**Location:** `src/config/settings.py`
**Purpose:** Central configuration management for entire application

### What It Does (In Simple Terms)
A **configuration vault** that loads API keys, email addresses, and preferences from `.env` file instead of hardcoding them in code.

### Key Configurations

#### **PubMed / NCBI Settings**

| Setting | Purpose |
|---------|---------|
| `NCBI_API_KEY` | Speed up PubMed queries |
| `NCBI_EMAIL` | Required contact for NCBI |

#### **Europe PMC Settings**

| Setting | Purpose |
|---------|---------|
| `EUROPE_PMC_BASE_URL` | API endpoint |
| `EUROPE_PMC_EMAIL` | Optional contact |

#### **General Settings**

| Setting | Purpose | Default |
|---------|---------|---------|
| `LOG_DIR` | Where to save logs | `logs/` |
| `REQUEST_TIMEOUT` | HTTP timeout in seconds | `30` |
| `RATE_LIMIT_DELAY` | Pause between API calls | `0.5` |

---

## **9. MAIN.PY** (16,304 characters)
**Location:** `main.py` (Project Root)
**Purpose:** Main entry point orchestrating entire application

### What It Does (In Simple Terms)
The **conductor of an orchestra**—coordinates all components to search scientific databases.

### Command-Line Usage

**Basic search:**
```bash
python main.py --query "cancer AND therapy" --source pubmed --limit 10
```

**Search from file:**
```bash
python main.py --query-file queries/coenzym_q10.txt --source europepmc
```

**With verbose logging:**
```bash
python main.py --query-file queries/test.txt --source pubmed --verbose --output results.csv
```

### Command-Line Arguments

| Argument | Purpose | Example |
|----------|---------|---------|
| `--query` | Direct query string | `"cancer AND therapy"` |
| `--query-file` | Load from file | `queries/test.txt` |
| `--source` | Database to search | `pubmed` / `europepmc` / `cochrane` |
| `--limit` | Max articles | `25` |
| `--output` | Save to file | `results.csv` |
| `--verbose` | Show DEBUG logs | - |

---

## **10. PUBMED.PY** (6,306 characters)
**Location:** `src/databases/pubmed.py`
**Purpose:** PubMed API adapter (E-Utilities)

### What It Does (In Simple Terms)
Communicates with **PubMed's search engine** using their E-Utilities API.

### Key Methods

**`search(query, limit)`**
- Takes query → passes to ESearch
- Gets article IDs
- Fetches metadata for each ID
- Returns standardized results

### Important Fix

⚠️ **DO NOT remove field tags from query!**

❌ **Wrong:** `cancer AND (2015:2025)` (0 results)
✅ **Correct:** `cancer AND (2015:2025[pdat])` (12,345 results)

---

## **11. EUROPE_PMC.PY** (9,505 characters)
**Location:** `src/databases/europe_pmc.py`
**Purpose:** Europe PMC REST API adapter

### What It Does (In Simple Terms)
Searches **Europe PMC's database** (covers PubMed + international journals).

### Date Format Conversion

| Source | Format | Example |
|--------|--------|---------|
| Universal | `YYYY:YYYY[pdat]` | `2015:2025[pdat]` |
| Europe PMC | `PUB_YEAR:(YYYY TO YYYY)` | `PUB_YEAR:(2015 TO 2025)` |

### Pagination System

Uses **cursor-based pagination** for efficient large result sets

---

## **12. COCHRANE.PY** (5,781 characters)
**Location:** `src/databases/cochrane.py`
**Purpose:** Cochrane Library adapter via Europe PMC

### What It Does (In Simple Terms)
Searches **Cochrane Systematic Reviews** (highest quality evidence).

### Implementation Strategy

1. Search Europe PMC with broader query
2. Filter results client-side for Cochrane-specific results
3. Return limited set

### Cochrane Review Detection

A result is Cochrane if it has:
- Journal contains "Cochrane"
- Title contains "Systematic Review"
- DOI starts with `10.1002/14651858`

---

## **13. PUBMED-SYNTAX.JSON** (5,443 characters)
**Location:** `src/config/pubmed-syntax.json`
**Purpose:** Machine-readable PubMed syntax rules

### Direct Search Rules

**Simple Terms:** Case-insensitive, automatic term mapping
**Phrase Search:** Requires double quotes `"..."`
**Boolean Operators:** AND, OR, NOT (uppercase only)
**Wildcard:** `*` with min 4 characters before

### Field-Specific Tags

| Tag | Meaning | Example |
|-----|---------|---------|
| `[ti]` | Title only | `cancer[ti]` |
| `[ab]` | Abstract only | `therapy[ab]` |
| `[tiab]` | Title + Abstract | `cancer[tiab]` |
| `[au]` | Author | `Smith[au]` |
| `[ta]` | Journal Title | `Nature[ta]` |
| `[pdat]` | Publication Date | `2020:2025[pdat]` |
| `[mh]` | MeSH Terms | `cancer[mh]` |

---

## **14. EUROPE-PMC-SYNTAX.JSON** (15,589 characters)
**Location:** `src/config/europe-pmc-syntax.json`
**Purpose:** Machine-readable Europe PMC syntax rules

### Field-Specific Search

| Field | Syntax | Example |
|-------|--------|---------|
| `TITLE` | `TITLE:term` | `TITLE:"breast cancer"` |
| `ABSTRACT` | `ABSTRACT:term` | `ABSTRACT:mitochondria` |
| `AUTH` | `AUTH:name` | `AUTH:"Smith J"` |
| `JOURNAL` | `JOURNAL:name` | `JOURNAL:"The Lancet"` |
| `PUB_YEAR` | `PUB_YEAR:(YYYY-YYYY)` | `PUB_YEAR:(2015-2025)` |

### CRITICAL Rules

**PUB_YEAR:**
- Format: `(YYYY-YYYY)` with dashes
- Parentheses: ROUND `()`
- Wrong: `PUB_YEAR:[2015 TO 2025]`

**FIRST_PDATE:**
- Format: `[YYYY-MM-DD TO YYYY-MM-DD]`
- Parentheses: SQUARE `[]`
- Correct: `FIRST_PDATE:[2020-01-01 TO 2020-12-31]`

---

## 📊 FILE SUMMARY TABLE

| File | Type | Size | Purpose | Location |
|------|------|------|---------|----------|
| boolean_parser.py | Python | 29.5 KB | Query validation | src/core/ |
| query_parser_with_comments.py | Python | 13.0 KB | File loading | src/core/ |
| query_compiler.py | Python | 9.4 KB | DB translation | src/core/ |
| query_detector.py | Python | 11.8 KB | Format detection | src/core/ |
| query_validator.py | Python | 2.7 KB | Syntax validation | src/core/ |
| logging_manager.py | Python | 8.2 KB | Centralized logging | src/core/ |
| database_adapter.py | Python | 1.5 KB | Abstract interface | src/core/ |
| settings.py | Python | 9.6 KB | Configuration | src/config/ |
| main.py | Python | 16.3 KB | Entry point | root |
| pubmed.py | Python | 6.3 KB | PubMed adapter | src/databases/ |
| europe_pmc.py | Python | 9.5 KB | Europe PMC adapter | src/databases/ |
| cochrane.py | Python | 5.8 KB | Cochrane adapter | src/databases/ |
| pubmed-syntax.json | JSON | 5.4 KB | PubMed rules | src/config/ |
| europe-pmc-syntax.json | JSON | 15.6 KB | Europe PMC rules | src/config/ |

---

## 🔗 DEPENDENCIES & RELATIONSHIPS

```
main.py (ENTRY POINT)
├── settings.py (Configuration)
├── query_parser_with_comments.py (File loading)
├── query_validator.py (Syntax check)
├── query_compiler.py (DB translation)
│   ├── pubmed-syntax.json
│   └── europe-pmc-syntax.json
├── logging_manager.py (Audit trail)
├── query_detector.py (Format detection)
├── database_adapter.py (Interface)
│   ├── pubmed.py
│   ├── europe_pmc.py
│   └── cochrane.py
└── boolean_parser.py (Deep analysis)
```

---

## 🎯 KEY ARCHITECTURAL PATTERNS

1. **Singleton Pattern:** LoggingManager (one instance per database)
2. **Abstract Base Class:** DatabaseAdapter (consistent interface)
3. **Adapter Pattern:** PubMed, EuropePMC, Cochrane implementations
4. **Compiler Pattern:** QueryCompiler (syntax transformation)
5. **Configuration Pattern:** Settings (environment variables)
6. **Strategy Pattern:** QueryDetector (different detection strategies)

---

**Analysis Complete** | Generated: December 22, 2025