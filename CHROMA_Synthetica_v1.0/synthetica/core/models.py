# synthetica/core/models.py

from typing import Any, Dict, List, Optional, TypedDict
from dataclasses import dataclass, field
import uuid

# ==============================================================================
# ABSTRACT CREATIVE OBJECT (ACO) - (Portado do Nexus 1.0, simplificado)
# ==============================================================================

@dataclass
class ACOCompositionalFlow:
    path: Optional[str] = None
    focal_point: Optional[str] = None

@dataclass
class ACOIntent:
    narrative_moment: Optional[str] = None
    compositional_flow: Optional[ACOCompositionalFlow] = None

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
    constraints: ACOConstraints = field(default_factory=ACOConstraints)
    applied_cognitive_operators: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        operators = ", ".join(self.applied_cognitive_operators) or "Nenhum"
        return f"ACO ID: {self.aco_id[:8]}... | Ops: {operators}"

# ==============================================================================
# INTERMEDIATE TECHNICAL INTENT (ITI) - Synthetica v1.0 (NOVO)
# ==============================================================================

@dataclass
class AbstractDirectives:
    """Diretivas abstratas (queries) geradas na Fase 1 para serem resolvidas na Fase 2 (WP 1.1)."""
    master_references_query: List[str] = field(default_factory=list)
    camera_query: Optional[str] = None
    lens_query: Optional[str] = None
    historical_process: Optional[str] = None 

@dataclass
class IntermediateTechnicalIntent:
    """Representa o plano de direção abstrato (Output Fase 1, Input Fase 2)."""
    source_aco_id: str
    reasoning_chain: List[str] = field(default_factory=list)
    core_concept: str = ""
    composition: Optional[str] = None
    abstract_directives: AbstractDirectives = field(default_factory=AbstractDirectives)

    def __str__(self) -> str:
        return f"ITI (Source ACO: {self.source_aco_id[:8]}...) | Directives: {self.abstract_directives}"

# ==============================================================================
# PROJECT STATE OBJECT (PSO) - Plano Técnico Final
# ==============================================================================

class CameraPackage(TypedDict, total=False):
    camera: Optional[str]
    lens: Optional[str]

@dataclass
class ProjectStateObject:
    """O plano de execução técnico final, após o enriquecimento."""
    source_aco_id: Optional[str] = None
    core_concept: str = ""
    reasoning_chain: List[str] = field(default_factory=list) # Combina Fases 1 e 2
    master_references: List[str] = field(default_factory=list)
    composition: Optional[str] = None
    camera_package: CameraPackage = field(default_factory=dict)
    process_artifacts: List[str] = field(default_factory=list)
    
    # (WP 1.3) Resolução de Conflitos Ontológicos
    ontological_conflicts: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        chain = '\n  -> '.join(self.reasoning_chain) if self.reasoning_chain else "Vazio"
        masters = ', '.join(self.master_references) if self.master_references else 'Nenhum'
        conflicts = '\n  ! '.join(self.ontological_conflicts) if self.ontological_conflicts else "Nenhum"

        return f"""
+----------------------------------------------------------------+
|             PROJECT STATE OBJECT (PSO) - Plano Final           |
+----------------------------------------------------------------+
 Mestres:  {masters}
 Câmara:   {self.camera_package.get('camera', 'N/D')} | Lente: {self.camera_package.get('lens', 'N/D')}
 Artefatos: {', '.join(self.process_artifacts) if self.process_artifacts else 'Nenhum'}
 Conflitos Ontológicos: {conflicts}
------------------------------------------------------------------
|                   CADEIA DE RACIOCÍNIO (Híbrida)               |
------------------------------------------------------------------
  -> {chain}
+----------------------------------------------------------------+
"""