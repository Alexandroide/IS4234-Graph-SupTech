import pandas as pd
import hashlib
import re

class Asset:
    def __init__(
        self,
        company_id: str,
        supplier_id: str,
        asset_name: str,
        purchase_date: str,
        deployment_date: str
    ):
        
        self.asset_id = self.compute_asset_id(supplier_id, asset_name)  # global asset hash
        self.company_asset_id = self.compute_company_asset_id(company_id, self.asset_id)  # unique per company

        self.asset_name = asset_name
        self.supplier_id = supplier_id
        self.company_id = company_id
        self.purchase_date = purchase_date
        self.deployment_date = deployment_date

    # Static methods
    @staticmethod
    def slugify(name: str) -> str:
        """Convert asset_name to a slug suitable for hashing."""
        name = name.lower()
        name = re.sub(r'\s+', '-', name)  # spaces -> hyphens
        name = re.sub(r'[^\w\-]', '', name)  # remove special chars
        return name

    @staticmethod
    def compute_asset_id(supplier_id: str, asset_name: str) -> str:
        """Generate a unique global asset ID based on supplier and slugified asset name."""
        slug_name = Asset.slugify(asset_name)
        hash_input = f"{supplier_id}-{slug_name}".encode('utf-8')
        return hashlib.sha256(hash_input).hexdigest()[:16]  # 16-char hash for brevity

    @staticmethod
    def compute_company_asset_id(company_id: str, asset_id: str) -> str:
        """Generate a unique ID for this asset owned by the company."""
        hash_input = f"{company_id}-{asset_id}".encode('utf-8')
        return hashlib.sha256(hash_input).hexdigest()[:16]
