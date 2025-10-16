"""Ferramentas para consulta e validação da KB do Synthetica."""
from typing import Any, Dict, List, Optional, Tuple
import difflib


class KnowledgeBroker:
    def __init__(self, kb_data: Dict[str, Any]):
        self._kb = kb_data
        self._cache: Dict[str, List[Any]] = {}
        print(
            f"🧠: KnowledgeBroker inicializado para KB ID: {kb_data.get('KB_ID', 'Desconhecido')}.")

    def get_entry(self, path: str, default: Any = None) -> Any:
        value: Any = self._kb
        remainder = path
        try:
            while remainder:
                if not isinstance(value, dict):
                    return default

                key, remainder = self._match_key(value, remainder)
                if key is None:
                    return default

                value = value.get(key)
                if value is None:
                    return default
            return value
        except TypeError:
            return default

    def _match_key(self, container: Dict[str, Any], remainder: str) -> Tuple[Optional[str], str]:
        """Resolve o próximo segmento do caminho, lidando com chaves com pontos."""
        if remainder in container:
            return remainder, ""

        for key in sorted(container.keys(), key=len, reverse=True):
            if remainder.startswith(key):
                rest = remainder[len(key):]
                if not rest:
                    return key, ""
                if rest.startswith('.'):
                    return key, rest[1:]
        return None, remainder

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
        """Converte estruturas arbitrárias em listas simples de valores."""
        items: List[Any] = []
        if isinstance(data, list):
            for item in data:
                items.extend(self._flatten(item))
        elif isinstance(data, dict):
            is_entity_lexicon = False
            if data:
                first_value = next(iter(data.values()))
                if isinstance(first_value, dict):
                    dict_ratio = sum(isinstance(v, dict) for v in data.values()) / len(data)
                    is_entity_lexicon = dict_ratio > 0.8

            if is_entity_lexicon:
                items.extend(k.replace('_', ' ') for k in data.keys())
            else:
                for value in data.values():
                    items.extend(self._flatten(value))
        elif data is not None:
            items.append(data)
        return items
