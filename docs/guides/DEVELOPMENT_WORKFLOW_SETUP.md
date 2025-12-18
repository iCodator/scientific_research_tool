# 🔧 DEVELOPMENT WORKFLOW SETUP - DETAILED CONFIRMATION

**Date**: December 18, 2025  
**Status**: ✅ **PRE-IMPLEMENTATION SETUP**  
**Purpose**: Establish develop branch workflow and code standards

---

## ✅ REQUIREMENTS CONFIRMATION

I confirm I understand and will implement the following requirements:

### Requirement 1: Use Develop Branch for Changes ✅

**What This Means**:
- ✅ ALL code changes go to `develop` branch, NOT `main`
- ✅ `main` branch remains stable and production-ready
- ✅ Changes are made in isolation, tested, then merged
- ✅ Clear separation between development and production

**Why This Matters**:
- Protects production code in `main`
- Allows parallel development
- Enables code review before merging
- Rollback capability if needed

**I Will Do This**: ✅ CONFIRMED

---

### Requirement 2: Versioning on All Code ✅

**What This Means**:
- ✅ Every file has version information at the top
- ✅ Version format: `v1.0.0` (semantic versioning)
- ✅ Include: Date, version, author, description
- ✅ Version increments with each significant change

**Example Format**:
```python
# ============================================================================
# FILE: boolean_parser.py
# VERSION: v1.1.0 (Enhanced with field-term recognition)
# DATE: December 18, 2025
# AUTHOR: AI Assistant
# DESCRIPTION: Boolean Query Parser with field-specific syntax support
#
# CHANGELOG:
# v1.0.0 - Initial implementation (Dec 17, 2025)
# v1.1.0 - Added field-term recognition (Dec 18, 2025)
# ============================================================================
```

**I Will Do This**: ✅ CONFIRMED

---

### Requirement 3: Detailed Comments for Laypeople ✅

**What This Means**:
- ✅ Comments explain WHAT the code does, not HOW it works technically
- ✅ Assume reader has basic Python knowledge but not domain expertise
- ✅ Explain WHY decisions were made
- ✅ Include examples where helpful
- ✅ No assumption of prior knowledge about Boolean parsers

**Comment Style**:
```python
# This function recognizes if a token is a field-specific term.
# For example: "cancer"[MeSH] or 'tumor'[TIAB]
# 
# A field-specific term has:
#   1. A quoted search term (with " or ')
#   2. Square brackets with a field code inside
#
# Examples that PASS this check:
#   "cancer"[MeSH]      ← Double-quoted term with field
#   'tumor'[TIAB]       ← Single-quoted term with field
#   "2020-2025"[pdat]   ← Date range with field
#
# Examples that FAIL this check:
#   cancer[MeSH]        ← Term not quoted
#   "cancer"field       ← No brackets
#   "cancer"[MeSH][PubMed]  ← Multiple brackets
#
# The function returns True if the pattern matches, False otherwise.
def is_field_term(token: str) -> bool:
```

**I Will Do This**: ✅ CONFIRMED

---

### Requirement 4: Files Always Available for Download ✅

**What This Means**:
- ✅ Every code file created is provided as a downloadable document
- ✅ NOT embedded only in responses
- ✅ Clear file paths provided
- ✅ Ready to copy-paste or download
- ✅ Includes file extension (.py, .json, etc.)

**Implementation**:
- Each file will be created using `create_text_file` tool
- Explicit directory path shown: `src/core/boolean_parser.py`
- File ready for immediate use
- Clear instructions on where to place it

**I Will Do This**: ✅ CONFIRMED

---

### Requirement 5: Directory Structure Always Specified ✅

**What This Means**:
- ✅ EVERY file includes its full path from project root
- ✅ Format: `src/core/boolean_parser.py`
- ✅ Never ambiguous about where to place files
- ✅ Consistent with existing project structure
- ✅ Include in file header AND in instructions

**Example Specification**:
```
FILE: is_field_term_function.py
DIRECTORY: src/core/
FULL PATH: src/core/boolean_parser.py
PURPOSE: Add field-term recognition function
PLACEMENT: Add this code to existing boolean_parser.py in validate_single_line()
```

**I Will Do This**: ✅ CONFIRMED

---

## 📋 STEP-BY-STEP BRANCH SETUP INSTRUCTIONS

### PHASE 1: UPDATE MAIN BRANCH

**Step 1.1: Check Git Status**
```bash
# Navigate to your project directory
cd /path/to/scientific-research-tool

# Check current branch
git branch

# Expected output:
# * main
#   (other branches if any)
```

