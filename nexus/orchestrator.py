# nexus/orchestrator.py

import json
from typing import Any, Dict, List, Optional

from nexus.core.knowledge_broker import KnowledgeBroker
from nexus.core.models import AbstractCreativeObject
from nexus.core.compiler import NexusCompiler
from nexus.engines.imtl import IMTLPolicyEngine
from nexus.engines.operators import CognitiveOperators

class ChromaNexusOrchestrator:
    """
    A classe principal do CHROMA Nexus v1.0.
    """
    def __init__(self, kb_path: str = "kb/nexus_kb_v1.0.json"):
        print("🚀 Inicializando CHROMA Nexus v1.0...")
        self._kb_data = self._load_kb(kb_path)
        self.broker = KnowledgeBroker(self._kb_data)
        
        # Inicialização dos Componentes Principais
        # O Compiler inicializa os CognitiveOperators internamente.
        self.compiler = NexusCompiler(self.broker)
        self.imtl = IMTLPolicyEngine(self.broker)
       
        kb_version = self.broker.get_entry("KB_Version", "desconhecida")
        print(f"✅ Base de Conhecimento v{kb_version} carregada. Nexus Operacional.")

    def _load_kb(self, kb_path: str) -> Dict[str, Any]:
        try:
            with open(kb_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"❌ ERRO CRÍTICO: KB não encontrada em '{kb_path}'.")
        except json.JSONDecodeError:
            raise ValueError(f"❌ ERRO CRÍTICO: KB não é um JSON válido.")

    def run_workflow(self, aco: AbstractCreativeObject, target_models: List[str], cognitive_pipeline: List[str] = []) -> Dict[str, str]:
        """
        Executa o fluxo de trabalho completo: ACO -> (Cognitive Ops) -> PSO -> IMTL -> Prompts.
        """
        print("\n" + "="*70)
        print("      INICIANDO FLUXO DE TRABALHO DO CHROMA NEXUS v1.0      ")
        print("="*70)
        print("--- FASE 1: INTENÇÃO E PRÉ-PROCESSAMENTO COGNITIVO (ACO) ---")
        # O pipeline cognitivo é passado para o compilador, que modifica o ACO.
        
        # FASE 2: Compilação (ACO -> PSO)
        print("\n--- FASE 2: COMPILAÇÃO (ACO -> PSO) ---")
        pso = self.compiler.compile(aco, cognitive_pipeline)
        
        print("--- ESTADO DO ACO PÓS-COGNITIVO ---")
        print(aco)
        print("--- ESTADO DO PSO PÓS-COMPILAÇÃO ---")
        print(pso)

        # FASE 3: Orquestração e Tradução (PSO -> Prompts)
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
        print(f"{prompt}")
        print("-"*70)