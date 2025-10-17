"""Gemini client wrapper for structured prompt generation."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import google.generativeai as genai
except ImportError as exc:  # pragma: no cover - handled at runtime
    raise RuntimeError(
        "A biblioteca 'google-generativeai' é necessária para usar o GeminiClient. "
        "Instale com 'pip install google-generativeai'."
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
                "GeminiClient requer uma chave de API. Defina GEMINI_API_KEY ou crie "
                "config/gemini_api_key.txt com a chave."
            )

        genai.configure(api_key=key)
        self._model_name = model_name
        self._safety_settings = safety_settings or {}

    def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Solicita ao modelo um JSON e faz parsing seguro."""
        model = genai.GenerativeModel(
            self._model_name,
            system_instruction=system_prompt,
        )
        response = model.generate_content(
            user_prompt,
            safety_settings=self._safety_settings,
        )

        if not response.candidates:
            raise RuntimeError("Resposta vazia do Gemini.")

        text = response.candidates[0].content.parts[0].text.strip()

        if text.startswith("`"):
            text = text.strip("")
            if text.lower().startswith("json"):
                text = text[4:].lstrip()

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Não foi possível decodificar JSON do Gemini. Conteúdo: {text}"
            ) from exc
