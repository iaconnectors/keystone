import difflib
from typing import Any, Dict, List, Optional


class KnowledgeBroker:
    def __init__(self, kb_data: Dict[str, Any]):
        self._kb = kb_data
        self._cache: Dict[str, List[Any]] = {}
        print(
            "[KnowledgeBroker] Initialised for KB ID: "
            f"{kb_data.get('KB_ID', 'Unknown')}."
        )

    # ==========================================================================
    # Entry navigation helpers
    # ==========================================================================

    def get_entry(self, path: str, default: Any = None) -> Any:
        """
        Navigate the knowledge base using dotted paths.
        Handles keys that already contain dots (e.g. "11.0_Narrative...").
        """
        try:
            parts = path.split(".")
            current_level = self._kb

            i = 0
            while i < len(parts):
                if not isinstance(current_level, dict):
                    return default

                current_key = parts[i]
                if current_key in current_level:
                    current_level = current_level[current_key]
                    i += 1
                    continue

                compound_key = current_key
                found_compound = False
                for j in range(i + 1, len(parts)):
                    compound_key += "." + parts[j]
                    if compound_key in current_level:
                        current_level = current_level[compound_key]
                        i = j + 1
                        found_compound = True
                        break

                if found_compound:
                    continue

                return default

            return current_level
        except Exception:
            return default

    # ==========================================================================
    # Cache-aware utilities
    # ==========================================================================

    def get_flat_list(self, path: str) -> List[Any]:
        if path in self._cache:
            return self._cache[path]
        data = self.get_entry(path)
        result = self._flatten(data) if data is not None else []
        self._cache[path] = result
        return result

    def validate_entry(self, path: str, entry: Any) -> bool:
        flat_list = self.get_flat_list(path)
        if not flat_list and entry:
            return False
        return any(str(item).lower() == str(entry).lower() for item in flat_list)

    def find_closest_match(self, path: str, query: str, cutoff: float = 0.6) -> Optional[str]:
        options = [str(opt) for opt in self.get_flat_list(path)]
        if not options:
            return None
        matches = difflib.get_close_matches(query, options, n=1, cutoff=cutoff)
        return matches[0] if matches else None

    def inject_entry(self, path: str, entry: Any) -> None:
        """Inject or override an entry inside the KB using dotted paths."""
        parts = path.split(".")
        current_level: Dict[str, Any] = self._kb
        i = 0

        while i < len(parts):
            if not isinstance(current_level, dict):
                break

            current_key = parts[i]
            if current_key in current_level:
                if i == len(parts) - 1:
                    current_level[current_key] = entry
                    self._cache.clear()
                    return
                current_level = current_level[current_key]
                i += 1
                continue

            compound_key = current_key
            found_compound = False
            for j in range(i + 1, len(parts)):
                compound_key += "." + parts[j]
                if compound_key in current_level:
                    if j == len(parts) - 1:
                        current_level[compound_key] = entry
                        self._cache.clear()
                        return
                    current_level = current_level[compound_key]
                    i = j + 1
                    found_compound = True
                    break

            if found_compound:
                continue

            remaining_key = ".".join(parts[i:])
            current_level[remaining_key] = entry
            self._cache.clear()
            return

        raise ValueError(f"Cannot inject entry at '{path}': parent is not a mapping.")

    # ==========================================================================
    # Internal helpers
    # ==========================================================================

    def _flatten(self, data: Any) -> List[Any]:
        """
        Flatten nested KB structures into a simple list.
        Handles lexicon dictionaries whose values are rich objects.
        """
        items: List[Any] = []
        if isinstance(data, list):
            for item in data:
                items.extend(self._flatten(item))
        elif isinstance(data, dict):
            if data and isinstance(next(iter(data.values()), None), dict):
                dict_count = sum(isinstance(v, dict) for v in data.values())
                is_entity_lexicon = dict_count / len(data.values()) > 0.8
            else:
                is_entity_lexicon = False

            if is_entity_lexicon:
                formatted_keys = [k.replace("_", " ") for k in data.keys()]
                items.extend(formatted_keys)
            else:
                for value in data.values():
                    items.extend(self._flatten(value))
        else:
            items.append(data)
        return items
