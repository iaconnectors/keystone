"""Phase 2 (technical enrichment) for the CHROMA Synthetica pipeline."""

from typing import List, Optional

from synthetica.core.knowledge_broker import KnowledgeBroker
from synthetica.core.models import (
    AbstractDirectives,
    CulturalCannibalizeDirective,
    IntermediateTechnicalIntent,
    ProjectStateObject,
)


class EnrichmentService:
    """Converts an ITI into a Project State Object with stylistic data."""

    def __init__(self, broker: KnowledgeBroker):
        self.broker = broker
        print("[EnrichmentService] Phase 2 (Enrichment) initialised.")

    def enrich_to_pso(self, iti: IntermediateTechnicalIntent) -> ProjectStateObject:
        """Build a PSO from the data surfaced during phase 1."""
        print("[EnrichmentService] Phase 2: enriching IntermediateTechnicalIntent.")

        pso = ProjectStateObject(source_aco_id=iti.source_aco_id)
        pso.core_concept = iti.core_concept
        pso.composition = iti.composition
        pso.reasoning_chain.extend(iti.reasoning_chain)
        pso.reasoning_chain.append("Enrichment phase started.")

        directives = iti.abstract_directives
        self._resolve_anthropophagy(directives.antropofagia_directive, pso)
        self._resolve_archetypal_dynamics(directives.psychological_state, pso)
        self._resolve_hybridism_links(iti, pso)
        self._resolve_technical_package(directives, pso)

        print("[EnrichmentService] Phase 2 complete. PSO generated.")
        return pso

    def _resolve_anthropophagy(
        self,
        directive: Optional[CulturalCannibalizeDirective],
        pso: ProjectStateObject,
    ) -> None:
        if directive is None:
            return

        pso.reasoning_chain.append(
            f"Resolving anthropophagy directive ({directive.synthesis_mode})."
        )

        devouring = directive.devouring_culture.split(".")[-1]
        devoured = directive.devoured_element.split(".")[-1]

        if devouring == "Solarpunk" and "Iris van Herpen" in devoured:
            synthesis = [
                "Sustainable solarpunk aesthetic",
                "3D printed photosynthetic structures",
                "Biophilic high-tech fashion",
                "Complex organic forms inspired by Iris van Herpen",
            ]
        elif devouring == "Yoruba" and devoured == "Brutalism":
            synthesis = [
                "Yoruba cosmology translated into architecture",
                "Monumental exposed concrete",
                "Geometric patterns derived from Ifa cosmology",
            ]
        else:
            devouring_keywords = self._string_list(
                self.broker.get_flat_list(directive.devouring_culture)
            )
            devoured_keywords = self._string_list(
                self.broker.get_flat_list(directive.devoured_element)
            )
            synthesis = devouring_keywords[:3] + devoured_keywords[:1]

        pso.visual_style_keywords.extend(synthesis)
        pso.reasoning_chain.append(f"Anthropophagy result: {synthesis}.")

    def _resolve_archetypal_dynamics(
        self, psychological_state: Optional[str], pso: ProjectStateObject
    ) -> None:
        if not psychological_state:
            return

        pso.reasoning_chain.append(
            f"Consulting translation matrix for state '{psychological_state}'."
        )

        matrix_path = (
            "2.0_Semiotics_and_Psychology_Database."
            "2.8_Archetypal_Dynamics_Framework (Jungian)."
            f"Translation_Matrix.{psychological_state}.Aesthetic_Signifiers"
        )
        signifier_paths = self.broker.get_entry(matrix_path)
        if not signifier_paths:
            return

        resolved_keywords: List[str] = []
        for path in signifier_paths:
            concept = path.split(".")[-1]
            if "5.3_Art_and_Design_References" in path:
                if concept not in pso.master_references:
                    pso.master_references.append(concept)
            else:
                resolved_keywords.append(concept)

        pso.visual_style_keywords.extend(resolved_keywords)
        pso.reasoning_chain.append(
            "Translation matrix resolved: "
            f"keywords {resolved_keywords}, masters {pso.master_references}."
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
                        "Hybridism link added: Gogi_Saroj_Pal."
                    )

    def _resolve_technical_package(
        self, directives: AbstractDirectives, pso: ProjectStateObject
    ) -> None:
        _ = directives  # Reserved for future use.
        pso.camera_package = {"camera": "High-fidelity digital render"}

    @staticmethod
    def _string_list(values: List[object]) -> List[str]:
        return [str(value) for value in values if isinstance(value, (str, bytes))]
