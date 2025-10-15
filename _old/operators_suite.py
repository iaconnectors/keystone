# operators_suite.py

from core_architecture import KeystoneCHROMA, ProjectStateObject, WorldStateObject, KnowledgeBroker
from typing import List, Optional, Dict

class GenerativeOperatorsSuite:
    """
    Representa a '4.0_Creative_Operators_and_Engines'.
    (v27.0: Utiliza o KnowledgeBroker otimizado com Busca Fuzzy para validação resiliente).
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
    # ========================================================================

    def set_camera_package(self, pso: ProjectStateObject, camera: str, lens: str, **kwargs) -> bool:
        """Define o pacote de câmara e lente, validando (com Fuzzy Match) contra a KB."""
        
        # Caminhos atualizados para a KB v27.0 (onde a estrutura foi ligeiramente ajustada)
        path_cameras = "10.0_Technical_Execution_Ontology.10.1_Cameras"
        path_lenses = "10.0_Technical_Execution_Ontology.10.2_Lenses_and_Optics"

        # (v27.0) Validação aprimorada com Fuzzy Match como fallback (Cutoff 0.7 para alta confiança)
        if not self.broker.validate_entry(path_cameras, camera):
            closest_camera = self.broker.find_closest_match(path_cameras, camera, cutoff=0.7)
            if closest_camera:
                print(f"⚠️ AVISO: Câmara exata '{camera}' não encontrada. A utilizar correspondência mais próxima: '{closest_camera}'.")
                camera = closest_camera
            else:
                print(f"❌ ERRO: Câmara '{camera}' inválida e nenhuma correspondência próxima encontrada.")
                return False
            
        if not self.broker.validate_entry(path_lenses, lens):
            closest_lens = self.broker.find_closest_match(path_lenses, lens, cutoff=0.7)
            if closest_lens:
                print(f"⚠️ AVISO: Lente exata '{lens}' não encontrada. A utilizar correspondência mais próxima: '{closest_lens}'.")
                lens = closest_lens
            else:
                print(f"❌ ERRO: Lente '{lens}' inválida e nenhuma correspondência próxima encontrada.")
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
        """Constrói um setup de iluminação detalhado."""
        
        path_lights = "10.0_Technical_Execution_Ontology.10.3_Professional_Lighting_Systems"
        path_modifiers = "10.0_Technical_Execution_Ontology.10.3_Professional_Lighting_Systems.Modifiers"
        
        # (v27.0) Validação aprimorada com Fuzzy Match, mas permitindo termos genéricos.
        if not self.broker.validate_entry(path_lights, key_light):
            closest_light = self.broker.find_closest_match(path_lights, key_light, cutoff=0.7)
            if closest_light:
                 print(f"⚠️ AVISO: Luz exata '{key_light}' não encontrada. A utilizar correspondência mais próxima: '{closest_light}'.")
                 key_light = closest_light
            else:
                # Permitir luzes não listadas (e.g., "Luz Solar") mas emitir aviso
                print(f"⚠️ AVISO: Luz principal '{key_light}' não encontrada na Ontologia Técnica. A prosseguir sem validação estrita.")

        valid_modifiers = []
        if modifiers:
            for mod in modifiers:
                if self.broker.validate_entry(path_modifiers, mod):
                    valid_modifiers.append(mod)
                else:
                    # Tentativa de fuzzy match para modificadores
                    closest_mod = self.broker.find_closest_match(path_modifiers, mod, cutoff=0.7)
                    if closest_mod:
                        valid_modifiers.append(closest_mod)
                        print(f"⚠️ AVISO: Modificador '{mod}' não encontrado. Usando: '{closest_mod}'.")
                    else:
                        print(f"⚠️ AVISO: Modificador '{mod}' não encontrado. A ignorar.")

        # Aplicação ao PSO
        pso.lighting_setup["style"] = style
        pso.lighting_setup["key_light"] = key_light
        pso.lighting_setup["modifiers"] = valid_modifiers
        pso.reasoning_chain.append(f"Setup de Iluminação: {style}")

        # (v27.0) Processamento de fenômenos (se passado via kwargs)
        phenomena = kwargs.get("phenomena")
        if phenomena and isinstance(phenomena, list):
            pso.lighting_setup["phenomena"] = phenomena
            pso.reasoning_chain.append(f"Fenômenos Ópticos: {', '.join(phenomena)}")

        return True

    def define_camera_movement(self, pso: ProjectStateObject, rig_model: str, movement: str, **kwargs) -> bool:
        """Define o movimento da câmara e o equipamento de estabilização."""

        path_support = "10.0_Technical_Execution_Ontology.10.4_Camera_Support_and_Stabilization"

        # (v27.0) Validação aprimorada com Fuzzy Match como fallback
        if not self.broker.validate_entry(path_support, rig_model):
            closest_rig = self.broker.find_closest_match(path_support, rig_model, cutoff=0.7)
            if closest_rig:
                 print(f"⚠️ AVISO: Equipamento exato '{rig_model}' não encontrado. A utilizar correspondência mais próxima: '{closest_rig}'.")
                 rig_model = closest_rig
            else:
                print(f"❌ ERRO: Equipamento '{rig_model}' inválido e nenhuma correspondência próxima encontrada.")
                return False
       
        # Aplicação ao PSO
        pso.stabilization_rig["model"] = rig_model
        pso.stabilization_rig["movement"] = movement
        pso.reasoning_chain.append(f"Movimento: {movement} com {rig_model}")
        
        return True

    # ========================================================================
    #   OPERADORES DE FLUXO DE TRABALHO (WORKFLOWS)
    # ========================================================================

    def Workflow_Art_Direction(self, pso: ProjectStateObject, inputs: Dict[str, str], **kwargs) -> bool:
        """
        Preenche um WSO. Recebe inputs como parâmetros (agnóstico de UI).
        """
        print("\n🎨: A iniciar a criação de um Guia de Estilo para o Mundo (WSO)...")
        
        world_name = inputs.get("world_name")
        mood = inputs.get("mood")
        stylization = inputs.get("stylization")
        architectural_style = inputs.get("architectural_style") # (v27.0)

        if not world_name or not mood or not stylization:
            print("❌ ERRO: Inputs incompletos para Workflow_Art_Direction.")
            return False

        wso = WorldStateObject(world_name)
        wso.aesthetic_laws['mood'] = mood
        wso.aesthetic_laws['stylization_level'] = stylization

        if architectural_style:
             wso.aesthetic_laws['architectural_style'] = architectural_style

        pso.world_state = wso
        pso.reasoning_chain.append(f"Direção de Arte definida: '{world_name}'")
        
        return True