import pandas as pd
import random
from faker import Faker

fake = Faker()

# ---------- 1️⃣ Generate fake company data ----------
num_companies = 20
companies = []

for i in range(1, num_companies + 1):
    company_id = f"COMP{i:03d}"
    company_name = fake.company()
    sector_id = random.randint(100, 999)
    employee_count = random.randint(100, 10000)
    revenue = round(random.uniform(5e6, 5e9), 2)
    market_cap = round(revenue * random.uniform(2, 5), 2)
    total_assets = round(revenue * random.uniform(1, 3), 2)
    num_business_clients = random.randint(10, 1000)
    num_critical_sector_clients = random.randint(0, 200)
    num_customers_in_critical_services = random.randint(100, 100000)
    healthcare_clients_affected = random.randint(0, 100)
    essential_service_clients_count = random.randint(0, 500)
    num_suppliers = random.randint(5, 50)
    market_share = round(random.uniform(0.01, 0.25), 2)

    companies.append([
        company_id, company_name, sector_id, employee_count, revenue, market_cap,
        total_assets, num_business_clients, num_critical_sector_clients,
        num_customers_in_critical_services, healthcare_clients_affected,
        essential_service_clients_count, num_suppliers, market_share
    ])

df_companies = pd.DataFrame(companies, columns=[
    "company_id","company_name","sector_id","employee_count","revenue","market_cap",
    "total_assets","num_business_clients","num_critical_sector_clients",
    "num_customers_in_critical_services","healthcare_clients_affected",
    "essential_service_clients_count","num_suppliers","market_share"
])

df_companies.to_csv("../data/test/test_C1_company_data.csv", index=False)
print("✅ Generated test_C1_company_data.csv")

# ---------- 2️⃣ Generate fake asset data ----------
num_assets = 60
suppliers = [f"SUP{i:03d}" for i in range(1, 21)]  # 20 fake suppliers
asset_types = ["Hardware", "Software"]
assets = []

for _ in range(num_assets):
    company_id = random.choice(df_companies["company_id"].tolist())
    supplier_id = random.choice(suppliers)
    asset_name = fake.word().capitalize() + "_" + random.choice(["A", "X", "Pro", "Plus", "Edge"])
    asset_type = random.choice(asset_types)
    purchase_date = fake.date_between(start_date="-3y", end_date="-1y")
    deployment_date = fake.date_between(start_date=purchase_date, end_date="today")

    revenue_share = round(random.uniform(0.05, 0.3), 2)
    critical_service_share = round(random.uniform(0.1, 0.5), 2)
    client_share = round(random.uniform(0.05, 0.4), 2)
    capacity_share = round(random.uniform(0.05, 0.4), 2)
    redundancy_level = round(random.uniform(0.0, 1.0), 2)
    revenue_impact = round(random.uniform(0.1, 0.8), 2)

    assets.append([
        company_id, supplier_id, asset_name, asset_type,
        purchase_date, deployment_date,
        revenue_share, critical_service_share, client_share,
        capacity_share, redundancy_level, revenue_impact
    ])

df_assets = pd.DataFrame(assets, columns=[
    "company_id","supplier_id","asset_name","asset_type","purchase_date","deployment_date",
    "revenue_share","critical_service_share","client_share",
    "capacity_share","redundancy_level","revenue_impact"
])

df_assets.to_csv("../data/test/test_C1_asset_data.csv", index=False)
print("✅ Generated test_C1_asset_data.csv")