**Step 1.2: Verify You're on Main**
```bash
# Make sure you're on the main branch
git checkout main

# Should output:
# Already on 'main'
```

**Step 1.3: View Current Status**
```bash
# Check if there are any uncommitted changes
git status

# Expected output will show:
# - "On branch main" ✓
# - "nothing to commit, working tree clean" ✓ (if no changes)
# OR
# - List of uncommitted files (if changes exist)
```

**Step 1.4: Add All Changes (if any exist)**
```bash
# If you have uncommitted changes, add them all
git add .

# Verify what will be committed
git diff --cached

# Confirm this includes all your changes
```

**Step 1.5: Create Commit (if changes exist)**
```bash
# Only do this if Step 1.3 showed uncommitted changes

git commit -m "Update: Complete boolean parser analysis and documentation (Dec 18, 2025)"

# Expected output:
# [main xxxxxxx] Update: Complete boolean parser analysis...
# X files changed, Y insertions(+), Z deletions(-)
```

**Step 1.6: Verify Commit (if you created one)**
```bash
# View the commit you just made
git log --oneline -1

# Expected output:
# xxxxxxx Update: Complete boolean parser analysis and documentation (Dec 18, 2025)
```

**Step 1.7: Pull Latest (Optional but Recommended)**
```bash
# If your repository is connected to a remote (GitHub, etc.)
# Pull the latest changes from remote main
git pull origin main

# If you get "Permission denied" or other errors, your repository might be local only
# This is fine - skip to next phase if local-only
```

**✅ RESULT**: Main branch is now up-to-date with all changes committed

---

### PHASE 2: CREATE DEVELOP BRANCH

**Step 2.1: Create Develop Branch from Main**
```bash
# Create a new branch called 'develop' based on current main
git branch develop

# This creates the branch locally
```

**Step 2.2: Verify Branch Was Created**
```bash
# List all branches
git branch

# Expected output:
# * main          ← You are here (asterisk shows current)
#   develop       ← Your new branch
```

**Step 2.3: Switch to Develop Branch**
```bash
# Switch to the develop branch
git checkout develop

# Expected output:
# Switched to branch 'develop'
```

**Step 2.4: Verify You're on Develop**
```bash
# Check current branch
git branch

# Expected output:
# * develop       ← You are now here
#   main
```

**Step 2.5: Verify Develop Has Main's Content**
```bash
# List files to confirm develop branch has all files from main
ls -la

# You should see the same files as before (all your analysis documents, etc.)
```

**✅ RESULT**: Develop branch is created and ready for development

---

### PHASE 3: VERIFY SETUP

**Step 3.1: Confirm You're Ready**
```bash
# Show current branch and status
echo "=== Current Branch ===" && git branch && \
echo "=== Git Status ===" && git status && \
echo "=== Latest Commit ===" && git log --oneline -1

# Expected output:
# === Current Branch ===
# * develop      ← Shows you're on develop
# === Git Status ===
# On branch develop
# nothing to commit, working tree clean
# === Latest Commit ===
# xxxxxxx Update: Complete boolean parser analysis... ← Shows main's commit
```

**Step 3.2: View Develop Branch Log**
```bash
# See the commit history of develop branch
git log --oneline -5

# Should show the same commits as main (since develop was created from main)
```

**✅ RESULT**: Setup is complete and verified

---

### PHASE 4: ONGOING WORKFLOW

**For Every Code Change**:

**Step 4.1: Before Starting Work**
```bash
# Always make sure you're on develop branch
git checkout develop

# Verify status
git status
# Should show: "On branch develop"
```

**Step 4.2: After Making Changes**
```bash
# View what changed
git status

# Add changes
git add .

# Create commit with clear message
git commit -m "Feature: Add is_field_term() function for field recognition (Dec 18, 2025)"

# Expected commit message format:
# [Action]: [What was changed] ([Date])
# Actions: Feature, Fix, Update, Refactor, etc.
```

**Step 4.3: View Your Work**
```bash
# See what you've done on develop branch
git log --oneline -5 develop

# See what's different from main
git diff main develop --stat

# This shows files changed since develop branched from main
```

**Step 4.4: When Ready to Merge to Main**
```bash
# DO NOT do this yet - just knowing the process

# 1. Switch to main
git checkout main

# 2. Merge develop into main
git merge develop

# 3. Switch back to develop for next iteration
git checkout develop
```

**✅ RESULT**: Clear, repeatable workflow established

---

