# core_architecture.py

import json
from typing import Any, Dict, List, Optional, TypedDict, Union
from dataclasses import dataclass, field
import difflib # (v27.0) Biblioteca padrão para busca fuzzy
import time

# ==============================================================================
# KNOWLEDGE ACCESS LAYER (Broker - O "Bibliotecário Inteligente" v27.0)
# ==============================================================================

class KnowledgeBroker:
    """
    Fornece acesso à Base de Conhecimento (KB).
    (v27.0: Otimizado com Caching de alta performance e Busca Fuzzy/Semântica).
    """
    def __init__(self, kb_data: Dict[str, Any]):
        self._kb = kb_data
        # (v27.0) Dicionário de cache para armazenar resultados de operações dispendiosas (Memoization).
        self._cache: Dict[str, List[Any]] = {}
        print("🧠: KnowledgeBroker v27.0 inicializado (Caching + Fuzzy Search ativos).")

    def get_entry(self, path: str, default: Any = None) -> Any:
        """
        Recupera uma entrada da KB usando uma notação de caminho por pontos (Acesso Direto).
        """
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
        """
        Recupera dados de um caminho e achata-os numa única lista.
        (v27.0) Utiliza Caching. Eficiência: O(N) na primeira chamada, O(1) nas subsequentes.
        """
        # Verifica a cache primeiro
        if path in self._cache:
            return self._cache[path]

        # Se não estiver na cache, calcula o resultado
        start_time = time.time()
        data = self.get_entry(path)
        if data is None:
            result = []
        else:
            result = self._flatten(data)
        
        # Armazena na cache antes de retornar
        self._cache[path] = result
        end_time = time.time()
        # Opcional: Debug de performance
        # print(f"DEBUG: Cache miss for '{path}'. Flattened in {end_time - start_time:.6f}s.") 
        return result

    def validate_entry(self, path: str, entry: Any) -> bool:
        """
        Verifica se uma entrada existe exatamente na ontologia.
        (v27.0) Beneficia do Caching e é Case-Insensitive.
        """
        flat_list = self.get_flat_list(path)
        # Comparação case-insensitive para robustez
        return any(str(item).lower() == str(entry).lower() for item in flat_list)

    def find_closest_match(self, path: str, query: str, n: int = 1, cutoff: float = 0.6) -> Optional[str]:
        """
        (v27.0) Busca Fuzzy/Semântica. Encontra a correspondência mais próxima para a consulta.
        """
        options = self.get_flat_list(path)
        # Garante que as opções são strings para comparação com difflib
        string_options = [str(opt) for opt in options]
        
        if not string_options:
            return None

        # Usa difflib para encontrar as melhores correspondências
        matches = difflib.get_close_matches(query, string_options, n=n, cutoff=cutoff)
        
        return matches[0] if matches else None

    def _flatten(self, data: Any) -> List[Any]:
        """Função auxiliar recursiva para achatar estruturas aninhadas."""
        items = []
        if isinstance(data, list):
            for item in data:
                items.extend(self._flatten(item))
        elif isinstance(data, dict):
            # Apenas achata os valores (folhas), não as chaves intermediárias
            for value in data.values():
                items.extend(self._flatten(value))
        else:
            # É um valor final (folha do grafo)
            items.append(data)
        return items

# ==============================================================================
# STATE MANAGEMENT STRUCTURES (PSO & WSO) (Atualizado v27.0)
# ==============================================================================

# --- TypedDicts (Tipagem Rigorosa) ---

class CameraPackage(TypedDict, total=False):
    camera: Optional[str]
    lens: Optional[str]
    format: Optional[str]

class LightingSetup(TypedDict, total=False):
    style: Optional[str]
    key_light: Optional[str]
    modifiers: List[str]
    phenomena: List[str] # (v27.0) Ex: Caustics, SSS, Anisotropy

class StabilizationRig(TypedDict, total=False):
    type: Optional[str]
    model: Optional[str]
    movement: Optional[str]

