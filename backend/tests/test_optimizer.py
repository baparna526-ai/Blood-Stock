# backend/tests/test_optimizer.py
from backend.simulator import build_world
from backend.optimizer import run_optimizer


def test_optimizer_prefers_earlier_expiring_unit_fefo():
    world = build_world()
    
    req = {
        "request_id": "R99",
        "hospital_id": "C",
        "component": "RBC",
        "patient_group": "A+",
        "units_needed": 1,
        "priority": "URGENT",
        "needed_by": 200,
        "status": "OPEN",
    }
    
    # Candidate 1: fresh (expires at 600 min)
    # Candidate 2: expiring sooner (expires at 150 min)
    unit_fresh = {
        "unit_id": "U_FRESH",
        "component": "RBC",
        "blood_group": "A+",
        "hospital_id": "A",
        "expires_at": 600,
        "status": "AVAILABLE",
    }
    unit_expiring_soon = {
        "unit_id": "U_SOON",
        "component": "RBC",
        "blood_group": "A+",
        "hospital_id": "A",
        "expires_at": 150,
        "status": "AVAILABLE",
    }

    world["requests"] = [req]
    world["units"] = [unit_fresh, unit_expiring_soon]

    allocations = run_optimizer(world)

    assert len(allocations) == 1
    # Optimizer should select the unit expiring sooner to prevent wastage
    assert allocations[0]["unit_id"] == "U_SOON"


def test_optimizer_locks_units():
    world = build_world()
    allocations = run_optimizer(world)

    allocated_unit_ids = [a["unit_id"] for a in allocations]
    locked_unit_ids = [entry["unit_id"] for entry in world["locked"]]

    assert allocated_unit_ids == locked_unit_ids
    assert len(allocated_unit_ids) == len(set(allocated_unit_ids))