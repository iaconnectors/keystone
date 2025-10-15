# model_translation_layer.py

from core_architecture import ProjectStateObject, KnowledgeBroker
from typing import List

class ModelTranslationLayer:
    """
    Pilar 1: A Transição da Sintaxe para a Retórica.
    Compilador adaptativo que traduz o PSO (DSL interna) para a 'linguagem' de cada modelo de IA.
    """
    def __init__(self, broker: KnowledgeBroker):
        self.broker = broker
        self.profiles = self.broker.get_entry("7.0_Model_Translation_Layer_Profiles.Model_Capability_Profiles", {})

    def translate(self, pso: ProjectStateObject, target_model: str) -> str:
        """
        Método principal de tradução.
        """
        # Normaliza o nome do modelo e seleciona o método de tradução.
        translation_method_name = f"_translate_for_{target_model.lower().replace('-', '_').replace('.', '_')}"
        translation_method = getattr(self, translation_method_name, self._translate_default)
       
        prompt = translation_method(pso)
        
        # Limpeza final do prompt.
        return prompt.strip().replace("  ", " ").replace(" .", ".").replace(" ,", ",")

    def _translate_default(self, pso: ProjectStateObject) -> str:
        """Fallback genérico."""
        parts = [
            pso.core_concept,
            self._get_master_style(pso),
            pso.visual_style,
            pso.emotional_intent,
            self._get_technical_package_string(pso)
        ]
        return ", ".join(filter(None, parts))

    # ========================================================================
    #   FUNÇÕES DE APOIO À TRADUÇÃO (Helpers)
    # ========================================================================

    def _get_master_style(self, pso: ProjectStateObject) -> str:
        if pso.master_references:
            return f"in the style of {', '.join(pso.master_references)}"
        return ""

    def _get_technical_package_string(self, pso: ProjectStateObject) -> str:
        """Gera uma string concisa com as especificações técnicas."""
        parts = []
        if pso.camera_package.get("camera"):
            cam_str = f"shot on {pso.camera_package['camera']}"
            if pso.camera_package.get("lens"):
                cam_str += f" with {pso.camera_package['lens']} lens"
            parts.append(cam_str)
            
        if pso.stabilization_rig.get("model"):
            rig_str = f"using a {pso.stabilization_rig['model']}"
            if pso.stabilization_rig.get('movement'):
                 rig_str += f" for a {pso.stabilization_rig['movement']} shot"
            parts.append(rig_str)
       
        return ", ".join(parts)
       
    def _get_lighting_string(self, pso: ProjectStateObject) -> str:
        """Gera uma string descritiva para a iluminação."""
        parts = []
        if pso.lighting_setup.get("style"):
            parts.append(f"Lighting style: {pso.lighting_setup['style']}")
        
        if pso.lighting_setup.get("key_light"):
            key_str = f"Key light: {pso.lighting_setup['key_light']}"
            if pso.lighting_setup.get("modifiers"):
                key_str += f" modified with {', '.join(pso.lighting_setup['modifiers'])}"
            parts.append(key_str)

        return ". ".join(parts) if parts else ""

    # ========================================================================
    #   ESTRATÉGIAS DE TRADUÇÃO ESPECÍFICAS DO MODELO
    # ========================================================================

    def _translate_for_dall_e_3(self, pso: ProjectStateObject) -> str:
        """Retórica: Descrição Literária."""
        narrative = f"A detailed, cinematic image depicting {pso.core_concept}. "
        
        if pso.emotional_intent:
            narrative += f"The atmosphere is charged with {pso.emotional_intent}. "

        master_style = self._get_master_style(pso)
        if master_style:
            narrative += f"The artwork should evoke the feeling of a piece created {master_style}. "
       
        lighting = self._get_lighting_string(pso)
        if lighting:
            narrative += f"The scene is dramatically illuminated. {lighting}. "

        tech_package = self._get_technical_package_string(pso)
        if tech_package:
            narrative += f"The image must have the visual fidelity and characteristics as if it was {tech_package}. "

        return narrative

    def _translate_for_midjourney_v6(self, pso: ProjectStateObject) -> str:
        """Retórica: Instrução Artística Poética."""
        prompt_parts = [pso.core_concept, pso.emotional_intent]
       
        if pso.visual_style:
            prompt_parts.append(pso.visual_style)
           
        lighting = self._get_lighting_string(pso)
        if lighting:
            # Simplifica para termos mais evocativos
            prompt_parts.append(lighting.replace("Lighting style: ", "").replace("Key light: ", ""))

        tech_package = self._get_technical_package_string(pso)
        if tech_package:
            prompt_parts.append(tech_package)
       
        prompt = ", ".join(filter(None, prompt_parts))

        params = []
        if pso.master_references:
            prompt += f", {self._get_master_style(pso)}"

        # Inferência de Aspect Ratio
        if pso.camera_package.get("format") == "Anamorphic 2.39:1":
             params.append("--ar 2.39:1")
        else:
            params.append("--ar 16:9")
            
        params.append("--style raw")
        params.append("--v 6.0")

        return f"{prompt} {' '.join(params)}"

    def _translate_for_stable_diffusion_3(self, pso: ProjectStateObject) -> str:
        """Retórica: Receita Técnica."""
        style = f"Style: {self._get_master_style(pso)}, {pso.visual_style}. Tone: {pso.emotional_intent}."
        subject = f"Subject: {pso.core_concept}."
        composition = f"Composition: {pso.composition if pso.composition else 'balanced'}."
        lighting = f"Lighting: {self._get_lighting_string(pso) if self._get_lighting_string(pso) else 'natural'}."
        technical = f"Technical: {self._get_technical_package_string(pso) if self._get_technical_package_string(pso) else 'digital photo'}."

        return f"{subject} {style} {composition} {lighting} {technical}"

    # As restantes funções (FLUX, Nano_Banana, Seedream) são mantidas para demonstração da arquitetura.
    
    def _translate_for_flux_1_kontext(self, pso: ProjectStateObject) -> str:
        """Retórica: Instrução Estruturada e Contextual."""
        prompt = f"Primary subject: {pso.core_concept}. "
        prompt += f"Artistic style: {self._get_master_style(pso)}, {pso.visual_style}. "
        prompt += f"Emotional context: {pso.emotional_intent}. "
        prompt += f"Technical look: {self._get_technical_package_string(pso)}. "
        prompt += f"Lighting setup: {self._get_lighting_string(pso)}."
        return prompt

    def _translate_for_nano_banana(self, pso: ProjectStateObject) -> str:
        """Retórica: Edição Conversacional e Iterativa."""
        commands = [f"Generate: {pso.core_concept}."]
        if self._get_master_style(pso):
            commands.append(f"Apply style: {self._get_master_style(pso)}.")
        if self._get_lighting_string(pso):
            commands.append(f"Change lighting: {self._get_lighting_string(pso)}.")
        return " -> ".join(commands)

    def _translate_for_seedream_4_0(self, pso: ProjectStateObject) -> str:
        """Retórica: Instrução Multimodal Detalhada."""
        prompt = f"High fidelity shot of {pso.core_concept}. "
        prompt += f"Style: {self._get_master_style(pso)}. Lighting: {self._get_lighting_string(pso)}. "
        prompt += f"Camera: {self._get_technical_package_string(pso)}. Mood: {pso.emotional_intent}."
        return prompt