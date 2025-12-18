# 📖 COMPREHENSIVE INTEGRATION GUIDE

**Time to Complete**: 15 minutes  
**Difficulty**: ⭐⭐ Easy to Medium  
**Status**: Production Ready

---

## Table of Contents

1. [Preparation](#preparation)
2. [File Organization](#file-organization)
3. [Step-by-Step Integration](#step-by-step-integration)
4. [Configuration](#configuration)
5. [Testing & Verification](#testing--verification)
6. [Troubleshooting](#troubleshooting)
7. [Production Deployment](#production-deployment)

---

## Preparation

### Prerequisites
- Python 3.8+
- All 5 uploaded files ready
- Text editor (nano, vim, or VS Code)
- Terminal access

### Files You'll Need
```
boolean_parser.py
logging_manager.py
query_parser_with_comments.py
database_adapter.py
env.txt
```

---

## File Organization

### Current Project Structure
```
scientific_research_tool/
├── main.py
├── src/
│   ├── core/
│   │   ├── boolean_parser.py (old, if exists)
│   │   ├── query_compiler.py
│   │   ├── settings.py
│   │   ├── database_adapter.py (old, if exists)
│   │   └── __init__.py
│   ├── databases/
│   │   ├── pubmed.py
│   │   ├── europe_pmc.py
│   │   ├── cochrane.py
│   │   └── __init__.py
│   └── config/
│       ├── settings.py
│       ├── pubmed-syntax.json
│       └── europe-pmc-syntax.json
├── .env (or env.txt if not renamed yet)
└── README.md
```

### Target Project Structure
```
scientific_research_tool/
├── main.py
├── .env                          ← Renamed from env.txt
├── src/
│   ├── __init__.py               ← NEW/UPDATED
│   ├── core/
│   │   ├── __init__.py           ← UPDATED (critical!)
│   │   ├── boolean_parser.py     ← NEW
│   │   ├── logging_manager.py    ← NEW
│   │   ├── query_parser_with_comments.py ← NEW
│   │   ├── database_adapter.py   ← NEW (replaces old if exists)
│   │   ├── query_compiler.py     ← EXISTING
│   │   └── settings.py           ← EXISTING
│   ├── databases/
│   │   ├── __init__.py           ← NEW/UPDATED
│   │   ├── pubmed.py
│   │   ├── europe_pmc.py
│   │   └── cochrane.py
│   └── config/
│       ├── __init__.py           ← NEW/UPDATED
│       ├── settings.py
│       ├── pubmed-syntax.json
│       └── europe-pmc-syntax.json
└── docs/                         ← NEW (for documentation)
    ├── UPDATE_INIT_GUIDE.md
    ├── FINAL_STATUS_REPORT.md
    ├── README_INTEGRATION.md
    └── integration_guide.md (this file)
```

---

## Step-by-Step Integration

### ✅ Step 1: Backup Current Files (1 minute)
```bash
# Create backup of existing __init__ files (just in case)
cp src/core/__init__.py src/core/__init__.py.backup
cp src/__init__.py src/__init__.py.backup 2>/dev/null || true
```

### ✅ Step 2: Copy New Core Files (2 minutes)
```bash
# Navigate to project root
cd /path/to/scientific_research_tool

# Copy uploaded files to src/core/
cp /path/to/uploaded/boolean_parser.py src/core/
cp /path/to/uploaded/logging_manager.py src/core/
cp /path/to/uploaded/query_parser_with_comments.py src/core/
cp /path/to/uploaded/database_adapter.py src/core/

# Copy configuration
cp /path/to/uploaded/env.txt .env
```

### ✅ Step 3: Create Empty Package Markers (1 minute)
```bash
# Create __init__.py files (these can be empty initially)
touch src/__init__.py
touch src/databases/__init__.py
touch src/config/__init__.py

# src/core/__init__.py will be updated next
```

### ✅ Step 4: Update src/core/__init__.py (3 minutes)

This is the CRITICAL step. Replace the entire contents:

```bash
nano src/core/__init__.py
```

**Delete all existing content and paste:**

```python
"""
Scientific Research Tool - Core Modules

This package contains the core functionality:
- Boolean Query Parser
- Logging Management
- Query Parsing with Comments
- Database Adapter Interface
- Query Compilation
"""

# ════════════════════════════════════════════════════════════════════════════
# IMPORTS FROM NEW MODULES
# ════════════════════════════════════════════════════════════════════════════

# Boolean Parser - Parse complex multi-line and single-line queries
from .boolean_parser import (
    parse_query,
    preprocess,
    detect_format,
    OPERATOR_MAP,
    ParseError,
)

# Logging Manager - Centralized logging with Singleton pattern
from .logging_manager import LoggingManager

# Query Parser with Comments - Load queries with Python-style # comments
from .query_parser_with_comments import (
    load_query_with_comments,
)

# Database Adapter - Abstract base class for all database adapters
from .database_adapter import DatabaseAdapter

# Query Compiler - Translate queries to database-specific formats
from .query_compiler import QueryCompiler

# ════════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Boolean Parser
    'parse_query',
    'preprocess',
    'detect_format',
    'OPERATOR_MAP',
    'ParseError',
    
    # Logging Manager
    'LoggingManager',
    
    # Query Parser
    'load_query_with_comments',
    
    # Database Adapter
    'DatabaseAdapter',
    
    # Query Compiler
    'QueryCompiler',
]

# ════════════════════════════════════════════════════════════════════════════
# VERSION INFO
# ════════════════════════════════════════════════════════════════════════════

__version__ = '1.0.0'
__author__ = 'Scientific Research Tool Team'
__description__ = 'Boolean Query Parser for Scientific Databases'
```

**Save:** Ctrl+O → Enter → Ctrl+X

### ✅ Step 5: Configure Environment Variables (3 minutes)
```bash
nano .env
```

**Fill in these required fields:**
```bash
# NCBI PubMed API Configuration
NCBI_API_KEY=your_ncbi_api_key_here
NCBI_EMAIL=your_email@example.com

# Optional: Europe PMC Email
EUROPE_PMC_EMAIL=your_email@example.com

# Logging Configuration
LOG_DIR=logs

# Request Configuration
REQUEST_TIMEOUT=30
RATE_LIMIT_DELAY=0.5
```

**Save:** Ctrl+O → Enter → Ctrl+X

### ✅ Step 6: Verify Installation (2 minutes)

Run verification tests:

```bash
# Test 1: Basic imports
python -c "
from src.core import parse_query, LoggingManager, load_query_with_comments, DatabaseAdapter
print('✅ All imports successful!')
"

# Test 2: Parse a query
python -c "
from src.core import parse_query
result = parse_query('(cancer OR tumor) AND treatment')
print('✅ Parser works:', result['success'])
print('   Output:', result['output'])
"

# Test 3: Logging manager
python -c "
from src.core import LoggingManager
manager = LoggingManager('test')
logger = manager.get_logger(__name__)
logger.info('✅ Logging works!')
print('✅ Log file created at:', manager.get_log_file())
"

# Test 4: All modules at once
python -c "
from src.core import (
    parse_query,
    preprocess,
    detect_format,
    LoggingManager,
    load_query_with_comments,
    DatabaseAdapter,
    QueryCompiler
)
print('✅ ALL MODULES IMPORTED SUCCESSFULLY!')
"
```

---

## Configuration

### Required Settings (.env)
```bash
NCBI_API_KEY          # Get from https://www.ncbi.nlm.nih.gov/account/settings/
NCBI_EMAIL            # Your email address
LOG_DIR               # Directory for log files (default: logs)
REQUEST_TIMEOUT       # HTTP timeout in seconds (default: 30)
RATE_LIMIT_DELAY      # Delay between requests in seconds (default: 0.5)
```

### Optional Settings (.env)
```bash
EUROPE_PMC_EMAIL      # For Europe PMC searches
DEBUG                 # Set to true for verbose logging
```

---

## Testing & Verification

### Unit Test: Boolean Parser
```python
from src.core import parse_query

# Test multi-line format
result = parse_query('''(cancer OR tumor)
AND
(treatment OR therapy)
NOT
benign''')

assert result['success'] == True
assert result['format'] == 'MULTI_LINE'
print('✅ Multi-line parsing works!')

# Test single-line format
result = parse_query('(cancer OR tumor) AND treatment')
assert result['success'] == True
assert result['format'] == 'SINGLE_LINE'
print('✅ Single-line parsing works!')

# Test German operators
result = parse_query('cancer UND tumor')
assert 'AND' in result['output']
print('✅ German operator normalization works!')
```

### Unit Test: Query Parser with Comments
```python
from src.core import load_query_with_comments
import tempfile

# Create temporary query file
with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
    f.write("'cancer' # Main term\n")
    f.write("AND\n")
    f.write("'treatment' # Intervention\n")
    temp_file = f.name

query, original = load_query_with_comments(temp_file)
assert "'cancer'" in query
assert "'treatment'" in query
assert "# Main term" not in query
print('✅ Comment removal works!')
```

### Unit Test: Logging Manager
```python
from src.core import LoggingManager
import os

manager = LoggingManager('test_db')
logger = manager.get_logger('test_module')

logger.info('Test message')
logger.warning('Test warning')

log_file = manager.get_log_file()
assert os.path.exists(log_file)
print('✅ Logging manager works!')
print(f'   Log file: {log_file}')
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'src'"
**Solution:**
```bash
# Make sure you're in the project root
cd /path/to/scientific_research_tool
python -c "from src.core import parse_query"
```

### Issue: "ImportError: cannot import name 'parse_query'"
**Check:**
- [ ] Is `boolean_parser.py` in `src/core/`?
- [ ] Run: `ls -la src/core/boolean_parser.py`
- [ ] Check file contains `def parse_query`
- [ ] Try: `python -c "from src.core.boolean_parser import parse_query"`

### Issue: ".env not found or not loaded"
**Solution:**
```bash
# Verify .env exists
ls -la .env

# Verify it's in project root
pwd
# Should show: /path/to/scientific_research_tool

# Verify content
cat .env | head -5
```

### Issue: "AttributeError: module has no attribute 'parse_query'"
**Solution:**
- Update `src/core/__init__.py` correctly
- Verify imports match the template exactly
- Run: `python -c "from src.core.boolean_parser import parse_query"`

---

## Production Deployment

### Pre-Deployment Checklist
- [ ] All 5 files copied to correct locations
- [ ] `src/core/__init__.py` updated correctly
- [ ] `.env` configured with actual API keys
- [ ] All verification tests pass
- [ ] Log directory permissions correct
- [ ] No import errors when running main.py

### Deployment Commands
```bash
# Final verification
python -c "
from src.core import (
    parse_query, LoggingManager, 
    load_query_with_comments, DatabaseAdapter
)
print('✅ Production ready!')
"

# Run main application
python main.py --help

# Test with sample query
python main.py --query '(cancer OR tumor) AND treatment' --source pubmed
```

### Post-Deployment Monitoring
```bash
# Check log files
ls -la logs/

# Monitor for errors
tail -f logs/europepmc_search_*.log

# Verify database adapters
python -c "
from src.databases import PubMedAdapter, EuropePMCAdapter, CochraneAdapter
print('✅ All adapters loaded')
"
```

---

## Success Indicators

You'll know everything is working when:

✅ All import commands succeed  
✅ Boolean parser CLI runs interactively  
✅ Log files created with timestamps  
✅ Comments removed from query files  
✅ main.py runs without errors  
✅ Database searches return results  

---

## Next Steps

1. Run all verification tests
2. Execute a sample query through main.py
3. Check generated log files
4. Deploy to production

---

**Integration Complete!** 🎉
