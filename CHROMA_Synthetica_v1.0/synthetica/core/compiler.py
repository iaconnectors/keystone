"""Phase 1 (reasoning) compiler for the CHROMA Synthetica pipeline."""

from typing import Any, Dict, List, Optional

from synthetica.core.knowledge_broker import KnowledgeBroker
from synthetica.core.models import AbstractCreativeObject, IntermediateTechnicalIntent
from synthetica.engines.operators import OperatorsEngine


class NexusCompiler:
    """Transforms an ACO into an Intermediate Technical Intent (ITI)."""

    def __init__(self, broker: KnowledgeBroker):
        self.broker = broker
        self.operators_engine = OperatorsEngine(broker)
        print("[NexusCompiler] Phase 1 (Reasoning) initialised.")

    def compile_to_iti(
        self,
        aco: AbstractCreativeObject,
        operator_pipeline: Optional[List[Dict[str, Any]]] = None,
    ) -> IntermediateTechnicalIntent:
        """Run the operator pipeline and project the ACO into an ITI."""
        print("[NexusCompiler] Phase 1: compiling AbstractCreativeObject.")
        iti = IntermediateTechnicalIntent(source_aco_id=aco.aco_id)

        pipeline = operator_pipeline or []
        if pipeline:
            iti.reasoning_chain.append("Operator pipeline started.")
            for operator_spec in pipeline:
                op_name = operator_spec.get("name")
                op_params = operator_spec.get("params", {})
                if not op_name:
                    continue
                self.operators_engine.apply(op_name, aco, iti, op_params)

        self._translate_elements(aco, iti)
        self._translate_intent(aco, iti)
        self._define_technical_queries(aco, iti)

        print("[NexusCompiler] Phase 1 completed. ITI generated.")
        return iti

    def _translate_intent(
        self, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent
    ) -> None:
        """Translate intent-level information into the ITI."""
        if aco.intent.compositional_flow and aco.intent.compositional_flow.path:
            flow = aco.intent.compositional_flow
            iti.composition = f"Path: {flow.path}"
            if flow.focal_point:
                iti.reasoning_chain.append(
                    f"Compositional focal point defined: {flow.focal_point}."
                )

        if (
            not iti.abstract_directives.psychological_state
            and aco.intent.archetypal_dynamics
        ):
            iti.abstract_directives.psychological_state = (
                aco.intent.archetypal_dynamics.shadow_integration_state
            )

    def _translate_elements(
        self, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent
    ) -> None:
        """Collect element descriptions and hybrid traits into the ITI."""
        descriptions: List[str] = []

        for subject in aco.elements.subjects:
            description = subject.description

            if subject.hybrid_ontology_ref:
                keywords: List[str] = []
                if subject.hybrid_variant:
                    variant_path = (
                        f"{subject.hybrid_ontology_ref}.Variants."
                        f"{subject.hybrid_variant}.Keywords"
                    )
                    keywords = self.broker.get_flat_list(variant_path)

                if not keywords:
                    properties_path = f"{subject.hybrid_ontology_ref}.Properties"
                    keywords = self.broker.get_flat_list(properties_path)

                filtered_keywords = [str(keyword) for keyword in keywords if keyword]
                if filtered_keywords:
                    keyword_block = ", ".join(filtered_keywords)
                    description += f" (Hybrid Traits: {keyword_block})"
                    iti.reasoning_chain.append(
                        "Hybridism translated for "
                        f"{subject.hybrid_ontology_ref.split('.')[-1]}."
                    )

            descriptions.append(description)

        if aco.intent.narrative_moment:
            iti.core_concept = (
                f"{aco.intent.narrative_moment} Featuring: "
                f"{'. '.join(descriptions)}"
            )
        else:
            iti.core_concept = ". ".join(descriptions)

    def _define_technical_queries(
        self, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent
    ) -> None:
        """Add technical directives derived from ACO constraints."""
        constraints = aco.constraints.style_constraints
        if constraints and constraints.historical_process:
            process = constraints.historical_process
            iti.abstract_directives.historical_process = process
            iti.reasoning_chain.append(
                f"Historical process directive added: {process}."
            )
