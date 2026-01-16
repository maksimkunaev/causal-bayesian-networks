**What is the point of "Causal Bayesian Network"?** The point is in two things that are missing in a regular table:

### 1. Intervention (Do-calculus) — The Most Important

A regular table (statistics) tells you: *"When people have umbrellas, it rains"*.
If you just look at the table, you'll see correlation.

**Causal Network** gives you the ability to perform **Intervention**.

* **Statistics question:** "What's the probability of rain if I **see** an umbrella?" (P(Rain | Umbrella))
* **Causal AI question:** "What's the probability of rain if I **force** everyone to open umbrellas?" (P(Rain | **do**(Umbrella)))

In a Causal Network, the connection is `Rain -> Umbrella`. If you do `do(Umbrella)`, you "cut off" the umbrella from rain. The network will tell you: *"If you force people to open umbrellas, it won't rain"*. A regular probability table (without arrow structure) doesn't understand this — for it, umbrella and rain just "often occur together".

### 2. Indirect (Hidden) Influences

Imagine a chain: **Coffee -> Blood Pressure -> Headache**.
In reality, you collected data:

* Day 1: Drank coffee, headache.
* Day 2: Didn't drink coffee, no headache.

You might think coffee directly causes headaches. But the network allows you to calculate: *"What if I give blood pressure medication but keep coffee?"*.
The network allows you to "propagate" the signal through the chain. It will say: *"Coffee isn't directly to blame, it's only to blame through blood pressure"*.

**This is the "why did this happen".** The table says: "Coffee is associated with pain". The network says: "The mechanism of pain goes through blood pressure".

---

### Why did we discuss "Fit" and "TabularCPD"?

This is just a technical implementation.

* `TabularCPD` — is a **local** rule (e.g., how Coffee affects Blood Pressure).
* **Bayesian Network** — is how these rules **connect** into a system.

**The key point** is that having small local tables (Coffee -> Blood Pressure and Blood Pressure -> Pain), the network can predict the result of the entire system, even if you never measured Coffee and Pain simultaneously.

### Answer to your question about prediction:

Inference is **not just** a query to an existing cell.
It's a calculation of a **new** probability that doesn't exist in your original data, by combining paths in the graph.

**Example:**
You have data:

1. Coffee affects Sleep.
2. Sleep affects Code Errors.

You **don't have data** for "Coffee -> Errors". There's no such column in your CSV.
But Causal Bayesian Network **will predict** (perform Inference) how an extra cup of coffee will increase bugs, because it knows the "path" through Sleep.

---

### Summary (What's the point?):

1. **Direction:** We strictly set that `Rain -> Umbrella`, so the model doesn't think that opening an umbrella causes rain.
2. **Tracing:** We can change the cause at the beginning of the chain and see what falls at the end, even if we don't have direct data about this connection.
3. **Simulation (Do):** We can simulate actions (interventions) and see the result without conducting a real experiment.
