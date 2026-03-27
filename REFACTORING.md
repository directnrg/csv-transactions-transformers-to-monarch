# Refactoring Summary

## Overview

Extracted common functionality from two working transaction processing scripts into a shared utility module. This reduces duplication, improves maintainability, and applies SOLID principles without changing existing behavior.

## Changes Made

### 1. Shared Utility Module (`transaction_utils.py`)

**CSVLoader**
- Centralized encoding detection (utf-8, latin1, cp1252, iso-8859-1)
- Eliminates repeated try-except logic across scripts

**CategoryMapper**
- Reusable keyword-to-category matching logic
- Accepts keyword mapping as parameter
- Builds sorted keyword list (longest first for specificity)
- Warns on duplicate keywords across categories

**CategoryNormalizer**
- Consistent category name formatting (Title Case)
- Removes underscores and extra spaces

### 2. Script Updates

Both `Bancolombia transactions processing to monarch.py` and `Neo transactions processing to monarch.py` now:
- Import shared utilities instead of duplicating logic
- Use `CSVLoader.load()` for encoding detection
- Use `CategoryMapper` for keyword matching
- Use `CategoryNormalizer` for formatting
- Support directory paths (auto-generates filename)

## Benefits

| Aspect | Improvement |
|--------|-------------|
| **Maintainability** | Change keyword matching logic once, affects both scripts |
| **Reusability** | Utility classes can be imported by future scripts |
| **Testing** | Pure functions in utilities are easier to unit test |
| **Clarity** | Each class has a single, well-defined responsibility |
| **Flexibility** | Path handling supports files and directories |

## Preserved Behavior

✅ Exact same output format
✅ All keywords maintained
✅ Currency conversion (Bancolombia)
✅ Column transformations
✅ Categorization results
✅ User experience

## Design Approach

**Single Responsibility**: Each utility class handles one concern (encoding, categorization, normalization).

**Dependency Injection**: Scripts pass keyword mappings to CategoryMapper rather than having it hardcoded.

**Minimal Abstraction**: Utilities are focused classes, not over-engineered frameworks.
