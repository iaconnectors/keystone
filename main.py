# main.py

"""
Demonstração da integração do Keystone-CHROMA v27.0,
alavancando a KB enciclopédica e o KnowledgeBroker otimizado (Cache + Fuzzy Search).
"""

from core_architecture import KeystoneCHROMA, ProjectStateObject
from operators_suite import GenerativeOperatorsSuite
from model_translation_layer import ModelTranslationLayer 
from typing import Optional
import traceback

def setup_system() -> Optional[KeystoneCHROMA]:
    """Instancia e configura o sistema completo."""
   
    try:
        # O caminho padrão é "Keystone-CHROMA-KB-v27.0.json"
        keystone_system = KeystoneCHROMA()
    except (FileNotFoundError, ValueError) as e:
        print(f"\nFalha ao inicializar o sistema: {e}")
        return None

    # Injetar as dependências (Dependency Injection).
    keystone_system.operators = GenerativeOperatorsSuite(keystone_system)
    keystone_system.mtl = ModelTranslationLayer(keystone_system.broker)
   
    return keystone_system

def run_advanced_creative_session(keystone_system: KeystoneCHROMA):
    """Simula uma sessão avançada, demonstrando o uso da nova KB e a busca fuzzy nos operadores."""
   
    print("\n" + "="*70)
    print("      INICIANDO SESSÃO CRIATIVA AVANÇADA (Keystone-CHROMA v27.0)      ")
    print("="*70)
    
    # --- FASE 1: BRIEFING E CONSTRUÇÃO INICIAL (Foco em Arquitetura/Design) ---
    
    # Simulação da escolha '2' (Arquitetura Especulativa).
    pso = keystone_system._build_pso_simulation("Briefing Inicial", '2')

    # --- FASE 2: REFINAMENTO TÉCNICO (Testando o Fuzzy Match e Novos Domínios) ---
    print("\n" + "-"*70)
    print("      FASE DE REFINAMENTO TÉCNICO (Teste de Fuzzy Match Ativo)      ")
    print("-"*70)
   
    operators: GenerativeOperatorsSuite = keystone_system.operators
   
    # 2.1 Definir a "câmara" (perspetiva arquitetônica)
    # Teste Fuzzy: Usando nomes ligeiramente incorretos/simplificados que devem ser corrigidos pelo Broker.
    print("Teste Fuzzy (Câmara e Lente):")
    operators.apply_operator("set_camera_package", pso,
                             camera="Canon R5 Architectural", # Deve corresponder a "Canon EOS R5 (High-Res Architectural)"
                             lens="Canon TS-E 17mm Tilt") # Deve corresponder a "Canon TS-E 17mm f/4L (Tilt-Shift)"
                             
    # 2.2 Definir a iluminação e Fenômenos Ópticos (v27.0)
    print("\nTeste Fuzzy e Novos Campos (Iluminação/Física):")
    operators.apply_operator("build_lighting_setup", pso,
                             style="Iluminação Natural Otimizada com Destaque (Accent Lighting) LED",
                             key_light="Luz Solar Direta (Filtrada)", # Termo genérico
                             modifiers=["Octabank Large", "Refletor Silver"], # Nomes ligeiramente diferentes
                             # (v27.0) Passando fenômenos ópticos via kwargs
                             phenomena=["Caustics (from nearby water feature)", "Volumetric Lighting (God rays)"])

    # 2.3 Definir o Workflow de Consistência
    art_direction_inputs = {
        "world_name": "Expo Futuro Sustentável 2050",
        "mood": "Inspirador e Sereno",
        "stylization": "Futurismo Orgânico",
        "architectural_style": "Parametric Solarpunk" # (v27.0)
    }
    operators.apply_operator("Workflow_Art_Direction", pso, inputs=art_direction_inputs)

    # Mostrar o PSO final
    print("\n" + "-"*70)
    print("                PLANO DE EXECUÇÃO (PSO) FINALIZADO                ")
    print("-"*70)
    print(pso)

    # --- FASE 3: ORQUESTRAÇÃO MULTIMODELO ---
    target_models = [
        "DALL-E_3",
        "Midjourney_V6",
        "Stable_Diffusion_3"
    ]

    print("\n" + "="*70)
    print("               INICIANDO ORQUESTRAÇÃO MULTIMODELO (MTL)               ")
    print("="*70)

    for model in target_models:
        keystone_system.orchestrate(pso, model)
        print("\n")

if __name__ == "__main__":
    try:
        system = setup_system()
        if system:
            run_advanced_creative_session(system)
        else:
            print("\nA encerrar a aplicação devido a falha na inicialização.")
    except Exception as e:
        # Captura exceções não tratadas
        print(f"\n--- ERRO CRÍTICO NO SISTEMA ---")
        traceback.print_exc()
        print(f"Erro: {e}")
        print("A encerrar a aplicação.")