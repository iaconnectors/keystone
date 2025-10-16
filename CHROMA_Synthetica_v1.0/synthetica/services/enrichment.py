-# synthetica/services/enrichment.py
-
-# (v1.1) Importações atualizadas
-from synthetica.core.models import IntermediateTechnicalIntent, ProjectStateObject, CameraPackage, AbstractDirectives, CulturalCannibalizeDirective
+"""Serviço responsável pela Fase 2 (Enriquecimento Técnico) do Synthetica."""
 from synthetica.core.knowledge_broker import KnowledgeBroker
+from synthetica.core.models import (
+    AbstractDirectives,
+    CulturalCannibalizeDirective,
+    IntermediateTechnicalIntent,
+    ProjectStateObject,
+)
+
 
 class EnrichmentService:
-    """
-    Fase 2 da Mente Híbrida: Enriquecimento Técnico.
-    (v1.1) Implementa a resolução da Antropofagia e da Translation Matrix.
-    """
+    """Transforma o ITI em um Project State Object enriquecido."""
+
     def __init__(self, broker: KnowledgeBroker):
         self.broker = broker
         print("📚: EnrichmentService (Fase 2: Enriquecimento) inicializado.")
 
     def enrich_to_pso(self, iti: IntermediateTechnicalIntent) -> ProjectStateObject:
-        print(f"💡: Fase 2 (Enriquecimento Técnico): Iniciando enriquecimento do ITI...")
+        print("💡: Fase 2 (Enriquecimento Técnico): Iniciando enriquecimento do ITI...")
         pso = ProjectStateObject(source_aco_id=iti.source_aco_id)
         pso.core_concept = iti.core_concept
         pso.composition = iti.composition
         pso.reasoning_chain.extend(iti.reasoning_chain)
         pso.reasoning_chain.append("Início da Fase de Enriquecimento")
 
         directives = iti.abstract_directives
 
-        # (v1.1) ORDEM DE PRECEDÊNCIA: 
-        
-        # 1. Resolver Antropofagia (Pilar 3)
         self._resolve_antropofagia(directives.antropofagia_directive, pso)
-        
-        # 2. Resolver Dinâmicas Arquetípicas (Pilar 4 - Translation Matrix)
         self._resolve_archetypal_dynamics(directives.psychological_state, pso)
-
-        # 3. Resolver Hibridismo (Pilar 2 - Links de Artistas)
         self._resolve_hybridism_links(iti, pso)
-
-        # 4. Resolver Pacote Técnico (Simplificado)
         self._resolve_technical_package(directives, pso)
-        
+
         print("✅: Fase 2 concluída. PSO final gerado.")
         return pso
 
-    # --- NOVOS MÉTODOS DE RESOLUÇÃO (v1.1) ---
-
-    def _resolve_antropofagia(self, directive: CulturalCannibalizeDirective, pso: ProjectStateObject):
-        """(v1.1) Processa a diretiva de Antropofagia (Simulado conforme WP 3.3)."""
-        if not directive: return
+    def _resolve_antropofagia(
+        self, directive: CulturalCannibalizeDirective, pso: ProjectStateObject
+    ) -> None:
+        if directive is None:
+            return
 
-        pso.reasoning_chain.append(f"Processando Antropofagia: Modo {directive.synthesis_mode}...")
+        pso.reasoning_chain.append(
+            f"Processando Antropofagia: Modo {directive.synthesis_mode}..."
+        )
 
-        # Extrai os nomes dos conceitos dos caminhos
         devouring = directive.devouring_culture.split('.')[-1]
         devoured = directive.devoured_element.split('.')[-1]
 
-        # Lógica de síntese específica baseada nos exemplos do relatório (WP 5.1)
         if devouring == "Solarpunk" and "Iris van Herpen" in devoured:
-            # Solarpunk (Sintaxe: Sustentabilidade) + Iris van Herpen (Léxico: Formas complexas, Impressão 3D)
-            synthesis = ["Sustainable Solarpunk aesthetic", "3D printed photosynthetic structures", "Biophilic High-Tech", "Complex organic forms inspired by Iris van Herpen"]
-        
+            synthesis = [
+                "Sustainable Solarpunk aesthetic",
+                "3D printed photosynthetic structures",
+                "Biophilic High-Tech",
+                "Complex organic forms inspired by Iris van Herpen",
+            ]
         elif devouring == "Yoruba" and devoured == "Brutalism":
-             # Yoruba (Sintaxe: Cosmologia) + Brutalism (Léxico: Concreto, Monumentalidade)
-             synthesis = ["Yoruba cosmology expressed in architecture", "Monumental exposed concrete structures", "Geometric patterns based on Ifá cosmology"]
-
+            synthesis = [
+                "Yoruba cosmology expressed in architecture",
+                "Monumental exposed concrete structures",
+                "Geometric patterns based on Ifá cosmology",
+            ]
         else:
-            # Síntese Genérica (Extrai keywords e combina)
             keywords_devouring = self.broker.get_flat_list(directive.devouring_culture)
             keywords_devoured = self.broker.get_flat_list(directive.devoured_element)
