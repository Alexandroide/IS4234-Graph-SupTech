import os
import json
import pandas as pd
from asset import Asset

CSV_FILE = "../data/test/test_C1_asset_data.csv"
DB_FILE = "../data/asset_data.json"

# Step 1: Read CSV
df = pd.read_csv(CSV_FILE)

# Load existing database if it exists
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        asset_db = json.load(f)
else:
    asset_db = []

# Step 2: Process each asset row
for idx, row in df.iterrows():
    asset_obj = Asset(
        company_id=row["company_id"],
        supplier_id=row["supplier_id"],
        asset_name=row["asset_name"],
        asset_type=row["asset_type"],
        purchase_date=row["purchase_date"],
        deployment_date=row["deployment_date"],
        revenue_share=row.get("revenue_share"),
        critical_service_share=row.get("critical_service_share"),
        client_share=row.get("client_share"),
        capacity_share=row.get("capacity_share"),
        redundancy_level=row.get("redundancy_level"),
        revenue_impact=row.get("revenue_impact"),
    )

    asset_dict = asset_obj.to_dict()

    # Replace existing asset if same company_asset_id exists
    existing_index = next((i for i, a in enumerate(asset_db)
                           if a["company_asset_id"] == asset_dict["company_asset_id"]), None)
    if existing_index is not None:
        asset_db[existing_index] = asset_dict
    else:
        asset_db.append(asset_dict)

# Step 3: Save updated database
with open(DB_FILE, "w") as f:
    json.dump(asset_db, f, indent=2)

print(f"Asset database updated: {DB_FILE}")
