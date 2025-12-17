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
