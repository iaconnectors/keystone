# scripts/migrate_kb.py

import json

# Configuração dos caminhos dos arquivos
NEXUS_KB_PATH = "kb/nexus_kb_v1.0.json"
KEYSTONE_KB_PATH = "kb/keystone_kb_v27.0.json"
OUTPUT_KB_PATH = "kb/synthetica_kb_v1.0.json"

class KBMigrationTool:
    """
    Pilar III.2: Ferramenta de Migração e Fusão.
    """
    def __init__(self):
        self.nexus_kb = self._load_json(NEXUS_KB_PATH)
        self.keystone_kb = self._load_json(KEYSTONE_KB_PATH)
        self.unified_kb = {}

    def _load_json(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Erro: Arquivo não encontrado em {path}")
            return {}

    def migrate(self):
        if not self.nexus_kb or not self.keystone_kb: return
            
        print("\n--- Iniciando Migração para Synthetica KB v1.0 (Épico 3) ---")
        
        # 1. Fusão Básica
        self._basic_merge()

        # 2. Fusão Semântica (Criação de meta.links)
        self._semantic_linking()

        # 3. Salvar Resultado
        self._save_unified_kb()

    def _basic_merge(self):
        # Define os metadados unificados
        self.unified_kb = {
            "KB_ID": "CHROMA_SYNTHETICA_KB_v1.0",
            "KB_Version": "1.0.0 (Unified)"
        }
        
        # Copia domínios do Keystone (Enciclopédico) como base
        for key, value in self.keystone_kb.items():
            # Copia apenas os domínios de conhecimento, não metadados de alto nível
            if any(key.startswith(str(i)) for i in range(1, 16)):
                 self.unified_kb[key] = value

        # Insere/Funde o Framework Cognitivo do Nexus (Garante a versão do Nexus)
        cognitive_framework = self.nexus_kb.get("2.0_Semiotics_and_Psychology_Database", {}).get("2.6_Cognitive_Impact_Framework (Neuroaesthetics)")
        
        if cognitive_framework:
            if "2.0_Semiotics_and_Psychology_Database" not in self.unified_kb:
                self.unified_kb["2.0_Semiotics_and_Psychology_Database"] = {}
            
            # Insere o framework cognitivo na estrutura unificada
            self.unified_kb["2.0_Semiotics_and_Psychology_Database"]["2.6_Cognitive_Impact_Framework"] = cognitive_framework
            print("✅ Fusão básica concluída.")

    def _semantic_linking(self):
        """
        Usa LLM (Simulado) para criar links semânticos (Pilar III.1).
        """
        print("🔗 Iniciando Linkagem Semântica (Simulação LLM)...")
        
        # Exemplo: Linkar "Symmetry" com nós relevantes do Keystone.
        
        # Resposta Simulada do LLM:
        related_nodes = [
            "5.0_Masters_Lexicon.5.3_Art_and_Design_References.Architects (Tadao Ando)",
            "3.0_Visual_Language_and_Composition.3.1_Compositional_Principles.Symmetry"
        ]

        # Aplicar os links na KB Unificada
        try:
            # Caminho para o conceito abstrato
            symmetry_node = self.unified_kb["2.0_Semiotics_and_Psychology_Database"]["2.6_Cognitive_Impact_Framework"]["Principles"]["Symmetry"]
            
            # Adiciona o campo 'meta.links' (Conforme WP 3.1)
            symmetry_node["meta"] = {"links": {"related_nodes": related_nodes}}
            print("✅ Linkagem Semântica concluída.")

        except KeyError as e:
            print(f"⚠️ Aviso durante a linkagem semântica: Nó não encontrado ({e}).")


    def _save_unified_kb(self):
        try:
            with open(OUTPUT_KB_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.unified_kb, f, indent=2, ensure_ascii=False)
            print(f"\n🎉 Migração concluída! KB Unificada salva em: {OUTPUT_KB_PATH}")
        except Exception as e:
            print(f"❌ Erro ao salvar KB Unificada: {e}")

if __name__ == "__main__":
    tool = KBMigrationTool()
    tool.migrate()