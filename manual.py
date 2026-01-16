from pprint import pprint
import pandas as pd
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator, BayesianEstimator
from pgmpy.inference import VariableElimination
import itertools

# === LOAD DATA ===
df = pd.read_csv("startup_dataset.csv")
print(f"Loaded {len(df)} cases\n")

# === DEFINE STRUCTURE ===
model = DiscreteBayesianNetwork(
    [
        ("founder_experience", "funding"),
        ("founder_experience", "success"),
        ("market_timing", "success"),
        ("funding", "team_size"),
        ("team_size", "success"),
    ]
)

# === TRAIN MODEL ===
model.fit(df, estimator=BayesianEstimator)
print("✅ Model trained\n")

cpd = model.get_cpds("success")

# === 1. BASIC INFO ===
print("Variable:", cpd.variable)
print("All variables (including evidence):", cpd.variables)
print("Cardinality (number of states):", cpd.cardinality)
print("Table shape:", cpd.values.shape)
print("Total elements:", cpd.values.size)
print()

# === 2. FIRST 10 ELEMENTS (flat array) ===
print("First 10 elements (flat):")
print(cpd.values.flatten()[:10])
print()

# === 3. FULL TABLE (slice) ===
print("First columns of table:")
print(cpd.values[:, :10])  # First 10 columns
print()

# === 4. READABLE FORMAT ===
print("Readable format:")
print(cpd)
# 5. Access specific probability
# P(success=1 | founder_experience=1, market_timing=1, team_size=2)
prob = cpd.values[1, 1, 1, 2]  # [success_value, founder_exp, market_timing, team_size]
print(f"P(success=1 | founder=1, timing=1, team=2) = {prob:.3f}")


# === DISPLAY CPT TABLE ===
def show_cpt(model, variable):
    cpd = model.get_cpds(variable)

    # Get evidence variables and their cardinalities
    evidence_vars = cpd.variables[1:]
    evidence_cards = cpd.cardinality[1:]

    # Generate all combinations
    if evidence_vars:
        combos = list(itertools.product(*[range(c) for c in evidence_cards]))

        # Header
        header = " | ".join([f"{v:20s}" for v in evidence_vars])
        header += " | " + " | ".join(
            [f"P({variable}={i})" for i in range(cpd.cardinality[0])]
        )
        print(header)
        print("-" * len(header))

        # Rows
        for combo in combos:
            row = " | ".join([f"{val:20d}" for val in combo])
            probs = " | ".join(
                [f"{cpd.values[(i,) + combo]:.3f}" for i in range(cpd.cardinality[0])]
            )
            row += " | " + probs
            print(row)
    else:
        # No evidence (root node)
        print(f"P({variable}=0) = {cpd.values[0]:.3f}")
        print(f"P({variable}=1) = {cpd.values[1]:.3f}")

    print("\n")


# === SHOW ALL CPTs ===
print("=" * 80)
print("CPT: success")
print("=" * 80)
show_cpt(model, "success")

print("=" * 80)
print("CPT: team_size")
print("=" * 80)
show_cpt(model, "team_size")

print("=" * 80)
print("CPT: funding")
print("=" * 80)
show_cpt(model, "funding")

# === INFERENCE EXAMPLE ===
inference = VariableElimination(model)

# Question: What's P(success=1) if founder_experience=1 and market_timing=1?
result = inference.query(
    [
        "success",
        # "founder_experience",
        # "funding",
        # "market_timing",
        # "team_size",
    ],
    evidence={
        # "success": 0,
        "founder_experience": 1,
        # "funding": 0,
        # "market_timing": 1,
        # "team_size": 1,
    },
)

print("QUERY: What is the probability")
print(result)
