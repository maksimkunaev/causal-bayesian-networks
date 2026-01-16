**What & Why:**
A DiscreteBayesianNetwork models probabilistic relationships between discrete variables using directed acyclic graphs (DAGs). Used for reasoning under uncertainty, diagnosis, prediction, and causal inference.

**How it works:**
- Nodes = random variables (discrete states)
- Edges = probabilistic dependencies (A→B means A influences B)
- Each node stores a conditional probability table (CPT)
- Calculates joint probabilities by multiplying CPTs along the graph
- Inference: compute probabilities of unknowns given observed evidence

**Example - Medical Diagnosis:**
```python
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD

# Structure: Flu → Fever, Flu → Cough
model = BayesianNetwork([('Flu', 'Fever'), ('Flu', 'Cough')])

# P(Flu)
cpd_flu = TabularCPD('Flu', 2, [[0.9], [0.1]])

# P(Fever|Flu)
cpd_fever = TabularCPD('Fever', 2, 
    [[0.95, 0.1],   # No fever
     [0.05, 0.9]],  # Fever
    evidence=['Flu'], evidence_card=[2])

# P(Cough|Flu)
cpd_cough = TabularCPD('Cough', 2,
    [[0.98, 0.2],
     [0.02, 0.8]],
    evidence=['Flu'], evidence_card=[2])

model.add_cpds(cpd_flu, cpd_fever, cpd_cough)
```

Given fever+cough, it calculates flu probability via Bayes' theorem.


####


**Exactly right!** Your interpretation is correct.

**The table represents P(Fever | Flu):**

```
              Flu=0 (No)  Flu=1 (Yes)
Fever=0 (No)    0.95        0.1
Fever=1 (Yes)   0.05        0.9
```

**Reading it:**
- **Column 1 (Flu=0):** If no flu → 95% chance no fever, 5% chance fever
- **Column 2 (Flu=1):** If has flu → 10% chance no fever, 90% chance fever

Each column must sum to 1.0 (they're probability distributions).

**The logic:**
- Healthy people rarely have fever (5%)
- Sick people usually have fever (90%)

So when you observe someone with fever, the network uses Bayes' theorem to reverse-calculate: "Given they have fever, what's the probability they have flu?"



#####
**Joint Probability (Forward):**
Calculate P(Flu, Fever, Cough) by multiplying:

```
P(Flu, Fever, Cough) = P(Flu) × P(Fever|Flu) × P(Cough|Flu)
```

**Example calculation:**
```
P(Flu=1, Fever=1, Cough=1) = 0.1 × 0.9 × 0.8 = 0.072
```

The graph structure tells you which probabilities to multiply. Only multiply by parent nodes.

---

**Inference (Backward):**
You observe evidence and want to find unknowns. Uses Bayes' theorem.

**Example - observed: Fever=1, Cough=1. Want: P(Flu=1)?**

```python
from pgmpy.inference import VariableElimination

inference = VariableElimination(model)
result = inference.query(['Flu'], evidence={'Fever': 1, 'Cough': 1})
print(result)
# Flu=1: 0.86  (86% chance has flu)
# Flu=0: 0.14
```

**What happens internally:**
1. Calculate all joint probabilities matching evidence
2. Sum over unknown combinations
3. Normalize to get probability distribution

The network "reasons backwards" from symptoms to cause.