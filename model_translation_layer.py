# model_translation_layer.py

from core_architecture import ProjectStateObject, KnowledgeBroker
from typing import List

class ModelTranslationLayer:
    """
    Implementação do Pilar 1: A Transição da Sintaxe para a Retórica.
    Funciona como um compilador que traduz o PSO (uma DSL de cinematografia)
    para a 'linguagem' preferida de cada modelo de IA.
    """
    def __init__(self, broker: KnowledgeBroker):
        self.broker = broker
        self.profiles = self.broker.get_entry("7.0_Model_Translation_Layer_Profiles.Model_Capability_Profiles", {})

    def translate(self, pso: ProjectStateObject, target_model: str) -> str:
        """
        Método principal que direciona para a lógica de tradução específica do modelo.
        """
        translation_method_name = f"_translate_for_{target_model.lower().replace('-', '_')}"
        translation_method = getattr(self, translation_method_name, self._translate_default)
        
        return translation_method(pso)

    def _translate_default(self, pso: ProjectStateObject) -> str:
        """Fallback para modelos não suportados explicitamente."""
        return f"Modelo alvo '{pso.target_model}' não suportado. Conceito central: {pso.core_concept}"

    # --- Funções de Apoio à Tradução ---

    def _get_master_style(self, pso: ProjectStateObject) -> str:
        if pso.master_references:
            return f"no estilo de {', '.join(pso.master_references)}"
        return ""

    def _get_technical_package_string(self, pso: ProjectStateObject) -> str:
        """Gera uma string concisa com as especificações técnicas."""
        parts =
        if pso.camera_package.get("camera"):
            parts.append(f"shot on {pso.camera_package['camera']}")
        if pso.camera_package.get("lens"):
            parts.append(f"with {pso.camera_package['lens']} lens")
        if pso.stabilization_rig.get("model"):
            parts.append(f"using a {pso.stabilization_rig['model']} for a {pso.stabilization_rig.get('movement', 'smooth')} shot")
        
        return ", ".join(parts)
        
    def _get_lighting_string(self, pso: ProjectStateObject) -> str:
        """Gera uma string descritiva para a iluminação."""
        parts =
        if pso.lighting_setup.get("style"):
            parts.append(pso.lighting_setup["style"])
        if pso.lighting_setup.get("key_light"):
            key_str = f"key light from {pso.lighting_setup['key_light']}"
            if pso.lighting_setup.get("modifiers"):
                key_str += f" with {', '.join(pso.lighting_setup['modifiers'])}"
            parts.append(key_str)

        return ", ".join(parts)

    # --- Estratégias de Tradução Específicas do Modelo ---

    def _translate_for_dall_e_3(self, pso: ProjectStateObject) -> str:
        """Retórica: Descrição Literária."""
        narrative = f"Uma imagem detalhada e cinematográfica de {pso.core_concept}. "
        narrative += f"A atmosfera é carregada de {pso.emotional_intent}. "

        master_style = self._get_master_style(pso)
        if master_style:
            narrative += f"A obra deve ser criada {master_style}. "
        
        tech_package = self._get_technical_package_string(pso)
        if tech_package:
            narrative += f"A imagem deve ter a qualidade visual de ter sido {tech_package}. "
            
        lighting = self._get_lighting_string(pso)
        if lighting:
            narrative += f"A cena é iluminada com um setup dramático: {lighting}. "

        return narrative.strip().replace("  ", " ")

    def _translate_for_midjourney_v6(self, pso: ProjectStateObject) -> str:
        """Retórica: Instrução Artística Poética."""
        prompt_parts = [pso.core_concept, pso.emotional_intent]
        
        if pso.visual_style:
            prompt_parts.append(pso.visual_style)
            
        lighting = self._get_lighting_string(pso)
        if lighting:
            prompt_parts.append(lighting)

        tech_package = self._get_technical_package_string(pso)
        if tech_package:
            prompt_parts.append(tech_package)
        
        prompt = ", ".join(filter(None, prompt_parts))

        params =
        if pso.master_references:
            # Em um sistema real, isso seria um URL de imagem de referência
            # params.append(f"--sref <url_da_imagem_de_{pso.master_references}>")
            prompt += f", in the style of {', '.join(pso.master_references)}"

        params.append("--ar 16:9")
        params.append("--style raw")
        params.append("--v 6.0")

        return f"{prompt} {' '.join(params)}"

    def _translate_for_stable_diffusion_3(self, pso: ProjectStateObject) -> str:
        """Retórica: Receita Técnica."""
        style = f"Style: {self._get_master_style(pso)}, {pso.visual_style}, {pso.emotional_intent}."
        subject = f"Subject: {pso.core_concept}."
        composition = f"Composition: {pso.composition if pso.composition else 'balanced composition'}."
        lighting = f"Lighting: {self._get_lighting_string(pso) if self._get_lighting_string(pso) else 'natural lighting'}."
        technical = f"Technical: {self._get_technical_package_string(pso) if self._get_technical_package_string(pso) else 'standard digital photo'}."

        return f"{style} {subject} {composition} {lighting} {technical}"

    def _translate_for_flux_1_kontext(self, pso: ProjectStateObject) -> str:
        """Retórica: Instrução Estruturada e Contextual."""
        prompt = f"Primary subject: {pso.core_concept}. "
        prompt += f"Artistic style: {self._get_master_style(pso)}, {pso.visual_style}. "
        prompt += f"Emotional context: {pso.emotional_intent}. "
        prompt += f"Technical specifications: {self._get_technical_package_string(pso)}. "
        prompt += f"Lighting setup: {self._get_lighting_string(pso)}."
        return prompt.strip().replace("  ", " ")

    def _translate_for_nano_banana(self, pso: ProjectStateObject) -> str:
        """Retórica: Edição Conversacional e Iterativa."""
        commands = [f"Gere uma imagem de: {pso.core_concept}."]
        
        if pso.master_references:
            commands.append(f"Agora, aplique o estilo de {', '.join(pso.master_references)}.")
        
        lighting = self._get_lighting_string(pso)
        if lighting:
            commands.append(f"Mude a iluminação para ser: {lighting}.")
            
        tech = self._get_technical_package_string(pso)
        if tech:
            commands.append(f"Ajuste a imagem para parecer que foi {tech}.")
            
        commands.append(f"Faça a cena parecer mais {pso.emotional_intent}.")

        return " -> ".join(commands)

    def _translate_for_seedream_4_0(self, pso: ProjectStateObject) -> str:
        """Retórica: Instrução Multimodal Detalhada."""
        prompt = f"Um shot de alta fidelidade de {pso.core_concept}. "
        prompt += f"Estilo: {self._get_master_style(pso)}, {pso.visual_style}. "
        prompt += f"Iluminação: {self._get_lighting_string(pso)}. "
        prompt += f"Especificações da câmara: {self._get_technical_package_string(pso)}. "
        prompt += f"Humor: {pso.emotional_intent}."
        return prompt.strip().replace("  ", " ")