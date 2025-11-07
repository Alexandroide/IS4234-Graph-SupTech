# 📘 Data Dictionary

This document describes the structure of the key data objects used in the **IS4234 Graph-SupTech** framework.  
It covers both persistent JSON datasets and their corresponding Python class attributes.

---

## 🏢 Company Object (`src/company.py`)

Each company is represented as a structured object that combines **economic**, **societal**, and **network dependency** indicators.  
Instances are serialized into `data/company_data.json`.

### JSON Schema Overview
| Field | Type | Description |
|--------|------|-------------|
| `company_id` | `str` | Unique identifier for the company. |
| `company_name` | `str` | Legal name of the company. |
| `sector_id` | `int` | NAICS industry code associated with the company. |
| `sector_name` | `str` | Human-readable sector name (looked up from `NAICS_codes.json`). |
| `employee_count` | `float` | Total number of employees. |
| `revenue` | `float` | Company annual revenue (used in economic criticality). |
| `market_cap` | `float` | Market capitalization. |
| `total_assets` | `float` | Value of total assets held. |
| `num_business_clients` | `int` | Number of business clients relying on this company. |
| `num_critical_sector_clients` | `int` | Number of clients that operate in regulated or critical sectors. |
| `num_customers_in_critical_services` | `int` | Number of customers served in essential or public services. |
| `healthcare_clients_affected` | `int` | Healthcare sector clients directly dependent on this company. |
| `essential_service_clients_count` | `int` | Count of clients offering essential or utility services. |
| `num_suppliers` | `int` | Number of suppliers the company depends on. |
| `market_share` | `float` | Proportion of total market controlled by the company (0–1). |
| `regulated_sector_flag` | `bool` | Indicates if the company belongs to a regulated or critical sector (`True`/`False`). |
| `economic_criticality_score` | `float` | Computed measure of economic importance (based on financial size and client exposure). |
| `societal_criticality_score` | `float` | Computed measure of social/systemic impact (based on human and service metrics). |
| `total_criticality_score` | `float` | Weighted combination of economic (45%) and societal (55%) scores. |
| `timestamp` | `str (ISO-8601)` | UTC time of object creation. |

### Derived Attributes & Logic
| Attribute | Computation | Description |
|------------|-------------|-------------|
| `regulated_sector_flag` | `sector_id ∈ CRITICAL_SECTORS` | Flags if the firm operates in a regulated sector. |
| `economic_criticality_score` | Weighted √(size, exposure) metrics | Higher for large and connected firms. |
| `societal_criticality_score` | Weighted √(human impact) metrics × regulated bonus | Highlights essential-service providers. |
| `total_criticality_score` | 0.45×economic + 0.55×societal | Aggregated systemic importance. |

---

## 🧩 Asset Object (`src/asset.py`)

Each asset represents a **hardware or software component** owned by one company and supplied by another.  
Assets are serialized into `data/asset_data.json`.

### JSON Schema Overview
| Field | Type | Description |
|--------|------|-------------|
| `asset_id` | `str` | Global asset identifier (SHA-256 hash of supplier + asset name). |
| `company_asset_id` | `str` | Unique asset ID within the owning company (SHA-256 of company + asset_id). |
| `asset_name` | `str` | Human-readable name of the asset. |
| `asset_type` | `str` | Category of asset (e.g., software, hardware, cloud service). |
| `company_id` | `str` | Identifier of the company **owning** the asset. |
| `supplier_id` | `str` | Identifier of the company **supplying** the asset. |
| `purchase_date` | `str` | Date of asset acquisition (ISO format). |
| `deployment_date` | `str` | Date when the asset was deployed. |
| `revenue_share` | `float` | Proportion of company revenue depending on this asset (0–1). |
| `critical_service_share` | `float` | Share of critical/regulated services using this asset (0–1). |
| `client_share` | `float` | Portion of clients relying on this asset (0–1). |
| `capacity_share` | `float` | Proportion of operational capacity dependent on the asset (0–1). |
| `redundancy_level` | `float` | Degree of redundancy (0 = none, 1 = fully redundant). |
| `revenue_impact` | `float` | Expected revenue loss impact if asset fails (0–1). |
| `operational_reliance` | `float` | Computed composite reliance score across all above metrics (bounded to ≤ 1.0). |
| `timestamp` | `str (ISO-8601)` | UTC time of object creation. |

### Derived Attributes & Logic
| Attribute | Computation | Description |
|------------|-------------|-------------|
| `asset_id` | `sha256(supplier_id + slugified(asset_name))[:16]` | Global 16-char hash identifier. |
| `company_asset_id` | `sha256(company_id + asset_id)[:16]` | Asset’s unique ID within owner context. |
| `operational_reliance` | Weighted linear combination of metrics | Reflects criticality of the asset to operations. Formula:  
`0.25·revenue_share + 0.25·critical_service_share + 0.15·client_share + 0.15·capacity_share + 0.10·(1-redundancy_level) + 0.10·revenue_impact` |

---

## 🔗 Data Relationships

| Relationship | Description |
|---------------|-------------|
| **Asset → Company (Owner)** | `asset.company_id` refers to `company.company_id`. |
| **Asset → Company (Supplier)** | `asset.supplier_id` refers to `company.company_id` of the provider. |
| **Company → Sector** | `company.sector_id` maps to `NAICS_codes.json` for industry name lookup. |
| **Graph Construction** | Each company becomes a **node**; asset dependencies define **edges** between supplier and owner companies with weights = `asset.operational_reliance`. |

---

## 📅 Update Flow Summary

1. New CSVs are uploaded into `/data/test/`.  
2. `update_company_data.py` and `update_asset_data.py` parse and convert entries into structured JSON.  
3. `update_graph_data.py` builds the dependency graph (`graph_data.json`) from company/asset relations.  
4. `graph_analyzer_cidm.py` analyzes criticality propagation and systemic influence.

---

## 🧠 Notes

- All timestamps use **UTC ISO-8601** format for traceability.  
- All proportion variables (`*_share`, `*_impact`, `operational_reliance`) are **bounded between 0 and 1**.  
- Hash IDs ensure deterministic and collision-resistant identifiers across updates.  
- Criticality scores are **normalized metrics**, not percentages, designed for relative comparison across entities.

---
