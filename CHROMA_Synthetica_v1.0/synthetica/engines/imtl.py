"""Model Translation Layer policies for prompt generation."""

from synthetica.core.models import ProjectStateObject
from synthetica.core.knowledge_broker import KnowledgeBroker


class IMTLPolicyEngine:
    """Selects rhetoric policies per downstream model."""

    def __init__(self, broker: KnowledgeBroker):
        self.broker = broker

    def translate(self, pso: ProjectStateObject, target_model: str) -> str:
        policy_method_name = f"_policy_{target_model.lower().replace('-', '_')}"
        policy_method = getattr(self, policy_method_name, self._policy_default)
        prompt = policy_method(pso)
        return prompt.strip().replace("_", " ")

    # --------------------------------------------------------------------- #
    # Helpers
    # --------------------------------------------------------------------- #
    def _get_style(self, pso: ProjectStateObject) -> str:
        parts = []
        if pso.master_references:
            masters = ", ".join(pso.master_references)
            parts.append(f"in the style of {masters}")
        if pso.visual_style_keywords:
            parts.append(", ".join(pso.visual_style_keywords))
        return ", ".join(parts)

    def _get_technical(self, pso: ProjectStateObject) -> str:
        parts = []
        camera = pso.camera_package.get("camera")
        if camera:
            parts.append(f"shot on {camera}")
        if pso.process_artifacts:
            parts.append(", ".join(pso.process_artifacts))
        return ", ".join(parts)

    # --------------------------------------------------------------------- #
    # Policies
    # --------------------------------------------------------------------- #
    def _policy_default(self, pso: ProjectStateObject) -> str:
        segments = [pso.core_concept, self._get_style(pso), self._get_technical(pso)]
        return ", ".join(seg for seg in segments if seg)

    def _policy_dall_e_3(self, pso: ProjectStateObject) -> str:
        narrative = f"A detailed visualization depicting: {pso.core_concept}. "
        style = self._get_style(pso)
        if style:
            narrative += f"The aesthetic style, mood, and influences include: {style}. "
        if pso.composition:
            narrative += f"Composition guidelines: {pso.composition}. "
        tech = self._get_technical(pso)
        if tech:
            narrative += f"Visual characteristics: {tech}. "
        return narrative

    def _policy_midjourney_v6(self, pso: ProjectStateObject) -> str:
        style = self._get_style(pso)
        tech = self._get_technical(pso)
        segments = [
            f"imagine {pso.core_concept}",
            style and f"evoke {style}",
            pso.composition and f"compose with {pso.composition}",
            tech and f"render with {tech}",
        ]
        poetic_instruction = " -- ".join(seg for seg in segments if seg)
        return poetic_instruction or pso.core_concept

    def _policy_stable_diffusion_3(self, pso: ProjectStateObject) -> str:
        steps = [f"Step 1: Concept - {pso.core_concept}"]
        style = self._get_style(pso)
        if style:
            steps.append(f"Step 2: Aesthetic references - {style}")
        if pso.composition:
            steps.append(f"Step 3: Composition plan - {pso.composition}")
        tech = self._get_technical(pso)
        if tech:
            steps.append(f"Step 4: Technical settings - {tech}")
        steps.append("Step 5: Output - high fidelity render with balanced exposure.")
        return "\n".join(steps)

    def _policy_seedream_4_0(self, pso: ProjectStateObject) -> str:
        style = self._get_style(pso)
        tech = self._get_technical(pso)
        modules = [
            f"Module A - Scenario: {pso.core_concept}",
            style and f"Module B - Visual Language: {style}",
            pso.composition and f"Module C - Blocking: {pso.composition}",
            tech and f"Module D - Capture Specs: {tech}",
            "Module E - Delivery: seamless motion-ready frames.",
        ]
        return "\n".join(mod for mod in modules if mod)

    def _policy_nano_banana(self, pso: ProjectStateObject) -> str:
        style = self._get_style(pso)
        tech = self._get_technical(pso)
        lines = [f"core: {pso.core_concept}"]
        if style:
            lines.append(f"vibe: {style}")
        if pso.composition:
            lines.append(f"frame: {pso.composition}")
        if tech:
            lines.append(f"gear: {tech}")
        lines.append("mood: bold, curious, joyful.")
        return "\n".join(lines)

    def _policy_flux_1(self, pso: ProjectStateObject) -> str:
        style = self._get_style(pso)
        tech = self._get_technical(pso)
        brief = [f"Objective: {pso.core_concept}"]
        if style:
            brief.append(f"Key visuals: {style}")
        if pso.composition:
            brief.append(f"Composition cue: {pso.composition}")
        if tech:
            brief.append(f"Execution notes: {tech}")
        brief.append("Delivery: cinematic, high-impact frames with crisp detailing.")
        return "\n".join(brief)
