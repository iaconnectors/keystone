# synthetica/engines/imtl.py

# (Synthetica v1.0: Portado do Nexus 1.0 sem alterações funcionais significativas)

from synthetica.core.models import ProjectStateObject
from synthetica.core.knowledge_broker import KnowledgeBroker

class IMTLPolicyEngine:
    """
    Motor de Políticas (IMTL).
    """
    def __init__(self, broker: KnowledgeBroker):
        # Usa o Nexus Broker para perfis retóricos
        self.broker = broker

    def translate(self, pso: ProjectStateObject, target_model: str) -> str:
        # print(f"🗣️: IMTL ativado. Aplicando política para: {target_model}...")

        policy_method_name = f"_policy_{target_model.lower().replace('-', '_')}"
        policy_method = getattr(self, policy_method_name, self._policy_default)
       
        prompt = policy_method(pso)
        return prompt.strip()

    # --- Helpers ---
    def _get_style(self, pso: ProjectStateObject) -> str:
        style_parts = []
        if pso.master_references:
            style_parts.append(f"in the style of {', '.join(pso.master_references)}")
        return ", ".join(style_parts)

    def _get_technical(self, pso: ProjectStateObject) -> str:
        parts = []
        if pso.camera_package.get("camera"):
            cam_str = f"shot on {pso.camera_package['camera']}"
            if pso.camera_package.get("lens"):
                cam_str += f" with {pso.camera_package['lens']} lens"
            parts.append(cam_str)
            
        # Inclui Artefatos de Processo Físico
        if pso.process_artifacts:
            parts.append(", ".join(pso.process_artifacts))
        return ", ".join(parts)

    # --- Políticas Retóricas ---

    def _policy_default(self, pso: ProjectStateObject) -> str:
        parts = [pso.core_concept, self._get_style(pso), self._get_technical(pso)]
        return ", ".join(filter(None, parts))

    def _policy_dall_e_3(self, pso: ProjectStateObject) -> str:
        """Política: Descrição Literária."""
        narrative = f"A detailed visualization depicting: {pso.core_concept}. "
        
        style = self._get_style(pso)
        if style:
             narrative += f"The aesthetic style is {style}. "
        
        if pso.composition and "symmetrical_balance" in pso.composition:
                narrative += "The scene is composed with perfect symmetry, conveying stability and formal order. "
        
        tech = self._get_technical(pso)
        if tech:
            narrative += f"Visual characteristics and fidelity details: {tech}. "

        return narrative