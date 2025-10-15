# operators_suite.py

from core_architecture import KeystoneCHROMA, ProjectStateObject, WorldStateObject, KnowledgeBroker
from typing import List, Optional, Dict

class GenerativeOperatorsSuite:
    """
    Representa a '4.0_Creative_Operators_and_Engines'.
    (Melhoria v26.0: Validação robusta centralizada e desacoplamento da UI).
    """
    def __init__(self, core_system: KeystoneCHROMA):
        self.system = core_system
        self.broker: KnowledgeBroker = core_system.broker

    def apply_operator(self, operator_name: str, pso: ProjectStateObject, **kwargs) -> bool:
        """
        Gateway seguro para aplicar operadores. Retorna True se sucesso, False se falha.
        """
        if hasattr(self, operator_name):
            print(f"\n🔧: Ativando operador: {operator_name}...")
            
            # Chama o método do operador.
            success = getattr(self, operator_name)(pso, **kwargs)
            
            if success:
                pso.activated_operators.append(operator_name)
                print(f"✅: Operador '{operator_name}' aplicado com sucesso.")
                return True
            else:
                print(f"❌: Falha ao aplicar operador '{operator_name}'. Estado do PSO não modificado.")
                return False
        else:
            print(f"⚠️: AVISO: Operador '{operator_name}' não encontrado na suite.")
            return False

    # ========================================================================
    #   OPERADORES TÉCNICOS
    #   Definem parâmetros de execução com validação robusta.
    # ========================================================================

    def set_camera_package(self, pso: ProjectStateObject, camera: str, lens: str, **kwargs) -> bool:
        """Define o pacote de câmara e lente, validando rigorosamente contra a KB."""
        
        # Validação (Refatorada v26.0) - Usa o KnowledgeBroker melhorado.
        path_cameras = "10.0_Technical_Execution_Ontology.10.1_Digital_Cinema_Cameras"
        path_lenses = "10.0_Technical_Execution_Ontology.10.2_Lenses_and_Optics"

        if not self.broker.validate_entry(path_cameras, camera):
            print(f"❌ ERRO: Câmara '{camera}' inválida ou não encontrada na Ontologia Técnica.")
            return False
            
        if not self.broker.validate_entry(path_lenses, lens):
            print(f"❌ ERRO: Lente '{lens}' inválida ou não encontrada na Ontologia Técnica.")
            return False
       
        # Aplicação ao PSO
        pso.camera_package["camera"] = camera
        pso.camera_package["lens"] = lens
        pso.reasoning_chain.append(f"Pacote de Câmara: {camera} + {lens}")

        # Inferência de Formato
        if "Anamorphic" in lens:
            pso.camera_package["format"] = "Anamorphic 2.39:1"

        return True

    def build_lighting_setup(self, pso: ProjectStateObject, style: str, key_light: str, modifiers: Optional[List[str]] = None, **kwargs) -> bool:
        """Constrói um setup de iluminação detalhado, validando o equipamento."""
        
        # Validação (Refatorada v26.0)
        path_lights = "10.0_Technical_Execution_Ontology.10.3_Professional_Lighting_Systems"
        path_modifiers = "10.0_Technical_Execution_Ontology.10.3_Professional_Lighting_Systems.Modifiers"
        
        if not self.broker.validate_entry(path_lights, key_light):
            print(f"❌ ERRO: Luz principal '{key_light}' inválida ou não encontrada na Ontologia Técnica.")
            return False

        valid_modifiers = []
        if modifiers:
            for mod in modifiers:
                if self.broker.validate_entry(path_modifiers, mod):
                    valid_modifiers.append(mod)
                else:
                    print(f"⚠️ AVISO: Modificador '{mod}' não encontrado. A ignorar este modificador.")

        # Aplicação ao PSO
        pso.lighting_setup["style"] = style
        pso.lighting_setup["key_light"] = key_light
        pso.lighting_setup["modifiers"] = valid_modifiers
        pso.reasoning_chain.append(f"Setup de Iluminação: {style}")

        return True

    def define_camera_movement(self, pso: ProjectStateObject, rig_model: str, movement: str, **kwargs) -> bool:
        """Define o movimento da câmara e o equipamento de estabilização."""

        # Validação (Refatorada v26.0)
        path_support = "10.0_Technical_Execution_Ontology.10.4_Camera_Support_and_Stabilization"

        if not self.broker.validate_entry(path_support, rig_model):
             print(f"❌ ERRO: Equipamento '{rig_model}' inválido ou não encontrado na Ontologia.")
             return False
       
        # Aplicação ao PSO
        pso.stabilization_rig["model"] = rig_model
        pso.stabilization_rig["movement"] = movement
        pso.reasoning_chain.append(f"Movimento: {movement} com {rig_model}")
        
        # Inferência de Tipo (Simplificada)
        if "DJI" in rig_model or "Gimbal" in rig_model:
             pso.stabilization_rig["type"] = "Gimbal"
        
        return True

    # ========================================================================
    #   OPERADORES DE FLUXO DE TRABALHO (WORKFLOWS)
    #   Guiam o processo criativo. Desacoplados da UI (v26.0).
    # ========================================================================

    def Workflow_Art_Direction(self, pso: ProjectStateObject, inputs: Dict[str, str], **kwargs) -> bool:
        """
        Preenche um WSO. Recebe inputs como parâmetros (agnóstico de UI).
        inputs: Dicionário contendo 'world_name', 'mood', 'stylization'.
        """
        print("\n🎨: A iniciar a criação de um Guia de Estilo para o Mundo (WSO)...")
        
        world_name = inputs.get("world_name")
        mood = inputs.get("mood")
        stylization = inputs.get("stylization")

        if not world_name or not mood or not stylization:
            print("❌ ERRO: Inputs incompletos para Workflow_Art_Direction.")
            return False

        wso = WorldStateObject(world_name)
        wso.aesthetic_laws['mood'] = mood
        wso.aesthetic_laws['stylization_level'] = stylization

        pso.world_state = wso
        pso.reasoning_chain.append(f"Direção de Arte definida: '{world_name}'")
        
        return True

    # Outros operadores estratégicos (e.g., Workflow_Speculative_Design) seguiriam o mesmo padrão desacoplado.