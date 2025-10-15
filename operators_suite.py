# operators_suite.py

from core_architecture import KeystoneCHROMA, ProjectStateObject, WorldStateObject
from typing import List

class GenerativeOperatorsSuite:
    """
    Representa a '4.0_Creative_Operators_and_Engines'. Cada método é um operador
    que modifica o ProjectStateObject (PSO), aplicando conhecimento da KB.
    """
    def __init__(self, system_instance: KeystoneCHROMA):
        self.system = system_instance
        self.broker = system_instance.broker

    def apply_operator(self, operator_name: str, pso: ProjectStateObject, **kwargs):
        """Método de gateway para aplicar operadores de forma segura."""
        if hasattr(self, operator_name):
            print(f": Ativando operador: {operator_name}")
            pso.activated_operators.append(operator_name)
            # Chama o método do operador correspondente
            getattr(self, operator_name)(pso, **kwargs)
        else:
            print(f": AVISO: Operador '{operator_name}' não encontrado na suite.")

    # --- OPERADORES DE FLUXO DE TRABALHO ---

    def Workflow_Speculative_Design(self, pso: ProjectStateObject):
        """
        Guia o utilizador através de um processo de design especulativo.
        """
        print("\n: A iniciar diálogo socrático para Design Especulativo...")

        q1 = "Sobre que tendência social ou tecnológica emergente gostaria de especular?"
        trend = input(f": {q1} ")
        pso.reasoning_chain.append(f"Especulação sobre '{trend}'")

        q2 = f"Vamos imaginar um futuro em 2050 onde '{trend}' se tornou dominante. Quais são as implicações para a vida quotidiana?"
        implications = input(f": {q2} ")
        pso.reasoning_chain.append(f"Cenário: {implications}")

        q3 = "Que 'artefato do futuro' provocador poderia existir neste mundo que encapsule as suas tensões?"
        artifact = input(f": {q3} ")
        pso.core_concept = f"Um artefato do futuro: {artifact}, num mundo dominado por '{trend}'. {implications}"
        print(": Conceito central do PSO atualizado com o artefato especulativo.")

    def Workflow_Art_Direction(self, pso: ProjectStateObject):
        """
        Preenche um WorldStateObject (WSO) para garantir consistência visual.
        """
        print("\n: A iniciar a criação de um Guia de Estilo para o Mundo...")
        world_name = input(": Qual é o nome deste universo? ")
        wso = WorldStateObject(world_name)

        mood = input(": Qual é a intenção emocional primária? (ex: melancolia, otimismo) ")
        wso.aesthetic_laws['mood'] = mood

        stylization = input(": Qual o nível de estilização? (ex: realista, cartoon, pictórico) ")
        wso.aesthetic_laws['stylization_level'] = stylization

        pso.world_state = wso
        pso.reasoning_chain.append(f"Direção de Arte definida para '{world_name}'")
        print(f": World State Object '{world_name}' criado e associado ao PSO.")

    # --- OPERADORES ESTRATÉGICOS ---

    def Abstraction_Intent_Selector(self, pso: ProjectStateObject):
        """
        Clarifica a intenção do utilizador para a arte abstrata.
        """
        print("\n: A definir a intenção da abstração...")
        anadol_path = "5.0_Masters_Lexicon.5.3_Art_and_Design_References.Digital_and_Bio_Artists"
        bass_path = "5.0_Masters_Lexicon.5.3_Art_and_Design_References.Designers_and_Illustrators"
        
        anadol_exists = "Refik_Anadol" in self.broker.get_entry(anadol_path,)
        bass_exists = "Saul_Bass" in self.broker.get_entry(bass_path,)
        
        if not anadol_exists or not bass_exists:
            print(": AVISO: Mestres de referência para abstração não encontrados na KB.")
            return

        print("  A. Abstração Guiada por Dados (estilo Refik Anadol)")
        print("  B. Abstração Guiada pela Emoção (estilo Saul Bass)")
        choice = input(": Qual caminho exploratório seguimos? (A/B) ")

        if choice.upper() == 'A':
            pso.master_references.append("Refik_Anadol")
            pso.reasoning_chain.append("Intenção: Abstração de Dados")
            pso.visual_style = "Pintura de dados fluida, baseada em partículas, com cores vibrantes e movimento dinâmico."
        else:
            pso.master_references.append("Saul_Bass")
            pso.reasoning_chain.append("Intenção: Abstração de Emoção")
            pso.visual_style = "Composição gráfica minimalista com formas de recorte e tipografia cinética para simbolizar uma ideia."

    # --- NOVOS OPERADORES TÉCNICOS (v25.1) ---

    def set_camera_package(self, pso: ProjectStateObject, camera: str, lens: str):
        """Define o pacote de câmara e lente, validando contra a KB."""
        pso.reasoning_chain.append(f"Seleção de Pacote de Câmara: {camera} + {lens}")
        
        # Validação (exemplo simplificado)
        all_cameras =
        cam_dict = self.broker.get_entry("10.0_Technical_Execution_Ontology.10.1_Digital_Cinema_Cameras", {})
        for brand_list in cam_dict.values():
            all_cameras.extend(brand_list)
            
        if camera not in all_cameras:
            print(f": AVISO: Câmara '{camera}' não encontrada na ontologia técnica.")
        
        pso.camera_package["camera"] = camera
        pso.camera_package["lens"] = lens
        print(f": Pacote de câmara definido: {camera} com lente {lens}.")

    def build_lighting_setup(self, pso: ProjectStateObject, style: str, key_light: str, modifiers: List[str] =):
        """Constrói um setup de iluminação detalhado."""
        pso.reasoning_chain.append(f"Construção de Iluminação: Estilo {style}")
        
        # Validação (exemplo simplificado)
        all_lights =
        light_dict = self.broker.get_entry("10.0_Technical_Execution_Ontology.10.3_Professional_Lighting_Systems", {})
        for brand in light_dict.values():
            if isinstance(brand, dict):
                for type_list in brand.values():
                    all_lights.extend(type_list)
        
        if key_light not in all_lights:
            print(f": AVISO: Luz principal '{key_light}' não encontrada na ontologia técnica.")

        pso.lighting_setup["style"] = style
        pso.lighting_setup["key_light"] = key_light
        pso.lighting_setup["modifiers"] = modifiers
        print(f": Setup de iluminação definido. Estilo: {style}, Key: {key_light}, Modificadores: {', '.join(modifiers)}.")

    def define_camera_movement(self, pso: ProjectStateObject, rig_model: str, movement: str):
        """Define o movimento da câmara e o equipamento de estabilização."""
        pso.reasoning_chain.append(f"Definição de Movimento: {movement} com {rig_model}")

        # Validação (exemplo simplificado)
        all_rigs =
        rig_dict = self.broker.get_entry("10.0_Technical_Execution_Ontology.10.4_Camera_Support_and_Stabilization.Gimbals", {})
        for category_list in rig_dict.values():
            all_rigs.extend(category_list)

        if rig_model not in all_rigs:
            print(f": AVISO: Equipamento de estabilização '{rig_model}' não encontrado na ontologia.")
        
        pso.stabilization_rig["model"] = rig_model
        pso.stabilization_rig["movement"] = movement
        pso.stabilization_rig["type"] = "Gimbal" # Inferência simplificada
        print(f": Movimento de câmara definido: {movement} utilizando {rig_model}.")