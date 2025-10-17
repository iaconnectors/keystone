"""Testes para os operadores conceituais do Synthetica."""

from __future__ import annotations

from synthetica.core.models import (
    ACOSubject,
    AbstractCreativeObject,
    IntermediateTechnicalIntent,
)
from synthetica.engines.operators import OperatorsEngine


def _build_aco(subject_id: str = "Hero") -> AbstractCreativeObject:
    aco = AbstractCreativeObject()
    aco.elements.subjects.append(
        ACOSubject(id=subject_id, description="Primary hybrid subject.")
    )
    return aco


def test_define_hybridism_applies_subject_metadata(sample_kb) -> None:
    engine = OperatorsEngine(sample_kb)
    aco = _build_aco()
    iti = IntermediateTechnicalIntent(source_aco_id=aco.aco_id)

    engine.apply(
        "Operator_DefineHybridism",
        aco,
        iti,
        params={
            "subject_id": "Hero",
            "ontology_ref": (
                "2.0_Semiotics_and_Psychology_Database."
                "2.7_Theriocephalic_Iconography.Kinnari"
            ),
            "variant": "Pal_Subversive",
        },
    )

    subject = aco.elements.subjects[0]
    assert subject.hybrid_variant == "Pal_Subversive"
    assert subject.hybrid_ontology_ref.endswith("Kinnari")
    assert "Operator_DefineHybridism" in aco.applied_operators
    assert any("Hybridism" in step for step in iti.reasoning_chain)


def test_cultural_cannibalize_creates_directive(sample_kb) -> None:
    engine = OperatorsEngine(sample_kb)
    aco = _build_aco()
    iti = IntermediateTechnicalIntent(source_aco_id=aco.aco_id)

    engine.apply(
        "Operator_CulturalCannibalize",
        aco,
        iti,
        params={
            "devouring_culture": (
                "11.0_Narrative_Structure_and_Storytelling."
                "11.4_Speculative_Fiction_and_Futurism.Solarpunk"
            ),
            "devoured_element": (
                "5.0_Masters_Lexicon.5.6_Fashion_and_Costume_Design."
                "Iris van Herpen"
            ),
            "synthesis_mode": "Aesthetic",
        },
    )

    directive = iti.abstract_directives.antropofagia_directive
    assert directive is not None
    assert directive.devouring_culture.endswith("Solarpunk")
    assert directive.devoured_element.endswith("Iris van Herpen")
    assert any("Anthropophagy" in step for step in iti.reasoning_chain)


def test_set_archetypal_dynamics_validates_state(sample_kb) -> None:
    engine = OperatorsEngine(sample_kb)
    aco = _build_aco()
    iti = IntermediateTechnicalIntent(source_aco_id=aco.aco_id)

    engine.apply(
        "Operator_SetArchetypalDynamics",
        aco,
        iti,
        params={
            "shadow_state": "Assimilating",
            "manifestation": "2.0_Semiotics_and_Psychology_Database.Shadow.Anima",
            "trickster": "Internal_Catalyst",
        },
    )

    dynamics = aco.intent.archetypal_dynamics
    assert dynamics is not None
    assert dynamics.shadow_integration_state == "Assimilating"
    assert iti.abstract_directives.psychological_state == "Assimilating"
    assert any("Archetypal Dynamics" in step for step in iti.reasoning_chain)
