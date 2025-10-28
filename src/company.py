import datetime
import pandas as pd
import json

# Load NAICS JSON from file
with open("../data/NAICS_codes.json", "r") as f:
    naics_data = json.load(f)

CRITICAL_SECTORS = ["TO COMPLETE"]  # Replace with actual NAICS codes as strings

class Company:
    def __init__(
        self,
        company_id: str,
        company_name: str,
        sector_id: int,
        employee_count: float,
        revenue: float,
        market_cap: float,
        total_assets: float,
        num_business_clients: int,
        num_critical_sector_clients: int,
        num_customers_in_critical_services: int,
        healthcare_clients_affected: int,
        essential_service_clients_count: int,
        num_suppliers: int,
        market_share: float,
    ):
        # Basic identifiers
        self.company_id = company_id
        self.company_name = company_name
        self.sector_id = sector_id
        self.sector_name = self.get_sector_name()

        # Economic & Financial criticality
        self.revenue = revenue
        self.market_cap = market_cap
        self.total_assets = total_assets
        self.market_share = market_share

        # Network dependency exposure
        self.num_business_clients = num_business_clients
        self.num_critical_sector_clients = num_critical_sector_clients
        self.num_suppliers = num_suppliers

        # Societal criticality
        self.employee_count = employee_count
        self.num_customers_in_critical_services = num_customers_in_critical_services
        self.healthcare_clients_affected = healthcare_clients_affected
        self.essential_service_clients_count = essential_service_clients_count

        # Regulatory / systemic importance
        self.regulated_sector_flag = self.is_regulated_sector()

        # Computed metrics
        self.economic_criticality_score = self.compute_economic_criticality_score()
        self.societal_criticality_score = self.compute_societal_criticality_score()
        self.total_criticality_score = self.compute_total_criticality_score()

        self.timestamp = datetime.datetime.utcnow().isoformat()

    # Helper methods
    def is_regulated_sector(self) -> bool:
        """Return True if the company operates in a regulated or critical sector."""
        return str(self.sector_id) in CRITICAL_SECTORS
    
    def get_sector_name(self) -> str:
        for entry in naics_data:
            if entry.get("2022 NAICS US Code") == str(self.sector_id):
                return entry.get("2022 NAICS US Title")
        return None

    # Scoring Functions
    def compute_economic_criticality_score(self) -> float:
        """
        Computes an economic criticality score based on size, exposure, and market position.
        Weights are normalized so larger, more central firms score higher.
        """
        weights = {
            "revenue": 0.30,
            "market_cap": 0.20,
            "total_assets": 0.10,
            "market_share": 0.15,
            "num_business_clients": 0.10,
            "num_critical_sector_clients": 0.10,
            "num_suppliers": 0.05,
        }

        score = (
            weights["revenue"] * (self.revenue ** 0.5)
            + weights["market_cap"] * (self.market_cap ** 0.5)
            + weights["total_assets"] * (self.total_assets ** 0.5)
            + weights["market_share"] * (self.market_share * 100)
            + weights["num_business_clients"] * (self.num_business_clients ** 0.5)
            + weights["num_critical_sector_clients"] * (self.num_critical_sector_clients ** 0.5)
            + weights["num_suppliers"] * (self.num_suppliers ** 0.5)
        )

        return round(score, 2)

    def compute_societal_criticality_score(self) -> float:
        """
        Computes societal importance based on human and service impact.
        """
        weights = {
            "employee_count": 0.25,
            "num_customers_in_critical_services": 0.25,
            "healthcare_clients_affected": 0.25,
            "essential_service_clients_count": 0.15,
            "regulated_sector_flag": 0.10,
        }

        flag_bonus = 1.5 if self.regulated_sector_flag else 1.0

        score = (
            weights["employee_count"] * (self.employee_count ** 0.5)
            + weights["num_customers_in_critical_services"] * (self.num_customers_in_critical_services ** 0.5)
            + weights["healthcare_clients_affected"] * (self.healthcare_clients_affected ** 0.5)
            + weights["essential_service_clients_count"] * (self.essential_service_clients_count ** 0.5)
        ) * flag_bonus

        return round(score, 2)

    def compute_total_criticality_score(self) -> float:
        """
        Combines economic and societal scores into a single criticality measure.
        """
        total_score = (0.45 * self.economic_criticality_score) + (0.55 * self.societal_criticality_score)
        return round(total_score, 2)
    
    def to_dict(self) -> dict:
        """
        Converts the company object into a dictionary for JSON storage.
        """
        return {
            "company_id": self.company_id,
            "company_name": self.company_name,
            "sector_id": self.sector_id,
            "sector_name": self.sector_name,
            "employee_count": self.employee_count,
            "revenue": self.revenue,
            "market_cap": self.market_cap,
            "total_assets": self.total_assets,
            "num_business_clients": self.num_business_clients,
            "num_critical_sector_clients": self.num_critical_sector_clients,
            "num_customers_in_critical_services": self.num_customers_in_critical_services,
            "healthcare_clients_affected": self.healthcare_clients_affected,
            "essential_service_clients_count": self.essential_service_clients_count,
            "num_suppliers": self.num_suppliers,
            "market_share": self.market_share,
            "regulated_sector_flag": self.regulated_sector_flag,
            "economic_criticality_score": self.economic_criticality_score,
            "societal_criticality_score": self.societal_criticality_score,
            "total_criticality_score": self.total_criticality_score,
            "timestamp": self.timestamp
        }