# --------------------------------------------------------------------

@dataclass
class WorldStateObject:
    """
    Implementação da consistência de mundo (WSO). (Atualizado v27.0)
    """
    world_name: str
    physics: str = "realista"
    technology_level: str = "contemporâneo"
    socio_political_system: str = "indefinido"
    aesthetic_laws: Dict[str, Any] = field(default_factory=lambda: {
        "mood": "neutro",
        "stylization_level": "realista",
        "color_palette": [],
        "lighting_style": "natural",
        "architectural_style": None # (v27.0) Ex: Brutalism, Solarpunk
    })

    def __str__(self) -> str:
        return f"--- WSO: {self.world_name} | Estilo: {self.aesthetic_laws.get('stylization_level')} | Arq: {self.aesthetic_laws.get('architectural_style', 'N/D')} ---"

@dataclass
class ProjectStateObject:
    """
    Armazena o estado conceptual e técnico de um projeto criativo (PSO). (Atualizado v27.0)
    """
    initial_brief: str
    core_concept: str = ""
    emotional_intent: str = ""
    
    # Metadados do Processo
    reasoning_chain: List[str] = field(default_factory=list)
    activated_operators: List[str] = field(default_factory=list)
    master_references: List[str] = field(default_factory=list)
    
    # Especificações Visuais
    visual_style: Optional[str] = None
    composition: Optional[str] = None
    color_palette: Optional[str] = None
    
    # Especificações Técnicas
    camera_package: CameraPackage = field(default_factory=dict)
    # (v27.0) Atualização na inicialização do LightingSetup
    lighting_setup: LightingSetup = field(default_factory=lambda: {"modifiers": [], "phenomena": []})
    stabilization_rig: StabilizationRig = field(default_factory=dict)
    post_production_workflow: List[str] = field(default_factory=list)
    
    # Consistência de Mundo
    world_state: Optional[WorldStateObject] = None

    def __str__(self) -> str:
        # Geração de strings formatadas
        masters = ', '.join(self.master_references) if self.master_references else "Nenhum"
        operators = ', '.join(self.activated_operators) if self.activated_operators else "Nenhum"
        chain = ' -> '.join(self.reasoning_chain) if self.reasoning_chain else "Não iniciada"
        world_status = f"Sim ({self.world_state.world_name})" if self.world_state else "Não"
        phenomena_str = ', '.join(self.lighting_setup.get('phenomena', [])) or 'N/D'

        # Formatação da saída (Semiótica da Apresentação)
        return f"""
+----------------------------------------------------------------+
|                  PROJECT STATE OBJECT (PSO)                    |
+----------------------------------------------------------------+
 Briefing Inicial:  {self.initial_brief[:60]}...
 Conceito Central:  {self.core_concept}
 Intenção Emocional:{self.emotional_intent}
 Estilo Visual:     {self.visual_style}
------------------------------------------------------------------
 Referências (Mestres): {masters}
 Operadores Ativados:   {operators}
 Cadeia de Raciocínio:  {chain}
 Mundo Associado:       {world_status}
------------------------------------------------------------------
|                   ESPECIFICAÇÕES TÉCNICAS                      |
------------------------------------------------------------------
 Câmara:        {self.camera_package.get('camera', 'N/D')}
 Lente:         {self.camera_package.get('lens', 'N/D')}
 Iluminação:    {self.lighting_setup.get('style', 'N/D')}
 Fenômenos Óticos: {phenomena_str}
 Estabilização: {self.stabilization_rig.get('model', 'N/D')} ({self.stabilization_rig.get('movement', 'N/D')})
+----------------------------------------------------------------+
"""

# ==============================================================================
# CORE ORCHESTRATION SYSTEM
# ==============================================================================

