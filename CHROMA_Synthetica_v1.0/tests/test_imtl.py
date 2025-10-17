"""Testes para a camada de traducao IMTL."""

from __future__ import annotations

from synthetica.core.models import ProjectStateObject
from synthetica.engines.imtl import IMTLPolicyEngine


def _build_pso() -> ProjectStateObject:
    pso = ProjectStateObject(
        source_aco_id="aco-test",
        core_concept="Futuristic arcology skyline at dawn.",
        composition="Path: symmetrical_balance",
    )
    pso.master_references.extend(["Roger_Deakins"])
    pso.visual_style_keywords.extend(["Golden hour glow", "Atmospheric haze"])
    pso.camera_package["camera"] = "shot on ARRI Alexa 35 cinema camera"
    pso.process_artifacts.append("Kodak Vision3 500T film stock")
    return pso


def test_seedream_policy_formats_modules(sample_kb) -> None:
    engine = IMTLPolicyEngine(sample_kb)
    pso = _build_pso()

    prompt = engine.translate(pso, "Seedream_4_0")

    assert "Module A - Scenario" in prompt
    assert "Module D - Capture Specs" in prompt
    assert "Kodak Vision3 500T film stock" in prompt


def test_midjourney_policy_uses_poetic_segments(sample_kb) -> None:
    engine = IMTLPolicyEngine(sample_kb)
    pso = _build_pso()

    prompt = engine.translate(pso, "Midjourney_V6")

    assert prompt.lower().startswith("imagine")
    assert "evoke in the style of Roger Deakins" in prompt


def test_default_policy_concatenates_segments(sample_kb) -> None:
    engine = IMTLPolicyEngine(sample_kb)
    pso = _build_pso()

    prompt = engine.translate(pso, "Unknown_Model")

    assert "Futuristic arcology skyline at dawn." in prompt
    assert "Golden hour glow" in prompt
    assert "shot on ARRI Alexa 35 cinema camera" in prompt
