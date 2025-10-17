import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from synthetica.core.knowledge_broker import KnowledgeBroker
from synthetica.core.models import AbstractCreativeObject
from synthetica.core.compiler import NexusCompiler
from synthetica.services.enrichment import EnrichmentService
from synthetica.engines.imtl import IMTLPolicyEngine


class ChromaSyntheticaOrchestrator:
    """Core orchestrator for CHROMA Synthetica v1.1 (unified broker)."""

    def __init__(self, kb_path: str = "kb/synthetica_kb_v1.1.json"):
        print(
            "[Orchestrator] Initialising CHROMA Synthetica v1.1 "
            "(Active Generative Philosophy)."
        )

        kb_data = self._load_kb(kb_path)

        print("\nBooting Knowledge Broker:")
        self.broker = KnowledgeBroker(kb_data)

        print("\nBooting Services:")
        self.compiler = NexusCompiler(self.broker)
        self.enrichment_service = EnrichmentService(self.broker)
        self.imtl = IMTLPolicyEngine(self.broker)

        print(
            f"\n[Orchestrator] System online. "
            f"KB version: {self.broker.get_entry('KB_Version')}"
        )

    def _load_kb(self, kb_path: str) -> Dict[str, Any]:
        def expand_candidates(raw_path: str) -> List[Path]:
            if not raw_path:
                return []
            kb_file = Path(raw_path)
            if kb_file.is_absolute():
                return [kb_file]
            base_dir = Path(__file__).resolve().parent
            return [
                Path.cwd() / kb_file,
                base_dir / kb_file,
                base_dir.parent / kb_file,
            ]

        env_override = os.getenv("SYNTHETICA_KB_PATH")

        search_paths: List[Path] = []
        seen: set[str] = set()
        for candidate in (
            expand_candidates(env_override)
            + expand_candidates(kb_path)
            + expand_candidates("kb/synthetica_kb_v1.0.json")
        ):
            key = str(candidate.resolve())
            if key not in seen:
                seen.add(key)
                search_paths.append(candidate)

        for candidate in search_paths:
            if candidate.exists():
                with candidate.open("r", encoding="utf-8") as handle:
                    return json.load(handle)

        search_list = "\n  - ".join(str(path) for path in search_paths)
        raise FileNotFoundError(
            "CRITICAL ERROR: knowledge base not found.\n"
            "Paths verificadas:\n"
            f"  - {search_list}\n"
            "Defina SYNTHETICA_KB_PATH ou execute 'python scripts/migrate_kb.py' "
            "para gerar a KB v1.1 antes de continuar."
        )

    def run_workflow(
        self,
        aco: AbstractCreativeObject,
        target_models: List[str],
        operator_pipeline: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, str]:
        """
        Execute the hybrid mind workflow.
        """
        print("\n" + "=" * 70)
        print("      STARTING CHROMA SYNTHETICA v1.1 WORKFLOW      ")
        print("=" * 70)

        operator_pipeline = operator_pipeline or []

        print("\n--- PHASE 1: ABSTRACT REASONING (Compiler + Operators) ---")
        iti = self.compiler.compile_to_iti(aco, operator_pipeline)

        print("\n--- INTERMEDIATE STATE (ITI) ---")
        print(iti)

        print("\n--- PHASE 2: TECHNICAL ENRICHMENT (EnrichmentService) ---")
        pso = self.enrichment_service.enrich_to_pso(iti)

        print("\n--- FINAL STATE (PSO) ---")
        print(pso)

        print("\n--- PHASE 3: TRANSLATION (IMTL) ---")
        results: Dict[str, str] = {}
        for model in target_models:
            final_prompt = self.imtl.translate(pso, model)
            results[model] = final_prompt
            self._generate_report(model, final_prompt)

        return results

    def _generate_report(self, model: str, prompt: str) -> None:
        print("\n" + "-" * 70)
        print(f" Optimised Prompt (IMTL -> {model}):\n")
        print(prompt)
        print("-" * 70)
