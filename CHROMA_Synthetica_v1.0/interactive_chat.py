"""Chat CLI for the SeaDream prompt architect."""

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from interactive_assistant import run_interaction, DEFAULT_THEME

THEME_LIST = [
    "cinematografico",
    "publicitario",
    "design",
    "arquitetura",
    "montagem_de_stands",
    "criacao_de_personagem",
    "criacao_de_cena",
    "estudo_de_objeto",
    "estudo_de_personagem",
]

CASE_LIBRARY_PATH = Path("playgrounds/seedream_cases.json")


def _load_case_library() -> Dict[str, Dict[str, Any]]:
    try:
        payload = json.loads(CASE_LIBRARY_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as exc:
        print(f"[AVISO] Falha ao ler {CASE_LIBRARY_PATH}: {exc}")
        return {}

    cases = payload.get("cases", {})
    return cases if isinstance(cases, dict) else {}


def main() -> None:
    parser = argparse.ArgumentParser(description="Chat interativo SeaDream.")
    parser.add_argument(
        "--model",
        type=str,
        default="models/gemini-2.5-pro",
        help="Modelo Gemini a ser utilizado (padrao: models/gemini-2.5-pro).",
    )
    parser.add_argument(
        "--theme",
        type=str,
        default=DEFAULT_THEME,
        choices=THEME_LIST,
        help="Tema inicial do blueprint.",
    )
    args = parser.parse_args()

    current_model = args.model
    current_theme = args.theme
    case_library = _load_case_library()

    print("=== SeaDream Prompt Architect Chat ===")
    print(
        "Digite seu briefing e pressione Enter. "
        "Comandos: /theme <nome>, /model <nome>, /case <id>, /quit"
    )

    while True:
        try:
            user_input = input(f"({current_theme})> ").strip()
        except EOFError:
            print("\nEncerrando chat.")
            break

        if not user_input:
            continue

        command = user_input.lower()
        if command in {"/quit", "/exit"}:
            print("Encerrado.")
            break

        if user_input.startswith("/theme"):
            parts = user_input.split(maxsplit=1)
            if len(parts) == 2 and parts[1] in THEME_LIST:
                current_theme = parts[1]
                print(f"Tema atualizado para {current_theme}.")
            else:
                print("Temas disponiveis: " + ", ".join(THEME_LIST))
            continue

        if user_input.startswith("/model"):
            parts = user_input.split(maxsplit=1)
            if len(parts) == 2:
                current_model = parts[1]
                print(f"Modelo atualizado para {current_model}.")
            else:
                print("Uso: /model models/gemini-2.5-pro")
            continue

        if user_input.startswith("/case"):
            if not case_library:
                print("Nenhum caso pre-configurado encontrado.")
                continue

            parts = user_input.split(maxsplit=1)
            if len(parts) != 2:
                print("Uso: /case <id>. Casos disponiveis: " + ", ".join(case_library))
                continue

            case_id = parts[1].strip()
            case_data = case_library.get(case_id)
            if not case_data:
                print("Caso nao encontrado. Disponiveis: " + ", ".join(case_library))
                continue

            case_title = case_data.get("title", case_id)
            case_theme = case_data.get("theme", current_theme)
            if case_theme not in THEME_LIST:
                print(
                    f"[AVISO] Tema '{case_theme}' nao reconhecido. "
                    "Usando tema atual."
                )
                case_theme = current_theme

            brief = case_data.get("brief", "")
            notes = case_data.get("notes") or []

            print(f"\n--- Caso: {case_title} ({case_id}) ---")
            print(f"Tema sugerido : {case_theme}")
            if brief:
                print(f"Brief padrao : {brief}")
            if notes:
                print("Notas:")
                for note in notes:
                    print(f"- {note}")
            print("--- Executando caso ---")

            try:
                run_interaction(brief, current_model, case_theme)
            except Exception as exc:  # pragma: no cover
                print(f"[ERRO] {exc}")
            continue

        try:
            run_interaction(user_input, current_model, current_theme)
        except Exception as exc:  # pragma: no cover
            print(f"[ERRO] {exc}")


if __name__ == "__main__":
    main()

