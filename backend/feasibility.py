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