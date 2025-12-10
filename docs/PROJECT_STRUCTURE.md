════════════════════════════════════════════════════════════════════════════════
RECOMMENDED PROJECT STRUCTURE - Query Parser Documentation
════════════════════════════════════════════════════════════════════════════════

CURRENT SITUATION:
──────────────────
Files scattered, need better organization for documentation & tests.

RECOMMENDED STRUCTURE:
──────────────────────

scientific_research_tool/
│
├── docs/                           ← Dokumentation (NEU)
│   ├── parser/
│   │   ├── README.md               ← Overview
│   │   ├── PARSER_DESIGN.md        ← Architecture & Design
│   │   ├── TEST_RESULTS.md         ← Test Report (v2.3)
│   │   ├── KNOWN_ISSUES.md         ← Issues & Fixes
│   │   └── INTEGRATION_GUIDE.md    ← Wie man den Parser nutzt
│   │
│   └── API/
│       ├── PUBMED_API.md
│       └── EUROPEPMC_API.md
│
├── tests/
│   ├── queries/                    ← Test Input Files
│   │   ├── test_valid_1.txt        ✅ Single-Line AND
│   │   ├── test_valid_2.txt        ✅ Single-Line Grouped
│   │   ├── test_valid_3_multiline.txt  ⚠️  Multi-Line
│   │   ├── 1.txt                   ❌ Invalid (mixed operators)
│   │   ├── 2.txt
│   │   └── 3.txt
│   │
│   └── src/
│       └── core/
│           └── parser_test_precedence.py  ← Parser Module (v2.2)
│
├── src/                            ← Main Code
│   ├── core/
│   │   └── parser.py               ← Production Parser
│   │
│   └── api/
│       ├── pubmed.py
│       └── europepmc.py
│
├── query_parser_v2_3.py            ← Test Runner (Root Level)
├── main.py
├── requirements.txt
└── README.md

════════════════════════════════════════════════════════════════════════════════
MIGRATION PLAN
════════════════════════════════════════════════════════════════════════════════

SCHRITT 1: Erstelle Verzeichnisse
──────────────────────────────────
mkdir -p docs/parser docs/API

SCHRITT 2: Verschiebe/Kopiere Dokumentation
─────────────────────────────────────────────
# Diese Dateien wurden bereits erstellt:
cp TEST_RESULTS.md docs/parser/TEST_RESULTS.md
cp KNOWN_ISSUES.md docs/parser/KNOWN_ISSUES.md

SCHRITT 3: Erstelle fehlende Dokumentation
───────────────────────────────────────────
touch docs/parser/README.md
touch docs/parser/PARSER_DESIGN.md
touch docs/parser/INTEGRATION_GUIDE.md

SCHRITT 4: Cleanup
──────────────────
# Optional: alte Dateien löschen/archivieren
rm TEST_RESULTS.md KNOWN_ISSUES.md  (after copying)

════════════════════════════════════════════════════════════════════════════════
FILE NAMING CONVENTIONS
════════════════════════════════════════════════════════════════════════════════

Documentation Files:
  • README.md              ← Überblick
  • DESIGN.md             ← Architecture & Patterns
  • TEST_RESULTS.md       ← Test Reports
  • KNOWN_ISSUES.md       ← Bugs & Fixes
  • INTEGRATION_GUIDE.md  ← Usage Documentation

Code Files:
  • parser_test_precedence.py   ← Development/Testing
  • parser.py                   ← Production
  • query_parser_v2_3.py        ← Test Runner

Test Files:
  • test_valid_*.txt      ← Valid test cases
  • test_invalid_*.txt    ← Invalid test cases
  • test_edge_*.txt       ← Edge cases

════════════════════════════════════════════════════════════════════════════════
WHATS IN EACH DOCUMENTATION FILE
════════════════════════════════════════════════════════════════════════════════

docs/parser/README.md
  ├─ Overview des Query Parsers
  ├─ Quick Start
  ├─ Features & Limitations
  └─ Links zu anderen Docs

docs/parser/PARSER_DESIGN.md
  ├─ Architecture (4 Phases)
  ├─ Phase 1: Cleaning & Format Detection
  ├─ Phase 2: Operator Precedence Validation
  ├─ Phase 3: Parsing & Parenthesization
  ├─ Phase 4: Date Formatting & Source Conversion
  └─ Data Flow Diagram

docs/parser/TEST_RESULTS.md  ← Du erstellst dies jetzt!
  ├─ Test Overview
  ├─ Test 1 Results
  ├─ Test 2 Results
  ├─ Test 3 Results (mit Issues)
  ├─ Known Issues Summary
  └─ Recommendations

docs/parser/KNOWN_ISSUES.md  ← Code Fixes!
  ├─ Issue #1: Über-Klammerung
  ├─ Root Cause Analysis
  ├─ Fix #1: Smart Parenthesizing
  ├─ Fix #2: Correct Outer Parentheses
  ├─ Complete Fix Checklist
  ├─ Code Diff
  └─ Validation Script

docs/parser/INTEGRATION_GUIDE.md
  ├─ Installation
  ├─ Basic Usage
  ├─ Advanced Usage
  ├─ API Reference
  ├─ Error Handling
  └─ Examples

════════════════════════════════════════════════════════════════════════════════
RECOMMENDED READING ORDER
════════════════════════════════════════════════════════════════════════════════

For New Developers:
  1. docs/parser/README.md           ← What & Why
  2. docs/parser/PARSER_DESIGN.md    ← How it works
  3. docs/parser/TEST_RESULTS.md     ← What's tested
  4. docs/parser/INTEGRATION_GUIDE.md  ← How to use it

For Maintainers:
  1. docs/parser/KNOWN_ISSUES.md     ← What's broken
  2. docs/parser/PARSER_DESIGN.md    ← Internal structure
  3. Code in tests/src/core/parser_test_precedence.py

For Testers:
  1. docs/parser/TEST_RESULTS.md     ← Test Status
  2. docs/parser/KNOWN_ISSUES.md     ← What to test
  3. Run: python query_parser_v2_3.py tests/queries/<test>.txt

════════════════════════════════════════════════════════════════════════════════
SHELL COMMANDS ZUM SETUP
════════════════════════════════════════════════════════════════════════════════

# 1. Create directories
mkdir -p docs/parser
mkdir -p docs/API

# 2. Copy test results
cp TEST_RESULTS.md docs/parser/
cp KNOWN_ISSUES.md docs/parser/

# 3. List structure
tree docs/

# 4. Verify parser location
find . -name "parser_test_precedence.py" -type f

# 5. Run tests to verify
cd scientific_research_tool
python query_parser_v2_3.py tests/queries/test_valid_1.txt
python query_parser_v2_3.py tests/queries/test_valid_2.txt
python query_parser_v2_3.py tests/queries/test_valid_3_multiline.txt

════════════════════════════════════════════════════════════════════════════════
SUMMARY
════════════════════════════════════════════════════════════════════════════════

✅ Where to put TEST_RESULTS.md:
   → docs/parser/TEST_RESULTS.md

✅ Where to put KNOWN_ISSUES.md:
   → docs/parser/KNOWN_ISSUES.md

✅ Test files belong in:
   → tests/queries/

✅ Parser code belongs in:
   → tests/src/core/parser_test_precedence.py

✅ Test runner:
   → query_parser_v2_3.py (root level, stays where it is)

════════════════════════════════════════════════════════════════════════════════
