"""Módulo responsável pela Fase 1 (Raciocínio Abstrato) do Synthetica."""
from typing import Any, Dict, List, Optional

from synthetica.core.knowledge_broker import KnowledgeBroker
from synthetica.core.models import AbstractCreativeObject, IntermediateTechnicalIntent
from synthetica.engines.operators import OperatorsEngine


class NexusCompiler:
    """Executa a fase de raciocínio do pipeline."""

    def __init__(self, broker: KnowledgeBroker):
        self.broker = broker
        self.operators_engine = OperatorsEngine(broker)
        print("🎨: NexusCompiler (Fase 1: Raciocínio) inicializado.")

    def compile_to_iti(
        self,
        aco: AbstractCreativeObject,
        operator_pipeline: Optional[List[Dict[str, Any]]] = None,
    ) -> IntermediateTechnicalIntent:
        """Processa o ACO e gera o ITI intermediário."""
        print("🧠: Fase 1 (Raciocínio Abstrato): Iniciando compilação do ACO...")
        iti = IntermediateTechnicalIntent(source_aco_id=aco.aco_id)

        operator_pipeline = operator_pipeline or []
        if operator_pipeline:
            iti.reasoning_chain.append("Início do Pipeline de Operadores")
            for op_spec in operator_pipeline:
                op_name = op_spec.get("name")
                op_params = op_spec.get("params", {})
                if op_name:
                    self.operators_engine.apply(op_name, aco, iti, op_params)

        self._translate_intent(aco, iti)
        self._translate_elements(aco, iti)
        self._define_technical_queries(aco, iti)

        print("✅: Fase 1 concluída. ITI gerado.")
        return iti

    def _translate_intent(self, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent) -> None:
        if aco.intent.compositional_flow:
            flow = aco.intent.compositional_flow
            iti.composition = f"Path: {flow.path}"

        if not iti.abstract_directives.psychological_state and aco.intent.archetypal_dynamics:
            iti.abstract_directives.psychological_state = (
                aco.intent.archetypal_dynamics.shadow_integration_state
            )

    def _translate_elements(self, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent) -> None:
        """Gera descrições dos elementos do ACO, incluindo hibridismo."""
        element_descriptions: List[str] = []
        for subject in aco.elements.subjects:
            desc = subject.description

            if subject.hybrid_ontology_ref:
                keywords: List[str] = []
                if subject.hybrid_variant:
                    variant_path = (
                        f"{subject.hybrid_ontology_ref}.Variants.{subject.hybrid_variant}.Keywords"
                    )
                    keywords = self.broker.get_flat_list(variant_path)

                if not keywords:
                    prop_path = f"{subject.hybrid_ontology_ref}.Properties"
                    keywords = self.broker.get_flat_list(prop_path)

                if keywords:
                    filtered_keywords = ', '.join(str(k) for k in keywords if k)
                    desc += f" (Hybrid Traits: {filtered_keywords})"
                    iti.reasoning_chain.append(
                        f"Hibridismo: Traduzido {subject.hybrid_ontology_ref.split('.')[-1]} para keywords."
                    )

            element_descriptions.append(desc)

        if aco.intent.narrative_moment:
            iti.core_concept = (
                f"{aco.intent.narrative_moment} Featuring: {'. '.join(element_descriptions)}"
            )
        else:
            iti.core_concept = '. '.join(element_descriptions)

    def _define_technical_queries(self, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent) -> None:
        if aco.constraints.style_constraints and aco.constraints.style_constraints.historical_process:
            process = aco.constraints.style_constraints.historical_process
            iti.abstract_directives.historical_process = process
            iti.reasoning_chain.append(f"Diretiva de Processo Histórico adicionada: {process}")
