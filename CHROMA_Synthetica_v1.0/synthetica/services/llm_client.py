"""LLM clients used for structured prompt generation."""

from __future__ import annotations

import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional

LLM_PROVIDER_ENV = "SYNTHETICA_LLM_PROVIDER"


class BaseLLMClient(ABC):
    """Interface para clientes de LLM usados pelo Synthetica."""

    @abstractmethod
    def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Retorna uma resposta estruturada em JSON."""


class StubLLMClient(BaseLLMClient):
    """
    Cliente local para desenvolvimento offline.

    Gera payloads determinísticos e ASCII-only a partir do briefing.
    Evita dependências externas ou chaves de API.
    """

    def __init__(self, *, default_theme: str = "cinematic") -> None:
        self._default_theme = default_theme

    def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        # Extrai o briefing (último bloco não vazio).
        briefing_lines = [line.strip() for line in user_prompt.splitlines() if line.strip()]
        briefing_text = briefing_lines[-1] if briefing_lines else "Creative exploration"

        if "translation" in system_prompt.lower():
            return {"translation": briefing_text}

        description = briefing_text[:120]
        return {
            "atmosphere": f"Controlled atmosphere for {self._default_theme} storytelling.",
            "intent": f"Deliver on the briefing: {description}",
            "image_content": {
                "subject": "Primary subject derived from the briefing.",
                "action_pose": "Subject engaged in the key action described.",
                "environment": "Scene environment mirrors the requested context.",
            },
            "composition": {
                "shot_type": "Medium-wide shot for clarity.",
                "camera_angle": "Eye-level perspective for balanced narration.",
                "composition_principles": "Rule of thirds, leading lines.",
            },
            "camera_lens_film": {
                "camera": "shot on ARRI Alexa 35 cinema camera",
                "lens": "using Cooke anamorphic prime lenses",
                "treatment": "captured on Kodak Vision3 500T film stock with subtle grain",
            },
            "lighting_color": {
                "lighting": "Three-point cinematic lighting with motivated key.",
                "color_temperature": "Warm key, cool fill contrast.",
                "palette": "Analogous palette tuned for emotional resonance.",
            },
            "dna_visual": {
                "reference": "in the style of Roger Deakins",
                "mood": "Evocative and immersive.",
                "quality": "High fidelity render with narrative depth.",
            },
            "output_parameters": {
                "framing": "16:9 cinematic frame.",
                "delivery": "High-resolution still.",
                "consistency": "Maintain continuity across variations.",
            },
            "checklist_questions": [],
            "notes": [
                "Stub response generated locally. Adjust fields as needed.",
            ],
        }


def _load_key_from_config() -> Optional[str]:
    config_path = Path(__file__).resolve().parent.parent / "config" / "gemini_api_key.txt"
    if config_path.exists():
        key = config_path.read_text(encoding="utf-8").strip()
        return key or None
    return None


class GeminiClient(BaseLLMClient):
    """Thin wrapper around the Gemini GenerativeModel API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "models/gemini-2.5-pro",
        safety_settings: Optional[Dict[str, Any]] = None,
    ) -> None:
        try:
            import google.generativeai as genai
        except ImportError as exc:  # pragma: no cover - handled at runtime
            raise RuntimeError(
                "The 'google-generativeai' package is required by GeminiClient. "
                "Install it with 'pip install google-generativeai'."
            ) from exc

        key = api_key or os.getenv("GEMINI_API_KEY") or _load_key_from_config()
        if not key:
            raise RuntimeError(
                "GeminiClient requires an API key. Set GEMINI_API_KEY or create "
                "config/gemini_api_key.txt using the key."
            )

        genai.configure(api_key=key)
        self._genai = genai
        self._model_name = model_name
        self._safety_settings = safety_settings or {}

    def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Request JSON output from the model and parse it safely."""
        model = self._genai.GenerativeModel(
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


def create_llm_client(
    *,
    provider: Optional[str] = None,
    **kwargs: Any,
) -> BaseLLMClient:
    """
    Cria um cliente LLM com base na configuração do ambiente.

    - Defina SYNTHETICA_LLM_PROVIDER=stub para desenvolvimento offline.
    - Padrão: Gemini.
    """
    chosen = (provider or os.getenv(LLM_PROVIDER_ENV) or "gemini").lower()
    if chosen == "stub":
        return StubLLMClient(**kwargs)
    if chosen == "gemini":
        return GeminiClient(**kwargs)
    raise ValueError(f"Unknown LLM provider '{chosen}'.")


__all__ = [
    "BaseLLMClient",
    "GeminiClient",
    "StubLLMClient",
    "create_llm_client",
]
