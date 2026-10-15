# backend/simulator.py

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