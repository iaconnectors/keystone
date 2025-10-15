# nexus/core/knowledge_broker.py

import json
from typing import Any, Dict, List, Optional
import difflib

class KnowledgeBroker:
    """
    Fornece acesso à Base de Conhecimento (KB). Otimizado com Caching e Busca Fuzzy.
    """
    def __init__(self, kb_data: Dict[str, Any]):
        self._kb = kb_data
        self._cache: Dict[str, List[Any]] = {}
        print("🧠: KnowledgeBroker inicializado (Caching + Fuzzy Search ativos).")

    def get_entry(self, path: str, default: Any = None) -> Any:
        keys = path.split('.')
        value = self._kb
        try:
            for key in keys:
                if isinstance(value, dict):
                   value = value.get(key)
                else:
                    return default
                if value is None:
                    return default
            return value
        except (TypeError):
            return default

    def get_flat_list(self, path: str) -> List[Any]:
        if path in self._cache:
            return self._cache[path]

        data = self.get_entry(path)
        result = self._flatten(data) if data is not None else []
        
        self._cache[path] = result
        return result

    def validate_entry(self, path: str, entry: Any) -> bool:
        flat_list = self.get_flat_list(path)
        return any(str(item).lower() == str(entry).lower() for item in flat_list)

    def find_closest_match(self, path: str, query: str, cutoff: float = 0.6) -> Optional[str]:
        options = [str(opt) for opt in self.get_flat_list(path)]
        if not options:
            return None
        matches = difflib.get_close_matches(query, options, n=1, cutoff=cutoff)
        return matches[0] if matches else None

    def _flatten(self, data: Any) -> List[Any]:
        items = []
        if isinstance(data, list):
            for item in data:
                items.extend(self._flatten(item))
        elif isinstance(data, dict):
            # Achata os valores (folhas)
            for value in data.values():
                items.extend(self._flatten(value))
        else:
            items.append(data)
        return items