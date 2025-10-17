"""Utility to merge legacy KBs into the unified Synthetica v1.1 format."""

import json
from pathlib import Path

NEXUS_KB_PATH = Path("kb/nexus_kb_v1.0.json")
KEYSTONE_KB_PATH = Path("kb/Keystone-CHROMA-KB-v27.0.json")
OUTPUT_KB_PATH = Path("kb/synthetica_kb_v1.1.json")


class KBMigrationTool:
    """Merges data sources and enriches them with simulated semantic links."""

    def __init__(self) -> None:
        self.nexus_kb = self._load_json(NEXUS_KB_PATH)
        self.keystone_kb = self._load_json(KEYSTONE_KB_PATH)
        self.unified_kb: dict = self._load_json(OUTPUT_KB_PATH) or {}

    def _load_json(self, path: Path) -> dict:
        try:
            with path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except FileNotFoundError:
            print(f"ERRO: Arquivo nao encontrado em {path}")
            return {}

    def migrate(self) -> None:
        if not self.nexus_kb or not self.keystone_kb:
            print("Arquivos de origem ausentes. Migracao cancelada.")
            return

        print("\n--- Iniciando migracao para Synthetica KB v1.1 (Epico 3) ---")
        self._basic_merge()
        self._semantic_linking()
        self._save_unified_kb()

    def _basic_merge(self) -> None:
        """Combine metadata and core domains from both sources."""
        self.unified_kb.setdefault("KB_ID", "CHROMA_SYNTHETICA_KB_v1.1")
        self.unified_kb.setdefault(
            "KB_Version", "1.1.0 (Hybridity, Antropofagia & Contradiction Expansion)"
        )

        for key, value in self.keystone_kb.items():
            if any(key.startswith(str(i)) for i in range(1, 16)) and key not in self.unified_kb:
                self.unified_kb[key] = value

        nexus_framework = (
            self.nexus_kb.get("2.0_Semiotics_and_Psychology_Database", {})
            .get("2.6_Cognitive_Impact_Framework (Neuroaesthetics)")
        )

        if nexus_framework:
            target = self.unified_kb.setdefault(
                "2.0_Semiotics_and_Psychology_Database", {}
            )
            target.setdefault("2.6_Cognitive_Impact_Framework", nexus_framework)
            print("Fusao basica concluida (framework cognitivo preservado).")
        else:
            print("Aviso: framework cognitivo do Nexus nao encontrado.")

    def _semantic_linking(self) -> None:
        """Add simulated semantic links to the merged KB."""
        print("[Linking] Iniciando criacao de links semanticos simulados...")
        related_nodes = [
            (
                "5.0_Masters_Lexicon.5.3_Art_and_Design_References."
                "Architects.Tadao_Ando"
            ),
            "3.0_Visual_Language_and_Composition.3.1_Compositional_Principles.Symmetry",
        ]

        try:
            symmetry_node = (
                self.unified_kb["2.0_Semiotics_and_Psychology_Database"]
                ["2.6_Cognitive_Impact_Framework"]["Principles"]["Symmetry"]
            )
            symmetry_node.setdefault("meta", {}).setdefault("links", {})[
                "related_nodes"
            ] = related_nodes
            print("[Linking] Links adicionados ao no 'Symmetry'.")
        except KeyError as error:
            print(f"Aviso: nao foi possivel aplicar links semanticos ({error}).")

    def _save_unified_kb(self) -> None:
        try:
            OUTPUT_KB_PATH.write_text(
                json.dumps(self.unified_kb, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            print(f"\nMigracao concluida. KB unificada salva em: {OUTPUT_KB_PATH}")
        except Exception as error:
            print(f"Erro ao salvar KB unificada: {error}")


if __name__ == "__main__":
    KBMigrationTool().migrate()
