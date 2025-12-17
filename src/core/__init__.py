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

# ════════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ════════════════════════════════════════════════════════════════════════════

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

# ════════════════════════════════════════════════════════════════════════════
# VERSION INFO
# ════════════════════════════════════════════════════════════════════════════

__version__ = '1.0.0'
__author__ = 'Scientific Research Tool Team'
__description__ = 'Boolean Query Parser for Scientific Databases'
