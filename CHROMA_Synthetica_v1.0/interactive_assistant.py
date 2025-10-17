"""SeaDream prompt architect CLI (protocolo v8.0)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from synthetica.services.llm_client import GeminiClient

SEA_PLAYBOOK_PATH = Path("kb/synthetica_kb_v1.1.json")
SEA_PLAYBOOK_KEY = "16.0_Creative_Suites_Playbooks"
SEA_PLAYBOOK_ENTRY = "16.1_SeaDream_Freepik"

THEMES = [
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

DEFAULT_THEME = "cinematografico"

MODEL_TARGETS = [
    "DALL-E_3",
    "Midjourney_V6",
    "Stable_Diffusion_3",
    "Seedream_4_0",
    "Nano_Banana",
    "Flux_1",
]

EXPECTED_STRUCTURE = {
    "atmosphere": None,
    "intent": None,
    "image_content": {"subject": None, "action_pose": None, "environment": None},
    "composition": {"shot_type": None, "camera_angle": None, "composition_principles": None},
    "camera_lens_film": {"camera": None, "lens": None, "treatment": None},
    "lighting_color": {"lighting": None, "color_temperature": None, "palette": None},
    "dna_visual": {"reference": None, "mood": None, "quality": None},
    "output_parameters": {"framing": None, "delivery": None, "consistency": None},
    "checklist_questions": list,
    "notes": list,
}


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------


def _load_playbook() -> Dict[str, Any]:
    data = json.loads(SEA_PLAYBOOK_PATH.read_text(encoding="utf-8"))
    playbook = data.get(SEA_PLAYBOOK_KEY, {}).get(SEA_PLAYBOOK_ENTRY)
    if playbook is None:
        raise SystemExit("SeaDream playbook not found in KB. Please migrate the KB first.")
    return playbook


def _collect_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for nested in value.values():
            yield from _collect_strings(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _collect_strings(nested)


def _payload_is_english(payload: Dict[str, Any]) -> bool:
    for text in _collect_strings(payload):
        if not text:
            continue
        if any(ord(ch) >= 128 for ch in text):
            return False
    return True


def _request_payload(llm: GeminiClient, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
    prompt = user_prompt
    last_payload: Dict[str, Any] | None = None
    for _ in range(3):
        last_payload = llm.generate_json(system_prompt, prompt)
        if _payload_is_english(last_payload):
            return last_payload
        prompt += "\nRewrite the entire response strictly in English (ASCII only)."
    raise RuntimeError("Gemini did not return an English response after retries.")


def _ensure_ascii(text: str, llm: GeminiClient) -> str:
    if not text or all(ord(ch) < 128 for ch in text):
        return text
    translation_prompt = (
        "Translate the following text into natural English (ASCII only). "
        "Return only the translated sentence without explanations:\n"
        f"{text}"
    )
    translated = llm.generate_json(
        'Return the translation as a JSON object {"translation": "..."}.',
        translation_prompt,
    )
    return translated.get("translation", text)


def _normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "atmosphere": payload.get("atmosphere"),
        "intent": payload.get("intent"),
        "image_content": payload.get("image_content") or {},
        "composition": payload.get("composition") or {},
        "camera_lens_film": payload.get("camera_lens_film") or payload.get("camera") or {},
        "lighting_color": payload.get("lighting_color") or {},
        "dna_visual": payload.get("dna_visual") or {},
        "output_parameters": payload.get("output_parameters") or {},
        "checklist_questions": payload.get("checklist_questions") or [],
        "notes": payload.get("notes") or [],
    }

    if isinstance(result["camera_lens_film"], str):
        result["camera_lens_film"] = {
            "camera": result["camera_lens_film"],
            "lens": None,
            "treatment": None,
        }

    return result


def _missing_fields(payload: Dict[str, Any]) -> List[Tuple[str, str | None]]:
    missing: List[Tuple[str, str | None]] = []
    for key, template in EXPECTED_STRUCTURE.items():
        value = payload.get(key)
        if isinstance(template, dict):
            if not isinstance(value, dict):
                value = payload[key] = {}
            for sub_key in template:
                sub_value = value.get(sub_key)
                if not sub_value or not str(sub_value).strip():
                    missing.append((key, sub_key))
        elif template is list:
            payload.setdefault(key, [])
        else:
            if not value or not str(value).strip():
                missing.append((key, None))
    return missing


def _set_field(payload: Dict[str, Any], component: str, field: str | None, value: str) -> None:
    if field is None:
        payload[component] = value
    else:
        payload.setdefault(component, {})
        payload[component][field] = value


def _enforce_defaults(payload: Dict[str, Any], theme_defaults: Dict[str, Any], llm: GeminiClient) -> None:
    defaults = theme_defaults.get("defaults", {})
    camera_block = payload["camera_lens_film"]

    camera_text = camera_block.get("camera") or ""
    if "arri" not in camera_text.lower() and "arriflex" not in camera_text.lower():
        camera_block["camera"] = defaults.get("camera", "shot on ARRI Alexa 35 cinema camera")

    lens_text = camera_block.get("lens") or ""
    if not lens_text or any(word in lens_text.lower() for word in ["dslr", "mirrorless"]):
        camera_block["lens"] = defaults.get("lens", "using Cooke anamorphic prime lenses")

    treatment = camera_block.get("treatment")
    if not treatment:
        camera_block["treatment"] = defaults.get(
            "treatment", "captured on Kodak Vision3 500T film stock with subtle grain"
        )

    reference = payload["dna_visual"].get("reference") or ""
    aliases = defaults.get("dp_aliases", [])
    if not any(alias.lower() in reference.lower() for alias in aliases):
        dp_name = defaults.get("dp", "Roger Deakins")
        payload["dna_visual"]["reference"] = (
            f"{reference} | in the style of {dp_name}" if reference else dp_name
        )

    for comp, field in EXPECTED_STRUCTURE.items():
        if isinstance(field, dict):
            for sub in field:
                text = payload[comp].get(sub)
                if text:
                    payload[comp][sub] = _ensure_ascii(text, llm)
        elif comp in payload and payload[comp]:
            payload[comp] = _ensure_ascii(payload[comp], llm)


def _format_blueprint(payload: Dict[str, Any], theme_key: str, theme_desc: str) -> str:
    ic = payload["image_content"]
    comp = payload["composition"]
    cam = payload["camera_lens_film"]
    light = payload["lighting_color"]
    dna = payload["dna_visual"]
    output = payload["output_parameters"]

    sections = [
        ("Theme", f"{theme_key} - {theme_desc}"),
        ("Atmosphere", payload["atmosphere"]),
        ("Intent", payload["intent"]),
        ("Image/Frame Content", f"subject: {ic['subject']} | action: {ic['action_pose']} | environment: {ic['environment']}"),
        (
            "Cinematography/Composition",
            f"shot type: {comp['shot_type']} | angle: {comp['camera_angle']} | principles: {comp['composition_principles']}",
        ),
        (
            "Camera, Lens & Film",
            f"camera: {cam['camera']} | lens: {cam['lens']} | treatment: {cam['treatment']}",
        ),
        (
            "Lighting & Color",
            f"quality: {light['lighting']} | temperature: {light['color_temperature']} | palette: {light['palette']}",
        ),
        (
            "Visual DNA & Style",
            f"reference: {dna['reference']} | mood: {dna['mood']} | refinements: {dna['quality']}",
        ),
        (
            "Output Parameters",
            f"framing: {output['framing']} | delivery: {output['delivery']} | consistency: {output['consistency']}",
        ),
    ]
    formatted = []
    width = max(len(label) for label, _ in sections)
    for label, value in sections:
        formatted.append(f"{label:<{width}} : {value}")
    return "\n".join(formatted)


def _build_prompt_text(payload: Dict[str, Any]) -> str:
    ic = payload["image_content"]
    comp = payload["composition"]
    cam = payload["camera_lens_film"]
    light = payload["lighting_color"]
    dna = payload["dna_visual"]
    output = payload["output_parameters"]

    return (
        f"Atmosphere: {payload['atmosphere']}. "
        f"Intent: {payload['intent']}. "
        f"Subject: {ic['subject']} performing {ic['action_pose']} within {ic['environment']}. "
        f"Cinematography: {comp['shot_type']} shot from {comp['camera_angle']} with {comp['composition_principles']}. "
        f"Camera setup: {cam['camera']} paired with {cam['lens']} and treatment {cam['treatment']}. "
        f"Lighting: {light['lighting']} with {light['color_temperature']} color temperature and palette {light['palette']}. "
        f"Visual DNA: {dna['reference']} mood {dna['mood']} and refinements {dna['quality']}. "
        f"Output: {output['framing']} | {output['delivery']} | {output['consistency']}."
    )


def _build_model_prompts(payload: Dict[str, Any], theme_desc: str) -> Dict[str, str]:
    base = _build_prompt_text(payload)
    return {
        "DALL-E_3": base,
        "Midjourney_V6": f"{base} :: cinematic quality --stylize 250 --quality 2 --v 6",
        "Stable_Diffusion_3": (
            f"PROMPT: {base}\n"
            "NEGATIVE PROMPT: blurry, low quality, amateur lighting, distorted anatomy, watermark"
        ),
        "Seedream_4_0": base,
        "Nano_Banana": f"{base} // playful, bold typographic rhythm",
        "Flux_1": f"Creative brief: {theme_desc}. {base}",
    }


# ---------------------------------------------------------------------------
# Main execution flow
# ---------------------------------------------------------------------------


def run_interaction(user_brief: str, model_name: str, theme_key: str) -> None:
    playbook = _load_playbook()
    themes = playbook.get("themes", {})
    if theme_key not in themes:
        raise SystemExit(f"Tema '{theme_key}' não está configurado. Temas disponíveis: {', '.join(themes)}")
    theme_data = themes[theme_key]
    theme_desc = theme_data.get("description", theme_key)

    llm = GeminiClient(model_name=model_name)
    system_prompt = build_system_prompt(playbook, theme_key, theme_data)
    user_prompt = build_user_prompt(user_brief, theme_key)
    payload_raw = _request_payload(llm, system_prompt, user_prompt)
    payload = _normalize_payload(payload_raw)

    missing = _missing_fields(payload)
    while missing:
        print("\n=== Campos obrigatórios pendentes ===")
        for comp, field in missing:
            if field:
                print(f"- {comp}.{field}")
            else:
                print(f"- {comp}")
        print("Forneça respostas em inglês para os itens acima.")
        for comp, field in missing:
            prompt = f"{comp}.{field} (English): " if field else f"{comp} (English): "
            answer = input(prompt).strip()
            while not answer:
                answer = input("Valor obrigatório. Informe novamente: ").strip()
            _set_field(payload, comp, field, answer)
        missing = _missing_fields(payload)

    _enforce_defaults(payload, theme_data, llm)
    blueprint = _format_blueprint(payload, theme_key, theme_desc)
    prompts = _build_model_prompts(payload, theme_desc)

    print("\n" + "=" * 100)
    print(f"SeaDream v8.0 Blueprint - Theme: {theme_key}")
    print("=" * 100)
    print(blueprint)
    print("=" * 100)
    if payload.get("checklist_questions"):
        print("Checklist / Questions:")
        for item in payload["checklist_questions"]:
            print(f"- {item}")
        print("-" * 100)
    if payload.get("notes"):
        print("Notes:")
        for note in payload["notes"]:
            print(f"- {note}")
        print("-" * 100)

    print("Prompts por modelo:")
    for model in MODEL_TARGETS:
        print(f"\n[{model}]")
        print(prompts[model])
    print("=" * 100)


def build_system_prompt(manual: Dict[str, Any], theme_key: str, theme_data: Dict[str, Any]) -> str:
    framework = manual.get("framework_prompt_seedream4", {})
    estrutura = framework.get("estrutura_mestra", [])
    regras = framework.get("regras", [])
    melhores_praticas = manual.get("melhores_praticas", [])
    capacidades = manual.get("o_que_faz", {}).get("capacidade", [])
    ferramentas = manual.get("o_que_possui", {}).get("ai_suite", [])

    theme_description = theme_data.get("description", theme_key)
    estrutura_formatada = "\n".join(f"- {item}" for item in estrutura)
    regras_formatadas = "\n".join(f"- {item}" for item in regras)
    praticas_formatadas = "\n".join(f"- {item}" for item in melhores_praticas)
    capacidades_str = ", ".join(capacidades)
    ferramentas_str = ", ".join(ferramentas)

    context = theme_data.get("context", "cinematic")
    mode_description = (
        "DPV - Cinema (narrativa, emoção, léxico cinematográfico)"
        if context == "cinematic"
        else "DPV - Comercial (apelo visual, clareza de marca, léxico publicitário)"
    )

    return (
        "You are GEM, the SeaDream 4.0 Prompt Architect. "
        f"Operate strictly as a Director of Photography Virtual in '{mode_description}'. "
        "Your mission is to fill every field of the SeaDream Formula v8.0 (6 components × 3 sub-elements) "
        "with precise, cinematic language. Ask questions only via the 'checklist_questions' array.\n\n"
        "Return JSON exactly as:\n"
        "{\n"
        '  "atmosphere": "string",\n'
        '  "intent": "string",\n'
        '  "image_content": {\n'
        '    "subject": "string",\n'
        '    "action_pose": "string",\n'
        '    "environment": "string"\n'
        "  },\n"
        '  "composition": {\n'
        '    "shot_type": "string",\n'
        '    "camera_angle": "string",\n'
        '    "composition_principles": "string"\n'
        "  },\n"
        '  "camera_lens_film": {\n'
        '    "camera": "string",\n'
        '    "lens": "string",\n'
        '    "treatment": "string"\n'
        "  },\n"
        '  "lighting_color": {\n'
        '    "lighting": "string",\n'
        '    "color_temperature": "string",\n'
        '    "palette": "string"\n'
        "  },\n"
        '  "dna_visual": {\n'
        '    "reference": "string",\n'
        '    "mood": "string",\n'
        '    "quality": "string"\n'
        "  },\n"
        '  "output_parameters": {\n'
        '    "framing": "string",\n'
        '    "delivery": "string",\n'
        '    "consistency": "string"\n'
        "  },\n"
        '  "checklist_questions": ["string"],\n'
        '  "notes": ["string"]\n'
        "}\n\n"
        "Rules:\n"
        f"{regras_formatadas}\n\n"
        "Best practices:\n"
        f"{praticas_formatadas}\n\n"
        "Master structure order:"
        f"{estrutura_formatada}\n\n"
        "Core capabilities: " + capacidades_str + "\n"
        "Relevant AI Suite tools: " + ferramentas_str + "\n"
        "Always mention a renowned cinematographer/director/photographer in Visual DNA or Camera. "
        "Use only cinema cameras (ARRI/Arriflex, film cameras) unless the user explicitly requests otherwise. "
        "Respond strictly in English and ensure all sub-elements are populated."
    )


def build_user_prompt(user_brief: str, theme_key: str) -> str:
    return (
        f"Theme: {theme_key}\n"
        "SeaDream briefing (Portuguese or English accepted as input):\n"
        f"{user_brief}\n\n"
        "If information is missing, include questions in 'checklist_questions' for the Director."
    )


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="SeaDream v8.0 prompt architect CLI.")
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
    parser.add_argument(
        "--theme",
        type=str,
        choices=THEMES,
        default=DEFAULT_THEME,
        help="Tema alvo (cinematografico, publicitario, design, arquitetura, montagem_de_stands, "
        "criacao_de_personagem, criacao_de_cena, estudo_de_objeto, estudo_de_personagem).",
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

    run_interaction(user_brief, args.model, args.theme)


if __name__ == "__main__":
    main()

