"""
Demonstração do CHROMA Synthetica v1.1 (Hibridismo, Antropofagia, Contradição).
"""

# Importação atualizada
from synthetica.orchestrator import ChromaSyntheticaOrchestrator
from synthetica.core.models import (
    AbstractCreativeObject, ACOIntent, ACOElements, ACOSubject
)
import traceback

# (v1.1) Caminho para a KB Unificada e atualizada.
KB_PATH = "kb/synthetica_kb_v1.1.json"

# ==============================================================================
# PROTÓTIPOS DE ESTUDO (Relatório de Expansão)
# ==============================================================================

def create_prototype_a_kinnari_solarpunk() -> AbstractCreativeObject:
    """Protótipo A (WP 5.1): A Kinnari Solarpunk."""
    aco = AbstractCreativeObject()
    aco.intent = ACOIntent(
        narrative_moment="A bio-engineered diplomat negotiating atmospheric treaties on a terraformed Venus."
    )
    # (v1.1) Definimos o sujeito para que o operador de Hibridismo possa atuar sobre ele.
    aco.elements = ACOElements(
        subjects=[ACOSubject(id="Kinnari", description="Human-bird hybrid diplomat.")]
    )
    return aco

def create_prototype_c_centaur_chiaroscuro() -> AbstractCreativeObject:
    """Protótipo C (WP 5.3): O Centauro Chiaroscuro."""
    aco = AbstractCreativeObject()
    aco.intent = ACOIntent(
        narrative_moment="A solitary security agent in a decaying neo-noir metropolis. Struggles intensely to repress primal rage. A labyrinth of deep shadows and harsh lights."
    )
    # (v1.1) Definimos o sujeito.
    aco.elements = ACOElements(
        subjects=[ACOSubject(id="CentaurAgent", description="Centaur security agent.")]
    )
    return aco

# ==============================================================================

def main():
    try:
        # 1. Inicializar o Orquestrador Synthetica v1.1 (Broker Unificado)
        synthetica = ChromaSyntheticaOrchestrator(kb_path=KB_PATH)

        target_models = [
            "DALL-E_3",
            "Midjourney_V6",
            "Stable_Diffusion_3",
            "Seedream_4_0",
            "Nano_Banana",
            "Flux_1",
        ]

        # 2. Executar Protótipo A (Kinnari Solarpunk)
        print("\n\n" + "="*80)
        print("=== DEMO 1: PROTÓTIPO A (Kinnari Solarpunk) ===")
        print("Testando: Hibridismo + Antropofagia + Contradição")
        print("="*80)

        acoA = create_prototype_a_kinnari_solarpunk()

        # O pipeline agora usa a estrutura {name, params}
        pipelineA = [
            # 1. Hibridismo (Pilar 2): Define a ontologia como Kinnari (Variante Pal_Subversive)
            {"name": "Operator_DefineHybridism", "params": {
                "subject_id": "Kinnari",
                "ontology_ref": "2.0_Semiotics_and_Psychology_Database.2.7_Theriocephalic_Iconography.Kinnari",
                "variant": "Pal_Subversive"
            }},
            # 2. Antropofagia (Pilar 3): Solarpunk devora Iris van Herpen
            {"name": "Operator_CulturalCannibalize", "params": {
                "devouring_culture": "11.0_Narrative_Structure_and_Storytelling.11.4_Speculative_Fiction_and_Futurism.Solarpunk",
                "devoured_element": "5.0_Masters_Lexicon.5.6_Fashion_and_Costume_Design.Iris van Herpen",
                "synthesis_mode": "Aesthetic"
            }},
            # 3. Dinâmica Arquetípica (Pilar 4): Assimilating (Trickster Interno)
            {"name": "Operator_SetArchetypalDynamics", "params": {
                "shadow_state": "Assimilating",
                "trickster": "Internal_Catalyst"
            }}
        ]
        synthetica.run_workflow(acoA, target_models, operator_pipeline=pipelineA)


        # 3. Executar Protótipo C (Centauro Chiaroscuro)
        print("\n\n" + "="*80)
        print("=== DEMO 2: PROTÓTIPO C (Centauro Chiaroscuro) ===")
        print("Testando: Hibridismo + Contradição Extrema (Translation Matrix)")
        print("="*80)

        acoC = create_prototype_c_centaur_chiaroscuro()

        pipelineC = [
            # 1. Hibridismo (Pilar 2): Define a ontologia como Centauro (Variante Thessalian_Horde)
            {"name": "Operator_DefineHybridism", "params": {
                "subject_id": "CentaurAgent",
                "ontology_ref": "2.0_Semiotics_and_Psychology_Database.2.7_Theriocephalic_Iconography.Centaur",
                "variant": "Thessalian_Horde"
            }},
            # 2. Dinâmica Arquetípica (Pilar 4): Projected (Simulando o colapso de Repressed)
            {"name": "Operator_SetArchetypalDynamics", "params": {
                "shadow_state": "Projected",
                "manifestation": "2.0_Semiotics_and_Psychology_Database.2.7_Theriocephalic_Iconography.Minotaur"
            }}
        ]
        synthetica.run_workflow(acoC, target_models, operator_pipeline=pipelineC)


    except Exception as e:
        print(f"\n--- ERRO CRÍTICO NO SISTEMA SYNTHETICA ---")
        traceback.print_exc()
        print(f"\nCertifique-se de que a KB v1.1 está em '{KB_PATH}'. Erro: {e}")

if __name__ == "__main__":
    main()
