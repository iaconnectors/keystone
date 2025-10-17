"""
Pydantic models shared across the playground backend.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    brief: str = Field(..., description="Creative briefing provided by the user.")
    theme: str = Field(..., description="SeaDream theme key (e.g., cinematografico).")
    model: str = Field(
        default="models/gemini-2.5-pro",
        description="Gemini model identifier.",
    )
    case_id: Optional[str] = Field(
        default=None,
        description="Optional preset/case identifier when the request is based on a saved example.",
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Optional tags for organizing sessions.",
    )


class PromptSession(BaseModel):
    id: str
    created_at: str
    liked: bool
    brief: str
    theme: str
    model_name: str
    blueprint: str
    prompts: Dict[str, str]
    payload: Dict[str, Any]
    checklist_questions: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    case_id: Optional[str] = None


class GenerateResponse(BaseModel):
    session: PromptSession


class HistoryResponse(BaseModel):
    items: List[PromptSession]


class LikeRequest(BaseModel):
    liked: bool = Field(..., description="Whether the session should be marked as reference.")


class ReferenceResponse(BaseModel):
    items: List[PromptSession]

