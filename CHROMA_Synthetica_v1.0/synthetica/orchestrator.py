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
    A classe principal do CHROMA Synthetica v1.0. Orquestra a Mente Híbrida com Dual Brokers.
    """
    def __init__(self, nexus_kb_path: str, keystone_kb_path: str):
        print("🚀 Inicializando CHROMA Synthetica v1.0 (Mente Híbrida)...")
        
        # 1. Carregar as Bases de Conhecimento
        nexus_kb_data = self._load_kb(nexus_kb_path)
        keystone_kb_data = self._load_kb(keystone_kb_path)

        # 2. Inicializar Brokers Distintos
        print("\nInicializando Brokers:")
        # Broker de Raciocínio (Nexus KB)
        self.nexus_broker = KnowledgeBroker(nexus_kb_data)
        # Broker Enciclopédico (Keystone KB)
        self.keystone_broker = KnowledgeBroker(keystone_kb_data)
        
        # 3. Inicializar Componentes da Mente Híbrida
        print("\nInicializando Serviços:")
        # Fase 1: Raciocínio (Usa Nexus Broker)
        self.compiler = NexusCompiler(self.nexus_broker)
        # Fase 2: Enriquecimento (Usa Keystone Broker)
        self.enrichment_service = EnrichmentService(self.keystone_broker)
        
        # 4. Inicializar Motor de Tradução (IMTL) - Usa Nexus Broker para perfis retóricos
        self.imtl = IMTLPolicyEngine(self.nexus_broker)
       
        print(f"\n✅ Sistema Operacional. Nexus v{self.nexus_broker.get_entry('KB_Version')} | Keystone v{self.keystone_broker.get_entry('KB_Version')}")

    def _load_kb(self, kb_path: str) -> Dict[str, Any]:
        try:
            with open(kb_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"❌ ERRO CRÍTICO: KB não encontrada em '{kb_path}'.")
        
    def run_workflow(self, aco: AbstractCreativeObject, target_models: List[str], cognitive_pipeline: List[str] = []) -> Dict[str, str]:
        """
        Executa o fluxo de trabalho da Mente Híbrida: ACO -> ITI -> PSO -> Prompts.
        """
        print("\n" + "="*70)
        print("      INICIANDO FLUXO DE TRABALHO CHROMA SYNTHETICA v1.0      ")
        print("="*70)
        
        # FASE 1: Raciocínio Abstrato (ACO -> ITI)
        print("\n--- FASE 1: RACIOCÍNIO ABSTRATO (Compiler + Nexus KB) ---")
        iti = self.compiler.compile_to_iti(aco, cognitive_pipeline)
        
        print("\n--- ESTADO INTERMEDIÁRIO (ITI) ---")
        print(iti)

        # FASE 2: Enriquecimento Técnico (ITI + Keystone KB -> PSO)
        print("\n--- FASE 2: ENRIQUECIMENTO TÉCNICO (EnrichmentService + Keystone KB) ---")
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

    def introspect_knowledge(self, query: str) -> str:
        """(Épico 3.3) Operador de Introspecção (Simulado)."""
        print(f"\n🔍 Introspecção (Simulado): '{query}'")
        return "Operador de Introspecção (Épico 3.3) ainda não implementado (requer Grafo de Conhecimento)."

    def _generate_report(self, model: str, prompt: str):
        print("\n" + "-"*70)
        print(f" Prompt Otimizado (IMTL -> {model}):\n")
        print(f"{prompt}")
        print("-"*70)