# 📝 HOW TO UPDATE `src/core/__init__.py` - VISUAL GUIDE

---

## 🎯 QUICK SUMMARY

```
File Location: src/core/__init__.py
Task:          Replace all content with new imports
Time:          2 minutes
Difficulty:    ⭐ Easy
```

---

## 📍 BEFORE → AFTER

### ❌ BEFORE (Old/Wrong Content)
```python
# Add this import to make parser accessible
from .boolean_parser import BooleanParser

__all__ = [
    'BooleanParser',
    'DatabaseAdapter',
    'LoggingManager',
    'QueryCompiler',
    'QueryDetector',
    'QueryValidator',
]
```

### ✅ AFTER (New/Correct Content)
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

from .boolean_parser import (
    parse_query,
    preprocess,
    detect_format,
    OPERATOR_MAP,
    ParseError,
)

from .logging_manager import LoggingManager

from .query_parser_with_comments import (
    load_query_with_comments,
)

from .database_adapter import DatabaseAdapter

from .query_compiler import QueryCompiler

__all__ = [
    'parse_query',
    'preprocess',
    'detect_format',
    'OPERATOR_MAP',
    'ParseError',
    'LoggingManager',
    'load_query_with_comments',
    'DatabaseAdapter',
    'QueryCompiler',
]

__version__ = '1.0.0'
__author__ = 'Scientific Research Tool Team'
__description__ = 'Boolean Query Parser for Scientific Databases'
```

---

## 🚀 3 WAYS TO DO IT

### Way 1: Manual Edit (Easiest)
```
┌─────────────────────────────────────────┐
│ 1. Open:  nano src/core/__init__.py     │
│ 2. Select all: Ctrl+A                   │
│ 3. Delete: Delete key                   │
│ 4. Paste: (the new content from above)  │
│ 5. Save:  Ctrl+O → Enter → Ctrl+X      │
└─────────────────────────────────────────┘
```

### Way 2: One Command (Linux/Mac)
```bash
cat > src/core/__init__.py << 'EOF'
"""
Scientific Research Tool - Core Modules
...
(paste the new content here)
...
"""
EOF
```

### Way 3: Python Script
```bash
python << 'EOF'
content = """
Scientific Research Tool - Core Modules
...
(paste the new content here)
...
"""
with open('src/core/__init__.py', 'w') as f:
    f.write(content)
print('✅ Done!')
EOF
```

---

## ✅ VERIFY IT WORKS

After saving, run this:

```bash
python -c "from src.core import parse_query; print('✅ Success!')"
```

**Expected output:**
```
✅ Success!
```

---

## 📊 FILE STRUCTURE VISUALIZATION

```
scientific_research_tool/
│
└── src/
    │
    ├── __init__.py ........................ Empty (or minimal)
    │
    └── core/
        │
        ├── __init__.py ................... 👈 THIS FILE (UPDATE IT!)
        │
        ├── boolean_parser.py ............ ✅ Imported
        ├── logging_manager.py ........... ✅ Imported
        ├── query_parser_with_comments.py ✅ Imported
        ├── database_adapter.py .......... ✅ Imported
        ├── query_compiler.py ............ ✅ Imported (existing)
        │
        ├── databases/
        │   ├── __init__.py
        │   ├── pubmed.py
        │   ├── europe_pmc.py
        │   └── cochrane.py
        │
        └── config/
            ├── __init__.py
            ├── settings.py
            ├── pubmed-syntax.json
            └── europe-pmc-syntax.json
```

---

## 🎬 STEP-BY-STEP WALKTHROUGH

### Step 1: Navigate to file
```bash
cd scientific_research_tool
nano src/core/__init__.py
```

You'll see something like:
```python
# Add this import to make parser accessible
from .boolean_parser import BooleanParser

__all__ = [
    'BooleanParser',
    ...
]
```

### Step 2: Select all content
```
Press: Ctrl+A
```

All text turns highlighted.

### Step 3: Delete everything
```
Press: Delete (or Backspace)
```

File is now empty.

### Step 4: Paste new content
```
Paste the content from the "AFTER" section above
(Or copy from COMPLETE_INIT_COPY_PASTE.txt)
```

### Step 5: Save the file
```
Press: Ctrl+O
Press: Enter
Press: Ctrl+X
```

File is saved! ✅

---

## 🧪 TEST SCENARIOS

### Test 1: Basic import
```python
python -c "
from src.core import parse_query
print('✅ parse_query imported')
"
```

### Test 2: All imports
```python
python -c "
from src.core import (
    parse_query,
    LoggingManager,
    load_query_with_comments,
    DatabaseAdapter,
    QueryCompiler
)
print('✅ All imports work!')
"
```

### Test 3: Use the parser
```python
python -c "
from src.core import parse_query
result = parse_query('(cancer OR tumor) AND treatment')
print('Result:', result)
"
```

Expected output:
```
Result: {'success': True, 'format': 'SINGLE_LINE', 'output': '((cancer) OR (tumor)) AND (treatment)'}
```

---

## ❓ TROUBLESHOOTING

### Error: "ImportError: cannot import name 'parse_query'"
**Check:**
- [ ] Is `boolean_parser.py` in `src/core/`?
- [ ] Is it named correctly (not `boolean_parser.txt` or similar)?
- [ ] Does the file contain `def parse_query(...)`?

### Error: "No module named 'src.core'"
**Check:**
- [ ] Does `src/core/__init__.py` exist?
- [ ] Does `src/__init__.py` exist?

### Error: File won't save in nano
**Try:**
- [ ] Press Ctrl+O first, then Enter, then Ctrl+X
- [ ] Or use different editor: `code src/core/__init__.py`

---

## 📋 CHECKLIST

- [ ] File location correct: `src/core/__init__.py`
- [ ] All old content deleted
- [ ] New content pasted correctly
- [ ] File saved
- [ ] Test command runs successfully: `python -c "from src.core import parse_query; print('✅ Success')"`

---

## 🎉 DONE!

Your `src/core/__init__.py` is now properly configured with all the new modules.

You can now use clean imports everywhere:

```python
# Clean import syntax
from src.core import parse_query, LoggingManager, load_query_with_comments
```

Instead of:

```python
# Old verbose syntax
from src.core.boolean_parser import parse_query
from src.core.logging_manager import LoggingManager
from src.core.query_parser_with_comments import load_query_with_comments
```

Much better! ✨

---

**Time elapsed**: ~2 minutes ⏱️
**Difficulty**: ⭐ Easy
**Next step**: Continue with integration guide
