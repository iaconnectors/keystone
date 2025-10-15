# main.py

"""
Demonstração da integração do Keystone-CHROMA v26.0, 
alavancando a KB expandida e a arquitetura semântica melhorada.
"""

from core_architecture import KeystoneCHROMA, ProjectStateObject
from operators_suite import GenerativeOperatorsSuite
from model_translation_layer import ModelTranslationLayer
from typing import Optional
import traceback

def setup_system() -> Optional[KeystoneCHROMA]:
    """Instancia e configura o sistema completo."""
   
    # 1. Instanciar o sistema principal (utiliza o caminho padrão da KB v26.0).
    try:
        # O caminho padrão é "Keystone-CHROMA-KB-v26.0.json"
        keystone_system = KeystoneCHROMA()
    except (FileNotFoundError, ValueError) as e:
        print(f"\nFalha ao inicializar o sistema: {e}")
        return None

    # 2. Injetar as dependências (Dependency Injection).
    keystone_system.operators = GenerativeOperatorsSuite(keystone_system)
    keystone_system.mtl = ModelTranslationLayer(keystone_system.broker)
   
    return keystone_system

def run_advanced_creative_session(keystone_system: KeystoneCHROMA):
    """Simula uma sessão avançada, testando a validação robusta e o desacoplamento da UI."""
   
    print("\n" + "="*70)
    print("      INICIANDO SESSÃO CRIATIVA AVANÇADA (Keystone-CHROMA v26.0)      ")
    print("="*70)
    
    # --- FASE 1: BRIEFING E CONSTRUÇÃO INICIAL ---
    user_brief = "Criar uma cena de thriller psicológico tensa ao estilo de David Fincher, focada numa personagem num escritório mal iluminado. Sensação de câmara digital moderna e movimentos suaves."
    print(f"👤 Briefing: {user_brief}\n")

    # Simulação da escolha '2' (retrato clássico/dramático) do diálogo socrático.
    pso = keystone_system._build_pso_simulation(user_brief, '2')
    
    if "David Fincher" not in pso.master_references:
        pso.master_references.append("David Fincher")
        pso.reasoning_chain.append("Adicionada referência do briefing: David Fincher")

    # --- FASE 2: REFINAMENTO TÉCNICO COM OPERADORES ---
    print("\n" + "-"*70)
    print("      FASE DE REFINAMENTO TÉCNICO (Validação Robusta Ativa)      ")
    print("-"*70)
   
    operators: GenerativeOperatorsSuite = keystone_system.operators
   
    # 2.1 Teste de Validação (Item Inválido) - Deve falhar.
    print("Teste de Validação (Falha esperada):")
    operators.apply_operator("set_camera_package", pso,
                             camera="Câmera Inválida XYZ", # Inválido
                             lens="Zeiss Supreme Prime Radiance")

    # 2.2 Definir o pacote de câmara (Itens Válidos da KB v26.0) - Deve ter sucesso.
    print("\nAplicação Válida:")
    operators.apply_operator("set_camera_package", pso,
                             camera="Sony VENICE 2",
                             lens="Zeiss Supreme Prime Radiance")
                             
    # 2.3 Definir o setup de iluminação
    operators.apply_operator("build_lighting_setup", pso,
                             style="Low-key, alto contraste (Fincher-esque), tons esverdeados",
                             key_light="Aputure Nova P600c",
                             # Testando um modificador válido e um inválido
                             modifiers=["Softbox (Large)", "Grid (40 degree)", "Modificador Inexistente"])

    # 2.4 Definir o movimento da câmara
    operators.apply_operator("define_camera_movement", pso,
                             rig_model="DJI RS 4 Pro",
                             movement="slow, creeping push-in")

    # 2.5 Aplicar workflow de consistência (Desacoplado da UI)
    print(f"\nSimulando inputs para criação de 'Mundo' (WSO)...")
    # Os inputs são passados como um dicionário, simulando uma API ou UI externa.
    art_direction_inputs = {
        "world_name": "Escritório Neo-Noir",
        "mood": "Tensão e Paranoia",
        "stylization": "Realismo Cinematográfico"
    }
    # O operador recebe o dicionário no parâmetro 'inputs'.
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
        "Stable_Diffusion_3",
        "FLUX_1_Kontext",
        "Nano_Banana",
        "Seedream_4_0"
    ]

    print("\n" + "="*70)
    print("               INICIANDO ORQUESTRAÇÃO MULTIMODELO (MTL)               ")
    print("="*70)

    for model in target_models:
        keystone_system.orchestrate(pso, model)
        print("\n") # Espaço entre modelos

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
        print("A encerrar a aplicação.")