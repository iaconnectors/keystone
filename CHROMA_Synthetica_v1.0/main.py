"""Demonstração do CHROMA Synthetica v1.1."""
import traceback

from synthetica.core.models import ACOElements, ACOIntent, ACOSubject, AbstractCreativeObject
from synthetica.orchestrator import ChromaSyntheticaOrchestrator

KB_PATH = "kb/synthetica_kb_v1.1.json"


def create_prototype_a_kinnari_solarpunk() -> AbstractCreativeObject:
    """Protótipo A (WP 5.1): A Kinnari Solarpunk."""
    aco = AbstractCreativeObject()
    aco.intent = ACOIntent(
        narrative_moment="A bio-engineered diplomat negotiating atmospheric treaties on a terraformed Venus."
    )
    aco.elements = ACOElements(
        subjects=[ACOSubject(id="Kinnari", description="Human-bird hybrid diplomat.")]
    )
    return aco


def create_prototype_c_centaur_chiaroscuro() -> AbstractCreativeObject:
    """Protótipo C (WP 5.3): O Centauro Chiaroscuro."""
    aco = AbstractCreativeObject()
    aco.intent = ACOIntent(
        narrative_moment=(
            "A solitary security agent in a decaying neo-noir metropolis. "
            "Struggles intensely to repress primal rage. A labyrinth of deep shadows and harsh lights."
        )
    )
    aco.elements = ACOElements(
        subjects=[ACOSubject(id="CentaurAgent", description="Centaur security agent.")]
    )
    return aco


def main() -> None:
    try:
        synthetica = ChromaSyntheticaOrchestrator(kb_path=KB_PATH)
        target_models = ["DALL-E_3"]

        print("\n\n" + "=" * 80)
        print("=== DEMO 1: PROTÓTIPO A (Kinnari Solarpunk) ===")
        print("Testando: Hibridismo + Antropofagia + Contradição")
        print("=" * 80)

        aco_a = create_prototype_a_kinnari_solarpunk()
        pipeline_a = [
            {
                "name": "Operator_DefineHybridism",
                "params": {
                    "subject_id": "Kinnari",
                    "ontology_ref": "2.0_Semiotics_and_Psychology_Database.2.7_Theriocephalic_Iconography.Kinnari",
                    "variant": "Pal_Subversive",
                },
            },
            {
                "name": "Operator_CulturalCannibalize",
                "params": {
                    "devouring_culture": "11.0_Narrative_Structure_and_Storytelling.11.4_Speculative_Fiction_and_Futurism.Solarpunk",
                    "devoured_element": "5.0_Masters_Lexicon.5.6_Fashion_and_Costume_Design.Iris van Herpen",
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

        print("\n\n" + "=" * 80)
        print("=== DEMO 2: PROTÓTIPO C (Centauro Chiaroscuro) ===")
        print("Testando: Hibridismo + Contradição Extrema (Translation Matrix)")
        print("=" * 80)

        aco_c = create_prototype_c_centaur_chiaroscuro()
        pipeline_c = [
            {
                "name": "Operator_DefineHybridism",
                "params": {
                    "subject_id": "CentaurAgent",
                    "ontology_ref": "2.0_Semiotics_and_Psychology_Database.2.7_Theriocephalic_Iconography.Centaur",
                    "variant": "Thessalian_Horde",
                },
            },
            {
                "name": "Operator_SetArchetypalDynamics",
                "params": {
                    "shadow_state": "Projected",
                    "manifestation": "2.0_Semiotics_and_Psychology_Database.2.7_Theriocephalic_Iconography.Minotaur",
                },
            },
        ]
        synthetica.run_workflow(aco_c, target_models, operator_pipeline=pipeline_c)

    except Exception as exc:  # pragma: no cover - fluxo demonstrativo
        print("\n--- ERRO CRÍTICO NO SISTEMA SYNTHETICA ---")
        traceback.print_exc()
        print(f"\nCertifique-se de que a KB v1.1 está em '{KB_PATH}'. Erro: {exc}")


if __name__ == "__main__":
    main()
