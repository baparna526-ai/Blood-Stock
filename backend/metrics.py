# backend/metrics.py
import copy
from backend.simulator import build_world
from backend.baseline import run_baseline
from backend.optimizer import run_optimizer


def compute_metrics(world, allocations):
    """
    Computes performance KPIs for a given set of allocations in a world state.
    """
    total_requests = len(world["requests"])
    allocated_request_ids = {a["request_id"] for a in allocations}
    fulfilled_count = len(allocated_request_ids)
    fulfillment_rate = (fulfilled_count / total_requests) if total_requests > 0 else 1.0

    total_travel_time = sum(a["travel_minutes"] for a in allocations)
    avg_travel_time = (total_travel_time / len(allocations)) if allocations else 0.0

    # Locked units
    allocated_unit_ids = {a["unit_id"] for a in allocations}
    
    # Check remaining unallocated units for spoilage / expiry risk
    # (e.g. units expiring within the next 2 hours that were NOT utilized)
    unallocated_units = [u for u in world["units"] if u["unit_id"] not in allocated_unit_ids]
    near_expiry_waste = sum(1 for u in unallocated_units if u["expires_at"] <= 120)

    # Expiry safety margins of allocated units: (expires_at - arrival_time)
    safety_margins = []
    unit_map = {u["unit_id"]: u for u in world["units"]}
    for a in allocations:
        unit = unit_map.get(a["unit_id"])
        if unit:
            margin = unit["expires_at"] - a["arrival_time"]
            safety_margins.append(margin)

    avg_safety_margin = (sum(safety_margins) / len(safety_margins)) if safety_margins else 0.0

    return {
        "total_requests": total_requests,
        "fulfilled_requests": fulfilled_count,
        "fulfillment_rate": round(fulfillment_rate * 100, 2),
        "total_allocations": len(allocations),
        "total_travel_minutes": total_travel_time,
        "avg_travel_minutes": round(avg_travel_time, 2),
        "avg_safety_margin_minutes": round(avg_safety_margin, 2),
        "at_risk_unallocated_units": near_expiry_waste,
    }


def compare_baseline_and_optimizer(world=None):
    """
    Clones the world state, runs both strategies independently,
    and returns a side-by-side metric comparison.
    """
    if world is None:
        world = build_world()

    # Deepcopy to ensure both algorithms start from the exact same initial state
    world_baseline = copy.deepcopy(world)
    world_optimizer = copy.deepcopy(world)

    allocs_baseline = run_baseline(world_baseline)
    allocs_optimizer = run_optimizer(world_optimizer)

    metrics_baseline = compute_metrics(world_baseline, allocs_baseline)
    metrics_optimizer = compute_metrics(world_optimizer, allocs_optimizer)

    return {
        "baseline": {
            "metrics": metrics_baseline,
            "allocations": allocs_baseline,
        },
        "optimizer": {
            "metrics": metrics_optimizer,
            "allocations": allocs_optimizer,
        },
        "summary": {
            "travel_time_difference": (
                metrics_optimizer["total_travel_minutes"] - metrics_baseline["total_travel_minutes"]
            ),
            "at_risk_waste_reduction": (
                metrics_baseline["at_risk_unallocated_units"] - metrics_optimizer["at_risk_unallocated_units"]
            ),
        }
    }