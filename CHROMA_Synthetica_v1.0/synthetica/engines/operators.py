# synthetica/engines/operators.py

# (v1.1) Importações atualizadas
from synthetica.core.models import AbstractCreativeObject, ACOCompositionalFlow, IntermediateTechnicalIntent, CulturalCannibalizeDirective, ACOArchetypalDynamics, ACOSubject
from synthetica.core.knowledge_broker import KnowledgeBroker

# (v1.1) Renomeado para OperatorsEngine para refletir escopo expandido
class OperatorsEngine:
    """
    (Synthetica v1.1): Motor de Operadores (Cognitivos e Conceituais).
    Modifica o ACO e gera diretivas no ITI.
    """
    def __init__(self, broker: KnowledgeBroker):
        self.broker = broker

    def apply(self, operator_name: str, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent, params: dict = {}):
        """Gateway para aplicar operadores."""
        if hasattr(self, operator_name):
            print(f"✨: Aplicando Operador: {operator_name}...")
            # Passa o ITI e parâmetros opcionais para o operador
            success = getattr(self, operator_name)(aco, iti, **params)
            if success:
                aco.applied_operators.append(operator_name)
        else:
            print(f"⚠️: Operador '{operator_name}' não encontrado.")

    # --- Operadores Cognitivos (Neuroestética) ---

    def Operator_ImposeSymmetry(self, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent, **kwargs):
        # (Implementação anterior mantida)
        if not aco.intent.compositional_flow:
            aco.intent.compositional_flow = ACOCompositionalFlow()
        aco.intent.compositional_flow.path = "symmetrical_balance"
        iti.reasoning_chain.append("Cognitivo: Aplicado Operator_ImposeSymmetry.")
        return True

    # --- Operadores Conceituais (Pilar 2, 3 e 4) ---

    def Operator_DefineHybridism(self, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent, subject_id: str, ontology_ref: str, variant: str = None, **kwargs):
        """(v1.1) Define a ontologia híbrida de um sujeito (Pilar 2)."""
        subject_found = False
        for subject in aco.elements.subjects:
            if subject.id == subject_id:
                subject.hybrid_ontology_ref = ontology_ref
                subject.hybrid_variant = variant
                subject_found = True
                iti.reasoning_chain.append(f"Conceitual (Hibridismo): Definido '{subject_id}' como '{ontology_ref.split('.')[-1]}' (Variante: {variant}).")
                break
        
        if not subject_found:
            iti.reasoning_chain.append(f"❌ Erro Hibridismo: Sujeito '{subject_id}' não encontrado no ACO.")
            return False
        return True

    def Operator_CulturalCannibalize(self, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent, devouring_culture: str, devoured_element: str, synthesis_mode: str = "Aesthetic", **kwargs):
        """(v1.1) Implementação do Operador de Antropofagia (Pilar 3)."""
        
        # Validação básica dos caminhos
        if not self.broker.get_entry(devouring_culture):
            iti.reasoning_chain.append(f"❌ Erro Antropofagia: Cultura devoradora '{devouring_culture}' não encontrada na KB.")
            return False
            
        if not self.broker.get_entry(devoured_element):
            iti.reasoning_chain.append(f"❌ Erro Antropofagia: Elemento devorado '{devoured_element}' não encontrado na KB.")
            return False

        # Cria a diretiva para o EnrichmentService processar
        directive = CulturalCannibalizeDirective(
            devouring_culture=devouring_culture,
            devoured_element=devoured_element,
            synthesis_mode=synthesis_mode
        )
        iti.abstract_directives.antropofagia_directive = directive
        iti.reasoning_chain.append(f"Conceitual (Antropofagia): Diretiva criada ({devouring_culture.split('.')[-1]} devora {devoured_element.split('.')[-1]}).")
        return True

    def Operator_SetArchetypalDynamics(self, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent, shadow_state: str, manifestation: str = None, trickster: str = None, **kwargs):
        """(v1.1) Define os parâmetros psicológicos no ACO (Pilar 4)."""
        
        # Validação do estado da sombra contra a KB (2.8)
        valid_states_path = "2.0_Semiotics_and_Psychology_Database.2.8_Archetypal_Dynamics_Framework (Jungian).Parameters.Shadow_Integration_State.Values"
        valid_states = self.broker.get_entry(valid_states_path, default=[])
        
        if shadow_state not in valid_states:
             iti.reasoning_chain.append(f"❌ Erro Dinâmica Arquetípica: Estado '{shadow_state}' inválido. Válidos: {valid_states}.")
             return False

        # Define a dinâmica no ACO
        dynamics = ACOArchetypalDynamics(
            shadow_integration_state=shadow_state,
            shadow_manifestation=manifestation,
            trickster_function=trickster
        )
        aco.intent.archetypal_dynamics = dynamics
        
        # Passa o estado psicológico para o ITI para que o EnrichmentService use a Translation Matrix
        iti.abstract_directives.psychological_state = shadow_state
        
        iti.reasoning_chain.append(f"Conceitual (Psicologia): Definida Dinâmica Arquetípica (Estado: {shadow_state}).")
        return True