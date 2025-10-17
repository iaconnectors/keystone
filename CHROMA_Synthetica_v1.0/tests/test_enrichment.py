"""Testes para a fase de enrichment do pipeline."""

from __future__ import annotations

from synthetica.core.models import (
    CulturalCannibalizeDirective,
    IntermediateTechnicalIntent,
)
from synthetica.services.enrichment import EnrichmentService


def test_enrichment_merges_anthropophagy_and_translation(sample_kb) -> None:
    enrichment = EnrichmentService(sample_kb)

    iti = IntermediateTechnicalIntent(source_aco_id="aco-test")
    iti.core_concept = "Hybrid diplomat negotiating regenerative futures."
    iti.abstract_directives.antropofagia_directive = CulturalCannibalizeDirective(
        devouring_culture=(
            "11.0_Narrative_Structure_and_Storytelling."
            "11.4_Speculative_Fiction_and_Futurism.Solarpunk"
        ),
        devoured_element=(
            "5.0_Masters_Lexicon.5.6_Fashion_and_Costume_Design.Iris van Herpen"
        ),
        synthesis_mode="Aesthetic",
    )
    iti.abstract_directives.psychological_state = "Assimilating"

    pso = enrichment.enrich_to_pso(iti)

    assert pso.core_concept.startswith("Hybrid diplomat")
    assert "Enrichment phase started." in pso.reasoning_chain

    # Antropofagia deve combinar narrativas e materiais das duas referências
    assert pso.visual_style_keywords[0].lower().startswith("solarpunk converges with iris van herpen")
    assert any("Regenerative urban design" in keyword for keyword in pso.visual_style_keywords)
    assert any("Complex organic couture" in keyword for keyword in pso.visual_style_keywords)

    # Translation matrix adiciona mestres e palavras-chave
    assert "Roger_Deakins" in pso.master_references
    assert any("Positive_Reconciliation" in keyword for keyword in pso.visual_style_keywords)
