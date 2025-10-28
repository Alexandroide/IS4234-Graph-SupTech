"""
Executive Summary:
This script calculates the societal impact scores for a company based on the potential consequences if its services were temporarily unavailable.
Each theme's score is derived by normalizing the relevant variables, and the global score is the average of all theme scores.


📚 Sources and Motivations

Critical Infrastructure Resilience Strategy (Australia): Provides a framework for enhancing the resilience of critical infrastructure through collaboration between industry and government. 
cisc.gov.au

Infrastructure Resilience Planning Framework (IRPF): Offers methods and resources to address critical infrastructure security and resilience through planning. 
cisa.gov

Indicator-Based Resilience Assessment: Utilizes specific indicators to assess the resilience of critical infrastructures. 
ScienceDirect

"""

# Example data for a company
company_data = {
    "human_safety": {
        "num_employees": 1200,
        "num_customers_in_critical_services": 5000,
        "healthcare_clients_affected": 10
    },
    "essential_services_continuity": {
        "num_key_clients": 50,
        "critical_service_hours_per_month": 720,
        "number_of_facilities_providing_critical_services": 3
    },
    "social_stability": {
        "num_downstream_business_clients": 120,
        "num_communities_served": 8
    },
    "regulatory_sectoral_importance": {
        "regulated_sector_flag": True,
        "number_of_mandatory_compliances": 5
    }
}

# Maximum expected values for normalization
max_values = {
    "human_safety": {
        "num_employees": 10000,
        "num_customers_in_critical_services": 100000,
        "healthcare_clients_affected": 100
    },
    "essential_services_continuity": {
        "num_key_clients": 500,
        "critical_service_hours_per_month": 10000,
        "number_of_facilities_providing_critical_services": 50
    },
    "social_stability": {
        "num_downstream_business_clients": 1000,
        "num_communities_served": 100
    },
    "regulatory_sectoral_importance": {
        "regulated_sector_flag": 1,
        "number_of_mandatory_compliances": 50
    }
}

# Function to compute normalized score for a theme
def compute_theme_score(theme_data, theme_max):
    score = 0
    n = len(theme_data)
    for key, value in theme_data.items():
        max_val = theme_max[key]
        # Convert boolean to int if needed
        if isinstance(value, bool):
            value = int(value)
        # Normalize variable to 0-1
        score += value / max_val
    return score / n  # average of normalized variables

# Compute scores for each theme
theme_scores = {}
for theme, data in company_data.items():
    theme_scores[theme] = compute_theme_score(data, max_values[theme])

# Compute global societal impact score
global_societal_score = sum(theme_scores.values()) / len(theme_scores)

# Output results
print("Theme Scores:")
for theme, score in theme_scores.items():
    print(f"{theme.replace('_', ' ').title()}: {score:.3f}")
print(f"\nGlobal Societal Impact Score: {global_societal_score:.3f}")
