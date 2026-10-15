# backend/baseline.py
from backend.feasibility import is_feasible, find_best_path


def run_baseline(world, buffer=10):
    """
    Greedy nearest-unit heuristic:
    1. Evaluates open requests (prioritizing URGENT before ROUTINE, then earliest needed_by).
    2. For each request, finds all feasible units.
    3. Picks the feasible unit with the lowest travel time (nearest).
    4. Locks the unit and assigns it to the request.
    """
    allocations = []
    
    # Sort requests: URGENT first (URGENT < ROUTINE), then by deadline
    priority_order = {"URGENT": 0, "ROUTINE": 1}
    open_requests = [r for r in world["requests"] if r["status"] == "OPEN"]
    open_requests.sort(key=lambda r: (priority_order.get(r["priority"], 9), r["needed_by"]))

    for request in open_requests:
        needed = request.get("units_needed", 1)
        
        while needed > 0:
            best_unit = None
            min_travel = float("inf")
            best_route_info = None

            for unit in world["units"]:
                feasible, _ = is_feasible(unit, request, world, buffer=buffer)
                if not feasible:
                    continue

                route_res = find_best_path(world, unit["hospital_id"], request["hospital_id"])
                if route_res is None:
                    continue

                travel_minutes, path = route_res
                if travel_minutes < min_travel:
                    min_travel = travel_minutes
                    best_unit = unit
                    best_route_info = (travel_minutes, path)

            if best_unit is None:
                # No more feasible units for this request
                break

            # Lock the unit
            world["locked"].append({
                "unit_id": best_unit["unit_id"],
                "request_id": request["request_id"],
                "travel_minutes": best_route_info[0],
                "path": best_route_info[1],
                "arrival_time": world["now"] + best_route_info[0]
            })

            allocations.append({
                "request_id": request["request_id"],
                "unit_id": best_unit["unit_id"],
                "from_hospital": best_unit["hospital_id"],
                "to_hospital": request["hospital_id"],
                "travel_minutes": best_route_info[0],
                "path": best_route_info[1],
                "arrival_time": world["now"] + best_route_info[0],
            })

            needed -= 1

    return allocations