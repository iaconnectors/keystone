"""CLI para interação com a CHROMA Synthetica usando Gemini + KB."""

import argparse
from pathlib import Path
from typing import Any, Dict, List

from synthetica.core.models import (
    ACOArchetypalDynamics,
    ACOSubject,
    AbstractCreativeObject,
)
from synthetica.orchestrator import ChromaSyntheticaOrchestrator
from synthetica.services.llm_client import GeminiClient


TARGET_MODELS = [
    "DALL-E_3",
    "Midjourney_V6",
    "Stable_Diffusion_3",
    "Seedream_4_0",
    "Nano_Banana",
    "Flux_1",
]


def build_context(broker) -> str:
    """Extrai trechos da KB para orientar o LLM."""
    design_principles = broker.get_entry(
        "1.0_Ontology_and_Philosophy.Design_Principles", default=[]
    ) or []
    hybrid_nodes = broker.get_entry("2.0_Semiotics_and_Psychology_Database.2.7_Theriocephalic_Iconography", default={}) or {}
    hybrid_options = [
        f"{name} (variants: {', '.join(node.get('Variants', {}).keys())})"
        for name, node in hybrid_nodes.items()
        if isinstance(node, dict) and name != "Description"
    ]
    shadow_states = broker.get_entry(
        "2.0_Semiotics_and_Psychology_Database."
        "2.8_Archetypal_Dynamics_Framework (Jungian)."
        "Parameters.Shadow_Integration_State.Values",
        default=[],
    ) or []
    anthropophagy_examples = broker.get_entry(
        "4.0_Creative_Operators_and_Engines.4.4_Conceptual_Operators.Operator_CulturalCannibalize.Best_Practices",
        default=[],
    ) or []

    context_lines = [
        "Design principles:",
        *[f"- {item}" for item in design_principles],
        "",
        "Hybrid ontology options:",
        *[f"- {item}" for item in hybrid_options],
        "",
        "Shadow integration states: " + ", ".join(shadow_states),
        "",
        "Anthropophagy guidelines:",
    ]
    context_lines.extend(f"- {tip}" for tip in anthropophagy_examples)
    return "\n".join(context_lines)


def build_system_prompt(context: str) -> str:
    return (
        "Você é o analista criativo do CHROMA Synthetica. "
        "Receberá um briefing do usuário e um excerto da base de conhecimento. "
        "Com base nessas informações, devolva um JSON que descreva um AbstractCreativeObject e as diretivas necessárias. "
        "Formato obrigatório:\n"
        "{\n"
        '  "narrative_moment": "string",\n'
        '  "subjects": [\n'
        '    {\n'
        '      "id": "string",\n'
        '      "description": "string",\n'
        '      "hybrid_ontology_ref": "caminho da KB ou null",\n'
        '      "hybrid_variant": "string ou null"\n'
        "    }\n"
        "  ],\n"
        '  "anthropophagy": {\n'
        '      "devouring_culture": "caminho KB",\n'
        '      "devoured_element": "caminho KB",\n'
        '      "synthesis_mode": "Aesthetic | Narrative | Symbolic"\n'
        "  } ou null,\n"
        '  "archetypal_dynamics": {\n'
        '      "shadow_state": "valor das opções fornecidas",\n'
        '      "manifestation": "caminho KB ou null",\n'
        '      "trickster": "Internal_Catalyst|External_Agent|null"\n'
        "  } ou null\n"
        "}\n"
        "Não inclua texto extra além do JSON."
        "\n\nTrechos relevantes da KB:\n"
        f"{context}"
    )


def build_user_prompt(user_brief: str) -> str:
    return (
        "Briefing fornecido pelo usuário:\n"
        f"{user_brief}\n\n"
        "Responda somente com o JSON solicitado."
    )


def create_aco_from_payload(payload: Dict[str, Any]) -> (AbstractCreativeObject, List[Dict[str, Any]]):
    aco = AbstractCreativeObject()
    aco.intent.narrative_moment = payload.get("narrative_moment", "")

    for idx, subj_data in enumerate(payload.get("subjects", []), start=1):
        subject = ACOSubject(
            id=subj_data.get("id") or f"Subject{idx}",
            description=subj_data.get("description", "Creative subject"),
            hybrid_ontology_ref=subj_data.get("hybrid_ontology_ref"),
            hybrid_variant=subj_data.get("hybrid_variant"),
        )
        aco.elements.subjects.append(subject)

    dynamics_data = payload.get("archetypal_dynamics")
    if dynamics_data:
        aco.intent.archetypal_dynamics = ACOArchetypalDynamics(
            shadow_integration_state=dynamics_data.get("shadow_state"),
            shadow_manifestation=dynamics_data.get("manifestation"),
            trickster_function=dynamics_data.get("trickster"),
        )

    operator_pipeline: List[Dict[str, Any]] = []

    for subject in aco.elements.subjects:
        if subject.hybrid_ontology_ref:
            operator_pipeline.append(
                {
                    "name": "Operator_DefineHybridism",
                    "params": {
                        "subject_id": subject.id,
                        "ontology_ref": subject.hybrid_ontology_ref,
                        "variant": subject.hybrid_variant,
                    },
                }
            )

    anthropophagy = payload.get("anthropophagy") or {}
    if anthropophagy.get("devouring_culture") and anthropophagy.get("devoured_element"):
        operator_pipeline.append(
            {
                "name": "Operator_CulturalCannibalize",
                "params": {
                    "devouring_culture": anthropophagy["devouring_culture"],
                    "devoured_element": anthropophagy["devoured_element"],
                    "synthesis_mode": anthropophagy.get("synthesis_mode", "Aesthetic"),
                },
            }
        )

    if dynamics_data and dynamics_data.get("shadow_state"):
        operator_pipeline.append(
            {
                "name": "Operator_SetArchetypalDynamics",
                "params": {
                    "shadow_state": dynamics_data["shadow_state"],
                    "manifestation": dynamics_data.get("manifestation"),
                    "trickster": dynamics_data.get("trickster"),
                },
            }
        )

    return aco, operator_pipeline


def run_interaction(user_brief: str, model_name: str) -> None:
    orchestrator = ChromaSyntheticaOrchestrator()
    broker = orchestrator.broker

    context = build_context(broker)
    system_prompt = build_system_prompt(context)
    user_prompt = build_user_prompt(user_brief)

    llm = GeminiClient(model_name=model_name)
    payload = llm.generate_json(system_prompt, user_prompt)

    aco, pipeline = create_aco_from_payload(payload)

    print("\n=== JSON gerado pelo Gemini ===")
    print(payload)

    print("\n=== Gerando prompts com a CHROMA Synthetica ===")
    orchestrator.run_workflow(aco, TARGET_MODELS, operator_pipeline=pipeline)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Assistente interativo CHROMA Synthetica + Gemini."
    )
    parser.add_argument(
        "--prompt",
        type=str,
        help="Briefing textual do usuário. Se omitido, será solicitado via stdin.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="models/gemini-2.5-pro",
        help="Modelo Gemini a ser utilizado (padrão: models/gemini-2.5-pro).",
    )
    args = parser.parse_args()

    if args.prompt:
        user_brief = args.prompt
    else:
        print("Digite o briefing criativo (Ctrl+D/Ctrl+Z para concluir):")
        user_brief = ""
        try:
            while True:
                line = input()
                user_brief += line + "\n"
        except EOFError:
            user_brief = user_brief.strip()

    if not user_brief:
        raise SystemExit("Nenhum briefing fornecido.")

    run_interaction(user_brief, args.model)


if __name__ == "__main__":
    main()
