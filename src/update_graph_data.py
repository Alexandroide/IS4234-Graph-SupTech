import json
from collections import defaultdict

# Step 1: Load JSON data files
company_file = "../data/test_company_data.json"
asset_file = "../data/test_asset_data.json"

with open(company_file, "r") as f:
    companies_data = json.load(f)

with open(asset_file, "r") as f:
    assets_data = json.load(f)

# Step 2: Build company weights dictionary
# Default supplier weights if not in company file
default_weight = 0.0

company_weights = {}
for c in companies_data:
    company_id = c["company_id"]
    company_weights[company_id] = {
        "societal": c.get("societal_criticality_score", default_weight),
        "economic": c.get("economic_criticality_score", default_weight),
        "global": c.get("total_criticality_score", default_weight)
    }

# Step 3: Build graph representation
graph_input = defaultdict(lambda: {"weights": {}, "edges": {}})

# Add nodes with weights
for company_id, weights in company_weights.items():
    graph_input[company_id]["weights"] = weights

# Add edges from assets
for asset in assets_data:
    company_id = asset["company_id"]
    supplier_id = asset["supplier_id"]
    op_rel = asset.get("operational_reliance", 0)

    # Ensure nodes exist in graph
    if supplier_id not in graph_input:
        graph_input[supplier_id]["weights"] = {
            "societal": company_weights.get(supplier_id, {}).get("societal", default_weight),
            "economic": company_weights.get(supplier_id, {}).get("economic", default_weight),
            "global": company_weights.get(supplier_id, {}).get("global", default_weight)
        }

    # Add edge
    graph_input[company_id]["edges"][supplier_id] = op_rel

# Convert defaultdict to normal dict for JSON saving
graph_input = dict(graph_input)

# Step 4: Save to JSON
with open("../data/graph_data.json", "w") as f:
    json.dump(graph_input, f, indent=2)

# Step 5: Test the graph
# Print some nodes and edges to check
# for node, data in graph_input.items():
#    print(f"Node: {node}")
#    print(f"  Weights: {data['weights']}")
#    print(f"  Edges: {data['edges']}\n")
