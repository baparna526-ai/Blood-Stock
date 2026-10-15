# backend/events.py

VALID_GROUPS = {"O+", "A+", "B+", "AB+", "O-", "A-", "B-", "AB-"}


def _log(world, text):
    world.setdefault("event_log", []).append({"sim_time": world["now"], "text": text})


def _check_hospital(world, hospital_id):
    if hospital_id not in [h["hospital_id"] for h in world["hospitals"]]:
        raise ValueError(f"Unknown hospital: {hospital_id}")


def block_route(world, from_id, to_id, both_directions=True):
    changed = 0
    for route in world["travel"]:
        forward = route["from_id"] == from_id and route["to_id"] == to_id
        backward = (both_directions
                    and route["from_id"] == to_id and route["to_id"] == from_id)
        if forward or backward:
            route["blocked"] = True
            changed += 1
    if changed == 0:
        raise ValueError(f"No route between {from_id} and {to_id}")
    _log(world, f"Transport failure: route {from_id}-{to_id} blocked")
    return changed


def add_urgent_requests(world, hospital_id, patient_group, count, needed_by):
    _check_hospital(world, hospital_id)
    if patient_group not in VALID_GROUPS:
        raise ValueError(f"Unknown blood group: {patient_group}")
    if count < 1:
        raise ValueError("count must be at least 1")
    new_requests = []
    for _ in range(count):
        number = len(world["requests"]) + 1
        request = {
            "request_id": f"R{number:02d}", "hospital_id": hospital_id,
            "component": "RBC", "patient_group": patient_group,
            "units_needed": 1, "priority": "URGENT",
            "needed_by": needed_by, "status": "OPEN",
        }
        world["requests"].append(request)
        new_requests.append(request)
    _log(world, f"Demand spike: {count} urgent {patient_group} request(s) at {hospital_id}")
    return new_requests

def cancel_request(world, request_id):
    for request in world["requests"]:
        if request["request_id"] == request_id:
            request["status"] = "CANCELLED"
            world["locked"] = [r for r in world["locked"]
                               if r["request_id"] != request_id]
            _log(world, f"Cancellation: request {request_id} cancelled")
            return request
    raise ValueError(f"Unknown request: {request_id}")

def add_stock(world, hospital_id, blood_group, count, expires_at):
    _check_hospital(world, hospital_id)
    if blood_group not in VALID_GROUPS:
        raise ValueError(f"Unknown blood group: {blood_group}")
    if count < 1:
        raise ValueError("count must be at least 1")
    if expires_at <= world["now"]:
        raise ValueError("expires_at must be later than the current time")
    new_units = []
    for _ in range(count):
        number = len(world["units"]) + 1
        unit = {
            "unit_id": f"U{number:02d}", "component": "RBC",
            "blood_group": blood_group, "hospital_id": hospital_id,
            "expires_at": expires_at, "status": "AVAILABLE",
        }
        world["units"].append(unit)
        new_units.append(unit)
    _log(world, f"New stock: {count} unit(s) of {blood_group} at {hospital_id}")
    return new_units