class KeystoneCHROMA:
    """
    O Nexus Agnóstico Keystone-CHROMA (v27.0).
    """
    # (v27.0) Atualização do caminho padrão da KB
    def __init__(self, kb_path: str = "Keystone-CHROMA-KB-v27.0.json"):
        print("🚀 Inicializando Keystone-CHROMA (v27.0)...")
        self._kb_data = self._load_kb(kb_path)
        self.broker = KnowledgeBroker(self._kb_data)
       
        # Dependências a serem injetadas
        self.operators = None
        self.mtl = None
       
        kb_version = self.broker.get_entry("KB_Version", "desconhecida")
        print(f"✅ Base de Conhecimento v{kb_version} carregada. Sistema operacional.")

    def _load_kb(self, kb_path: str) -> Dict[str, Any]:
        """Carrega a KB. Lança exceções em caso de erro."""
        try:
            with open(kb_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"❌ ERRO CRÍTICO: KB não encontrada em '{kb_path}'.")
        except json.JSONDecodeError:
            raise ValueError(f"❌ ERRO CRÍTICO: KB '{kb_path}' não é um JSON válido.")

    # --- FASE 1 & 2: DIÁLOGO E CONSTRUÇÃO DO PLANO (Simulação) ---

    def _build_pso_simulation(self, brief: str, choice: str) -> ProjectStateObject:
        """
        Simula a construção do PSO com base na escolha do utilizador.
        """
        pso = ProjectStateObject(brief)
        print("\n🏗️: A construir o Plano de Execução (PSO)...")

        # Lógica simulada (Adaptada para Arquitetura/Design na v27.0)
        if choice == '2':
            pso.core_concept = "Um pavilhão de exposições com arquitetura paramétrica fluida, inspirado em formas orgânicas, integrando design biofílico e fachadas vivas."
            pso.emotional_intent = "Inovação, harmonia com a natureza, otimismo futurista"
            pso.reasoning_chain.append("Seleção de Caminho: Arquitetura Especulativa")
            
            # (v27.0) Adicionando referências dos novos domínios
            pso.master_references.extend(["Zaha Hadid", "James Turrell"])

            pso.lighting_setup["style"] = "Iluminação Arquitetônica Integrada, Foco em Luz Natural"
            pso.visual_style = "Parametric Architecture, Biophilic Design, Solarpunk"
        else:
            pso.core_concept = brief
            pso.reasoning_chain.append("Seleção de Caminho: Genérico")
       
        return pso

    # --- FASE 3: ORQUESTRAÇÃO ---

    def orchestrate(self, pso: ProjectStateObject, target_model: str) -> str:
        """
        FASE 3: ORQUESTRAÇÃO E GERAÇÃO. Invoca a MTL.
        """
        print(f"\n🔄: Plano cognitivo finalizado. A iniciar a Camada de Tradução de Modelo (MTL) para: {target_model}.")

        if not self.mtl:
            raise RuntimeError("MTL (Model Translation Layer) não foi inicializada.")
           
        final_prompt = self.mtl.translate(pso, target_model)

        # Geração do Relatório Cognitivo
        self._generate_cognitive_report(pso, target_model, final_prompt)

        return final_prompt

    def _generate_cognitive_report(self, pso: ProjectStateObject, target_model: str, final_prompt: str):
        """Gera um relatório detalhado do processo de orquestração."""
        print("\n" + "="*70)
        print("             RELATÓRIO COGNITIVO (Keystone-CHROMA)             ")
        print("="*70)
        kb_id = self.broker.get_entry('KB_ID', 'N/A')
        kb_version = self.broker.get_entry('KB_Version', 'N/A')
        print(f" KB Status: {kb_id} v{kb_version}")
        print("\n Cadeia de Raciocínio:")
        print(f"  -> ".join(pso.reasoning_chain))
        print("\n Operadores Ativados:")
        print(f"  {', '.join(pso.activated_operators) if pso.activated_operators else 'Nenhum'}")
        print("\n Mestres Referenciados:")
        print(f"  {', '.join(pso.master_references) if pso.master_references else 'Nenhum'}")
        print("="*70)
        print(f" Prompt Otimizado (MTL -> {target_model}):\n")
        print(f"{final_prompt}")
        print("="*70)