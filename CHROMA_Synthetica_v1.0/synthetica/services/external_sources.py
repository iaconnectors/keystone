"""Lightweight connectors to open cultural data sources (no API key required)."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, Optional
import os
import requests

LOGGER = logging.getLogger(__name__)


@dataclass
class ExternalResult:
    source: str
    title: str
    extract: str
    url: str


DEFAULT_TIMEOUT = float(os.getenv("SYNTHETICA_HTTP_TIMEOUT", "5"))


class WikipediaConnector:
    """Fetches summaries from Wikipedia REST API."""

    API_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/{title}"

    def __init__(self, *, timeout: float = DEFAULT_TIMEOUT) -> None:
        self._timeout = timeout

    def fetch(self, topic: str) -> Optional[ExternalResult]:
        slug = topic.replace(" ", "_")
        try:
            resp = requests.get(self.API_URL.format(title=slug), timeout=self._timeout)
            if resp.status_code != 200:
                return None
            data = resp.json()
            if data.get("extract"):
                return ExternalResult(
                    source="wikipedia",
                    title=data.get("title", topic),
                    extract=data["extract"],
                    url=data.get("content_urls", {}).get("desktop", {}).get("page", ""),
                )
        except Exception as exc:  # pragma: no cover - best effort fetch
            LOGGER.debug("Wikipedia fetch failed for %s: %s", topic, exc)
        return None


class WikidataConnector:
    """Query Wikidata for entity descriptions."""

    SEARCH_URL = "https://www.wikidata.org/w/api.php"
    ENTITY_URL = "https://www.wikidata.org/wiki/Special:EntityData/{entity}.json"

    def __init__(self, *, timeout: float = DEFAULT_TIMEOUT) -> None:
        self._timeout = timeout

    def fetch(self, topic: str) -> Optional[ExternalResult]:
        try:
            search_resp = requests.get(
                self.SEARCH_URL,
                params={
                    "action": "wbsearchentities",
                    "format": "json",
                    "language": "en",
                    "limit": 1,
                    "search": topic,
                },
                timeout=self._timeout,
            )
            search_resp.raise_for_status()
            results = search_resp.json().get("search", [])
            if not results:
                return None
            entity_id = results[0]["id"]
            entity_resp = requests.get(
                self.ENTITY_URL.format(entity=entity_id), timeout=self._timeout
            )
            entity_resp.raise_for_status()
            entity_data = entity_resp.json()["entities"][entity_id]
            labels = entity_data.get("labels", {})
            descriptions = entity_data.get("descriptions", {})
            title = labels.get("en", {}).get("value") or topic
            extract = descriptions.get("en", {}).get("value", "")
            return ExternalResult(
                source="wikidata",
                title=title,
                extract=extract,
                url=f"https://www.wikidata.org/wiki/{entity_id}",
            )
        except Exception as exc:  # pragma: no cover - best effort fetch
            LOGGER.debug("Wikidata fetch failed for %s: %s", topic, exc)
        return None


class ExternalKnowledgeHub:
    """Aggregates multiple connectors to suggest content for knowledge gaps."""

    def __init__(self, *, timeout: float = DEFAULT_TIMEOUT, use_cache: bool = True) -> None:
        self.connectors = [
            WikipediaConnector(timeout=timeout),
            WikidataConnector(timeout=timeout),
        ]
        self._cache_enabled = use_cache
        self._cache: Dict[str, Dict[str, ExternalResult]] = {}

    def gather(self, topic: str) -> Dict[str, ExternalResult]:
        normalized_topic = topic.strip().lower()
        if self._cache_enabled and normalized_topic in self._cache:
            return self._cache[normalized_topic]

        results: Dict[str, ExternalResult] = {}
        for connector in self.connectors:
            result = connector.fetch(topic)
            if result:
                results[result.source] = result
        if self._cache_enabled:
            self._cache[normalized_topic] = results
        return results
