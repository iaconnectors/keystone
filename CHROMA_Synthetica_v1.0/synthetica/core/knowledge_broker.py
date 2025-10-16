import json
from typing import Any, Dict, List, Optional
import difflib

class KnowledgeBroker:
    def __init__(self, kb_data: Dict[str, Any]):
        self._kb = kb_data
        self._cache: Dict[str, List[Any]] = {}
        print(f"🧠: KnowledgeBroker inicializado para KB ID: {kb_data.get('KB_ID', 'Desconhecido')}.")

    # ==============================================================================
    # FUNÇÃO 'get_entry' CORRIGIDA
    # ==============================================================================
    
    def get_entry(self, path: str, default: Any = None) -> Any:
        """
        Navega pela KB.
        Esta versão corrigida trata chaves que contêm pontos
        (e.g., "11.0_Narrative_Structure_and_Storytelling").
        """
        try:
            parts = path.split('.')
            current_level = self._kb
            
            i = 0
            while i < len(parts):
                if not isinstance(current_level, dict):
                    # Não é um dicionário, não podemos navegar mais
                    return default

                # 1. Tenta encontrar a chave simples primeiro (e.g., "Solarpunk")
                current_key = parts[i]
                if current_key in current_level:
                    current_level = current_level[current_key]
                    i += 1
                    continue

                # 2. Se a chave simples falhar, tenta construir uma chave composta
                # (e.g., "11.0_Narrative_Structure_and_Storytelling")
                compound_key = current_key
                found_compound = False
                
                # Itera de j=i+1 até o fim das partes
                for j in range(i + 1, len(parts)):
                    compound_key += "." + parts[j]
                    if compound_key in current_level:
                        # Encontrou uma chave composta válida!
                        current_level = current_level[compound_key]
                        i = j + 1  # Pula o índice para depois da chave composta
                        found_compound = True
                        break
                
                if found_compound:
                    continue

                # 3. Se nem a chave simples nem a composta funcionaram
                return default
                
            return current_level
        except Exception:
            # Captura qualquer outro erro (e.g., TypeError) e retorna o padrão
            return default

    # ==============================================================================
    # O RESTANTE DO ARQUIVO (Sem alterações)
    # ==============================================================================

    def get_flat_list(self, path: str) -> List[Any]:
        if path in self._cache:
            return self._cache[path]
        data = self.get_entry(path)
        result = self._flatten(data) if data is not None else []
        self._cache[path] = result
        return result

    def validate_entry(self, path: str, entry: Any) -> bool:
        flat_list = self.get_flat_list(path)
        # (v1.1) Validação agora usa get_entry corrigido
        if not flat_list and entry:
             # Se a lista está vazia porque get_entry falhou, retorna False
             # (A menos que a entrada esperada também seja vazia/None)
             return False
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