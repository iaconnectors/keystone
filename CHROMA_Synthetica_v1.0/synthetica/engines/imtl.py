# synthetica/engines/imtl.py

from synthetica.core.models import ProjectStateObject
from synthetica.core.knowledge_broker import KnowledgeBroker

class IMTLPolicyEngine:
    # (init e translate permanecem iguais)
    def __init__(self, broker: KnowledgeBroker):
        self.broker = broker

    def translate(self, pso: ProjectStateObject, target_model: str) -> str:
        policy_method_name = f"_policy_{target_model.lower().replace('-', '_')}"
        policy_method = getattr(self, policy_method_name, self._policy_default)
        prompt = policy_method(pso)
        # Limpeza final: Remove underscores extras que podem vir da KB
        return prompt.strip().replace('_', ' ')

    # --- Helpers (Atualizado v1.1) ---
    def _get_style(self, pso: ProjectStateObject) -> str:
        style_parts = []
        if pso.master_references:
            # O IMTL formata os nomes dos mestres (e.g., Ganesh_Pyne -> Ganesh Pyne)
            style_parts.append(f"in the style of {', '.join(pso.master_references)}")
        
        # (v1.1) Adiciona os keywords de estilo derivados da Matriz ou Antropofagia
        if pso.visual_style_keywords:
            style_parts.append(", ".join(pso.visual_style_keywords))
            
        return ", ".join(style_parts)

    def _get_technical(self, pso: ProjectStateObject) -> str:
        # (Permanece igual)
        parts = []
        if pso.camera_package.get("camera"):
            cam_str = f"shot on {pso.camera_package['camera']}"
            parts.append(cam_str)
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
        
        # (v1.1) O _get_style agora inclui Mestres e Keywords de Estilo
        style = self._get_style(pso)
        if style:
             # A linguagem é ajustada para soar mais natural.
             narrative += f"The aesthetic style, mood, and influences include: {style}. "
        
        if pso.composition:
             narrative += f"Composition guidelines: {pso.composition}. "
        
        tech = self._get_technical(pso)
        if tech:
            narrative += f"Visual characteristics: {tech}. "

        return narrative