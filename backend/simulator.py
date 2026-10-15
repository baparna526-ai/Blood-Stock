# backend/simulator.py
import random

def make_hospitals():
    return [
        {"hospital_id": "A", "name": "Sanjeevni Hospital", "lat": 26.9124, "lng": 75.7873},
        {"hospital_id": "B", "name": "Medanta Hospital",    "lat": 26.9450, "lng": 75.8200},
        {"hospital_id": "C", "name": "Max Healthcare", "lat": 27.0100, "lng": 75.7700},
        {"hospital_id": "D", "name": "Manipal Hospitals",     "lat": 26.8600, "lng": 75.8300},
        {"hospital_id": "E", "name": "Fortis Escorts Hospital",    "lat": 26.8800, "lng": 75.7000},
    ]

def make_travel_times():
    one_way = {
        ("A", "B"): 20,
        ("A", "C"): 60,
        ("A", "D"): 35,
        ("A", "E"): 75,
        ("B", "C"): 45,
        ("B", "D"): 40,
        ("B", "E"): 70,
        ("C", "D"): 80,
        ("C", "E"): 90,
        ("D", "E"): 50,
    }

    routes = []
    for (from_id, to_id), minutes in one_way.items():
        routes.append({"from_id": from_id, "to_id": to_id,
                       "minutes": minutes, "blocked": False})
        routes.append({"from_id": to_id, "to_id": from_id,
                       "minutes": minutes, "blocked": False})
    return routes

def make_units():
    rng = random.Random(42)

    hospital_ids = ["A", "B", "C", "D", "E"]
    groups  = ["O+", "A+", "B+", "AB+", "O-", "A-", "B-", "AB-"]
    weights = [38, 27, 8, 2, 7, 6, 2, 1]

    units = [
        {"unit_id": "U01", "component": "RBC", "blood_group": "A+",
         "hospital_id": "B", "expires_at": 40, "status": "AVAILABLE"},
        {"unit_id": "U02", "component": "RBC", "blood_group": "A+",
         "hospital_id": "A", "expires_at": 360, "status": "AVAILABLE"},
    ]

    for number in range(3, 31):
        units.append({
            "unit_id": f"U{number:02d}",
            "component": "RBC",
            "blood_group": rng.choices(groups, weights=weights)[0],
            "hospital_id": rng.choice(hospital_ids),
            "expires_at": rng.randint(30, 720),
            "status": "AVAILABLE",
        })
    return units

def make_requests():
    return [
        {"request_id": "R01", "hospital_id": "C", "component": "RBC",
         "patient_group": "A+", "units_needed": 1,
         "priority": "URGENT", "needed_by": 90, "status": "OPEN"},
        {"request_id": "R02", "hospital_id": "C", "component": "RBC",
         "patient_group": "O+", "units_needed": 1,
         "priority": "ROUTINE", "needed_by": 300, "status": "OPEN"},
        {"request_id": "R03", "hospital_id": "D", "component": "RBC",
         "patient_group": "B+", "units_needed": 2,
         "priority": "ROUTINE", "needed_by": 400, "status": "OPEN"},
        {"request_id": "R04", "hospital_id": "E", "component": "RBC",
         "patient_group": "O-", "units_needed": 1,
         "priority": "URGENT", "needed_by": 150, "status": "OPEN"},
        {"request_id": "R05", "hospital_id": "B", "component": "RBC",
         "patient_group": "A-", "units_needed": 1,
         "priority": "ROUTINE", "needed_by": 500, "status": "OPEN"},
    ]

def build_world():
    return {
        "now": 0,
        "hospitals": make_hospitals(),
        "travel": make_travel_times(),
        "units": make_units(),
        "requests": make_requests(),
        "locked": [],
    }