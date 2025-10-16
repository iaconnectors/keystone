-# synthetica/core/compiler.py
+"""Módulo responsável pela Fase 1 (Raciocínio Abstrato) do Synthetica."""
+from typing import Any, Dict, List, Optional
 
-from synthetica.core.models import AbstractCreativeObject, IntermediateTechnicalIntent
 from synthetica.core.knowledge_broker import KnowledgeBroker
-# (v1.1) Importação atualizada
+from synthetica.core.models import AbstractCreativeObject, IntermediateTechnicalIntent
 from synthetica.engines.operators import OperatorsEngine
-from typing import List, Dict, Any
+
 
 class NexusCompiler:
-    """
-    Fase 1 da Mente Híbrida: Raciocínio Abstrato.
-    """
+    """Executa a fase de raciocínio do pipeline."""
+
     def __init__(self, broker: KnowledgeBroker):
         self.broker = broker
-        # (v1.1) Inicialização do motor de operadores unificado
         self.operators_engine = OperatorsEngine(broker)
         print("🎨: NexusCompiler (Fase 1: Raciocínio) inicializado.")
 
-    # (v1.1) O pipeline agora aceita dicionários para parâmetros de operadores
-    def compile_to_iti(self, aco: AbstractCreativeObject, operator_pipeline: List[Dict[str, Any]] = []) -> IntermediateTechnicalIntent:
-        """
-        Processo de compilação da Fase 1. Gera o ITI.
-        """
-        print(f"🧠: Fase 1 (Raciocínio Abstrato): Iniciando compilação do ACO...")
+    def compile_to_iti(
+        self,
+        aco: AbstractCreativeObject,
+        operator_pipeline: Optional[List[Dict[str, Any]]] = None,
+    ) -> IntermediateTechnicalIntent:
+        """Processa o ACO e gera o ITI intermediário."""
+        print("🧠: Fase 1 (Raciocínio Abstrato): Iniciando compilação do ACO...")
         iti = IntermediateTechnicalIntent(source_aco_id=aco.aco_id)
 
-        # Etapa 1.1: Pipeline de Operadores (Cognitivos e Conceituais)
+        operator_pipeline = operator_pipeline or []
         if operator_pipeline:
             iti.reasoning_chain.append("Início do Pipeline de Operadores")
             for op_spec in operator_pipeline:
                 op_name = op_spec.get("name")
                 op_params = op_spec.get("params", {})
                 if op_name:
-                    # Os operadores modificam o ACO e adicionam diretivas ao ITI
                     self.operators_engine.apply(op_name, aco, iti, op_params)
 
-        # Etapa 1.2: Tradução da Intenção e Elementos
         self._translate_intent(aco, iti)
-        self._translate_elements(aco, iti) # (v1.1) Adicionado
-
-        # Etapa 1.3: Geração de Queries Técnicas
+        self._translate_elements(aco, iti)
         self._define_technical_queries(aco, iti)
 
         print("✅: Fase 1 concluída. ITI gerado.")
         return iti
 
-    def _translate_intent(self, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent):
-        # (v1.1) A narrativa agora é processada após os elementos em _translate_elements.
-
+    def _translate_intent(self, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent) -> None:
         if aco.intent.compositional_flow:
             flow = aco.intent.compositional_flow
             iti.composition = f"Path: {flow.path}"
-            
-        # (v1.1) Se a dinâmica não foi definida via Operador, verifica se está no ACO e passa para o ITI.
+
         if not iti.abstract_directives.psychological_state and aco.intent.archetypal_dynamics:
-            iti.abstract_directives.psychological_state = aco.intent.archetypal_dynamics.shadow_integration_state
+            iti.abstract_directives.psychological_state = (
+                aco.intent.archetypal_dynamics.shadow_integration_state
+            )
 
-    def _translate_elements(self, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent):
-        """(v1.1) Processa elementos e Hibridismo (Pilar 2)."""
-        element_descriptions = []
+    def _translate_elements(self, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent) -> None:
+        """Gera descrições dos elementos do ACO, incluindo hibridismo."""
+        element_descriptions: List[str] = []
         for subject in aco.elements.subjects:
             desc = subject.description
-            
-            # Processamento de Hibridismo (Pilar 2)
+
             if subject.hybrid_ontology_ref:
-                # Consulta a KB 2.7 para obter keywords da variante ou propriedades gerais.
-                keywords = []
+                keywords: List[str] = []
                 if subject.hybrid_variant:
-                    # Tenta obter keywords da variante específica
-                    variant_path = f"{subject.hybrid_ontology_ref}.Variants.{subject.hybrid_variant}.Keywords"
+                    variant_path = (
+                        f"{subject.hybrid_ontology_ref}.Variants.{subject.hybrid_variant}.Keywords"
+                    )
                     keywords = self.broker.get_flat_list(variant_path)
-                
+
                 if not keywords:
-                     # Fallback para propriedades gerais se a variante não tiver keywords
-                     prop_path = f"{subject.hybrid_ontology_ref}.Properties"
-                     keywords = self.broker.get_flat_list(prop_path)
+                    prop_path = f"{subject.hybrid_ontology_ref}.Properties"
+                    keywords = self.broker.get_flat_list(prop_path)
 
                 if keywords:
-                    # Filtra e formata keywords (garante que são strings)
-                    filtered_keywords = ', '.join([str(k) for k in keywords if k])
+                    filtered_keywords = ', '.join(str(k) for k in keywords if k)
                     desc += f" (Hybrid Traits: {filtered_keywords})"
-                    iti.reasoning_chain.append(f"Hibridismo: Traduzido {subject.hybrid_ontology_ref.split('.')[-1]} para keywords.")
+                    iti.reasoning_chain.append(
+                        f"Hibridismo: Traduzido {subject.hybrid_ontology_ref.split('.')[-1]} para keywords."
+                    )
 
             element_descriptions.append(desc)
 
-        # Combina narrativa e elementos para o conceito central
         if aco.intent.narrative_moment:
-             iti.core_concept = f"{aco.intent.narrative_moment} Featuring: {'. '.join(element_descriptions)}"
+            iti.core_concept = (
+                f"{aco.intent.narrative_moment} Featuring: {'. '.join(element_descriptions)}"
+            )
         else:
             iti.core_concept = '. '.join(element_descriptions)
 
-
-    def _define_technical_queries(self, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent):
-        # (Lógica mantida da v1.0)
+    def _define_technical_queries(self, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent) -> None:
         if aco.constraints.style_constraints and aco.constraints.style_constraints.historical_process:
             process = aco.constraints.style_constraints.historical_process
             iti.abstract_directives.historical_process = process
-            iti.reasoning_chain.append(f"Diretiva de Processo Histórico adicionada: {process}")
\ No newline at end of file
+            iti.reasoning_chain.append(f"Diretiva de Processo Histórico adicionada: {process}")
