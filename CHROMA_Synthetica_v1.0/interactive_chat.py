"""Chat CLI for the SeaDream prompt architect."""

import argparse

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


def main() -> None:
    parser = argparse.ArgumentParser(description="Chat interativo SeaDream.")
    parser.add_argument(
        "--model",
        type=str,
        default="models/gemini-2.5-pro",
        help="Modelo Gemini a ser utilizado (padrão: models/gemini-2.5-pro).",
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

    print("=== SeaDream Prompt Architect Chat ===")
    print("Digite seu briefing e pressione Enter. Comandos: /theme <nome>, /model <nome>, /quit")

    while True:
        try:
            user_input = input(f"({current_theme})> ").strip()
        except EOFError:
            print("\nEncerrando chat.")
            break

        if not user_input:
            continue

        if user_input.lower() in {"/quit", "/exit"}:
            print("Encerrado.")
            break

        if user_input.startswith("/theme"):
            parts = user_input.split(maxsplit=1)
            if len(parts) == 2 and parts[1] in THEME_LIST:
                current_theme = parts[1]
                print(f"Tema atualizado para {current_theme}.")
            else:
                print("Temas disponíveis: " + ", ".join(THEME_LIST))
            continue

        if user_input.startswith("/model"):
            parts = user_input.split(maxsplit=1)
            if len(parts) == 2:
                current_model = parts[1]
                print(f"Modelo atualizado para {current_model}.")
            else:
                print("Uso: /model models/gemini-2.5-pro")
            continue

        try:
            run_interaction(user_input, current_model, current_theme)
        except Exception as exc:  # pragma: no cover
            print(f"[ERRO] {exc}")


if __name__ == "__main__":
    main()
