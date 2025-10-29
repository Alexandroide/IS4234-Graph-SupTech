import os
import json
import pandas as pd
from asset import Asset


def update_asset_database(csv_file: str, db_file: str = "../data/asset_data.json") -> None:
    """
    Reads an asset CSV file, converts each row into an Asset object,
    and updates the central asset JSON database.

    If an asset with the same company_asset_id already exists, it is replaced.
    """
    # Step 1: Load CSV
    if not os.path.exists(csv_file):
        print(f"⚠️ CSV file not found: {csv_file}")
        return

    df = pd.read_csv(csv_file)

    # Step 2: Load or initialize JSON database
    if os.path.exists(db_file):
        with open(db_file, "r") as f:
            try:
                asset_db = json.load(f)
            except json.JSONDecodeError:
                asset_db = []
    else:
        asset_db = []

    # Step 3: Process each asset in CSV
    for _, row in df.iterrows():
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

        # Replace if same company_asset_id already exists
        existing_index = next(
            (i for i, a in enumerate(asset_db)
             if a["company_asset_id"] == asset_dict["company_asset_id"]),
            None
        )

        if existing_index is not None:
            asset_db[existing_index] = asset_dict
        else:
            asset_db.append(asset_dict)

    # Step 4: Save database
    with open(db_file, "w") as f:
        json.dump(asset_db, f, indent=2)

    print(f"✅ Asset database updated: {db_file} (from {csv_file})")