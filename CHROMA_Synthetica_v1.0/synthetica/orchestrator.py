import json
from pathlib import Path
from typing import Any, Dict, List, Optional

# Importações dos componentes do Synthetica
from synthetica.core.knowledge_broker import KnowledgeBroker
from synthetica.core.models import AbstractCreativeObject
from synthetica.core.compiler import NexusCompiler
from synthetica.services.enrichment import EnrichmentService
from synthetica.engines.imtl import IMTLPolicyEngine

class ChromaSyntheticaOrchestrator:
    """
    Core orchestrator for CHROMA Synthetica v1.1 (unified broker).
    """
    def __init__(self, kb_path: str = "kb/synthetica_kb_v1.1.json"):
        print(
            "[Orchestrator] Initialising CHROMA Synthetica v1.1 "
            "(Active Generative Philosophy)."
        )
        
        # 1. Carregar a Base de Conhecimento Unificada
        kb_data = self._load_kb(kb_path)

        # 2. Inicializar Broker Unificado
        print("\nInicializando Broker:")
        self.broker = KnowledgeBroker(kb_data)
        
        # 3. Inicializar Componentes da Mente Híbrida (Todos usam o Broker Unificado)
        print("\nInicializando Serviços:")
        # Fase 1: Raciocínio
        self.compiler = NexusCompiler(self.broker)
        # Fase 2: Enriquecimento
        self.enrichment_service = EnrichmentService(self.broker)
        
        # 4. Inicializar Motor de Tradução (IMTL)
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
            search_paths.extend([
                Path.cwd() / kb_file,
                Path(__file__).resolve().parent / kb_file,
                Path(__file__).resolve().parent.parent / kb_file,
            ])

        for candidate in search_paths:
            if candidate.exists():
                with candidate.open('r', encoding='utf-8') as handle:
                    return json.load(handle)

        raise FileNotFoundError(
            "CRITICAL ERROR: knowledge base not found. "
            f"Checked paths: {', '.join(str(path) for path in search_paths)}."
        )
        
    # (v1.1) O pipeline agora aceita dicionários {name, params}.
    def run_workflow(
        self,
        aco: AbstractCreativeObject,
        target_models: List[str],
        operator_pipeline: Optional[List[Dict]] = None,
    ) -> Dict[str, str]:
        """
        Executa o fluxo de trabalho da Mente Híbrida.
        """
        print("\n" + "="*70)
        print("      INICIANDO FLUXO DE TRABALHO CHROMA SYNTHETICA v1.1      ")
        print("="*70)
        
        operator_pipeline = operator_pipeline or []

        # FASE 1: Raciocínio Abstrato (ACO -> ITI)
        print("\n--- FASE 1: RACIOCÍNIO ABSTRATO (Compiler + Operadores) ---")
        iti = self.compiler.compile_to_iti(aco, operator_pipeline)
        
        print("\n--- ESTADO INTERMEDIÁRIO (ITI) ---")
        print(iti)

        # FASE 2: Enriquecimento Técnico (ITI -> PSO)
        print("\n--- FASE 2: ENRIQUECIMENTO TÉCNICO (EnrichmentService) ---")
        pso = self.enrichment_service.enrich_to_pso(iti)

        print("\n--- ESTADO FINAL (PSO) ---")
        print(pso)

        # FASE 3: Tradução (PSO -> Prompts)
        print("\n--- FASE 3: TRADUÇÃO (IMTL) ---")
        results = {}
        for model in target_models:
            final_prompt = self.imtl.translate(pso, model)
            results[model] = final_prompt
            self._generate_report(model, final_prompt)
        
        return results

    def _generate_report(self, model: str, prompt: str):
        print("\n" + "-"*70)
        print(f" Prompt Otimizado (IMTL -> {model}):\n")
        print(prompt)
        print("-" * 70)
