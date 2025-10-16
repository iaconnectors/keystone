# synthetica/engines/operators.py

from synthetica.core.models import AbstractCreativeObject, ACOCompositionalFlow, IntermediateTechnicalIntent
from synthetica.core.knowledge_broker import KnowledgeBroker

class CognitiveOperators:
    """
    (Synthetica v1.0): Atualizado para gerar diretivas no ITI (Pilar 1.2).
    """
    def __init__(self, broker: KnowledgeBroker):
        # Usa o Broker de Raciocínio (Nexus KB)
        self.broker = broker

    def apply(self, operator_name: str, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent):
        """Gateway para aplicar operadores cognitivos."""
        if hasattr(self, operator_name):
            print(f"✨: Aplicando Operador Cognitivo: {operator_name}...")
            # Passa o ITI para o operador para que ele possa adicionar diretivas
            success = getattr(self, operator_name)(aco, iti)
            if success:
                aco.applied_cognitive_operators.append(operator_name)
        else:
            print(f"⚠️: Operador Cognitivo '{operator_name}' não encontrado.")

    # --- Implementação dos Operadores ---

    def Operator_ImposeSymmetry(self, aco: AbstractCreativeObject, iti: IntermediateTechnicalIntent):
        """Princípio: Simetria."""
        if not aco.intent.compositional_flow:
            aco.intent.compositional_flow = ACOCompositionalFlow()
        
        aco.intent.compositional_flow.path = "symmetrical_balance"
        
        # (Synthetica v1.0) Gera diretiva de consulta proativa (WP 1.2)
        narrative = aco.intent.narrative_moment.lower() if aco.intent.narrative_moment else ""
        
        if "building" in narrative or "architecture" in narrative:
             query = ["architects known for symmetry"]
             # Inferência contextual
             if "concrete" in narrative or "brutalism" in narrative:
                 query.append("brutalism")
                 
             iti.abstract_directives.master_references_query.extend(query)
             iti.reasoning_chain.append(f"Cognitivo: Aplicado Operator_ImposeSymmetry. Gerada query: {query}.")
        else:
             iti.reasoning_chain.append("Cognitivo: Aplicado Operator_ImposeSymmetry.")
             
        return True