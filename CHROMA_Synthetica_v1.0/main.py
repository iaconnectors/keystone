"""Demonstracao do CHROMA Synthetica v1.1 (Hybridity, Anthropophagy, Contradiction)."""

import traceback

from synthetica.core.models import (
    AbstractCreativeObject,
    ACOElements,
    ACOIntent,
    ACOSubject,
)
from synthetica.orchestrator import ChromaSyntheticaOrchestrator

# Path for the unified knowledge base (v1.1)
KB_PATH = "kb/synthetica_kb_v1.1.json"


# ==============================================================================
# STUDY PROTOTYPES (Expansion Report)
# ==============================================================================

def create_prototype_a_kinnari_solarpunk() -> AbstractCreativeObject:
    """Prototype A (WP 5.1): Kinnari Solarpunk."""
    aco = AbstractCreativeObject()
    aco.intent = ACOIntent(
        narrative_moment=(
            "A bio-engineered diplomat negotiating atmospheric treaties on a terraformed Venus."
        )
    )
    aco.elements = ACOElements(
        subjects=[ACOSubject(id="Kinnari", description="Human-bird hybrid diplomat.")]
    )
    return aco


def create_prototype_c_centaur_chiaroscuro() -> AbstractCreativeObject:
    """Prototype C (WP 5.3): Centaur Chiaroscuro."""
    aco = AbstractCreativeObject()
    aco.intent = ACOIntent(
        narrative_moment=(
            "A solitary security agent in a decaying neo-noir metropolis. "
            "Struggles to repress primal rage amid deep shadows and harsh lights."
        )
    )
    aco.elements = ACOElements(
        subjects=[ACOSubject(id="CentaurAgent", description="Centaur security agent.")]
    )
    return aco


# ==============================================================================

def main():
    try:
        synthetica = ChromaSyntheticaOrchestrator(kb_path=KB_PATH)

        target_models = [
            "DALL-E_3",
            "Midjourney_V6",
            "Stable_Diffusion_3",
            "Seedream_4_0",
            "Nano_Banana",
            "Flux_1",
        ]

        # Demo A
        print("\n\n" + "=" * 80)
        print("=== DEMO 1: PROTOTIPO A (Kinnari Solarpunk) ===")
        print("Testing: Hybridism + Anthropophagy + Contradiction")
        print("=" * 80)

        aco_a = create_prototype_a_kinnari_solarpunk()
        pipeline_a = [
            {
                "name": "Operator_DefineHybridism",
                "params": {
                    "subject_id": "Kinnari",
                    "ontology_ref": (
                        "2.0_Semiotics_and_Psychology_Database."
                        "2.7_Theriocephalic_Iconography.Kinnari"
                    ),
                    "variant": "Pal_Subversive",
                },
            },
            {
                "name": "Operator_CulturalCannibalize",
                "params": {
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
            },
            {
                "name": "Operator_SetArchetypalDynamics",
                "params": {
                    "shadow_state": "Assimilating",
                    "trickster": "Internal_Catalyst",
                },
            },
        ]
        synthetica.run_workflow(aco_a, target_models, operator_pipeline=pipeline_a)

        # Demo C
        print("\n\n" + "=" * 80)
        print("=== DEMO 2: PROTOTIPO C (Centauro Chiaroscuro) ===")
        print("Testing: Hybridism + Extreme Contradiction (Translation Matrix)")
        print("=" * 80)

        aco_c = create_prototype_c_centaur_chiaroscuro()
        pipeline_c = [
            {
                "name": "Operator_DefineHybridism",
                "params": {
                    "subject_id": "CentaurAgent",
                    "ontology_ref": (
                        "2.0_Semiotics_and_Psychology_Database."
                        "2.7_Theriocephalic_Iconography.Centaur"
                    ),
                    "variant": "Thessalian_Horde",
                },
            },
            {
                "name": "Operator_SetArchetypalDynamics",
                "params": {
                    "shadow_state": "Projected",
                    "manifestation": (
                        "2.0_Semiotics_and_Psychology_Database."
                        "2.7_Theriocephalic_Iconography.Minotaur"
                    ),
                },
            },
        ]
        synthetica.run_workflow(aco_c, target_models, operator_pipeline=pipeline_c)

    except Exception as exc:  # pragma: no cover - demo safeguard
        print("\n--- CRITICAL ERROR IN SYNTHETICA ---")
        traceback.print_exc()
        print(f"\nCheck that KB v1.1 is available at '{KB_PATH}'. Error: {exc}")


if __name__ == "__main__":
    main()
