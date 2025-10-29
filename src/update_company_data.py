import os
import json
import pandas as pd
from company import Company


def update_company_database(csv_file: str, db_file: str = "../data/company_data.json") -> None:
    """
    Reads a company CSV file, creates Company objects for each row,
    and updates the company JSON database.
    
    If a company with the same company_id already exists, it is replaced.
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
                company_db = json.load(f)
            except json.JSONDecodeError:
                company_db = []
    else:
        company_db = []

    # Step 3: Process each company record
    for _, row in df.iterrows():
        comp = Company(
            company_id=row["company_id"],
            company_name=row["company_name"],
            sector_id=row["sector_id"],
            employee_count=row["employee_count"],
            revenue=row["revenue"],
            market_cap=row["market_cap"],
            total_assets=row["total_assets"],
            num_business_clients=row["num_business_clients"],
            num_critical_sector_clients=row["num_critical_sector_clients"],
            num_customers_in_critical_services=row["num_customers_in_critical_services"],
            healthcare_clients_affected=row["healthcare_clients_affected"],
            essential_service_clients_count=row["essential_service_clients_count"],
            num_suppliers=row["num_suppliers"],
            market_share=row["market_share"],
        )

        comp_dict = comp.to_dict()

        # Replace existing company if exists
        existing_index = next(
            (i for i, c in enumerate(company_db) if c["company_id"] == comp_dict["company_id"]),
            None
        )

        if existing_index is not None:
            company_db[existing_index] = comp_dict
        else:
            company_db.append(comp_dict)

    # Step 4: Save updated database
    with open(db_file, "w") as f:
        json.dump(company_db, f, indent=2)

    print(f"✅ Company database updated: {db_file} (from {csv_file})")