"""
Shared utilities for transaction processing.
Extracted for modularity and SOLID principles.
"""

import re
from typing import Optional

import pandas as pd


class CSVLoader:
    """Handles CSV loading with automatic encoding detection."""

    ENCODING_ATTEMPTS = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']

    @staticmethod
    def load(file_path: str, encoding: Optional[str] = None) -> pd.DataFrame:
        """Load CSV file, attempting multiple encodings if needed."""
        encodings_to_try = [encoding] if encoding else CSVLoader.ENCODING_ATTEMPTS

        for enc in encodings_to_try:
            try:
                return pd.read_csv(file_path, encoding=enc)
            except (UnicodeDecodeError, LookupError):
                continue

        raise ValueError(f"Failed to load CSV with any encoding: {encodings_to_try}")


class CategoryNormalizer:
    """Standardizes category names to Title Case."""

    @staticmethod
    def normalize(category: str) -> str:
        """Convert category to title case with proper spacing."""
        if pd.isna(category):
            return category

        normalized = str(category).replace("_", " ")
        normalized = " ".join(normalized.split())
        return normalized.title()


class CategoryMapper:
    """Maps transaction descriptions to categories using keyword matching."""

    def __init__(self, keyword_mapping: dict):
        """Initialize with keyword-to-category mapping."""
        self.keyword_mapping = keyword_mapping
        self._sorted_keywords = self._build_keyword_list()

    def _build_keyword_list(self) -> list:
        """Build sorted keyword list (longest first), detect duplicates."""
        keyword_to_category = {}
        conflicts = {}

        for category, keywords in self.keyword_mapping.items():
            for kw in keywords:
                kw_norm = str(kw).lower()
                if kw_norm in keyword_to_category:
                    conflicts.setdefault(kw_norm, set()).add(category)
                else:
                    keyword_to_category[kw_norm] = category

        if conflicts:
            print(f"⚠ Warning: {len(conflicts)} keywords found in multiple categories")
            for kw, cats in list(conflicts.items())[:5]:
                print(f"  '{kw}' in: {', '.join(sorted(cats))}")

        return sorted(keyword_to_category.items(), key=lambda x: -len(x[0]))

    def map_category(self, text: str, fallback: str = "") -> str:
        """Assign category based on keyword matching (simple substring match)."""
        if pd.isna(text):
            return fallback or "Uncategorized"

        text_lower = str(text).lower()

        for keyword, category in self._sorted_keywords:
            # Simple substring match (permissive, matches better)
            if keyword in text_lower:
                return category

        return fallback or "Uncategorized"
