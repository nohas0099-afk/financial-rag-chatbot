"""
Small, dependency-free utility functions used across the UI modules.
Nothing here touches the RAG pipeline (step01-step07) or the FAISS index
directly except reading/writing a sidecar JSON file that tracks which
PDFs have been indexed -- this is purely UI bookkeeping.
"""
import json
import os
from datetime import datetime

INDEXED_FILES_LOG = "indexed_files.json"


def format_file_size(num_bytes: int) -> str:
    """Human readable file size, e.g. 1.4 MB."""
    size = float(num_bytes)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def now_str() -> str:
    return datetime.now().strftime("%b %d, %Y - %I:%M %p")


def load_indexed_files() -> list:
    """Returns metadata for every PDF that has been merged into the FAISS index."""
    if not os.path.exists(INDEXED_FILES_LOG):
        return []
    try:
        with open(INDEXED_FILES_LOG, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def append_indexed_file(name: str, size_bytes: int, num_pages: int) -> None:
    files = load_indexed_files()
    # avoid duplicate entries if the same filename is re-uploaded
    files = [f for f in files if f["name"] != name]
    files.append(
        {
            "name": name,
            "size": format_file_size(size_bytes),
            "pages": num_pages,
            "uploaded_at": now_str(),
        }
    )
    with open(INDEXED_FILES_LOG, "w") as f:
        json.dump(files, f, indent=2)


def clear_indexed_files() -> None:
    if os.path.exists(INDEXED_FILES_LOG):
        os.remove(INDEXED_FILES_LOG)
