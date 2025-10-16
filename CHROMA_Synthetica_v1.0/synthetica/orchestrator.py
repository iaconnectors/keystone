# synthetica/orchestrator.py

import json
from typing import Any, Dict, List, Optional

# Importações dos componentes do Synthetica
from synthetica.core.knowledge_broker import KnowledgeBroker
from synthetica.core.models import AbstractCreativeObject
from synthetica.core.compiler import NexusCompiler
from synthetica.services.enrichment import EnrichmentService
from synthetica.engines.imtl import IMTLPolicyEngine

class ChromaSyntheticaOrchestrator:
    """
    A classe principal do CHROMA Synthetica v1.1. Orquestra a Mente Híbrida com Broker Unificado.
    """
    # (v1.1) O construtor agora aceita um único caminho para a KB Unificada.
    def __init__(self, kb_path: str = "kb/synthetica_kb_v1.1.json"):
        print(f"🚀 Inicializando CHROMA Synthetica v1.1 (Filosofia Gerativa Ativa)...")
        
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
       
        print(f"\n✅ Sistema Operacional. KB v{self.broker.get_entry('KB_Version')}")

    def _load_kb(self, kb_path: str) -> Dict[str, Any]:
        try:
            with open(kb_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"❌ ERRO CRÍTICO: KB não encontrada em '{kb_path}'. Verifique o caminho.")
        
    # (v1.1) O pipeline agora aceita dicionários {name, params}.
    def run_workflow(self, aco: AbstractCreativeObject, target_models: List[str], operator_pipeline: List[Dict] = []) -> Dict[str, str]:
        """
        Executa o fluxo de trabalho da Mente Híbrida.
        """
        print("\n" + "="*70)
        print("      INICIANDO FLUXO DE TRABALHO CHROMA SYNTHETICA v1.1      ")
        print("="*70)
        
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
        # (Mantido)
        print("\n" + "-"*70)
        print(f" Prompt Otimizado (IMTL -> {model}):\n")
        print(f"{prompt}")
        print("-"*70)