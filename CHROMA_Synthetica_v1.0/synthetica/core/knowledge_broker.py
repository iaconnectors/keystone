# synthetica/core/knowledge_broker.py
import json
from typing import Any, Dict, List, Optional
import difflib

class KnowledgeBroker:
    def __init__(self, kb_data: Dict[str, Any]):
        self._kb = kb_data
        self._cache: Dict[str, List[Any]] = {}
        print(f"🧠: KnowledgeBroker inicializado para KB ID: {kb_data.get('KB_ID', 'Desconhecido')}.")

    # get_entry, get_flat_list, validate_entry, find_closest_match permanecem iguais à v1.0.
    # (Omitidos para brevidade, use a versão anterior se necessário)

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
        """
        (v1.1) Ajustado para lidar com a nova estrutura do Masters Lexicon (Dicionário de Objetos).
        """
        items = []
        if isinstance(data, list):
            for item in data:
                items.extend(self._flatten(item))
        elif isinstance(data, dict):
            # Heurística v1.1: Detecta se é uma estrutura de léxico.
            # Se os valores do dicionário forem objetos complexos (outros dicionários), 
            # assumimos que as chaves são as entidades que queremos extrair (e.g., Nomes de Artistas).
            
            # Verifica se o dicionário não está vazio e se o primeiro valor é um dicionário
            if data and isinstance(next(iter(data.values()), None), dict):
                 # Verifica se a maioria (>80%) dos valores são dicionários
                 is_entity_lexicon = sum(isinstance(v, dict) for v in data.values()) / len(data.values()) > 0.8
            else:
                 is_entity_lexicon = False

            if is_entity_lexicon:
                # Extrai as chaves (nomes) e formata (e.g. Ganesh_Pyne -> Ganesh Pyne)
                formatted_keys = [k.replace('_', ' ') for k in data.keys()]
                items.extend(formatted_keys)
            else:
                # Comportamento padrão: recursão nos valores
                for value in data.values():
                    items.extend(self._flatten(value))
        else:
            # Valor final (folha)
            items.append(data)
        return items