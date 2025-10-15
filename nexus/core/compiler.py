# nexus/core/compiler.py

from nexus.core.models import AbstractCreativeObject, ProjectStateObject
from nexus.core.knowledge_broker import KnowledgeBroker
from nexus.engines.operators import CognitiveOperators
from typing import List

class NexusCompiler:
    """
    O Compilador do Nexus (O Diretor de Arte IA). 
    Traduz a intenção (ACO) num plano técnico (PSO).
    """
    def __init__(self, broker: KnowledgeBroker):
        self.broker = broker
        self.cognitive_ops = CognitiveOperators(broker)

    def compile(self, aco: AbstractCreativeObject, cognitive_pipeline: List[str] = []) -> ProjectStateObject:
        """
        Processo principal de compilação.
        """
        print(f"🔄: Iniciando compilação do ACO {aco.aco_id}...")
        pso = ProjectStateObject(source_aco_id=aco.aco_id)

        # FASE 0: Pipeline Cognitivo (Pilar II.3)
        # Aplica operadores neuroestéticos ao ACO antes da tradução técnica.
        if cognitive_pipeline:
            pso.reasoning_chain.append("Início do Pipeline Cognitivo (Neuroestética)")
            for op_name in cognitive_pipeline:
                self.cognitive_ops.apply(op_name, aco)
                pso.reasoning_chain.append(f"Aplicado: {op_name}")

        # FASE 1: Tradução da Intenção e Elementos
        self._translate_intent(aco, pso)
        self._translate_elements(aco, pso)

        # FASE 2: Aplicação de Estilo e Processos Físicos (Pilar II.2)
        self._apply_constraints(aco, pso)

        # FASE 3: Decisões Técnicas
        self._define_technical_package(pso)

        print("✅: Compilação concluída. PSO gerado.")
        return pso

    def _translate_intent(self, aco: AbstractCreativeObject, pso: ProjectStateObject):
        # Emoção
        if aco.intent.core_emotions:
            sorted_emotions = sorted(aco.intent.core_emotions, key=lambda x: x.weight, reverse=True)
            pso.emotional_intent = sorted_emotions[0].emotion
            pso.reasoning_chain.append(f"Intenção emocional primária: {pso.emotional_intent}")

        # Composição
        if aco.intent.compositional_flow:
            flow = aco.intent.compositional_flow
            pso.composition = f"Path: {flow.path}, Focal Point: {flow.focal_point}"
            pso.reasoning_chain.append(f"Fluxo composicional definido: {flow.path}")

    def _translate_elements(self, aco: AbstractCreativeObject, pso: ProjectStateObject):
        # Conceito Central (Narrativa + Sujeitos + Ambiente)
        parts = []
        if aco.intent.narrative_moment:
            parts.append(aco.intent.narrative_moment)

        for subject in aco.elements.subjects:
            desc = subject.description
            if subject.attributes:
                desc += f" ({', '.join(subject.attributes)})"
            parts.append(desc)
        
        if aco.elements.environment:
            parts.append(f"Located in: {aco.elements.environment.description}. Atmosphere: {aco.elements.environment.atmosphere}.")

        pso.core_concept = " ".join(parts)
        pso.reasoning_chain.append("Conceito central sintetizado.")

    def _apply_constraints(self, aco: AbstractCreativeObject, pso: ProjectStateObject):
        if aco.constraints.style_constraints:
            constraints = aco.constraints.style_constraints
            
            # Referências
            if constraints.reference_artists:
                pso.master_references.extend(constraints.reference_artists)
                pso.visual_style = f"Inspired by {', '.join(constraints.reference_artists)}"
                pso.reasoning_chain.append(f"Estilo definido por referências.")

            # Processos Históricos (Pilar II.2)
            if constraints.historical_process:
                self._apply_process_artifacts(constraints.historical_process, pso)

        if not pso.visual_style:
            # Inferência padrão se não houver restrições
            pso.visual_style = "Cinematic Realism"
            pso.reasoning_chain.append("Estilo visual padrão aplicado.")

    def _apply_process_artifacts(self, process_name: str, pso: ProjectStateObject):
        """Consulta a KB (Pilar II.2, Tabela 2) para artefatos de processo."""
        # Caminho para a taxonomia na KB Nexus v1.0
        base_path = f"10.0_Technical_Execution_Ontology.10.8_Physical_Process_Artifact_Taxonomy.{process_name}"
        
        # Acha todos os keywords na taxonomia para o processo dado.
        # A função get_flat_list navega recursivamente e coleta todas as folhas.
        artifacts = self.broker.get_flat_list(base_path)
        
        if artifacts:
            # Filtra para pegar apenas os keywords (strings que contêm espaços), excluindo nomes de categorias ou descrições.
            # Esta é uma heurística simples para extrair as palavras-chave do prompt da estrutura achatada.
            keywords = [k for k in artifacts if isinstance(k, str) and " " in k]
            pso.process_artifacts.extend(keywords)
            pso.reasoning_chain.append(f"Aplicados artefatos do processo: {process_name} ({len(keywords)} keywords).")
        else:
            pso.reasoning_chain.append(f"AVISO: Processo '{process_name}' não encontrado na KB ({base_path}).")

    def _define_technical_package(self, pso: ProjectStateObject):
        # Lógica simplificada de seleção de equipamento
        if pso.visual_style and "Cinematic" in pso.visual_style:
            pso.camera_package = {"camera": "ARRI Alexa Mini LF", "lens": "ARRI Signature Prime"}
        else:
            pso.camera_package = {"camera": "Digital Photo"}
        pso.reasoning_chain.append("Pacote técnico definido.")