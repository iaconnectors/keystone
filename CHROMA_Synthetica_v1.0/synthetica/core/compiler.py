# synthetica/core/compiler.py

from synthetica.core.models import AbstractCreativeObject, IntermediateTechnicalIntent
from synthetica.core.knowledge_broker import KnowledgeBroker
from synthetica.engines.operators import CognitiveOperators
from typing import List

class NexusCompiler:
    """
    Fase 1 da Mente Híbrida: Raciocínio Abstrato.
    Traduz a intenção (ACO) num plano abstrato (ITI).
    """
    def __init__(self, broker: KnowledgeBroker):
        # Usa o Broker de Raciocínio (Nexus KB)
        self.broker = broker
        self.cognitive_ops = CognitiveOperators(broker)
        print("🎨: NexusCompiler (Fase 1: Raciocínio) inicializado.")

    def compile_to_iti(self, aco: AbstractCreativeObject, cognitive_pipeline: List[str] = []) -> IntermediateTechnicalIntent:
        """
        Processo de compilação da Fase 1. Gera o ITI.
        """
        print(f"🧠: Fase 1 (Raciocínio Abstrato): Iniciando compilação do ACO...")
        iti = IntermediateTechnicalIntent(source_aco_id=aco.aco_id)

        # Etapa 1.1: Pipeline Cognitivo
        if cognitive_pipeline:
            iti.reasoning_chain.append("Início do Pipeline Cognitivo")
            for op_name in cognitive_pipeline:
                # Os operadores modificam o ACO e adicionam diretivas ao ITI
                self.cognitive_ops.apply(op_name, aco, iti)

        # Etapa 1.2: Tradução da Intenção e Elementos
        self._translate_intent(aco, iti)

        # Etapa 1.3: Geração de Queries Técnicas (Inferência)
        self._define_technical_queries(aco, iti)

        print("✅: Fase 1 concluída. ITI gerado.")
        return iti

    def _translate_intent(self, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent):
        if aco.intent.narrative_moment:
            iti.core_concept = aco.intent.narrative_moment

        if aco.intent.compositional_flow:
            flow = aco.intent.compositional_flow
            iti.composition = f"Path: {flow.path}"

    def _define_technical_queries(self, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent):
        # Inferência de Queries Técnicas (Pilar I.2)
        if "architecture" in iti.core_concept.lower() or "building" in iti.core_concept.lower():
             iti.abstract_directives.camera_query = "High-Res Architectural Camera"
             iti.abstract_directives.lens_query = "Tilt-Shift Lens"
             iti.reasoning_chain.append("Inferência: Contexto Arquitetônico detectado. Definidas queries técnicas.")
        
        # Processos Históricos
        if aco.constraints.style_constraints and aco.constraints.style_constraints.historical_process:
            process = aco.constraints.style_constraints.historical_process
            iti.abstract_directives.historical_process = process
            iti.reasoning_chain.append(f"Diretiva de Processo Histórico adicionada: {process}")