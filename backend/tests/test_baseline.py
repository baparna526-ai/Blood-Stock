# backend/tests/test_baseline.py
from backend.simulator import build_world
from backend.baseline import run_baseline
from backend.events import block_route


def test_baseline_avoids_trap_unit_for_r01():
    world = build_world()
    # Isolate to only the trap scenario units (U01 and U02) and request R01
    world["units"] = [u for u in world["units"] if u["unit_id"] in ("U01", "U02")]
    world["requests"] = [r for r in world["requests"] if r["request_id"] == "R01"]

    allocations = run_baseline(world)

    assert len(allocations) == 1
    r01_alloc = allocations[0]

    # U01 at B expires in 40 min (travel is 45 min) -> rejected
    # Baseline must bypass U01 and allocate U02 from A (60 min)
    assert r01_alloc["unit_id"] == "U02"
    assert r01_alloc["from_hospital"] == "A"
    assert r01_alloc["to_hospital"] == "C"
    assert r01_alloc["travel_minutes"] == 60


def test_baseline_locks_units_preventing_double_booking():
    world = build_world()
    allocations = run_baseline(world)

    allocated_unit_ids = [a["unit_id"] for a in allocations]
    locked_unit_ids = [entry["unit_id"] for entry in world["locked"]]

    # Every allocated unit must be in world["locked"]
    assert allocated_unit_ids == locked_unit_ids

    # No unit should be allocated more than once
    assert len(allocated_unit_ids) == len(set(allocated_unit_ids))


def test_baseline_handles_rerouting():
    world = build_world()
    # Isolate to U02 and R01 to test the specific detour route
    world["units"] = [u for u in world["units"] if u["unit_id"] == "U02"]
    world["requests"] = [r for r in world["requests"] if r["request_id"] == "R01"]

    # Block direct route A -> C (normally 60 min)
    block_route(world, "A", "C")

    allocations = run_baseline(world)
    assert len(allocations) == 1
    r01_alloc = allocations[0]

    # Fastest open route becomes A -> B -> C (20 + 45 = 65 min)
    assert r01_alloc["unit_id"] == "U02"
    assert r01_alloc["path"] == ["A", "B", "C"]
    assert r01_alloc["travel_minutes"] == 65


def test_baseline_priority_order():
    world = build_world()
    allocations = run_baseline(world)

    # Urgent requests (R01, R04) should be evaluated first
    allocated_request_ids = [a["request_id"] for a in allocations]
    assert "R01" in allocated_request_ids
    assert "R04" in allocated_request_ids