-            # Heurística: Top 3 da base + Top 1 do elemento
-            synthesis = [str(k) for k in keywords_devouring if isinstance(k, str)][:3] + [str(k) for k in keywords_devoured if isinstance(k, str)][:1]
-        
+            devouring_keywords = [str(k) for k in keywords_devouring if isinstance(k, str)]
+            devoured_keywords = [str(k) for k in keywords_devoured if isinstance(k, str)]
+            synthesis = devouring_keywords[:3] + devoured_keywords[:1]
+
         pso.visual_style_keywords.extend(synthesis)
         pso.reasoning_chain.append(f"Resultado Antropofagia: {synthesis}")
 
+    def _resolve_archetypal_dynamics(self, state: str, pso: ProjectStateObject) -> None:
+        if not state:
+            return
 
-    def _resolve_archetypal_dynamics(self, state: str, pso: ProjectStateObject):
-        """(v1.1) Implementação da Translation Matrix (Pilar 4, Tabela 4.1)."""
-        if not state: return
-
-        pso.reasoning_chain.append(f"Consultando Translation Matrix para estado psicológico: '{state}'...")
+        pso.reasoning_chain.append(
+            f"Consultando Translation Matrix para estado psicológico: '{state}'..."
+        )
 
-        # Caminho para a matriz na KB v1.1
-        matrix_path = f"2.0_Semiotics_and_Psychology_Database.2.8_Archetypal_Dynamics_Framework (Jungian).Translation_Matrix.{state}.Aesthetic_Signifiers"
-        
+        matrix_path = (
+            "2.0_Semiotics_and_Psychology_Database."
+            "2.8_Archetypal_Dynamics_Framework (Jungian)."
+            f"Translation_Matrix.{state}.Aesthetic_Signifiers"
+        )
         signifier_paths = self.broker.get_entry(matrix_path)
 
         if not signifier_paths:
             return
 
-        # Para cada caminho de significante, extrai o nome ou keywords relevantes.
         resolved_signifiers = []
         for path in signifier_paths:
-            # Extrai o último segmento do caminho
             concept_name = path.split('.')[-1]
-            
-            # Lógica especial para Mestres (Painters, Architects) - KB 5.3
+
             if "5.3_Art_and_Design_References" in path:
-                 # O IMTL cuidará da formatação (Ganesh_Pyne -> Ganesh Pyne)
-                 pso.master_references.append(concept_name)
+                if concept_name not in pso.master_references:
+                    pso.master_references.append(concept_name)
             else:
                 resolved_signifiers.append(concept_name)
 
         pso.visual_style_keywords.extend(resolved_signifiers)
-        pso.reasoning_chain.append(f"Translation Matrix Resolvido. Estilo: {resolved_signifiers}. Mestres: {pso.master_references}")
-
-    def _resolve_hybridism_links(self, iti: IntermediateTechnicalIntent, pso: ProjectStateObject):
-        """(v1.1) Verifica se as variantes híbridas têm links para artistas (e.g. Gogi Saroj Pal)."""
-        # Heurística: Procurar por referências conhecidas no conceito gerado pelo Compiler (Fase 1).
-        # Isso verifica se o Compiler traduziu corretamente as variantes híbridas.
-        if "Kinnari" in iti.core_concept or "Kamdhenu" in iti.core_concept:
-            # Verifica se a variante Pal_Subversive foi usada (keywords esperadas)
-            if "empowered female hybrid" in iti.core_concept or "feminist critique" in iti.core_concept:
-                # Adiciona a referência ao artista se ainda não estiver presente
+        pso.reasoning_chain.append(
+            "Translation Matrix Resolvido. Estilo: "
+            f"{resolved_signifiers}. Mestres: {pso.master_references}"
+        )
+
+    def _resolve_hybridism_links(
+        self, iti: IntermediateTechnicalIntent, pso: ProjectStateObject
+    ) -> None:
+        concept = iti.core_concept or ""
+        if "Kinnari" in concept or "Kamdhenu" in concept:
+            if "empowered female hybrid" in concept or "feminist critique" in concept:
                 if "Gogi_Saroj_Pal" not in pso.master_references:
                     pso.master_references.append("Gogi_Saroj_Pal")
-                    pso.reasoning_chain.append("Hibridismo: Adicionada referência 'Gogi Saroj Pal' (via link da variante).")
-
-    # Métodos restantes (simplificados)
-    def _resolve_technical_package(self, directives: AbstractDirectives, pso: ProjectStateObject):
-        pso.camera_package = {"camera": "High-fidelity digital render"}
\ No newline at end of file
+                    pso.reasoning_chain.append(
+                        "Hibridismo: Adicionada referência 'Gogi Saroj Pal' (via link da variante)."
+                    )
+
+    def _resolve_technical_package(
+        self, directives: AbstractDirectives, pso: ProjectStateObject
+    ) -> None:
+        pso.camera_package = {"camera": "High-fidelity digital render"}