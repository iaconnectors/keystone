# nexus/engines/operators.py

from nexus.core.models import AbstractCreativeObject, ACOCompositionalFlow
from nexus.core.knowledge_broker import KnowledgeBroker

class CognitiveOperators:
    """
    Pilar II.3: Framework de Impacto Cognitivo (Neuroestética).
    Operadores que modificam o ACO com base em princípios neuroestéticos (Tabela 3 do WP).
    """
    def __init__(self, broker: KnowledgeBroker):
        self.broker = broker

    def apply(self, operator_name: str, aco: AbstractCreativeObject):
        """Gateway para aplicar operadores cognitivos."""
        if hasattr(self, operator_name):
            print(f"✨: Aplicando Operador Cognitivo: {operator_name}...")
            success = getattr(self, operator_name)(aco)
            if success:
                aco.applied_cognitive_operators.append(operator_name)
        else:
            print(f"⚠️: Operador Cognitivo '{operator_name}' não encontrado.")

    # --- Implementação dos Operadores (Tabela 3) ---

    def Operator_ImposeSymmetry(self, aco: AbstractCreativeObject):
        """Princípio: Simetria. Efeito: Estabilidade, ordem."""
        if not aco.intent.compositional_flow:
            aco.intent.compositional_flow = ACOCompositionalFlow()
        
        aco.intent.compositional_flow.path = "symmetrical_balance"
        aco.intent.compositional_flow.focal_point = "center"
        return True

    def Operator_ApplyFractalStructure(self, aco: AbstractCreativeObject):
        """Princípio: Padrões Fractais. Efeito: Calma natural, biofilia."""
        if aco.elements.environment:
            # Modifica a descrição do ambiente para incluir a complexidade fractal.
            aco.elements.environment.description += " The environment incorporates mid-range fractal patterns (D≈1.3-1.5), mimicking natural structures."
            return True
        print("⚠️: Operator_ApplyFractalStructure requer um ambiente definido no ACO.")
        return False

    def Operator_AmplifyDefiningFeatures(self, aco: AbstractCreativeObject):
        """Princípio: Peak Shift. Efeito: Memorável, impactante."""
        # Implementação simplificada: Adiciona modificadores de intensidade aos sujeitos.
        if not aco.elements.subjects:
            print("⚠️: Operator_AmplifyDefiningFeatures requer sujeitos definidos no ACO.")
            return False
            
        for subject in aco.elements.subjects:
            subject.description += " The subject's defining features are exaggerated for visual impact."
            subject.attributes.append("exaggerated_proportions")
        return True

# Nota: Operadores Técnicos que atuam no PSO podem ser adicionados numa classe separada se necessário.