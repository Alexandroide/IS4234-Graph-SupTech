import datetime
import hashlib
import re

class Asset:
    def __init__(
        self,
        company_id: str,
        supplier_id: str,
        asset_name: str,
        asset_type: str,
        purchase_date: str,
        deployment_date: str,
        # reporting_period: str = None,
        # Reported metrics
        revenue_share: float = None,
        critical_service_share: float = None,
        client_share: float = None,
        capacity_share: float = None,
        redundancy_level: float = None,
        revenue_impact: float = None
    ):
        # Basic identifiers
        self.asset_id = self.compute_asset_id(supplier_id, asset_name)  # global asset hash
        self.company_asset_id = self.compute_company_asset_id(company_id, self.asset_id)  # unique per company
        self.asset_name = asset_name
        self.asset_type = asset_type
        self.company_id = company_id
        self.supplier_id = supplier_id
        self.purchase_date = purchase_date
        self.deployment_date = deployment_date

        # Reported metrics
        self.revenue_impact = revenue_impact
        self.revenue_share = revenue_share
        self.critical_service_share = critical_service_share
        self.client_share = client_share
        self.capacity_share = capacity_share
        self.redundancy_level = redundancy_level

        # Computed metrics
        self.operational_reliance = None
        self.timestamp = datetime.datetime.utcnow().isoformat()

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
    
    # Operational reliance computation
    def compute_operational_reliance(self) -> float:
        ### TBD
        return None
    
    # To save as json
    def to_dict(self) -> dict:
        """
        Converts the Asset object into a dictionary for JSON storage.
        """
        return {
            "asset_id": self.asset_id,
            "company_asset_id": self.company_asset_id,
            "asset_name": self.asset_name,
            "asset_type": self.asset_type,
            "company_id": self.company_id,
            "supplier_id": self.supplier_id,
            "purchase_date": self.purchase_date,
            "deployment_date": self.deployment_date,
            "revenue_share": self.revenue_share,
            "critical_service_share": self.critical_service_share,
            "client_share": self.client_share,
            "capacity_share": self.capacity_share,
            "redundancy_level": self.redundancy_level,
            "revenue_impact": self.revenue_impact,
            "operational_reliance": self.operational_reliance,
            "timestamp": self.timestamp
        }
