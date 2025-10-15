# main.py

"""
Este ficheiro demonstra como todos os componentes do Keystone-CHROMA v25.1
se integram para orquestrar um pedido criativo do início ao fim,
alavancando a nova e expandida Base de Conhecimento técnica.
"""

from core_architecture import KeystoneCHROMA, ProjectStateObject
from operators_suite import GenerativeOperatorsSuite
from model_translation_layer import ModelTranslationLayer

def setup_system() -> KeystoneCHROMA:
    """Instancia e configura o sistema Keystone-CHROMA completo."""
    
    # 1. Instanciar o sistema principal, que carrega a KB.
    keystone_system = KeystoneCHROMA(kb_path="Keystone-CHROMA-KB-v25.1.json")

    # 2. Injetar as dependências (Operadores e MTL) na instância principal.
    #    Isto torna o sistema mais modular e testável.
    keystone_system.operators = GenerativeOperatorsSuite(keystone_system)
    keystone_system.mtl = ModelTranslationLayer(keystone_system.broker)
    
    return keystone_system

def run_advanced_creative_session(keystone_system: KeystoneCHROMA):
    """Simula uma sessão de utilizador avançada, utilizando os novos operadores técnicos."""
    
    # --- FASE 1: BRIEFING E DIÁLOGO SOCRÁTICO ---
    print("="*60)
    print("INICIANDO SESSÃO CRIATIVA AVANÇADA COM KEYSTONE-CHROMA v25.1")
    print("="*60)
    user_brief = "Criar uma cena de thriller psicológico tensa ao estilo de David Fincher, focada numa personagem num escritório mal iluminado. Quero a sensação de que foi filmada com uma câmara de cinema digital moderna e um gimbal de topo para movimentos suaves e rastejantes."
    
    # O sistema inicia o diálogo e constrói um PSO base.
    # Para esta demonstração, vamos simular a escolha '2' (retrato clássico/dramático).
    print(f"\n: Recebido briefing: '{user_brief}'")
    pso = keystone_system._build_pso(user_brief, '2')
    pso.master_references.append("David_Fincher") # Adicionar o mestre principal
    pso.reasoning_chain.append("Adicionada referência a David Fincher")

    # --- FASE 2: REFINAMENTO TÉCNICO COM OPERADORES ---
    print("\n" + "-"*60)
    print("FASE DE REFINAMENTO TÉCNICO")
    print("-"*60)
    
    # O utilizador aplica operadores para especificar o plano de produção.
    operators = keystone_system.operators
    
    # 2.1 Definir o pacote de câmara
    operators.apply_operator("set_camera_package", pso, 
                             camera="Sony VENICE 2", 
                             lens="Zeiss Supreme Prime Radiance")
                             
    # 2.2 Definir o setup de iluminação
    operators.apply_operator("build_lighting_setup", pso,
                             style="Low-key, alto contraste, sombras suaves",
                             key_light="Aputure Nova P600c",
                             modifiers=["softbox", "grid"])

    # 2.3 Definir o movimento da câmara
    operators.apply_operator("define_camera_movement", pso,
                             rig_model="DJI RS 4 Pro",
                             movement="slow push-in")

    # 2.4 (Opcional) Aplicar um workflow para criar um mundo consistente
    apply_workflow = input("\nDeseja criar um 'Mundo' consistente para este projeto? (s/n): ")
    if apply_workflow.lower() == 's':
        operators.apply_operator("Workflow_Art_Direction", pso)
        if pso.world_state:
            print(pso.world_state)

    # Mostrar o PSO final e enriquecido
    print("\n" + "-"*60)
    print("PLANO DE EXECUÇÃO (PSO) FINALIZADO")
    print("-"*60)
    print(pso)

    # --- FASE 3: ORQUESTRAÇÃO MULTIMODELO ---
    target_models =

    print("\n" + "="*60)
    print("INICIANDO ORQUESTRAÇÃO PARA MÚLTIPLOS MODELOS")
    print("="*60)

    for model in target_models:
        keystone_system.orchestrate(pso, model)
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    try:
        system = setup_system()
        run_advanced_creative_session(system)
    except Exception as e:
        print(f"\n--- ERRO CRÍTICO NO SISTEMA ---")
        print(f"Ocorreu um erro inesperado: {e}")
        print("A encerrar a aplicação.")