"""Simulated autonomous curator workflow for CHROMA Synthetica."""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from synthetica.services.git_service import GitService


class AutonomousCurator:
    """Implements the Scout -> Analyst -> Curator -> Integrator loop."""

    def __init__(self) -> None:
        self.git_service = GitService()
        self.kb_file_path = "kb/synthetica_kb_v1.1.json"

    def run_cycle(self) -> None:
        print("\n--- Iniciando ciclo de curadoria autonoma (Epico 2) ---")

        raw_data = self.agent_scout()
        kb_patch, analysis_summary = self.agent_analyst(raw_data)

        validation_report = self.agent_curator(kb_patch)
        if validation_report.get("status") != "SUCCESS":
            print("Curadoria falhou. Encerrando ciclo.")
            return

        self.agent_integrator(kb_patch, analysis_summary, validation_report, raw_data)

    # --- Agents (simulated) -------------------------------------------------

    def agent_scout(self) -> Dict[str, Any]:
        print("[Scout] Capturando informacoes de fontes externas simuladas...")
        return {
            "source_type": "Blog Post",
            "source_url": "http://ai-blog.com/sd4-launch",
            "content": (
                "Stable Diffusion 4 (SD4) launched. Preferred rhetoric is "
                "'Direct Visual Instruction'."
            ),
        }

    def agent_analyst(self, raw_data: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
        print("[Analyst] Interpretando dados coletados (LLM simulado)...")

        patch = {
            (
                "7.0_Model_Translation_Layer_Profiles."
                "Model_Capability_Profiles.Stable_Diffusion_4"
            ): {"Rhetoric": "Direct Visual Instruction"}
        }
        summary = (
            "Identificado novo modelo SD4. Retorica predominante: "
            "'Direct Visual Instruction'."
        )
        return patch, summary

    def agent_curator(self, kb_patch: Dict[str, Any]) -> Dict[str, Any]:
        print("[Curator] Validando patch contra pipeline de QA simulado...")
        _ = kb_patch  # Placeholder for future validations.
        return {
            "status": "SUCCESS",
            "tests_passed": [
                "Schema Validation",
                "Ontological Consistency",
                "Semantic Redundancy Check",
            ],
        }

    def agent_integrator(
        self,
        kb_patch: Dict[str, Any],
        summary: str,
        validation_report: Dict[str, Any],
        raw_data: Dict[str, Any],
    ) -> None:
        print("[Integrator] Preparando alteracoes para commit e PR...")

        patch_json = json.dumps(kb_patch, indent=2, ensure_ascii=False)
        print(f"  Patch sugerido:\n{patch_json}")

        commit_title = "feat(KB): Add Stable Diffusion 4 profile (autonomous)"
        pr_body = self.generate_pr_description(kb_patch, summary, validation_report, raw_data)

        branch_name = self.git_service.create_feature_branch()
        print(f"  Aplicando patch ao arquivo local: {self.kb_file_path}...")

        self.git_service.commit_changes(self.kb_file_path, commit_title, branch_name)
        self.git_service.create_pull_request(commit_title, pr_body, branch_name)

    def generate_pr_description(
        self,
        patch: Dict[str, Any],
        summary: str,
        report: Dict[str, Any],
        raw_data: Dict[str, Any],
    ) -> str:
        """Build a pull-request body consistent with pillar II.1 template."""

        highlights = "Adiciona novo perfil para Stable Diffusion 4."
        diff_summary = "Inclui retorica 'Direct Visual Instruction' no perfil SD4."

        patch_section = json.dumps(patch, indent=2, ensure_ascii=False)

        template = f"""
## Fonte da Atualizacao
* Tipo: {raw_data['source_type']}
* Link: {raw_data['source_url']}

## Sumario do Analista (IA)
{summary}

## Resumo do Diff (IA)
{diff_summary}

## Destaques Criticos para Revisao
{highlights}

## Relatorio do Curador (CI/CD)
* Status: {report['status']}
* Testes: {', '.join(report.get('tests_passed', []))}

## Patch sugerido
```
{patch_section}
```
"""
        return template.strip()


if __name__ == "__main__":
    curator = AutonomousCurator()
    curator.run_cycle()
