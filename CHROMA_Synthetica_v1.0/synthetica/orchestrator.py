import json
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
        kb_file = Path(kb_path)

        search_paths = []
        if kb_file.is_absolute():
            search_paths.append(kb_file)
        else:
            search_paths.extend(
                [
                    Path.cwd() / kb_file,
                    Path(__file__).resolve().parent / kb_file,
                    Path(__file__).resolve().parent.parent / kb_file,
                ]
            )

        for candidate in search_paths:
            if candidate.exists():
                with candidate.open("r", encoding="utf-8") as handle:
                    return json.load(handle)

        raise FileNotFoundError(
            "CRITICAL ERROR: knowledge base not found. "
            f"Checked paths: {', '.join(str(path) for path in search_paths)}."
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
