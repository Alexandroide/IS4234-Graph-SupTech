import os
from tqdm import tqdm

# Import update functions
from update_asset_data import update_asset_database
from update_company_data import update_company_database
from update_graph_data import update_graph_database

# Paths
TEST_FOLDER = "../data/test/"
ASSET_DB = "../data/asset_data.json"
COMPANY_DB = "../data/company_data.json"
GRAPH_DB = "../data/graph_data.json"


def update_all_data():
    """Master update pipeline for assets, companies, and graphs with progress bars."""
    print("🚀 Starting full data update pipeline...\n")

    # --- 1️⃣ Update asset data ---
    asset_files = [f for f in os.listdir(TEST_FOLDER) if f.endswith("asset_data.csv")]
    if asset_files:
        print("🧩 Updating asset data...")
        for file in tqdm(asset_files, desc="Processing asset CSVs", ncols=80, colour="cyan"):
            csv_path = os.path.join(TEST_FOLDER, file)
            update_asset_database(csv_path, ASSET_DB)
    else:
        print("⚠️ No asset data files found.")

    # --- 2️⃣ Update company data ---
    company_files = [f for f in os.listdir(TEST_FOLDER) if f.endswith("company_data.csv")]
    if company_files:
        print("\n🏢 Updating company data...")
        for file in tqdm(company_files, desc="Processing company CSVs", ncols=80, colour="yellow"):
            csv_path = os.path.join(TEST_FOLDER, file)
            update_company_database(csv_path, COMPANY_DB)
    else:
        print("⚠️ No company data files found.")

    # --- 3️⃣ Update dependency graph ---
    print("\n🌐 Building dependency graph...")
    for _ in tqdm(range(1), desc="Generating graph", ncols=80, colour="green"):
        update_graph_database(company_file=COMPANY_DB, asset_file=ASSET_DB, db_file=GRAPH_DB)

    print("\n✅ All updates completed successfully.")


if __name__ == "__main__":
    update_all_data()