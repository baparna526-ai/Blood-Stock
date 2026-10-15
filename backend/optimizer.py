# backend/optimizer.py
from backend.feasibility import is_feasible, find_best_path


def score_candidate(unit, request, travel_minutes):
    """
    Lower score = better match.
    Prioritizes:
      1. FEFO (First-Expired, First-Out): uses units closest to expiry to prevent spoilage.
      2. Travel efficiency: penalizes excessively long transit.
    """
    expiry_penalty = unit["expires_at"]
    travel_penalty = travel_minutes * 1.5

    return expiry_penalty + travel_penalty


def run_optimizer(world, buffer=10):
    """
    Smart Optimizer:
    1. Sorts requests by priority (URGENT first) and tightest deadline.
    2. For each request, filters all feasible units.
    3. Ranks candidates using FEFO + travel penalty to minimize blood waste.
    4. Locks the chosen unit and records allocation.
    """
    allocations = []

    priority_order = {"URGENT": 0, "ROUTINE": 1}
    open_requests = [r for r in world["requests"] if r["status"] == "OPEN"]
    open_requests.sort(key=lambda r: (priority_order.get(r["priority"], 9), r["needed_by"]))

    for request in open_requests:
        needed = request.get("units_needed", 1)

        while needed > 0:
            candidates = []

            for unit in world["units"]:
                feasible, _ = is_feasible(unit, request, world, buffer=buffer)
                if not feasible:
                    continue

                route_res = find_best_path(world, unit["hospital_id"], request["hospital_id"])
                if route_res is None:
                    continue

                travel_minutes, path = route_res
                score = score_candidate(unit, request, travel_minutes)
                candidates.append((score, travel_minutes, path, unit))

            if not candidates:
                break

            candidates.sort(key=lambda c: c[0])
            best_score, best_travel, best_path, best_unit = candidates[0]

            world["locked"].append({
                "unit_id": best_unit["unit_id"],
                "request_id": request["request_id"],
                "travel_minutes": best_travel,
                "path": best_path,
                "arrival_time": world["now"] + best_travel,
            })

            allocations.append({
                "request_id": request["request_id"],
                "unit_id": best_unit["unit_id"],
                "from_hospital": best_unit["hospital_id"],
                "to_hospital": request["hospital_id"],
                "travel_minutes": best_travel,
                "path": best_path,
                "arrival_time": world["now"] + best_travel,
                "expires_at": best_unit["expires_at"],
            })

            needed -= 1

    return allocations