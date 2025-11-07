# IS4234 – Graph-Based SupTech Framework for Systemic Risk Analysis

## 🧭 Overview

This project explores a **SupTech (Supervisory Technology)** approach to monitoring digital infrastructure resilience through **graph theory**.  
It models **inter-company dependencies** between hardware and software providers to identify *systemically critical technology suppliers*.

By integrating company- and asset-level disclosures into a **weighted network**, regulators can compute systemic influence scores, using a **PageRank-style algorithm**, to pinpoint providers whose failure could cascade through the ecosystem.

---

## 🔍 Concept

> **Goal:** Build a continuously updating network model of companies and their technological dependencies, enabling regulators to identify “too-critical-to-fail” nodes.

1. **Firms disclose** hardware/software assets with quantitative risk metrics.  
2. **Regulators integrate** these into a graph:  
   - **Nodes:** Companies  
   - **Edges:** Operational reliance between firms  
   - **Weights:** Asset criticality, dependency strength, and systemic impact  
3. A **PageRank-like algorithm** propagates influence scores through the network to reveal which entities pose the highest systemic risk.  
4. Results are used to **prioritize oversight and resilience assessments**.

---

## 🧩 Repository Structure

```

IS4234-Graph-SupTech/
│
├── data/
│   ├── NAICS_codes.json          # Industry classification codes
│   ├── asset_data.json           # Hardware & software assets by company
│   ├── company_data.json         # Company metadata & attributes
│   ├── graph_data.json           # Graph nodes, edges, and weights
│   └── test/                     # Sample CSV data (simulated company submissions)
│
└── src/
├── asset.py                  # Asset class (criticality, ownership, reliance)
├── company.py                # Company class (metadata, risk scores)
├── generate_test_data.py     # Generates fake submission data in /data/test
├── update_data.py            # Master script that updates all datasets
├── update_company_data.py    # Parses new company CSVs → updates company_data.json
├── update_asset_data.py      # Parses new asset CSVs → updates asset_data.json
├── update_graph_data.py      # Builds graph_data.json from current company/asset data
└── graph_analyzer_cidm.py    # Core analytical engine (CIDM = Critical Infrastructure Dependency Model)

```

---

## ⚙️ How It Works

### 1️⃣ Data Ingestion

`update_data.py` orchestrates the ingestion of new submissions located in `/data/test/`.  
Each CSV (e.g., new company or asset disclosure) is transformed into structured JSON:

- **Company objects** → `company_data.json`  
- **Asset objects** → `asset_data.json`  

Linkages:
- Each asset has both a `company_id` (owner) and a `supplier_id` (provider company).

### 2️⃣ Graph Construction

`update_graph_data.py` consolidates the asset and company JSONs into a directed **dependency graph**:
- **Nodes** = Companies  
- **Node attributes** = Criticality weights (`societal`, `economic`, `global`)  
- **Edges** = Dependency links (`weight` ∈ [0, 1])

Result is stored in `graph_data.json`.

### 3️⃣ Graph Analysis

The **`GraphAnalyzerCIDM`** class (in `graph_analyzer_cidm.py`) performs:

| Function | Description |
|-----------|--------------|
| `summary()` | Prints network statistics (nodes, edges, samples) |
| `visualize()` | Generates network visualization using `matplotlib` and `networkx` |
| `systemic_influence()` | PageRank-style recursive influence propagation |
| `simulate_failure_recursive()` | Simulates cascading failures from a node |
| `get_company_info()` | Retrieves company details from stored JSON |

---

## 🚀 Quick Start

### Prerequisites
- Python ≥ 3.9  
- Dependencies:  

```bash

pip install networkx matplotlib

```

### Steps

```bash

# 1. Generate synthetic test data (optional)
python src/generate_test_data.py

# 2. Update datasets (companies, assets, and graph)
python src/update_data.py

# 3. Analyze the updated graph
python src/graph_analyzer_cidm.py

```

---

## 📊 Example Output

```
=== CIDM NETWORK SUMMARY ===
Nodes (Companies): 30
Edges (Dependencies): 112

Top 10 most systemically critical companies:
1. COMP021: 9213.44
2. COMP008: 8531.76
...
```

Visualization:

> Node size = global criticality
> Node color = societal importance
> Edge width = operational reliance

---

## 🧠 Key Insights

* **Dynamic supervision:** As companies update disclosures, the network graph evolves, enabling continuous oversight.
* **Systemic lens:** Identifies critical service providers across sectors—not just large firms.
* **Failure simulation:** Predicts cascading effects.

---

## 📁 Data Schema (Simplified)

**graph_data.json**

```json

{
  "COMP001": {
    "weights": {
      "societal": 91.09,
      "economic": 8627.86,
      "global": 3932.64
    },
    "edges": {
      "COMP021": 0.224,
      "COMP008": 0.253,
      "COMP024": 0.327
    }
  }
}

```

---

## 🙌 Acknowledgments

Developed as part of the **IS4234 Governance, Regulation, and Compliance Technology** course project.
