"""Gemini client wrapper for structured prompt generation."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import google.generativeai as genai
except ImportError as exc:  # pragma: no cover - handled at runtime
    raise RuntimeError(
        "The 'google-generativeai' package is required by GeminiClient. "
        "Install it with 'pip install google-generativeai'."
    ) from exc


def _load_key_from_config() -> Optional[str]:
    config_path = Path(__file__).resolve().parent.parent / "config" / "gemini_api_key.txt"
    if config_path.exists():
        key = config_path.read_text(encoding="utf-8").strip()
        return key or None
    return None


class GeminiClient:
    """Thin wrapper around the Gemini GenerativeModel API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "models/gemini-2.5-pro",
        safety_settings: Optional[Dict[str, Any]] = None,
    ) -> None:
        key = api_key or os.getenv("GEMINI_API_KEY") or _load_key_from_config()
        if not key:
            raise RuntimeError(
                "GeminiClient requires an API key. Set GEMINI_API_KEY or create "
                "config/gemini_api_key.txt using the key."
            )

        genai.configure(api_key=key)
        self._model_name = model_name
        self._safety_settings = safety_settings or {}

    def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Request JSON output from the model and parse it safely."""
        model = genai.GenerativeModel(
            self._model_name,
            system_instruction=system_prompt,
        )
        response = model.generate_content(
            user_prompt,
            safety_settings=self._safety_settings,
        )

        if not getattr(response, "candidates", None):
            raise RuntimeError("Empty response from Gemini.")

        candidate = response.candidates[0]
        content = getattr(candidate, "content", None)
        parts = getattr(content, "parts", []) if content else []

        text_fragment: Optional[str] = None
        for part in parts:
            value = getattr(part, "text", None)
            if value:
                text_fragment = value
                break

        if not text_fragment:
            raise RuntimeError("Gemini response did not contain text content.")

        text = text_fragment.strip()

        if text.startswith("```"):
            text = text.strip("`")
            if text.lower().startswith("json"):
                text = text[4:].lstrip()
        elif text.startswith("`"):
            text = text.strip("`")
            if text.lower().startswith("json"):
                text = text[4:].lstrip()

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Could not decode JSON returned by Gemini. Content: {text}"
            ) from exc
