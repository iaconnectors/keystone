"""Operators applied during the reasoning phase of the Synthetica pipeline."""

from typing import Any, Dict, Optional

from synthetica.core.knowledge_broker import KnowledgeBroker
from synthetica.core.models import (
    ACOArchetypalDynamics,
    ACOCompositionalFlow,
    AbstractCreativeObject,
    CulturalCannibalizeDirective,
    IntermediateTechnicalIntent,
)


class OperatorsEngine:
    """Gateway for cognitive and conceptual operators."""

    def __init__(self, broker: KnowledgeBroker):
        self.broker = broker

    def apply(
        self,
        operator_name: str,
        aco: AbstractCreativeObject,
        iti: IntermediateTechnicalIntent,
        params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Dispatch requested operator if it exists."""
        params = params or {}
        if hasattr(self, operator_name):
            print(f"[Operators] Running operator {operator_name}.")
            success = getattr(self, operator_name)(aco, iti, **params)
            if success:
                aco.applied_operators.append(operator_name)
        else:
            iti.reasoning_chain.append(
                f"Operator '{operator_name}' not found. Skipped."
            )

    # --- Cognitive operators ---

    def Operator_ImposeSymmetry(
        self,
        aco: AbstractCreativeObject,
        iti: IntermediateTechnicalIntent,
        **_: Any,
    ) -> bool:
        """Ensure the compositional flow includes a symmetry directive."""
        if not aco.intent.compositional_flow:
            aco.intent.compositional_flow = ACOCompositionalFlow()

        aco.intent.compositional_flow.path = "symmetrical_balance"
        iti.reasoning_chain.append("Cognitive: symmetry imposed on composition.")
        return True

    # --- Conceptual operators (Pillars 2, 3, 4) ---

    def Operator_DefineHybridism(
        self,
        aco: AbstractCreativeObject,
        iti: IntermediateTechnicalIntent,
        subject_id: str,
        ontology_ref: str,
        variant: Optional[str] = None,
        **_: Any,
    ) -> bool:
        """Attach hybrid ontology data to a subject."""
        subject_found = False
        for subject in aco.elements.subjects:
            if subject.id != subject_id:
                continue

            subject.hybrid_ontology_ref = ontology_ref
            subject.hybrid_variant = variant
            variant_label = variant if variant else "default"
            iti.reasoning_chain.append(
                "Conceptual (Hybridism): subject "
                f"{subject_id} mapped to {ontology_ref.split('.')[-1]} "
                f"(variant: {variant_label})."
            )
            subject_found = True
            break

        if not subject_found:
            iti.reasoning_chain.append(
                f"Conceptual (Hybridism) error: subject '{subject_id}' not available."
            )
            return False
        return True

    def Operator_CulturalCannibalize(
        self,
        aco: AbstractCreativeObject,
        iti: IntermediateTechnicalIntent,
        devouring_culture: str,
        devoured_element: str,
        synthesis_mode: str = "Aesthetic",
        **_: Any,
    ) -> bool:
        """Capture the cultural cannibalism directive for phase 2."""
        if not self.broker.get_entry(devouring_culture):
            iti.reasoning_chain.append(
                "Conceptual (Anthropophagy) error: "
                f"culture '{devouring_culture}' not found."
            )
            return False

        if not self.broker.get_entry(devoured_element):
            iti.reasoning_chain.append(
                "Conceptual (Anthropophagy) error: "
                f"element '{devoured_element}' not found."
            )
            return False

        directive = CulturalCannibalizeDirective(
            devouring_culture=devouring_culture,
            devoured_element=devoured_element,
            synthesis_mode=synthesis_mode,
        )
        iti.abstract_directives.antropofagia_directive = directive
        iti.reasoning_chain.append(
            "Conceptual (Anthropophagy): "
            f"{devouring_culture.split('.')[-1]} devours "
            f"{devoured_element.split('.')[-1]}."
        )
        return True

    def Operator_SetArchetypalDynamics(
        self,
        aco: AbstractCreativeObject,
        iti: IntermediateTechnicalIntent,
        shadow_state: str,
        manifestation: Optional[str] = None,
        trickster: Optional[str] = None,
        **_: Any,
    ) -> bool:
        """Set archetypal dynamics on the ACO and surface it to the ITI."""
        valid_states_path = (
            "2.0_Semiotics_and_Psychology_Database."
            "2.8_Archetypal_Dynamics_Framework (Jungian)."
            "Parameters.Shadow_Integration_State.Values"
        )
        valid_states = self.broker.get_entry(valid_states_path, default=[])

        if shadow_state not in valid_states:
            iti.reasoning_chain.append(
                "Conceptual (Archetypal Dynamics) error: "
                f"invalid state '{shadow_state}'. Allowed: {valid_states}."
            )
            return False

        dynamics = ACOArchetypalDynamics(
            shadow_integration_state=shadow_state,
            shadow_manifestation=manifestation,
            trickster_function=trickster,
        )
        aco.intent.archetypal_dynamics = dynamics
        iti.abstract_directives.psychological_state = shadow_state
        iti.reasoning_chain.append(
            f"Conceptual (Archetypal Dynamics): state set to {shadow_state}."
        )
        return True
