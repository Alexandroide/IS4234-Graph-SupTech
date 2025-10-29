import os
import json
from collections import defaultdict


def update_graph_database(
    company_file: str = "../data/company_data.json",
    asset_file: str = "../data/asset_data.json",
    db_file: str = "../data/graph_data.json"
) -> None:
    """
    Builds a directed, weighted graph representation of company dependencies.

    Nodes = companies (or suppliers)
    Edges = company → supplier (asset dependency)
    Edge weight = operational reliance
    Node weights = criticality scores
    """

    # --- Step 1: Load JSON databases ---
    if not os.path.exists(company_file):
        print(f"⚠️ Company file not found: {company_file}")
        return
    if not os.path.exists(asset_file):
        print(f"⚠️ Asset file not found: {asset_file}")
        return

    with open(company_file, "r") as f:
        try:
            companies_data = json.load(f)
        except json.JSONDecodeError:
            print(f"❌ Error reading {company_file}: invalid JSON")
            return

    with open(asset_file, "r") as f:
        try:
            assets_data = json.load(f)
        except json.JSONDecodeError:
            print(f"❌ Error reading {asset_file}: invalid JSON")
            return

    # --- Step 2: Build company weights dictionary ---
    default_weight = 0.0
    company_weights = {}
    for c in companies_data:
        company_id = c["company_id"]
        company_weights[company_id] = {
            "societal": c.get("societal_criticality_score", default_weight),
            "economic": c.get("economic_criticality_score", default_weight),
            "global": c.get("total_criticality_score", default_weight),
        }

    # --- Step 3: Build graph structure ---
    graph_input = defaultdict(lambda: {"weights": {}, "edges": {}})

    # Add all companies as nodes
    for company_id, weights in company_weights.items():
        graph_input[company_id]["weights"] = weights

    # Add edges from assets
    for asset in assets_data:
        company_id = asset["company_id"]
        supplier_id = asset["supplier_id"]
        op_rel = asset.get("operational_reliance", 0.0)

        # Ensure supplier node exists
        if supplier_id not in graph_input:
            graph_input[supplier_id]["weights"] = {
                "societal": company_weights.get(supplier_id, {}).get("societal", default_weight),
                "economic": company_weights.get(supplier_id, {}).get("economic", default_weight),
                "global": company_weights.get(supplier_id, {}).get("global", default_weight),
            }

        # Add or update edge
        graph_input[company_id]["edges"][supplier_id] = op_rel

    # Convert defaultdict → normal dict
    graph_input = dict(graph_input)

    # --- Step 4: Save graph to file ---
    with open(db_file, "w") as f:
        json.dump(graph_input, f, indent=2)

    print(f"✅ Graph database updated: {db_file}")