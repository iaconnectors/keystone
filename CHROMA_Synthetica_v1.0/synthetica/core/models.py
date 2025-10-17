# synthetica/core/models.py

from typing import Any, Dict, List, Optional, TypedDict, Literal
from dataclasses import dataclass, field
import uuid

# ==============================================================================
# TIPOS (v1.1)
# ==============================================================================

# (v1.1) Tipos Literais para os novos frameworks (KB 2.8 e 4.4)
ShadowIntegrationState = Literal["Repressed", "Projected", "Assimilating", "Integrated"]
SynthesisMode = Literal["Aesthetic", "Narrative", "Symbolic"]

# ==============================================================================
# ABSTRACT CREATIVE OBJECT (ACO)
# ==============================================================================

@dataclass
class ACOCompositionalFlow:
    path: Optional[str] = None
    focal_point: Optional[str] = None

# (v1.1) Novo: Parametros Psicologicos (Pilar 4)
@dataclass
class ACOArchetypalDynamics:
    persona_definition: Optional[str] = None
    shadow_integration_state: Optional[ShadowIntegrationState] = None
    shadow_manifestation: Optional[str] = None # KB Path (e.g. 2.7...Minotaur)
    trickster_function: Optional[Literal["Internal_Catalyst", "External_Agent"]] = None

@dataclass
class ACOIntent:
    narrative_moment: Optional[str] = None
    compositional_flow: Optional[ACOCompositionalFlow] = None
    # (v1.1) Adicao do motor psicologico
    archetypal_dynamics: Optional[ACOArchetypalDynamics] = None

# (v1.1) Adicao de ACOElements e ACOSubject para suportar Hibridismo (Pilar 2)
@dataclass
class ACOSubject:
    id: str
    description: str
    hybrid_ontology_ref: Optional[str] = None # KB Path (e.g. 2.7...Kinnari)
    hybrid_variant: Optional[str] = None      # e.g. Pal_Subversive

@dataclass
class ACOElements:
    subjects: List[ACOSubject] = field(default_factory=list)

@dataclass
class ACOStyleConstraints:
     historical_process: Optional[str] = None

@dataclass
class ACOConstraints:
    style_constraints: Optional[ACOStyleConstraints] = None

@dataclass
class AbstractCreativeObject:
    aco_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    intent: ACOIntent = field(default_factory=ACOIntent)
    elements: ACOElements = field(default_factory=ACOElements) # (v1.1) Adicionado
    constraints: ACOConstraints = field(default_factory=ACOConstraints)
    # (v1.1) Renomeado para refletir operadores conceituais e cognitivos
    applied_operators: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        operators = ", ".join(self.applied_operators) or "Nenhum"
        dynamics = self.intent.archetypal_dynamics
        psyche = f"Psyche: {dynamics.shadow_integration_state}" if dynamics else "Psyche: N/D"
        return f"ACO ID: {self.aco_id[:8]}... | Ops: {operators} | {psyche}"

# ==============================================================================
# INTERMEDIATE TECHNICAL INTENT (ITI)
# ==============================================================================

# (v1.1) Novo: Diretivas para Antropofagia (Pilar 3)
@dataclass
class CulturalCannibalizeDirective:
    devouring_culture: str # KB Path
    devoured_element: str # KB Path
    synthesis_mode: SynthesisMode

@dataclass
class AbstractDirectives:
    """Diretivas abstratas (queries) geradas na Fase 1."""
    master_references_query: List[str] = field(default_factory=list)
    camera_query: Optional[str] = None
    historical_process: Optional[str] = None
    # (v1.1) Adicao de diretivas de alto nivel
    antropofagia_directive: Optional[CulturalCannibalizeDirective] = None
    # (v1.1) Adicao de estado psicologico para a Translation Matrix
    psychological_state: Optional[ShadowIntegrationState] = None

@dataclass
class IntermediateTechnicalIntent:
    source_aco_id: str
    reasoning_chain: List[str] = field(default_factory=list)
    core_concept: str = ""
    composition: Optional[str] = None
    abstract_directives: AbstractDirectives = field(default_factory=AbstractDirectives)

    def __str__(self) -> str:
        return f"ITI (Source ACO: {self.source_aco_id[:8]}...) | Directives: {self.abstract_directives}"

# ==============================================================================
# PROJECT STATE OBJECT (PSO)
# ==============================================================================

class CameraPackage(TypedDict, total=False):
    camera: Optional[str]
    lens: Optional[str]

@dataclass
class ProjectStateObject:
    source_aco_id: Optional[str] = None
    core_concept: str = ""
    reasoning_chain: List[str] = field(default_factory=list)
    master_references: List[str] = field(default_factory=list)
    # (v1.1) Adicao de estilo visual derivado da Translation Matrix ou Antropofagia
    visual_style_keywords: List[str] = field(default_factory=list)
    composition: Optional[str] = None
    camera_package: CameraPackage = field(default_factory=dict)
    process_artifacts: List[str] = field(default_factory=list)
    ontological_conflicts: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        chain = '\n  -> '.join(self.reasoning_chain) if self.reasoning_chain else "Vazio"
        masters = ', '.join(self.master_references) if self.master_references else 'Nenhum'
        styles = ', '.join(self.visual_style_keywords) if self.visual_style_keywords else 'Nenhum'

        return f"""
+----------------------------------------------------------------+
|             PROJECT STATE OBJECT (PSO) - Plano Final           |
+----------------------------------------------------------------+
 Conceito: {self.core_concept[:150]}...
 Mestres:  {masters}
 Estilo (Keywords): {styles}
------------------------------------------------------------------
|                   CADEIA DE RACIOCINIO (Hibrida)               |
------------------------------------------------------------------
  -> {chain}
+----------------------------------------------------------------+
"""