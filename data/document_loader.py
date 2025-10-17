"""Utilities to load reference documents for the Água Segura chatbot."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Dict

REFERENCE_DIR = Path(__file__).resolve().parent / "references"


def _is_supported(path: Path) -> bool:
    """Return True when the file extension is supported for ingestion."""
    return path.is_file() and path.suffix.lower() in {".md", ".txt"}


@lru_cache(maxsize=1)
def load_reference_documents() -> Dict[str, str]:
    """Load every supported reference document from the repository.

    The function performs a recursive search inside ``data/references`` and returns
    a mapping where the keys are document identifiers relative to the reference
    directory and the values are the decoded file contents.
    """

    documents: Dict[str, str] = {}

    for path in sorted(REFERENCE_DIR.rglob("*")):
        if not _is_supported(path):
            continue

        identifier = path.relative_to(REFERENCE_DIR).with_suffix("")
        documents[str(identifier).replace("\\", "/")] = path.read_text(encoding="utf-8")

    return documents
