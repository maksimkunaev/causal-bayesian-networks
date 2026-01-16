import pandas as pd
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator, BayesianEstimator
from pgmpy.inference import VariableElimination
from helpers import display_table

# --- PHASE 1: DATA ---
# Variables that affect Alice's decisions/outcomes

data = {
    "bottle_labeled": [1, 1, 0, 0, 1, 1],  # 1=has label, 0=no label
    "alice_cautious": [1, 0, 1, 0, 1, 1],  # 1=checks for poison
    "alice_drinks": [1, 1, 0, 0, 1, 0],  # outcome
    "size_changed": [1, 1, 0, 0, 1, 1],  # after drinking
    "can_reach_key": [0, 0, 1, 1, 0, 1],  # if shrank too much
    "found_cake": [1, 1, 1, 0, 1, 1],
    "ate_cake": [1, 1, 0, 0, 1, 1],
    "reached_garden": [1, 0, 0, 0, 1, 0],  # final success
}
df = pd.DataFrame(data)


model = DiscreteBayesianNetwork(
    [
        ("bottle_labeled", "alice_drinks"),
        ("alice_cautious", "alice_drinks"),
        ("alice_drinks", "size_changed"),
        ("size_changed", "can_reach_key"),
        ("can_reach_key", "reached_garden"),
        ("found_cake", "ate_cake"),
        ("ate_cake", "reached_garden"),
    ]
)

# --- PHASE 3: THE ESTIMATOR (The "Filling" Process) ---
# This algorithm looks at the rows we have and fills the TabularCPD.
model.fit(
    df,
    ### Use MaximumLikelihoodEstimator - add 0s or 0.5s
    estimator=MaximumLikelihoodEstimator,
    ### Use "BayesianEstimator"
    # estimator=BayesianEstimator,
    # prior_type="dirichlet", # or "BDeu", "K2"
    # pseudo_counts=1,
    # equivalent_sample_size=5,  # strength of prior
)


# --- PHASE 4: THE TabularCPD (The Resulting Table) ---
# Now we can look at the "Hidden" table the estimator built.
# This table is what 'VariableElimination' will use to answer you.
display_table(model, "reached_garden")
print()


inference = VariableElimination(model)

###
print("If she reached garden, was she cautious?")
result = inference.query(["alice_cautious"], evidence={"reached_garden": 1})
print(result)
print()

###
print("# If bottle not labeled, did she drink?")
result2 = inference.query(["alice_drinks"], evidence={"bottle_labeled": 0})
print(result2)
print()

###
print("# If Alice ate a cake will reached the garden?")
result3 = inference.query(
    ["reached_garden"],
    evidence={
        "ate_cake": 1,
    },
)
print(result3)  # Should be ~100%
print()

print("#If Alice reached the garden → did she eat the cake?")
result4 = inference.query(["ate_cake"], evidence={"reached_garden": 1})
print(result4)
print()
