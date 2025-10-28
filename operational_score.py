"""
Executive Summary:
Compute a single operational_reliance score (0–1) per hardware asset.
- Uses five simple, auditable metrics:
    1. revenue_share        – fraction of revenue dependent on this hardware
    2. critical_service_share – fraction of critical services using it
    3. client_share         – share of clients depending on it
    4. capacity_share       – share of total operational capacity it represents
    5. redundancy_level     – share of its functions covered by backup systems (reduces score)
- The formula prioritizes operational exposure and financial importance,
  while moderating for redundancy.
- No subjective self-assessment required.

Default Weights (tunable by regulator):
- revenue_share:           0.3
- critical_service_share:  0.3
- client_share:            0.2
- capacity_share:          0.2

Final Formula:
operational_reliance = (weighted_sum) * (1 - redundancy_level)

Range: 0 (no reliance) → 1 (fully dependent)
"""

def compute_operational_reliance_simple(metrics, weights=None):
    """
    metrics: dict with keys:
        revenue_share, critical_service_share, client_share, capacity_share, redundancy_level
    weights: optional dict to override defaults
    returns: float in [0, 1]
    """
    # Default weights
    w = weights or {
        "revenue_share": 0.3,
        "critical_service_share": 0.3,
        "client_share": 0.2,
        "capacity_share": 0.2
    }

    # Helper: keep within [0,1]
    def clamp(x):
        return max(0.0, min(1.0, float(x)))

    # Clamp all metrics
    rs = clamp(metrics.get("revenue_share", 0))
    cs = clamp(metrics.get("critical_service_share", 0))
    cl = clamp(metrics.get("client_share", 0))
    cp = clamp(metrics.get("capacity_share", 0))
    rd = clamp(metrics.get("redundancy_level", 0))

    # Weighted sum (ignoring redundancy first)
    weighted_sum = (
        w["revenue_share"] * rs +
        w["critical_service_share"] * cs +
        w["client_share"] * cl +
        w["capacity_share"] * cp
    )

    # Adjust for redundancy (reduces impact)
    operational_reliance = weighted_sum * (1 - rd)

    # Clamp result
    return clamp(operational_reliance)


# Example usage
if __name__ == "__main__":
    example_metrics = {
        "revenue_share": 0.25,
        "critical_service_share": 0.4,
        "client_share": 0.3,
        "capacity_share": 0.35,
        "redundancy_level": 0.5
    }

    score = compute_operational_reliance_simple(example_metrics)
    print(f"Operational reliance score: {score:.3f}")
