# Cause and Effect

Learning materials and examples for Causal Bayesian Networks using [pgmpy](https://pgmpy.org/).

## Contents

- `parameter-estimation.md` - Parameter estimation and TabularCPD explanation
- `causal-inference.md` - Causal inference concepts and do-calculus
- `bayesian-network-basics.md` - Discrete Bayesian Network fundamentals
- `create_dataset.py` - Synthetic startup dataset generator
- `csv_way.py` - Example: learning from CSV data
- `manual.py` - Example: manual CPD definition and inference

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python create_dataset.py  # Generate startup_dataset.csv
python manual.py          # Run inference example
```
