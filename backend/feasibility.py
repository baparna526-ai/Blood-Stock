# backend/feasibility.py
import heapq


# For each patient group, the donor groups whose red cells are safe to give.
RBC_DONORS_FOR = {
    "O-":  {"O-"},
    "O+":  {"O-", "O+"},
    "A-":  {"O-", "A-"},
    "A+":  {"O-", "O+", "A-", "A+"},
    "B-":  {"O-", "B-"},
    "B+":  {"O-", "O+", "B-", "B+"},
    "AB-": {"O-", "A-", "B-", "AB-"},
    "AB+": {"O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"},
}


def check_compatible(unit, request):
    if unit["component"] != request["component"]:
        return False, f"unit is {unit['component']} but request needs {request['component']}"
    if unit["blood_group"] not in RBC_DONORS_FOR[request["patient_group"]]:
        return False, f"{unit['blood_group']} cannot be given to a {request['patient_group']} patient"
    return True, "compatible"

def check_free(unit, world=None):
    if unit["status"] != "AVAILABLE":
        return False, f"unit {unit['unit_id']} is not available (status: {unit['status']})"
    if world is not None:
        for entry in world["locked"]:
            if entry["unit_id"] == unit["unit_id"]:
                return False, (f"unit {unit['unit_id']} is already locked "
                               f"for request {entry['request_id']}")
    return True, "unit is free"

def find_route(world, from_id, to_id):
    for route in world["travel"]:
        if route["from_id"] == from_id and route["to_id"] == to_id:
            return route
    return None


def find_best_path(world, start, end):
    """Fastest open path. Returns (minutes, [hospital ids]) or None."""
    if start == end:
        return 0, [start]

    best = {start: 0}
    came_from = {}
    queue = [(0, start)]

    while queue:
        minutes, here = heapq.heappop(queue)
        if here == end:
            path = [end]
            while path[-1] != start:
                path.append(came_from[path[-1]])
            path.reverse()
            return minutes, path
        if minutes > best.get(here, float("inf")):
            continue
        for route in world["travel"]:
            if route["from_id"] != here or route["blocked"]:
                continue
            new_minutes = minutes + route["minutes"]
            if new_minutes < best.get(route["to_id"], float("inf")):
                best[route["to_id"]] = new_minutes
                came_from[route["to_id"]] = here
                heapq.heappush(queue, (new_minutes, route["to_id"]))

    return None

def check_route(unit, request, world):
    start = unit["hospital_id"]
    end = request["hospital_id"]
    result = find_best_path(world, start, end)
    if result is None:
        return False, f"no open route from {start} to {end}"
    minutes, path = result
    return True, f"best route {' -> '.join(path)} takes {minutes} min"

def check_timing(unit, request, world, buffer=10):
    result = find_best_path(world, unit["hospital_id"], request["hospital_id"])
    if result is None:
        return False, "no open route, so there is no arrival time"
    travel, path = result
    arrival = world["now"] + travel

    expiry_spare = unit["expires_at"] - arrival
    if expiry_spare < 0:
        return False, (f"would expire {-expiry_spare} min before arrival "
                       f"(arrives at minute {arrival}, expires at minute {unit['expires_at']})")
    if expiry_spare < buffer:
        return False, f"arrives only {expiry_spare} min before expiry, buffer needed is {buffer}"

    deadline_spare = request["needed_by"] - arrival
    if deadline_spare < 0:
        return False, (f"would arrive {-deadline_spare} min after the deadline "
                       f"(arrives at minute {arrival}, needed by minute {request['needed_by']})")
    if deadline_spare < buffer:
        return False, f"arrives only {deadline_spare} min before the deadline, buffer needed is {buffer}"

    return True, (f"arrives at minute {arrival}: {expiry_spare} min before expiry, "
                  f"{deadline_spare} min before deadline")

def is_feasible(unit, request, world, buffer=10):
    ok, reason = check_compatible(unit, request)
    if not ok:
        return False, reason

    ok, reason = check_free(unit, world)
    if not ok:
        return False, reason

    ok, reason = check_route(unit, request, world)
    if not ok:
        return False, reason

    ok, reason = check_timing(unit, request, world, buffer)
    if not ok:
        return False, reason

    return True, reason