# nexus/core/models.py

from typing import Any, Dict, List, Optional, TypedDict
from dataclasses import dataclass, field
import uuid

# ==============================================================================
# ABSTRACT CREATIVE OBJECT (ACO) - Pilar I: A Intenção Pura
# Implementação baseada no White Paper (Tabela 1).
# ==============================================================================

@dataclass
class ACOMetadata:
    project_name: Optional[str] = None
    source_brief_id: Optional[str] = None

@dataclass
class ACOEmotion:
    emotion: str
    weight: float # 0.0 to 1.0

@dataclass
class ACOSubjectRelationship:
    subject_a_id: str
    subject_b_id: str
    relationship: str # e.g., confrontation
    dominance: str = "balanced"

@dataclass
class ACOCompositionalFlow:
    path: Optional[str] = None # e.g., spiral_inward
    focal_point: Optional[str] = None
    gaze_direction: str = "leading_lines"

@dataclass
class ACOIntent:
    core_emotions: List[ACOEmotion] = field(default_factory=list)
    subject_relationships: List[ACOSubjectRelationship] = field(default_factory=list)
    compositional_flow: Optional[ACOCompositionalFlow] = None
    narrative_moment: Optional[str] = None

@dataclass
class ACOSubject:
    id: str
    description: str
    attributes: List[str] = field(default_factory=list)

@dataclass
class ACOEnvironment:
    description: str
    atmosphere: str

@dataclass
class ACOElements:
    subjects: List[ACOSubject] = field(default_factory=list)
    environment: Optional[ACOEnvironment] = None

@dataclass
class ACOStyleConstraints:
    brand_palette: List[str] = field(default_factory=list)
    reference_artists: List[str] = field(default_factory=list)
    historical_process: Optional[str] = None # Pilar II.2

@dataclass
class ACOConstraints:
    must_include: List[str] = field(default_factory=list)
    must_not_include: List[str] = field(default_factory=list)
    style_constraints: Optional[ACOStyleConstraints] = None

@dataclass
class ACONested:
    aco: Any # Referência recursiva ao ACO
    region: str

@dataclass
class AbstractCreativeObject:
    """
    Representa a intenção criativa pura. A fonte primária da verdade criativa.
    """
    schema_version: str = "1.0.0"
    aco_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: ACOMetadata = field(default_factory=ACOMetadata)

    intent: ACOIntent = field(default_factory=ACOIntent)
    elements: ACOElements = field(default_factory=ACOElements)
    constraints: ACOConstraints = field(default_factory=ACOConstraints)
    nested_acos: List[ACONested] = field(default_factory=list)
    
    # Rastreamento de operadores cognitivos aplicados (Pilar II.3)
    applied_cognitive_operators: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        emotions = ", ".join([f"{e.emotion} ({e.weight*100:.0f}%)" for e in self.intent.core_emotions])
        flow = self.intent.compositional_flow
        operators = ", ".join(self.applied_cognitive_operators) or "Nenhum"
        return f"""
+----------------------------------------------------------------+
|               ABSTRACT CREATIVE OBJECT (ACO) v{self.schema_version}              |
+----------------------------------------------------------------+
 ID: {self.aco_id}
------------------------------------------------------------------
 Emoções: {emotions or 'N/D'} | Narrativa: {self.intent.narrative_moment or 'N/D'}
 Fluxo:   {flow.path if flow else 'N/D'}
 Operadores Cognitivos: {operators}
+----------------------------------------------------------------+
"""

# ==============================================================================
# PROJECT STATE OBJECT (PSO) - O Plano de Execução Técnico
# ==============================================================================

class CameraPackage(TypedDict, total=False):
    camera: Optional[str]
    lens: Optional[str]

@dataclass
class ProjectStateObject:
    """
    O plano de execução técnico compilado a partir de um ACO.
    """
    source_aco_id: Optional[str] = None

    # Campos derivados do ACO
    core_concept: str = ""
    emotional_intent: str = ""
    
    # Gerados durante a compilação
    reasoning_chain: List[str] = field(default_factory=list)
    master_references: List[str] = field(default_factory=list)
    
    # Especificações Visuais
    visual_style: Optional[str] = None
    composition: Optional[str] = None
    
    # Especificações Técnicas
    camera_package: CameraPackage = field(default_factory=dict)

    # Artefatos de Processo (Pilar II.2)
    process_artifacts: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        chain = '\n  -> '.join(self.reasoning_chain) if self.reasoning_chain else "Vazio"

        return f"""
+----------------------------------------------------------------+
|             PROJECT STATE OBJECT (PSO) - Plano Técnico         |
+----------------------------------------------------------------+
 Fonte ACO ID: {self.source_aco_id}
------------------------------------------------------------------
 Conceito: {self.core_concept[:100]}...
 Estilo:   {self.visual_style} | Composição: {self.composition}
 Artefatos: {', '.join(self.process_artifacts) if self.process_artifacts else 'Nenhum'}
------------------------------------------------------------------
|                   CADEIA DE RACIOCÍNIO (Compilador)            |
------------------------------------------------------------------
  -> {chain}
+----------------------------------------------------------------+
"""