## 📝 BRANCH MANAGEMENT SUMMARY

### What's What

```
MAIN BRANCH (main)
├─ Contains: Stable, production-ready code
├─ Status: Never broken, always deployable
├─ Access: Only merge tested code from develop
└─ Files: Only verified, final versions

DEVELOP BRANCH (develop)
├─ Contains: New features, improvements, fixes
├─ Status: Work in progress, testing ground
├─ Access: Where all development happens
└─ Files: All versions with comments and documentation
```

### Branch Strategy

```
Day 1: Create develop branch from main
       ↓
Day 2-7: Work in develop branch
         ├─ Create new files
         ├─ Modify existing files
         ├─ Add comments and documentation
         ├─ Test thoroughly
         └─ Commit regularly with clear messages
       ↓
Day 7: Merge develop to main (if ready)
       ├─ All tests pass ✓
       ├─ All comments complete ✓
       ├─ All documentation updated ✓
       └─ Ready for production ✓
```

---

## 📂 FILE STRUCTURE & CONVENTIONS

### Directory Organization

```
project-root/
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── boolean_parser.py          ← Main parser (v1.1.0)
│   │   ├── logging_manager.py         ← Logging (v1.0.0)
│   │   └── query_parser_with_comments.py  ← Comment handler (v1.0.0)
│   ├── databases/
│   │   ├── __init__.py
│   │   ├── database_adapter.py        ← Abstract base (v1.0.0)
│   │   ├── pubmed.py                  ← PubMed adapter (v1.0.0)
│   │   ├── europe_pmc.py              ← EU PMC adapter (v1.0.0)
│   │   └── cochrane.py                ← Cochrane adapter (v1.0.0)
│   └── config/
│       ├── __init__.py
│       └── .env                       ← Configuration (v1.0.0)
├── tests/
│   ├── __init__.py
│   ├── test_boolean_parser.py         ← Parser tests (v1.0.0)
│   └── test_field_terms.py            ← Field-term tests (v1.1.0)
├── docs/
│   ├── COMPREHENSIVE_FIELD_SYNTAX_ANALYSIS.md
│   ├── SCENARIOS_VISUAL_SUMMARY.txt
│   ├── analysis-documents/
│   │   ├── EXECUTIVE_SUMMARY_NO_CODE_CHANGES.md
│   │   ├── QUICK_REFERENCE_SCENARIOS.txt
│   │   └── ... (other analysis documents)
│   └── guides/
│       ├── DEVELOPMENT_WORKFLOW_SETUP.md (this file)
│       └── PHASE_1_IMPLEMENTATION_GUIDE.md (to be created)
├── .git/                              ← Git repository
├── .gitignore
├── README.md
└── main.py                            ← Entry point
```

### File Header Format

Every file will include this header:

```python
# ============================================================================
# FILE: filename.py
# DIRECTORY: src/core/
# FULL PATH: src/core/filename.py
# VERSION: v1.0.0
# DATE: December 18, 2025
# AUTHOR: AI Assistant
# DESCRIPTION: What this file does in plain English
#
# PURPOSE: Why this file exists in the project
#
# DEPENDENCIES:
#   - Other files it depends on
#   - External libraries if any
#
# CHANGELOG:
# v1.0.0 - Initial creation (Dec 18, 2025)
# v1.0.1 - Bug fix for X (Dec 19, 2025)
# v1.1.0 - Added feature Y (Dec 20, 2025)
#
# ============================================================================
```

### Comment Standards

**Code Comments** (in functions):
```python
def is_field_term(token: str) -> bool:
    """
    Check if a token is a field-specific search term.
    
    WHAT THIS DOES:
    Recognizes patterns like "cancer"[MeSH] or 'tumor'[TIAB]
    These are search terms with database field codes attached.
    
    WHY IT MATTERS:
    PubMed and other databases allow searching specific fields (like titles, 
    abstracts, MeSH headings). This function identifies such patterns so they 
    can be properly handled during query parsing.
    
    PARAMETERS:
    token (str): A token from the parsed query
                 Example: "cancer"[MeSH]
    
    RETURNS:
    bool: True if token matches field-term pattern, False otherwise
    
    EXAMPLES:
    >>> is_field_term('"cancer"[MeSH]')
    True
    
    >>> is_field_term('cancer[MeSH]')  # Not quoted
    False
    
    >>> is_field_term('"cancer"')  # No field code
    False
    """
```

---

## ✅ DETAILED CONFIRMATION CHECKLIST

### Understanding Confirmed ✅

