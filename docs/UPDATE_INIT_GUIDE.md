# 📝 HOW TO UPDATE `src/core/__init__.py`

**Time**: 2 minutes | **Difficulty**: ⭐ Easy

---

## What is `__init__.py`?

This file tells Python: *"This folder is a package, and here's what's important in it."*

It lets you do this:
```python
# Instead of:
from src.core.boolean_parser import parse_query

# You can do:
from src.core import parse_query
```

---

## Current State

Your `src/core/__init__.py` currently has:
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

**Problem**: It references modules that don't exist (BooleanParser, QueryDetector, etc.)

---

## Solution: Replace the entire file

### Step 1: Open the file
```bash
nano src/core/__init__.py
# or
code src/core/__init__.py
# or
vim src/core/__init__.py
```

### Step 2: Delete all content
Select all and delete (Ctrl+A, then Delete)

### Step 3: Paste this new content

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

### Step 4: Save the file
- **nano**: Ctrl+O, Enter, Ctrl+X
- **vim**: Esc, :wq, Enter
- **VS Code**: Ctrl+S

---

## Verification

### ✅ Test that it works
```bash
python -c "
from src.core import parse_query, LoggingManager, load_query_with_comments, DatabaseAdapter
print('✅ All imports successful!')
print(f'   parse_query: {parse_query}')
print(f'   LoggingManager: {LoggingManager}')
print(f'   load_query_with_comments: {load_query_with_comments}')
print(f'   DatabaseAdapter: {DatabaseAdapter}')
"
```

Expected output:
```
✅ All imports successful!
   parse_query: <function parse_query at 0x...>
   LoggingManager: <class 'src.core.logging_manager.LoggingManager'>
   load_query_with_comments: <function load_query_with_comments at 0x...>
   DatabaseAdapter: <class 'src.core.database_adapter.DatabaseAdapter'>
```

---

## What This File Does

After updating, you can now use simpler imports:

### Before (without proper __init__.py):
```python
from src.core.boolean_parser import parse_query
from src.core.logging_manager import LoggingManager
from src.core.query_parser_with_comments import load_query_with_comments
from src.core.database_adapter import DatabaseAdapter
```

### After (with updated __init__.py):
```python
from src.core import parse_query, LoggingManager, load_query_with_comments, DatabaseAdapter
```

Much cleaner! ✨

---

## Full File Content (Copy-Paste Ready)

If you prefer, just copy and paste this entire block directly into your file:

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

---

## Usage Examples

After updating, you can use it like this:

### Example 1: Parse a query
```python
from src.core import parse_query

result = parse_query('(cancer OR tumor) AND treatment')
print(result)
```

### Example 2: Load a query with comments
```python
from src.core import load_query_with_comments

query, original = load_query_with_comments("queries/myquery.txt")
print(f"Cleaned: {query}")
```

### Example 3: Use logging
```python
from src.core import LoggingManager

manager = LoggingManager("europepmc")
logger = manager.get_logger(__name__)
logger.info("Search started")
```

### Example 4: Create a database adapter
```python
from src.core import DatabaseAdapter

class MyDatabaseAdapter(DatabaseAdapter):
    def search(self, query, limit=25):
        # Your implementation
        pass
```

---

## Troubleshooting

### Issue: "ImportError: cannot import name 'parse_query'"
**Solution**: Make sure all the files are in the correct locations:
- ✅ `src/core/boolean_parser.py` exists
- ✅ `src/core/logging_manager.py` exists
- ✅ `src/core/query_parser_with_comments.py` exists
- ✅ `src/core/database_adapter.py` exists
- ✅ `src/core/query_compiler.py` exists

### Issue: "No module named 'src.core'"
**Solution**: Make sure you have:
- ✅ `src/__init__.py` (exists, can be empty)
- ✅ `src/core/__init__.py` (the file you're updating)

### Issue: The file won't save
**Solution**: Check file permissions:
```bash
ls -la src/core/__init__.py
chmod 644 src/core/__init__.py  # Make readable/writable
```

---

## Quick Copy-Paste Commands

### For Linux/Mac:
```bash
cat > src/core/__init__.py << 'EOF'
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
EOF
```

Then verify:
```bash
python -c "from src.core import parse_query; print('✅ Success')"
```

---

## Summary

| Step | Action | Time |
|------|--------|------|
| 1 | Open `src/core/__init__.py` | 30 sec |
| 2 | Delete old content | 30 sec |
| 3 | Paste new content | 1 min |
| 4 | Save file | 30 sec |
| **Total** | | **2 min** |

---

**Done!** ✅ Your `src/core/__init__.py` is now updated and ready to use.
