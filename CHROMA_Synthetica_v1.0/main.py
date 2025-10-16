# main.py

"""
Demonstração do fluxo de trabalho do CHROMA Synthetica v1.0 (Mente Híbrida).
"""

# Importação atualizada
from synthetica.orchestrator import ChromaSyntheticaOrchestrator
from synthetica.core.models import (
    AbstractCreativeObject, ACOIntent, ACOConstraints, ACOStyleConstraints
)
import traceback

# Caminhos para as KBs de entrada
NEXUS_KB_PATH = "kb/nexus_kb_v1.0.json"
KEYSTONE_KB_PATH = "kb/keystone_kb_v27.0.json"

def create_aco_hybrid_mind_test() -> AbstractCreativeObject:
    """
    Teste da Mente Híbrida (WP 1.2).
    Intenção: Edifício governamental estável e imponente, com concreto (sugere Brutalismo).
    Fase 1 (Raciocínio): Aplicar Simetria; Gerar queries para arquitetos (Simetria+Brutalismo) e equipamento arquitetônico.
    Fase 2 (Enriquecimento): Consultar Keystone KB; Encontrar Tadao Ando; Encontrar Canon R5 Architectural e Lente Tilt-Shift.
    """
    aco = AbstractCreativeObject()
    aco.intent = ACOIntent(
        # Incluímos "concrete" para ativar a inferência de brutalismo no operador cognitivo.
        narrative_moment="A grand, imposing government building designed for stability, utilizing exposed concrete. Architectural visualization."
    )
    return aco

def main():
    try:
        # 1. Inicializar o Orquestrador Synthetica (Mente Híbrida com Dual Brokers)
        synthetica = ChromaSyntheticaOrchestrator(
            nexus_kb_path=NEXUS_KB_PATH,
            keystone_kb_path=KEYSTONE_KB_PATH
        )

        target_models = ["DALL-E_3"]

        # 2. Executar Teste: Mente Híbrida (Arquitetura)
        print("\n\n=== DEMO 1: MENTE HÍBRIDA (Arquitetura e Cognição) ===")
        aco1 = create_aco_hybrid_mind_test()
        # O operador deve gerar diretivas abstratas (Pilar I.2).
        cognitive_pipeline = ["Operator_ImposeSymmetry"]
        synthetica.run_workflow(aco1, target_models, cognitive_pipeline=cognitive_pipeline)
        
        # 3. Testar Introspecção (Épico 3)
        print("\n\n=== DEMO 2: INTROSPECÇÃO (Épico 3) ===")
        synthetica.introspect_knowledge("Quais são os princípios da neuroestética?")


    except Exception as e:
        print(f"\n--- ERRO CRÍTICO NO SISTEMA SYNTHETICA ---")
        traceback.print_exc()
        print(f"\nCertifique-se de que os arquivos KB estão no diretório 'kb/'.")

if __name__ == "__main__":
    # INSTRUÇÕES DE EXECUÇÃO:
    # 1. Execute 'python main.py' para demonstrar o Épico 1 (Mente Híbrida usando KBs separadas).
    # 2. Execute 'python scripts/autonomous_curator.py' para demonstrar o Épico 2.
    # 3. Execute 'python scripts/migrate_kb.py' para demonstrar o Épico 3 (Fusão de KB).
    main()