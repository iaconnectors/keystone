"""Detects missing KB paths and fills them with external knowledge."""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from synthetica.core.knowledge_broker import KnowledgeBroker
from synthetica.services.external_sources import ExternalKnowledgeHub

LOGGER = logging.getLogger(__name__)


@dataclass
class GapSuggestion:
    path: str
    topic: str
    sources: Dict[str, Dict[str, str]]


class KnowledgeGapResolver:
    """Attempts to patch missing KB paths using open data sources."""

    def __init__(self, broker: KnowledgeBroker) -> None:
        self.broker = broker
        self.external_hub = ExternalKnowledgeHub()
        self.generated_entries: List[GapSuggestion] = []
        self._auto_log_path = (
            Path(__file__).resolve().parent.parent.parent
            / "kb"
            / "auto_generated_entries.json"
        )

    def ensure_paths(self, items: Iterable[Dict[str, Any]]) -> None:
        """Check each item with 'path' and optional 'hint'."""
        for item in items:
            path = item.get("path")
            if not path:
                continue
            if self.broker.get_entry(path) is not None:
                continue
            topic = item.get("hint") or self._topic_from_path(path)
            suggestion = self._create_suggestion(path, topic)
            if suggestion:
                self._inject(path, suggestion)
                self.generated_entries.append(suggestion)
                self._log_suggestion(suggestion)

    def _topic_from_path(self, path: str) -> str:
        cleaned = path.strip("/").replace("_", " ")
        segments = [seg for seg in cleaned.split("/") if seg]
        return segments[-1] if segments else path

    def _create_suggestion(self, path: str, topic: str) -> Optional[GapSuggestion]:
        sources = self.external_hub.gather(topic)
        if not sources:
            LOGGER.info("No external data found for %s (%s)", path, topic)
            return None
        source_payload = {
            name: {
                "title": result.title,
                "summary": result.extract,
                "url": result.url,
            }
            for name, result in sources.items()
        }
        return GapSuggestion(path=path, topic=topic, sources=source_payload)

    def _inject(self, path: str, suggestion: GapSuggestion) -> None:
        entry = {
            "auto_generated": True,
            "topic": suggestion.topic,
            "sources": suggestion.sources,
        }
        try:
            self.broker.inject_entry(path, entry)
        except ValueError as exc:
            LOGGER.warning("Failed to inject KB entry for %s: %s", path, exc)
            return
        self._persist_suggestion(suggestion)

    def _log_suggestion(self, suggestion: GapSuggestion) -> None:
        LOGGER.info(
            "Auto-filled missing KB path '%s' with data for topic '%s' (sources: %s).",
            suggestion.path,
            suggestion.topic,
            ", ".join(suggestion.sources.keys()),
        )

    def _persist_suggestion(self, suggestion: GapSuggestion) -> None:
        try:
            if self._auto_log_path.exists():
                existing = json.loads(self._auto_log_path.read_text(encoding="utf-8"))
                if not isinstance(existing, list):
                    existing = []
            else:
                existing = []
            existing.append(asdict(suggestion))
            self._auto_log_path.parent.mkdir(parents=True, exist_ok=True)
            self._auto_log_path.write_text(
                json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8"
            )
        except Exception as exc:  # pragma: no cover - best effort persistence
            LOGGER.debug("Could not persist suggestion for %s: %s", suggestion.path, exc)