- ✅ Develop branch will be created from current main
- ✅ ALL future work happens in develop branch only
- ✅ Main branch remains stable and untouched
- ✅ Clear separation between development and production
- ✅ Git workflow is established for ongoing use

### Versioning Confirmed ✅

- ✅ Every file has version number (v1.0.0 format)
- ✅ Version header at top of every file
- ✅ CHANGELOG section tracks all changes
- ✅ Date of change always recorded
- ✅ Semantic versioning used (MAJOR.MINOR.PATCH)

### Comments Confirmed ✅

- ✅ Detailed comments for non-technical readers
- ✅ Explain WHAT and WHY, not just HOW
- ✅ Examples provided in docstrings
- ✅ No assumption of domain expertise required
- ✅ Clear sections: PURPOSE, DESCRIPTION, EXAMPLES, etc.

### File Management Confirmed ✅

- ✅ Every file provided for download
- ✅ NEVER embedded only in response text
- ✅ Always in downloadable format
- ✅ Directory path explicitly stated
- ✅ Full path from project root shown

### Path Specification Confirmed ✅

- ✅ Every file shows directory: `src/core/`
- ✅ Every file shows full path: `src/core/boolean_parser.py`
- ✅ Unambiguous placement instructions
- ✅ Consistent with project structure
- ✅ Included in both file header and instructions

---

## 📋 NEXT STEPS (Awaiting Confirmation)

### Step 1: User Confirms Understanding
**User should confirm**:
- ✅ "I understand the branch workflow"
- ✅ "I understand the versioning requirements"
- ✅ "I understand the comment standards"
- ✅ "I understand the file download/placement requirements"
- ✅ "I'm ready to proceed with Phase 1"

### Step 2: User Executes Setup Instructions
**User should run** (copy-paste ready):
```bash
# Phase 1: Update main branch
cd /path/to/scientific-research-tool
git status
git add .
git commit -m "Update: Complete boolean parser analysis and documentation (Dec 18, 2025)"

# Phase 2: Create develop branch
git branch develop
git checkout develop

# Phase 3: Verify
git branch
git status
git log --oneline -1
```

### Step 3: Confirmation of Ready State
**User should confirm**:
- ✅ "Branch setup complete"
- ✅ "Currently on develop branch"
- ✅ "Ready for Phase 1 implementation"

### Step 4: Begin Phase 1 Implementation
Once confirmed:
1. Create is_field_term() function (with full documentation)
2. Provide complete updated boolean_parser.py file
3. Provide test file (test_field_terms.py)
4. All files ready for download with clear paths
5. All files with version numbers and detailed comments

---

## 🎯 SUMMARY FOR YOU

### What I've Confirmed ✅

I understand and will implement:

1. **Develop Branch Workflow**
   - All code changes in `develop` branch
   - Main branch stays stable
   - Clear isolation of development work

2. **Versioning on All Code**
   - v1.0.0, v1.1.0, etc. format
   - Version header in every file
   - CHANGELOG section tracking changes
   - Date, author, description always included

3. **Detailed Comments for Everyone**
   - Explain WHAT code does, not just HOW
   - Assume basic Python, not domain expertise
   - Include examples and use cases
   - Clear PURPOSE and DESCRIPTION sections

4. **Files Always Available for Download**
   - Every file provided downloadable
   - NOT embedded only in response
   - Ready to copy-paste or download
   - Clear instructions for placement

5. **Directory Structure Always Specified**
   - Full path shown: `src/core/boolean_parser.py`
   - Unambiguous placement
   - In both header and instructions
   - Consistent with project structure

### What Comes Next ⏳

**When you confirm you've completed the branch setup**, I will:
1. Provide complete Phase 1 implementation
2. Create is_field_term() function with full documentation
3. Update boolean_parser.py with field-term support
4. Provide test file for verification
5. All files versioned, commented, and ready to download
6. All files with clear directory paths

---

## ❓ QUESTIONS TO CONFIRM

Please confirm the following:

### Question 1: Branch Setup
**"Do you understand the step-by-step instructions for setting up the develop branch?"**

### Question 2: Ongoing Workflow
**"Are you ready to use the git workflow for all future development?"**

### Question 3: Implementation Ready
**"Once you complete the branch setup, do you want me to immediately begin Phase 1 implementation?"**

### Question 4: Code Standards
**"Do the versioning, commenting, and file management standards match your expectations?"**

---

**Status**: ✅ **DETAILED CONFIRMATION COMPLETE**

**Next Action**: Await your confirmation on the questions above, then proceed with Phase 1 implementation.
