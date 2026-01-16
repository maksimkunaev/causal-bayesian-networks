import itertools


# --- PHASE 4: THE TabularCPD (The Resulting Table) ---
# Now we can look at the "Hidden" table the estimator built.
# This table is what 'VariableElimination' will use to answer you.
def display_table(model, variable):
    cpd = model.get_cpds(variable)
    evidence_vars = cpd.variables[1:]
    evidence_card = cpd.cardinality[1:]

    print(f"\n=== CPD for '{variable}' ===")
    print(f"Shape: {cpd.values.shape}")
    print(f"Variables: {cpd.variables}")
    print(f"Cardinality: {cpd.cardinality}\n")

    if evidence_vars:
        # Build header
        header_parts = [f"{v:15s}" for v in evidence_vars]
        header_parts.extend([f"P({variable}={i})" for i in range(cpd.cardinality[0])])
        header = " | ".join(header_parts)
        print(header)
        print("-" * len(header))

        # Generate all combinations
        combinations = list(itertools.product(*[range(c) for c in evidence_card]))

        # Print rows
        for combo in combinations:
            row_parts = [f"{val:15d}" for val in combo]
            probs = [
                f"{cpd.values[(i,) + combo]:.4f}" for i in range(cpd.cardinality[0])
            ]
            row_parts.extend(probs)
            print(" | ".join(row_parts))
    else:
        # Root node (no evidence)
        for i in range(cpd.cardinality[0]):
            print(f"P({variable}={i}) = {cpd.values[i]:.4f}")
