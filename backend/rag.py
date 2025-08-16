"""
Lightweight retrieval component for the CDSS backend.

This module implements a simple information retrieval engine using TF‑IDF.  It
indexes text files located in the `data/guidelines/` folder and returns the
most relevant paragraph given a free‑text query.  It can be replaced with a
vector database or integrated into a retrieval‑augmented generation pipeline.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class GuidelineRAG:
    """A simple retrieval helper for guideline documents."""

    def __init__(self, guidelines_path: Path) -> None:
        # Load and parse guidelines
        if not guidelines_path.exists():
            raise FileNotFoundError(f"Guidelines file not found: {guidelines_path}")
        with guidelines_path.open("r", encoding="utf-8") as f:
            raw_text = f.read()
        # Split paragraphs on blank lines
        paragraphs = [p.strip() for p in raw_text.split("\n\n") if p.strip()]
        if not paragraphs:
            raise ValueError("No guideline sections found in the file.")
        self.sections: List[str] = paragraphs
        # Fit TF‑IDF vectorizer
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.sections)

    def query(self, query_str: str) -> Tuple[str, float]:
        """Return the most relevant guideline section and its similarity score."""
        if not query_str:
            return "", 0.0
        query_vec = self.vectorizer.transform([query_str])
        # Compute cosine similarity scores
        scores = (self.tfidf_matrix @ query_vec.T).toarray().ravel()
        if scores.size == 0:
            return "", 0.0
        idx = int(np.argmax(scores))
        return self.sections[idx], float(scores[idx])


def load_rag() -> GuidelineRAG:
    """Helper to instantiate the RAG using the default guideline file.

    This function constructs the path to the guideline file relative to the
    project root.  It assumes the following directory layout:

    project_root/
        backend/
        data/guidelines/hf_guideline.txt
    """
    backend_dir = Path(__file__).resolve().parents[1]
    # The project root is the parent of the backend directory
    project_root = backend_dir
    guidelines_file = project_root / "data" / "guidelines" / "hf_guideline.txt"
    return GuidelineRAG(guidelines_file)
