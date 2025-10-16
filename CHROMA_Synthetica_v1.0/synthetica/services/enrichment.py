# synthetica/services/enrichment.py

from synthetica.core.models import IntermediateTechnicalIntent, ProjectStateObject, CameraPackage, AbstractDirectives
from synthetica.core.knowledge_broker import KnowledgeBroker

class EnrichmentService:
    """
    Fase 2 da Mente Híbrida: Enriquecimento Técnico.
    Resolve as diretivas abstratas do ITI consultando a KB Enciclopédica e gera o PSO final.
    """
    def __init__(self, broker: KnowledgeBroker):
        # Usa o Broker Enciclopédico (Keystone KB)
        self.broker = broker
        print("📚: EnrichmentService (Fase 2: Enriquecimento) inicializado.")

    def enrich_to_pso(self, iti: IntermediateTechnicalIntent) -> ProjectStateObject:
        """
        Processo de enriquecimento da Fase 2. Gera o PSO.
        """
        print(f"💡: Fase 2 (Enriquecimento Técnico): Iniciando enriquecimento do ITI...")
        pso = ProjectStateObject(source_aco_id=iti.source_aco_id)
        
        # Copiar campos básicos
        pso.core_concept = iti.core_concept
        pso.composition = iti.composition
        pso.reasoning_chain.extend(iti.reasoning_chain)
        pso.reasoning_chain.append("Início da Fase de Enriquecimento (Keystone KB)")

        directives = iti.abstract_directives

        # 1. Resolver Mestres (Consulta Proativa)
        self._resolve_masters(directives, pso)
        
        # 2. Resolver Pacote Técnico
        self._resolve_technical_package(directives, pso)

        # 3. Resolver Artefatos Históricos
        self._resolve_historical_artifacts(directives, pso)
        
        # 4. Resolução de Conflitos Ontológicos (WP 1.3)
        self._resolve_conflicts(pso)

        print("✅: Fase 2 concluída. PSO final gerado.")
        return pso

    def _resolve_masters(self, directives: AbstractDirectives, pso: ProjectStateObject):
        """Consulta a KB Enciclopédica com base nas queries geradas na Fase 1."""
        if not directives.master_references_query:
            return

        pso.reasoning_chain.append(f"Consultando KB Enciclopédica para: {directives.master_references_query}")
        
        # Simulação da consulta complexa (WP 1.2)
        # Exemplo: "architects known for symmetry" AND "brutalism"
        
        # Caminho na Keystone KB v27.0
        path_architects = "5.0_Masters_Lexicon.5.3_Art_and_Design_References.Architects"
        
        # Verificação de existência na KB (simulação de consulta estruturada)
        if "architects known for symmetry" in directives.master_references_query and "brutalism" in directives.master_references_query:
            # Sabemos que Tadao Ando corresponde a estes critérios.
            # Usamos o Broker para verificar a existência na KB Keystone.
            if self.broker.validate_entry(path_architects, "Tadao Ando"):
                pso.master_references.append("Tadao Ando")
                pso.reasoning_chain.append("KB Respondeu (Masters): 'Tadao Ando' selecionado (Simetria + Brutalismo).")

    def _resolve_technical_package(self, directives: AbstractDirectives, pso: ProjectStateObject):
        camera_package = CameraPackage()

        # Lógica de Consulta Proativa para Câmera (Usando Fuzzy Search)
        if directives.camera_query:
            pso.reasoning_chain.append(f"Consultando KB Enciclopédica para: '{directives.camera_query}'")
            # Path na KB Keystone v27.0
            path = "10.0_Technical_Execution_Ontology.10.1_Cameras"
            match = self.broker.find_closest_match(path, directives.camera_query, cutoff=0.7)
            if match:
                camera_package["camera"] = match
                pso.reasoning_chain.append(f"KB Respondeu (Fuzzy Match Câmera): {match}.")

        # Lógica de Consulta Proativa para Lente
        if directives.lens_query:
            path = "10.0_Technical_Execution_Ontology.10.2_Lenses_and_Optics"
            match = self.broker.find_closest_match(path, directives.lens_query, cutoff=0.7)
            if match:
                camera_package["lens"] = match
                pso.reasoning_chain.append(f"KB Respondeu (Fuzzy Match Lente): {match}.")

        if camera_package:
            pso.camera_package = camera_package

    def _resolve_historical_artifacts(self, directives: AbstractDirectives, pso: ProjectStateObject):
        if not directives.historical_process:
            return
            
        process_name = directives.historical_process
        # NOTA: A KB Keystone v27.0 não possui a taxonomia detalhada do Nexus 1.0 (Tabela 2 WP).
        # Tentamos acessar a estrutura simplificada da v27.0 (10.8) ou usamos um fallback.
        
        # Tentativa de acesso à estrutura da v27.0
        path = f"10.0_Technical_Execution_Ontology.10.8_Historical_Printing_Techniques.{process_name}"
        description = self.broker.get_entry(path)

        if description:
             pso.process_artifacts.append(f"{process_name} aesthetic")
             pso.reasoning_chain.append(f"Enriquecimento (Artefatos): {process_name} encontrado na KB v27.0.")
        else:
             # Fallback necessário para Daguerreotype (que não está em 10.8 na v27.0)
             pso.process_artifacts.append(f"{process_name} style, vintage photography artifacts")
             pso.reasoning_chain.append(f"Enriquecimento (Artefatos): {process_name} não encontrado em 10.8. Usando fallback genérico.")


    def _resolve_conflicts(self, pso: ProjectStateObject):
        # (WP 1.3) Implementação da política "Intenção Artística Prevalece com Notificação"
        if "Tadao Ando" in pso.master_references and "glass facade" in pso.core_concept.lower() and "concrete" not in pso.core_concept.lower():
            conflict_msg = "AVISO: O estilo de 'Tadao Ando' (associado a concreto) foi aplicado a 'glass facade'. Tratado como 'Contradição Artística Intencional'."
            pso.ontological_conflicts.append(conflict_msg)
            pso.reasoning_chain.append(f"Conflito Ontológico Detectado e Resolvido.")