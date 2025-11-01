# IS4234 — Graph-Based SupTech Framework for Systemic Risk Analysis

## 🧭 Overview

This project explores a **SupTech (Supervisory Technology)** approach to monitoring digital infrastructure resilience through **graph theory**.  
It models **inter-company dependencies** between hardware and software providers to identify *systemically critical technology suppliers*.

By integrating company- and asset-level disclosures into a **weighted network**, regulators can compute systemic influence scores—using a **PageRank-style algorithm**—to pinpoint providers whose failure could cascade through the ecosystem.

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
