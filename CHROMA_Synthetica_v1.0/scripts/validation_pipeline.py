# scripts/validation_pipeline.py

import json
import sys
import argparse
from typing import Dict, Any
import os

# Tenta importar jsonschema, lida graciosamente se não estiver disponível
try:
    from jsonschema import validate, ValidationError
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    print("WARNING: 'jsonschema' nao encontrado. A validacao estrutural sera ignorada.")
    print("Instale com 'pip install jsonschema' para validacao completa.\n")
    JSONSCHEMA_AVAILABLE = False
    ValidationError = Exception  # Define dummy exception

# Define o caminho para o arquivo de esquema (relativo à raiz do projeto)
# Assumimos que o script é executado a partir da raiz do projeto.
SCHEMA_PATH = "kb/kb_schema.json"

class ValidationPipeline:
    """
    Pilar IV: Governança de Produção. Executa testes de integridade na KB.
    """
    def __init__(self, kb_path: str):
        self.kb_path = kb_path
        # Carrega os dados da KB e do Schema (Sai se falhar - crítico para CI/CD)
        self.kb_data = self._load_json(kb_path)
        self.schema_data = self._load_json(SCHEMA_PATH) if JSONSCHEMA_AVAILABLE else None
        
        self.tests_passed = 0
        self.tests_failed = 0

    def _load_json(self, path: str) -> Dict[str, Any]:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(
                f"CRITICAL ERROR (Sintaxe/Carregamento): Arquivo nao encontrado em {path}"
            )
            # Verifica se o schema está faltando e dá instruções claras
            if path == SCHEMA_PATH:
                print("Certifique-se de que kb/kb_schema.json existe.")
            sys.exit(1)  # Saída com erro
        except json.JSONDecodeError:
            print(
                f"CRITICAL ERROR (Sintaxe/Carregamento): Arquivo JSON invalido em {path}"
            )
            sys.exit(1)

    def run(self):
        print(f"\n--- Iniciando Pipeline de Validação da KB (CI/CD) ---")
        print(f"Validando: {self.kb_path}\n")

        # Camada 1: Validação de Esquema
        self.test_schema_validation()
        
        # Camada 2: Consistência Ontológica
        self.test_ontological_consistency()

        # Camada 3: Integridade Referencial
        self.test_referential_integrity()
        
        # Camada 4: Verificação de Redundância (Simulada)
        self.test_semantic_redundancy()

        self.report_results()

    def _report_test(self, test_name: str, success: bool, message: str = ""):
        if success:
            print(f"PASS: {test_name}")
            self.tests_passed += 1
        else:
            print(f"FAIL: {test_name} (Detalhes: {message})")
            self.tests_failed += 1

    # --- Implementação dos Testes ---

    def test_schema_validation(self):
        """Camada 1: Verifica se o JSON está em conformidade com o esquema formal."""
        if not JSONSCHEMA_AVAILABLE:
            print("SKIP: Validacao de Esquema JSON (jsonschema nao instalado)")
            return

        try:
            validate(instance=self.kb_data, schema=self.schema_data)
            self._report_test("Validação de Esquema JSON (Estrutural)", True)
        except ValidationError as e:
            # Fornece detalhes úteis sobre onde a validação falhou
            path = ".".join(map(str, e.path)) or "Root"
            self._report_test("Validação de Esquema JSON (Estrutural)", False, f"Violação no caminho '{path}': {e.message}")

    def test_ontological_consistency(self):
        """Camada 2: Verifica as regras de negócio internas da KB."""
        # Teste: O Framework Cognitivo deve existir e conter 'Principles'.
        try:
            framework = self.kb_data.get("2.0_Semiotics_and_Psychology_Database", {}).get("2.6_Cognitive_Impact_Framework")
            if framework and "Principles" in framework and framework["Principles"]:
                self._report_test("Consistência Ontológica (Framework Cognitivo)", True)
            else:
                 # Pode falhar se estiver validando uma KB antiga (e.g. Keystone v27.0 puro) ou se a fusão falhou.
                 self._report_test("Consistência Ontológica (Framework Cognitivo)", False, "Framework 2.6 ausente ou incompleto.")
        except Exception as e:
            self._report_test("Consistência Ontológica (Geral)", False, f"Erro durante a verificação: {e}")

    def test_referential_integrity(self):
        """Camada 3: Verifica se os links internos apontam para nós existentes (Simulado)."""
        # Simulação: Verifica o link criado pelo migrate_kb.py (Épico 3)
        try:
            # Navega até o nó 'Symmetry' gerado pela fusão
            symmetry_node = self.kb_data["2.0_Semiotics_and_Psychology_Database"]["2.6_Cognitive_Impact_Framework"]["Principles"]["Symmetry"]
            
            # Verifica a estrutura 'meta.links'
            links = symmetry_node.get("meta", {}).get("links", {}).get("related_nodes", [])
            
            if not links:
                self._report_test("Integridade Referencial (meta.links)", False, "Nó 'Symmetry' não possui 'meta.links'.")
                return

            # Verifica se o link esperado (Tadao Ando) existe nos links gerados
            normalized_links = [link.replace("_", " ") for link in links]

            if any("Tadao Ando" in link for link in normalized_links):
                self._report_test("Integridade Referencial (meta.links)", True)
            else:
                 self._report_test("Integridade Referencial (meta.links)", False, "Link esperado (Symmetry -> Tadao Ando) nao encontrado.")

        except (KeyError, TypeError):
             # Se a estrutura não existir (e.g., KB antiga ou migração falhou), o teste falha.
             self._report_test("Integridade Referencial (meta.links)", False, "Estrutura necessária para verificar links semânticos não encontrada.")


    def test_semantic_redundancy(self):
        """Camada 4: Verifica se há duplicação de conceitos (Simulado)."""
        # Simulação: Verificar duplicatas exatas na lista de Arquitetos.
        # Em produção, isso usaria embeddings de NLP.
        try:
            # Caminho na KB Unificada (herdado do Keystone v27.0)
            path = "5.0_Masters_Lexicon.5.3_Art_and_Design_References.Architects"
            
            # Navegação manual segura para encontrar a lista
            parts = path.split('.')
            data = self.kb_data
            for part in parts:
                # Usa .get() para navegação segura
                data = data.get(part)
                if data is None: break

            if isinstance(data, list):
                unique_items = set(data)
                if len(data) != len(unique_items):
                    # Encontra os itens duplicados
                    duplicates = [item for item in unique_items if data.count(item) > 1]
                    self._report_test("Redundância Semântica (Arquitetos)", False, f"Duplicatas exatas encontradas: {duplicates}")
                else:
                    self._report_test("Redundância Semântica (Arquitetos)", True)
            else:
                 # Se o caminho não existir ou não for uma lista, o teste passa.
                 self._report_test("Redundância Semântica (Arquitetos)", True, "Caminho não é uma lista ou não encontrado.")

        except Exception as e:
             self._report_test("Redundância Semântica (Geral)", False, f"Erro durante a verificação: {e}")


    def report_results(self):
        print("\n--- Relatório do Pipeline de Validação ---")
        print(f"Total de Testes: {self.tests_passed + self.tests_failed}")
        print(f"Passaram: {self.tests_passed}")
        print(f"Falharam: {self.tests_failed}")

        if self.tests_failed > 0:
            print("\nSTATUS DO PIPELINE: FALHOU")
            sys.exit(1)  # Saída com erro para o CI/CD interromper o merge
        else:
            print("\nSTATUS DO PIPELINE: SUCESSO")
            sys.exit(0)  # Saída com sucesso

if __name__ == "__main__":
    # Interface de Linha de Comando (CLI) para integração com CI/CD
    parser = argparse.ArgumentParser(description="Validador de Integridade da Base de Conhecimento CHROMA Synthetica.")
    
    # O pipeline de CI passará o caminho do arquivo modificado como argumento.
    parser.add_argument("--kb_path", type=str, required=True, help="Caminho para o arquivo JSON da KB a ser validado.")
    
    args = parser.parse_args()

    # Executa o pipeline com o caminho fornecido
    pipeline = ValidationPipeline(args.kb_path)
    pipeline.run()
