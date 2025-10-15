# nexus/engines/imtl.py

from nexus.core.models import ProjectStateObject
from nexus.core.knowledge_broker import KnowledgeBroker

class IMTLPolicyEngine:
    """
    Pilar I.2: O Motor de Políticas (IMTL).
    Aplica políticas retóricas para traduzir o PSO em prompts otimizados.
    """
    def __init__(self, broker: KnowledgeBroker):
        self.broker = broker

    def translate(self, pso: ProjectStateObject, target_model: str) -> str:
        print(f"🗣️: IMTL ativado. Aplicando política para: {target_model}...")

        policy_method_name = f"_policy_{target_model.lower().replace('-', '_')}"
        policy_method = getattr(self, policy_method_name, self._policy_default)
       
        prompt = policy_method(pso)
        return prompt.strip().replace("  ", " ").replace(" .", ".").replace(" ,", ",")

    # --- Helpers ---
    def _get_style(self, pso: ProjectStateObject) -> str:
        style_parts = []
        if pso.visual_style:
            style_parts.append(pso.visual_style)
        if pso.master_references:
            style_parts.append(f"in the style of {', '.join(pso.master_references)}")
        return ", ".join(style_parts)

    def _get_technical(self, pso: ProjectStateObject) -> str:
        parts = []
        if pso.camera_package.get("camera"):
            parts.append(f"shot on {pso.camera_package['camera']}")
        # Inclui Artefatos de Processo Físico (Pilar II.2)
        if pso.process_artifacts:
            parts.append(", ".join(pso.process_artifacts))
        return ", ".join(parts)

    # --- Políticas Retóricas ---

    def _policy_default(self, pso: ProjectStateObject) -> str:
        parts = [pso.core_concept, self._get_style(pso), pso.emotional_intent, self._get_technical(pso)]
        return ", ".join(filter(None, parts))

    def _policy_dall_e_3(self, pso: ProjectStateObject) -> str:
        """Política: Descrição Literária."""
        narrative = f"A detailed image depicting: {pso.core_concept}. "
        
        style = self._get_style(pso)
        if style:
             narrative += f"The aesthetic style is {style}. "

        if pso.emotional_intent:
            narrative += f"The atmosphere is charged with a feeling of {pso.emotional_intent}. "

        # Tradução da Composição Abstrata para Narrativa (Conforme White Paper)
        if pso.composition and "spiral_inward" in pso.composition:
                narrative += "The scene is composed with a swirling vortex of elements that naturally draws the viewer's gaze inward. "
        elif pso.composition:
             narrative += f"Composition guidelines: {pso.composition}. "
        
        tech = self._get_technical(pso)
        if tech:
            # Inclui artefatos e detalhes técnicos
            narrative += f"Visual characteristics and fidelity details: {tech}. "

        return narrative

    def _policy_midjourney_v6(self, pso: ProjectStateObject) -> str:
        """Política: Instrução Artística Poética."""
        prompt_parts = [pso.core_concept, pso.emotional_intent]
       
        style = self._get_style(pso)
        if style:
            prompt_parts.append(style)

        # Tradução da Composição Abstrata para Poética (Conforme White Paper)
        if pso.composition and "spiral_inward" in pso.composition:
                prompt_parts.append("dynamic swirling composition leading the eye to the center")
        elif pso.composition and "symmetrical_balance" in pso.composition:
                prompt_parts.append("perfect symmetry, stable composition")

        tech = self._get_technical(pso)
        if tech:
            prompt_parts.append(tech)

        prompt = ", ".join(filter(None, prompt_parts))
        return f"{prompt} --ar 16:9 --style raw --v 6.0"

    def _policy_stable_diffusion_3(self, pso: ProjectStateObject) -> str:
        """Política: Receita Técnica."""
        subject = f"Subject: {pso.core_concept}."
        style = f"Style: {self._get_style(pso)}. Tone: {pso.emotional_intent}."
        
        # Tradução da Composição Abstrata para Técnica (Conforme White Paper)
        composition_str = 'balanced'
        if pso.composition and "spiral_inward" in pso.composition:
            composition_str = "(swirl:1.2), (leading lines:1.1), centered focus"
        elif pso.composition and "symmetrical_balance" in pso.composition:
            composition_str = "(symmetry:1.3), centered, stable"

        composition = f"Composition: {composition_str}."
        technical = f"Technical: {self._get_technical(pso)}." if self._get_technical(pso) else ""

        return f"{subject} {style} {composition} {technical}"