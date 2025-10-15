# core_architecture.py

import json
from typing import Any, Dict, List, Optional, TypedDict, Union
from dataclasses import dataclass, field

# ==============================================================================
# KNOWLEDGE ACCESS LAYER (Broker)
# ==============================================================================

class KnowledgeBroker:
    """
    Fornece acesso seguro, robusto e abstraído à Base de Conhecimento (KB).
    (v26.0: Aprimorado com validação centralizada e navegação recursiva).
    """
    def __init__(self, kb_data: Dict[str, Any]):
        self._kb = kb_data

    def get_entry(self, path: str, default: Any = None) -> Any:
        """
        Recupera uma entrada da KB usando uma notação de caminho por pontos.
        """
        keys = path.split('.')
        value = self._kb
        try:
            for key in keys:
                if isinstance(value, dict):
                    value = value[key]
                else:
                    return default
            return value
        except (KeyError, TypeError):
            return default

    def get_flat_list(self, path: str) -> List[Any]:
        """
        Recupera dados de um caminho e achata-os numa única lista.
        """
        data = self.get_entry(path)
        if data is None:
            return []
        return self._flatten(data)

    def validate_entry(self, path: str, entry: Any) -> bool:
        """
        Verifica se uma entrada existe na ontologia no caminho especificado.
        """
        flat_list = self.get_flat_list(path)
        return entry in flat_list

    def _flatten(self, data: Any) -> List[Any]:
        """Função auxiliar recursiva para achatar estruturas aninhadas."""
        items = []
        if isinstance(data, list):
            for item in data:
                items.extend(self._flatten(item))
        elif isinstance(data, dict):
            for value in data.values():
                items.extend(self._flatten(value))
        else:
            # É um valor final
            items.append(data)
        return items

# ==============================================================================
# STATE MANAGEMENT STRUCTURES (PSO & WSO)
# ==============================================================================

# --- TypedDicts (Melhoria Semântica: Tipagem Rigorosa) ---

class CameraPackage(TypedDict, total=False):
    camera: Optional[str]
    lens: Optional[str]
    format: Optional[str]

class LightingSetup(TypedDict, total=False):
    style: Optional[str]
    key_light: Optional[str]
    modifiers: List[str]

class StabilizationRig(TypedDict, total=False):
    type: Optional[str]
    model: Optional[str]
    movement: Optional[str]

# --------------------------------------------------------------------

@dataclass
class WorldStateObject:
    """
    Implementação da consistência de mundo (WSO).
    (Melhoria Semiótica: Convertido para dataclass)
    """
    world_name: str
    physics: str = "realista"
    technology_level: str = "contemporâneo"
    socio_political_system: str = "indefinido"
    aesthetic_laws: Dict[str, Any] = field(default_factory=lambda: {
        "mood": "neutro",
        "stylization_level": "realista",
        "color_palette": [],
        "lighting_style": "natural"
    })

    def __str__(self) -> str:
        return f"--- World State Object (WSO): {self.world_name} | Estilo: {self.aesthetic_laws.get('stylization_level')} ---"

@dataclass
class ProjectStateObject:
    """
    Armazena o estado conceptual e técnico de um projeto criativo (PSO).
    (Melhoria Semiótica: Convertido para dataclass)
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
    
    # Especificações Técnicas (Tipagem Rigorosa)
    camera_package: CameraPackage = field(default_factory=dict)
    lighting_setup: LightingSetup = field(default_factory=lambda: {"modifiers": []})
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

        # Formatação da saída (Semiótica da Apresentação)
        return f"""
+----------------------------------------------------------------+
|                  PROJECT STATE OBJECT (PSO)                    |
+----------------------------------------------------------------+
 Briefing Inicial:  {self.initial_brief[:60]}...
 Conceito Central:  {self.core_concept}
 Intenção Emocional:{self.emotional_intent}
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
 Estabilização: {self.stabilization_rig.get('model', 'N/D')} ({self.stabilization_rig.get('movement', 'N/D')})
+----------------------------------------------------------------+
"""

# ==============================================================================
# CORE ORCHESTRATION SYSTEM
# ==============================================================================

class KeystoneCHROMA:
    """
    O Nexus Agnóstico Keystone-CHROMA (v26.0).
    """
    def __init__(self, kb_path: str = "Keystone-CHROMA-KB-v26.0.json"):
        print("Inicializando Keystone-CHROMA (v26.0)...")
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
            # Melhoria Semântica: Lançar exceção em vez de exit()
            raise FileNotFoundError(f"❌ ERRO CRÍTICO: KB não encontrada em '{kb_path}'.")
        except json.JSONDecodeError:
            raise ValueError(f"❌ ERRO CRÍTICO: KB '{kb_path}' não é um JSON válido.")

    # --- FASE 1 & 2: DIÁLOGO E CONSTRUÇÃO DO PLANO (Simulação) ---

    def _build_pso_simulation(self, brief: str, choice: str) -> ProjectStateObject:
        """
        Simula a construção do PSO com base na escolha do utilizador durante o diálogo socrático.
        """
        pso = ProjectStateObject(brief)
        print("\n🏗️: A construir o Plano de Execução (PSO)...")

        # Lógica simulada
        if choice == '2':
            pso.core_concept = "Um retrato de um homem em chiaroscuro, metade do seu rosto iluminado por um ecrã de computador, refletindo código nos seus olhos."
            pso.emotional_intent = "Isolamento intenso, melancolia, contemplação focada"
            pso.reasoning_chain.append("Seleção de Caminho: Retrato Clássico")
            pso.master_references.extend(["Gordon Willis", "Caravaggio"])
            pso.lighting_setup["style"] = "Chiaroscuro"
            pso.visual_style = "Dramatic Portraiture, Cinematic Realism"
        else:
            # Lógica simplificada para outras escolhas
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