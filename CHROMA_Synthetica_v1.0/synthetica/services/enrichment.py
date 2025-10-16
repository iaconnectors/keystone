"""Serviço responsável pela Fase 2 (Enriquecimento Técnico) do Synthetica."""
from synthetica.core.knowledge_broker import KnowledgeBroker
from synthetica.core.models import (
    AbstractDirectives,
    CulturalCannibalizeDirective,
    IntermediateTechnicalIntent,
    ProjectStateObject,
)


class EnrichmentService:
    """Transforma o ITI em um Project State Object enriquecido."""

    def __init__(self, broker: KnowledgeBroker):
        self.broker = broker
        print("📚: EnrichmentService (Fase 2: Enriquecimento) inicializado.")

    def enrich_to_pso(self, iti: IntermediateTechnicalIntent) -> ProjectStateObject:
        print("💡: Fase 2 (Enriquecimento Técnico): Iniciando enriquecimento do ITI...")
        pso = ProjectStateObject(source_aco_id=iti.source_aco_id)
        pso.core_concept = iti.core_concept
        pso.composition = iti.composition
        pso.reasoning_chain.extend(iti.reasoning_chain)
        pso.reasoning_chain.append("Início da Fase de Enriquecimento")

        directives = iti.abstract_directives

        self._resolve_antropofagia(directives.antropofagia_directive, pso)
        self._resolve_archetypal_dynamics(directives.psychological_state, pso)
        self._resolve_hybridism_links(iti, pso)
        self._resolve_technical_package(directives, pso)

        print("✅: Fase 2 concluída. PSO final gerado.")
        return pso

    def _resolve_antropofagia(
        self, directive: CulturalCannibalizeDirective, pso: ProjectStateObject
    ) -> None:
        if directive is None:
            return

        pso.reasoning_chain.append(
            f"Processando Antropofagia: Modo {directive.synthesis_mode}..."
        )

        devouring = directive.devouring_culture.split('.')[-1]
        devoured = directive.devoured_element.split('.')[-1]

        if devouring == "Solarpunk" and "Iris van Herpen" in devoured:
            synthesis = [
                "Sustainable Solarpunk aesthetic",
                "3D printed photosynthetic structures",
                "Biophilic High-Tech",
                "Complex organic forms inspired by Iris van Herpen",
            ]
        elif devouring == "Yoruba" and devoured == "Brutalism":
            synthesis = [
                "Yoruba cosmology expressed in architecture",
                "Monumental exposed concrete structures",
                "Geometric patterns based on Ifá cosmology",
            ]
        else:
            keywords_devouring = self.broker.get_flat_list(directive.devouring_culture)
            keywords_devoured = self.broker.get_flat_list(directive.devoured_element)
            devouring_keywords = [str(k) for k in keywords_devouring if isinstance(k, str)]
            devoured_keywords = [str(k) for k in keywords_devoured if isinstance(k, str)]
            synthesis = devouring_keywords[:3] + devoured_keywords[:1]

        pso.visual_style_keywords.extend(synthesis)
        pso.reasoning_chain.append(f"Resultado Antropofagia: {synthesis}")

    def _resolve_archetypal_dynamics(self, state: str, pso: ProjectStateObject) -> None:
        if not state:
            return

        pso.reasoning_chain.append(
            f"Consultando Translation Matrix para estado psicológico: '{state}'..."
        )

        matrix_path = (
            "2.0_Semiotics_and_Psychology_Database."
            "2.8_Archetypal_Dynamics_Framework (Jungian)."
            f"Translation_Matrix.{state}.Aesthetic_Signifiers"
        )
        signifier_paths = self.broker.get_entry(matrix_path)

        if not signifier_paths:
            return

        resolved_signifiers = []
        for path in signifier_paths:
            concept_name = path.split('.')[-1]

            if "5.3_Art_and_Design_References" in path:
                if concept_name not in pso.master_references:
                    pso.master_references.append(concept_name)
            else:
                resolved_signifiers.append(concept_name)

        pso.visual_style_keywords.extend(resolved_signifiers)
        pso.reasoning_chain.append(
            "Translation Matrix Resolvido. Estilo: "
            f"{resolved_signifiers}. Mestres: {pso.master_references}"
        )

    def _resolve_hybridism_links(
        self, iti: IntermediateTechnicalIntent, pso: ProjectStateObject
    ) -> None:
        concept = iti.core_concept or ""
        if "Kinnari" in concept or "Kamdhenu" in concept:
            if "empowered female hybrid" in concept or "feminist critique" in concept:
                if "Gogi_Saroj_Pal" not in pso.master_references:
                    pso.master_references.append("Gogi_Saroj_Pal")
                    pso.reasoning_chain.append(
                        "Hibridismo: Adicionada referência 'Gogi Saroj Pal' (via link da variante)."
                    )

    def _resolve_technical_package(
        self, directives: AbstractDirectives, pso: ProjectStateObject
    ) -> None:
        pso.camera_package = {"camera": "High-fidelity digital render"}
