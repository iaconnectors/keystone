"""Motor de operadores cognitivos e conceituais do Synthetica."""
from typing import Any, Dict, Optional

from synthetica.core.knowledge_broker import KnowledgeBroker
from synthetica.core.models import (
    ACOArchetypalDynamics,
    ACOCompositionalFlow,
    AbstractCreativeObject,
    CulturalCannibalizeDirective,
    IntermediateTechnicalIntent,
)


class OperatorsEngine:
    """Orquestra a aplicação dos operadores do sistema."""

    def __init__(self, broker: KnowledgeBroker):
        self.broker = broker

    def apply(
        self,
        operator_name: str,
        aco: AbstractCreativeObject,
        iti: IntermediateTechnicalIntent,
        params: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Gateway para aplicar operadores com parâmetros opcionais."""
        params = params or {}
        if hasattr(self, operator_name):
            print(f"✨: Aplicando Operador: {operator_name}...")
            success = getattr(self, operator_name)(aco, iti, **params)
            if success:
                aco.applied_operators.append(operator_name)
        else:
            print(f"⚠️: Operador '{operator_name}' não encontrado.")

    # --- Operadores Cognitivos (Neuroestética) ---

    def Operator_ImposeSymmetry(
        self,
        aco: AbstractCreativeObject,
        iti: IntermediateTechnicalIntent,
        **_: Any,
    ) -> bool:
        if not aco.intent.compositional_flow:
            aco.intent.compositional_flow = ACOCompositionalFlow()
        aco.intent.compositional_flow.path = "symmetrical_balance"
        iti.reasoning_chain.append("Cognitivo: Aplicado Operator_ImposeSymmetry.")
        return True

    # --- Operadores Conceituais (Pilares 2, 3 e 4) ---

    def Operator_DefineHybridism(
        self,
        aco: AbstractCreativeObject,
        iti: IntermediateTechnicalIntent,
        subject_id: str,
        ontology_ref: str,
        variant: Optional[str] = None,
        **_: Any,
    ) -> bool:
        subject_found = False
        for subject in aco.elements.subjects:
            if subject.id == subject_id:
                subject.hybrid_ontology_ref = ontology_ref
                subject.hybrid_variant = variant
                subject_found = True
                variant_msg = variant if variant is not None else "default"
                iti.reasoning_chain.append(
                    "Conceitual (Hibridismo): Definido "
                    f"'{subject_id}' como '{ontology_ref.split('.')[-1]}' "
                    f"(Variante: {variant_msg})."
                )
                break

        if not subject_found:
            iti.reasoning_chain.append(
                f"❌ Erro Hibridismo: Sujeito '{subject_id}' não encontrado no ACO."
            )
            return False
        return True

    def Operator_CulturalCannibalize(
        self,
        aco: AbstractCreativeObject,
        iti: IntermediateTechnicalIntent,
        devouring_culture: str,
        devoured_element: str,
        synthesis_mode: str = "Aesthetic",
        **_: Any,
    ) -> bool:
        if not self.broker.get_entry(devouring_culture):
            iti.reasoning_chain.append(
                f"❌ Erro Antropofagia: Cultura devoradora '{devouring_culture}' não encontrada na KB."
            )
            return False

        if not self.broker.get_entry(devoured_element):
            iti.reasoning_chain.append(
                f"❌ Erro Antropofagia: Elemento devorado '{devoured_element}' não encontrado na KB."
            )
            return False

        directive = CulturalCannibalizeDirective(
            devouring_culture=devouring_culture,
            devoured_element=devoured_element,
            synthesis_mode=synthesis_mode,
        )
        iti.abstract_directives.antropofagia_directive = directive
        devouring_label = devouring_culture.split('.')[-1]
        devoured_label = devoured_element.split('.')[-1]
        iti.reasoning_chain.append(
            f"Conceitual (Antropofagia): Diretiva criada ({devouring_label} devora {devoured_label})."
        )
        return True

    def Operator_SetArchetypalDynamics(
        self,
        aco: AbstractCreativeObject,
        iti: IntermediateTechnicalIntent,
        shadow_state: str,
        manifestation: Optional[str] = None,
        trickster: Optional[str] = None,
        **_: Any,
    ) -> bool:
        valid_states_path = (
            "2.0_Semiotics_and_Psychology_Database."
            "2.8_Archetypal_Dynamics_Framework (Jungian)."
            "Parameters.Shadow_Integration_State.Values"
        )
        valid_states = self.broker.get_entry(valid_states_path, default=[])

        if shadow_state not in valid_states:
            iti.reasoning_chain.append(
                f"❌ Erro Dinâmica Arquetípica: Estado '{shadow_state}' inválido. "
                f"Válidos: {valid_states}."
            )
            return False

        dynamics = ACOArchetypalDynamics(
            shadow_integration_state=shadow_state,
            shadow_manifestation=manifestation,
            trickster_function=trickster,
        )
        aco.intent.archetypal_dynamics = dynamics
        iti.abstract_directives.psychological_state = shadow_state
        iti.reasoning_chain.append(
            f"Conceitual (Psicologia): Definida Dinâmica Arquetípica (Estado: {shadow_state})."
        )
        return True
