"""Fixtures compartilhadas para a suíte de testes do Synthetica."""

from __future__ import annotations

from typing import Dict, Any

import pytest

from synthetica.core.knowledge_broker import KnowledgeBroker


@pytest.fixture()
def sample_kb() -> KnowledgeBroker:
    """Retorna um KnowledgeBroker mínimo com caminhos usados nos testes."""

    kb_payload: Dict[str, Any] = {
        "KB_ID": "TEST_KB",
        "KB_Version": "0.0-test",
        "2.0_Semiotics_and_Psychology_Database": {
            "2.8_Archetypal_Dynamics_Framework (Jungian)": {
                "Parameters": {
                    "Shadow_Integration_State": {
                        "Values": ["Assimilating", "Projected", "Integrated"]
                    }
                },
                "Translation_Matrix": {
                    "Assimilating": {
                        "Aesthetic_Signifiers": [
                            "5.0_Masters_Lexicon.5.3_Art_and_Design_References.Cinematographers.Roger_Deakins",
                            "Mood.Positive_Reconciliation",
                        ]
                    }
                },
            }
        },
        "5.0_Masters_Lexicon": {
            "5.3_Art_and_Design_References": {
                "Cinematographers": ["Roger_Deakins", "Bradford_Young"]
            },
            "5.6_Fashion_and_Costume_Design": {
                "Iris van Herpen": [
                    "Complex organic couture",
                    "3D printed patterns",
                    "Futuristic silhouettes",
                ]
            },
        },
        "11.0_Narrative_Structure_and_Storytelling": {
            "11.4_Speculative_Fiction_and_Futurism": {
                "Solarpunk": [
                    "Regenerative urban design",
                    "Photosynthetic materials",
                    "Collective governance",
                ]
            }
        },
    }

    return KnowledgeBroker(kb_payload)
