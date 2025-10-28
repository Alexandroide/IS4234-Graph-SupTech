import os
import json
import pandas as pd
from company import Company  # adjust path according to your repo structure

CSV_FILE = "../data/test_C1_data.csv"
DB_FILE = "../data/company_data.json"

# Step 1: Read CSV
df = pd.read_csv(CSV_FILE)

for idx, row in df.iterrows():
    # Step 2: Create Company object
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

    # Convert to dictionary
    comp_dict = comp.to_dict()

    # Step 3: Save to JSON database
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    # Replace existing company if exists
    existing_index = next((i for i, c in enumerate(data) if c["company_id"] == comp_dict["company_id"]), None)
    if existing_index is not None:
        data[existing_index] = comp_dict
    else:
        data.append(comp_dict)

    # Save back to JSON
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

print(f"Company data saved to {DB_FILE}")
