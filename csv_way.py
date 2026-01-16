import pandas as pd
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator

# --- PHASE 1: DATA ---
# We have 3 variables. Total possible combinations = 8.
# Our data only covers 4 of those combinations.
df = pd.DataFrame(
    {
        "CloseRelationship": [1, 1, 0, 0, 1],
        "Argument": [1, 0, 1, 0, 1],
        "Silence": [0, 1, 1, 0, 0],
    }
)

model = DiscreteBayesianNetwork(
    [
        ("CloseRelationship", "Silence"),
        ("Argument", "Silence"),
    ]
)


# --- PHASE 3: THE ESTIMATOR (The "Filling" Process) ---
# This algorithm looks at the rows we have and fills the TabularCPD.
model.fit(
    df,
    # estimator=BayesianEstimator,
    estimator=MaximumLikelihoodEstimator,
    # prior_type="dirichlet",
    # pseudo_counts=1,
)


# --- PHASE 4: THE TabularCPD (The Resulting Table) ---
# Now we can look at the "Hidden" table the estimator built.
# This table is what 'VariableElimination' will use to answer you.
def display_table(model, variable):
    cpd = model.get_cpds(variable)
    evidence_vars = cpd.variables[1:]
    evidence_card = cpd.cardinality[1:]

    print(f"CPD shape: {cpd.values.shape}")
    print(cpd.values)

    header = f"{'CloseRel':<12}{'Argument':<12}{'P(Silence=0)':<15}{'P(Silence=1)':<15}"
    print(header)
    print("-" * 54)

    for rel in [0, 1]:
        for arg in [0, 1]:
            p_no = cpd.values[0, rel, arg]
            p_yes = cpd.values[1, rel, arg]
            print(f"{rel:<12}{arg:<12}{p_no:<15.4f}{p_yes:<15.4f}")


display_table(model, "Silence")
