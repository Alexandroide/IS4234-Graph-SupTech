import pandas as pd

class Company:
    def __init__(
        self,
        company_id: str,
        company_name: str,
        sector: str,
        total_revenue: float
    ):
        self.company_id = company_id
        self.company_name = company_name
        self.sector = sector
        self.total_revenue = total_revenue
