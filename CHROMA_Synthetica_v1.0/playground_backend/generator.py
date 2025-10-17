"""
Utilities to produce SeaDream prompts in a programmatic (non-interactive) flow.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any, Dict, List, Tuple

from fastapi import HTTPException

from interactive_assistant import (
    THEMES,
    MODEL_TARGETS,
    _load_playbook,
    _normalize_payload,
    _missing_fields,
    _enforce_defaults,
    _format_blueprint,
    _build_model_prompts,
    build_system_prompt,
    build_user_prompt,
    _request_payload,
)
from synthetica.services.llm_client import create_llm_client


@lru_cache(maxsize=1)
def _get_playbook() -> Dict[str, Any]:
    """Load and cache the SeaDream playbook."""
    return _load_playbook()


def _ensure_theme(theme_key: str) -> None:
    if theme_key not in THEMES:
        raise HTTPException(status_code=400, detail=f"Unsupported theme '{theme_key}'.")


def generate_prompt_session(
    brief: str,
    model_name: str,
    theme_key: str,
) -> Dict[str, Any]:
    """
    Generate prompts and blueprint for a single session.

    Returns a dictionary with blueprint text, normalized payload,
    prompts per downstream model, and any checklist/notes produced by the LLM.
    """
    if not brief:
        raise HTTPException(status_code=400, detail="Briefing text cannot be empty.")

    _ensure_theme(theme_key)

    playbook = _get_playbook()
    themes = playbook.get("themes", {})
    theme_data = themes.get(theme_key)
    if theme_data is None:
        raise HTTPException(
            status_code=400,
            detail=f"Theme '{theme_key}' is not configured in the playbook.",
        )

    llm = create_llm_client(model_name=model_name)

    system_prompt = build_system_prompt(playbook, theme_key, theme_data)
    user_prompt = build_user_prompt(brief, theme_key)

    payload_raw = _request_payload(llm, system_prompt, user_prompt)
    payload = _normalize_payload(payload_raw)

    missing = _missing_fields(payload)
    if missing:
        formatted_missing: List[Dict[str, str]] = []
        for component, field in missing:
            entry = {"component": component}
            if field:
                entry["field"] = field
            formatted_missing.append(entry)
        raise HTTPException(
            status_code=422,
            detail={
                "message": "LLM response missing required fields.",
                "missing_fields": formatted_missing,
            },
        )

    _enforce_defaults(payload, theme_data, llm)

    theme_desc = theme_data.get("description", theme_key)
    blueprint_text = _format_blueprint(payload, theme_key, theme_desc)
    prompts = _build_model_prompts(payload, theme_desc)

    return {
        "theme": theme_key,
        "model_name": model_name,
        "payload": payload,
        "blueprint": blueprint_text,
        "prompts": prompts,
        "model_targets": MODEL_TARGETS,
        "checklist_questions": payload.get("checklist_questions", []),
        "notes": payload.get("notes", []),
    }
