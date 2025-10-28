"""
Executive Summary:
This script computes an Economic Impact Score (0–1) representing the systemic economic importance
of a company based solely on objective, auditable variables.

Framework Basis:
- OECD Critical Infrastructure Resilience Indicators (2023)
- CISA IRPF (Infrastructure Resilience Planning Framework)
- BIS Systemic Importance Metrics (2022)

Approach:
Each sub-theme (Direct Exposure, Network Dependency, Market Position, Macroeconomic Linkages)
is normalized relative to benchmark values. Higher scores = greater systemic economic impact.
"""

# Example input data (objective metrics only)
company_data = {
    "direct_financial_exposure": {
        "monthly_revenue": 120_000_000,
        "gross_margin": 0.35,
        "total_assets": 950_000_000,
        "market_cap": 4_500_000_000
    },
    "network_dependency_exposure": {
        "num_business_clients": 250,
        "num_suppliers": 40
    },
    "market_position": {
        "market_share": 0.25,
        "industry_revenue_rank": 3
    },
    "macroeconomic_linkages": {
        "num_critical_sector_clients": 15,
        "exports_share": 0.3
    }
}

# Reference maximums for normalization (set by regulator per sector)
max_values = {
    "direct_financial_exposure": {
        "monthly_revenue": 1_000_000_000,
        "gross_margin": 1,
        "total_assets": 10_000_000_000,
        "market_cap": 50_000_000_000
    },
    "network_dependency_exposure": {
        "num_business_clients": 10_000,
        "num_suppliers": 2_000
    },
    "market_position": {
        "market_share": 1,
        "industry_revenue_rank": 50   # smaller rank = higher importance
    },
    "macroeconomic_linkages": {
        "num_critical_sector_clients": 100,
        "exports_share": 1
    }
}

def normalize(value, max_value, inverse=False):
    """
    Normalize a variable between 0–1.
    If inverse=True, lower values mean higher systemic importance (e.g. rank).
    """
    if inverse:
        return 1 - min(value / max_value, 1)
    return min(value / max_value, 1)

def compute_theme_score(theme_data, theme_max, invert_keys=None):
    """Compute average normalized score per theme."""
    if invert_keys is None:
        invert_keys = []
    normalized_vars = []
    for key, val in theme_data.items():
        normalized_vars.append(normalize(val, theme_max[key], key in invert_keys))
    return sum(normalized_vars) / len(normalized_vars)

# Compute theme scores
theme_scores = {
    "direct_financial_exposure": compute_theme_score(company_data["direct_financial_exposure"], max_values["direct_financial_exposure"]),
    "network_dependency_exposure": compute_theme_score(company_data["network_dependency_exposure"], max_values["network_dependency_exposure"]),
    "market_position": compute_theme_score(company_data["market_position"], max_values["market_position"], invert_keys=["industry_revenue_rank"]),
    "macroeconomic_linkages": compute_theme_score(company_data["macroeconomic_linkages"], max_values["macroeconomic_linkages"])
}

# Global Economic Impact Score (mean of all sub-themes)
global_economic_impact_score = sum(theme_scores.values()) / len(theme_scores)

# Results
print("=== Economic Impact Scores (Objective Metrics Only) ===")
for theme, score in theme_scores.items():
    print(f"{theme.replace('_', ' ').title()}: {score:.3f}")
print(f"\nGlobal Economic Impact Score: {global_economic_impact_score:.3f}")
