"""
Lightweight persistence layer for the playground backend.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import HTTPException

DATA_DIR = Path(__file__).resolve().parent / "data"
HISTORY_PATH = DATA_DIR / "prompt_history.json"


def _load_entries() -> List[Dict[str, Any]]:
    if not HISTORY_PATH.exists():
        return []
    try:
        data = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"Invalid history file: {exc}")
    return data if isinstance(data, list) else []


def _save_entries(entries: List[Dict[str, Any]]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_PATH.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def list_history() -> List[Dict[str, Any]]:
    """Return history sorted by creation date (descending)."""
    entries = _load_entries()
    return sorted(entries, key=lambda item: item.get("created_at", ""), reverse=True)


def list_references() -> List[Dict[str, Any]]:
    return [entry for entry in list_history() if entry.get("liked")]


def add_session(session: Dict[str, Any]) -> Dict[str, Any]:
    entries = _load_entries()
    now_iso = datetime.utcnow().isoformat()
    entry = {
        "id": str(uuid.uuid4()),
        "created_at": now_iso,
        "liked": False,
        **session,
    }
    entries.append(entry)
    _save_entries(entries)
    return entry


def set_like(session_id: str, liked: bool) -> Dict[str, Any]:
    entries = _load_entries()
    updated: Optional[Dict[str, Any]] = None
    for entry in entries:
        if entry.get("id") == session_id:
            entry["liked"] = liked
            updated = entry
            break

    if updated is None:
        raise HTTPException(status_code=404, detail="Session not found.")

    _save_entries(entries)
    return updated

