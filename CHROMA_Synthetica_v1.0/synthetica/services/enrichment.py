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

        synthesis = self._synthesize_anthropophagy(directive)
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

    @staticmethod
    def _normalise_label(raw: str) -> str:
        return raw.replace("_", " ")

    @staticmethod
    def _dedupe_preserve_order(items: List[str]) -> List[str]:
        seen = set()
        ordered: List[str] = []
        for item in items:
            key = item.lower()
            if key in seen or not item:
                continue
            seen.add(key)
            ordered.append(item)
        return ordered

    def _synthesize_anthropophagy(
        self, directive: CulturalCannibalizeDirective
    ) -> List[str]:
        devouring_label = self._normalise_label(
            directive.devouring_culture.split(".")[-1]
        )
        devoured_label = self._normalise_label(
            directive.devoured_element.split(".")[-1]
        )

        devouring_keywords = self._string_list(
            self.broker.get_flat_list(directive.devouring_culture)
        )
        devoured_keywords = self._string_list(
            self.broker.get_flat_list(directive.devoured_element)
        )

        if not devouring_keywords:
            devouring_keywords = [devouring_label]
        if not devoured_keywords:
            devoured_keywords = [devoured_label]

        synthesis: List[str] = [
            f"{devouring_label} converges with {devoured_label} "
            f"({directive.synthesis_mode.lower()} synthesis)"
        ]
        synthesis.extend(devouring_keywords[:3])
        synthesis.extend(devoured_keywords[:2])

        if directive.synthesis_mode == "Narrative":
            synthesis.append(f"Narrative throughline led by {devouring_label}")
        elif directive.synthesis_mode == "Symbolic":
            synthesis.append(f"Symbolic tension between {devouring_label} and {devoured_label}")

        return self._dedupe_preserve_order(synthesis)
