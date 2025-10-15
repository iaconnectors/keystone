# main.py

"""
Demonstração do fluxo de trabalho do CHROMA Nexus v1.0.
"""

from nexus.orchestrator import ChromaNexusOrchestrator
from nexus.core.models import (
    AbstractCreativeObject, ACOEmotion, ACOSubject, 
    ACOEnvironment, ACOCompositionalFlow, ACOStyleConstraints, ACOConstraints, ACOIntent, ACOElements
)
import traceback

def create_aco_pilar_i_composition() -> AbstractCreativeObject:
    """
    Teste do Pilar I: Composição Abstrata (spiral_inward).
    """
    aco = AbstractCreativeObject()
    aco.intent = ACOIntent(
        narrative_moment="The moment of singularity, where consciousness merges with the digital realm.",
        # Teste chave para a IMTL: Fluxo abstrato
        compositional_flow=ACOCompositionalFlow(
            path="spiral_inward",
            focal_point="center"
        )
    )
    aco.elements = ACOElements(
        subjects=[ACOSubject(id="figure", description="A human silhouette dissolving into light and data.")],
        environment=ACOEnvironment(description="An abstract digital landscape.", atmosphere="ethereal")
    )
    return aco

def create_aco_pilar_ii_process() -> AbstractCreativeObject:
    """
    Teste do Pilar II.2: Processos Físicos (Daguerreotype).
    """
    aco = AbstractCreativeObject()
    aco.intent = ACOIntent(
        narrative_moment="A portrait frozen in time."
    )
    aco.elements = ACOElements(
        subjects=[ACOSubject(id="sailor", description="A Victorian-era sailor with a weathered face.")]
    )
    # Teste chave: Restrição de processo histórico
    aco.constraints.style_constraints = ACOStyleConstraints(
        historical_process="Daguerreotype"
    )
    return aco

def create_aco_pilar_ii_cognitive() -> AbstractCreativeObject:
    """
    Teste do Pilar II.3: Operadores Cognitivos (Neuroestética).
    """
    aco = AbstractCreativeObject()
    aco.intent = ACOIntent(
        narrative_moment="A grand, imposing government building designed for stability."
    )
    aco.elements = ACOElements(
        environment=ACOEnvironment(description="A modern plaza at midday.", atmosphere="formal")
    )
    # Os operadores serão aplicados pelo Orchestrator no pipeline cognitivo.
    return aco


def main():
    try:
        # 1. Inicializar o Orquestrador
        # Certifique-se que a KB está em 'kb/nexus_kb_v1.0.json'
        nexus = ChromaNexusOrchestrator(kb_path="kb/nexus_kb_v1.0.json")

        # 2. Definir modelos alvo
        target_models = ["DALL-E_3", "Midjourney_V6", "Stable_Diffusion_3"]

        # 3. Executar Demonstrações

        print("\n\n=== DEMO 1: Composição Abstrata (Pilar I) ===")
        aco1 = create_aco_pilar_i_composition()
        nexus.run_workflow(aco1, target_models)

        print("\n\n=== DEMO 2: Processos Físicos (Pilar II.2) ===")
        aco2 = create_aco_pilar_ii_process()
        nexus.run_workflow(aco2, target_models)

        print("\n\n=== DEMO 3: Operadores Cognitivos (Pilar II.3) ===")
        aco3 = create_aco_pilar_ii_cognitive()
        # Aplicar Simetria e Estrutura Fractal durante a compilação
        cognitive_pipeline = ["Operator_ImposeSymmetry", "Operator_ApplyFractalStructure"]
        nexus.run_workflow(aco3, target_models, cognitive_pipeline=cognitive_pipeline)


    except Exception as e:
        print(f"\n--- ERRO CRÍTICO NO SISTEMA NEXUS ---")
        traceback.print_exc()

if __name__ == "__main__":
    main()