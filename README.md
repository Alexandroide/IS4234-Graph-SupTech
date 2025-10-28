start: 25 oct 2025

# SupTech CIDM Prototype — Systemic Risk Identification Framework

## 🧠 Executive Summary

This prototype models **digital dependency risk** in critical infrastructures using a graph-based approach.  
It enables regulators to:
- Collect standardized disclosures from companies (via CSV)
- Compute dependency metrics (operational & economic)
- Build a **weighted inter-company dependency graph**
- Identify the **most systemically critical vendors** (hardware or software)
- Generate visual and quantitative insights

---

## ⚙️ System Architecture Overview

### 🧱 Components

| Layer | Description |
|-------|--------------|
| **Data Ingestion** | Companies submit a CSV file listing their hardware dependencies and basic financial info |
| **Computation Layer** | OOP Python classes compute derived metrics: operational reliance, economic impact, and company-level aggregates |
| **Data Persistence** | Processed data is stored as a structured `database.json` file |
| **Analysis Layer** | A `DependencyGraph` (NetworkX) is built from all dependencies |
| **Visualization & Reporting** | Outputs include network graphs, ranking tables, and JSON/CSV reports |

---


---

## 🧠 Class Overview

### `Company`
Represents one company, its characteristics, and associated hardware assets.

- **Attributes:**  
  `company_id`, `sector`, `revenue`, `hardware_assets`, `metrics`
- **Key Methods:**  
  - `load_from_csv()` — loads company data from submission  
  - `compute_company_metrics()` — aggregates economic/societal impact  
  - `to_dict()` — converts to JSON for storage  

### `HardwareAsset`
Represents one critical hardware component and its dependency metrics.

- **Attributes:**  
  `hardware_id`, `vendor_company_id`, `metrics`, `operational_reliance`, `economic_impact`
- **Key Methods:**  
  - `compute_operational_reliance()` — based on redundancy, capacity share, etc.  
  - `compute_economic_impact()` — based on lost revenue, B2B clients, etc.

### `SupTechDatabase`
Central object storing all companies and enabling exports or graph generation.

- **Key Methods:**  
  - `add_company()`, `export_to_json()`, `build_dependency_graph()`

### `DependencyGraph`
Network representation of inter-company dependencies.

- **Methods:**  
  - `compute_pagerank()` — systemic importance ranking  
  - `plot_graph()` — network visualization  
  - `export_results()` — output to CSV/JSON

---

## 🧾 Practical Steps to Run

### 1️⃣ Data Submission by Companies
Companies provide a **CSV** file.

```
                             ...,?77??!~~~~!???77?<~.... 
                        ..?7`                           `7!.. 
                    .,=`          ..~7^`   I                  ?1. 
       ........  ..^            ?`  ..?7!1 .               ...??7 
      .        .7`        .,777.. .I.    . .!          .,7! 
      ..     .?         .^      .l   ?i. . .`       .,^ 
       b    .!        .= .?7???7~.     .>r .      .= 
       .,.?4         , .^         1        `     4... 
        J   ^         ,            5       `         ?<. 
       .%.7;         .`     .,     .;                   .=. 
       .+^ .,       .%      MML     F       .,             ?, 
        P   ,,      J      .MMN     F        6               4. 
        l    d,    ,       .MMM!   .t        ..               ,, 
        ,    JMa..`         MMM`   .         .!                .; 
         r   .M#            .M#   .%  .      .~                 ., 
       dMMMNJ..!                 .P7!  .>    .         .         ,, 
       .WMMMMMm  ?^..       ..,?! ..    ..   ,  Z7`        `?^..  ,, 
          ?THB3       ?77?!        .Yr  .   .!   ?,              ?^C 
            ?,                   .,^.` .%  .^      5. 
              7,          .....?7     .^  ,`        ?. 
                `<.                 .= .`'           1 
                ....dn... ... ...,7..J=!7,           ., 
             ..=     G.,7  ..,o..  .?    J.           F 
           .J.  .^ ,,,t  ,^        ?^.  .^  `?~.      F 
          r %J. $    5r J             ,r.1      .=.  .% 
          r .77=?4.    ``,     l ., 1  .. <.       4., 
          .$..    .X..   .n..  ., J. r .`  J.       `' 
        .?`  .5        `` .%   .% .' L.'    t 
        ,. ..1JL          .,   J .$.?`      . 
                1.          .=` ` .J7??7<.. .; 
                 JS..    ..^      L        7.: 
                   `> ..       J.  4. 
                    +   r `t   r ~=..G. 
                    =   $  ,.  J 
                    2   r   t  .; 
              .,7!  r   t`7~..  j.. 
              j   7~L...$=.?7r   r ;?1. 
               8.      .=    j ..,^   .. 
              r        G              . 
            .,7,        j,           .>=. 
         .J??,  `T....... %             .. 
      ..^     <.  ~.    ,.             .D 
    .?`        1   L     .7.........?Ti..l 
   ,`           L  .    .%    .`!       `j, 
 .^             .  ..   .`   .^  .?7!?7+. 1 
.`              .  .`..`7.  .^  ,`      .i.; 
.7<..........~<<3?7!`    4. r  `          G% 
                          J.` .!           % 
                            JiJ           .` 
                              .1.         J 
                                 ?1.     .'         
                                     7<..%
