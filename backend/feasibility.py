# backend/feasibility.py

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

def check_free(unit):
    if unit["status"] != "AVAILABLE":
        return False, f"unit {unit['unit_id']} is not available (status: {unit['status']})"
    return True, "unit is free"

def find_route(world, from_id, to_id):
    for route in world["travel"]:
        if route["from_id"] == from_id and route["to_id"] == to_id:
            return route
    return None


def check_route(unit, request, world):
    start = unit["hospital_id"]
    end = request["hospital_id"]
    if start == end:
        return True, "unit is already at the requesting hospital"
    route = find_route(world, start, end)
    if route is None:
        return False, f"no route from {start} to {end}"
    if route["blocked"]:
        return False, f"route from {start} to {end} is blocked"
    return True, f"route {start} to {end} is open"