# backend/tests/test_feasibility.py
from backend.simulator import build_world
from backend.feasibility import (
    check_compatible, check_free, find_best_path, check_route,
    check_timing, is_feasible,
)


def block(world, from_id, to_id):
    """Mark one road as blocked."""
    for route in world["travel"]:
        if route["from_id"] == from_id and route["to_id"] == to_id:
            route["blocked"] = True


def get(world):
    """Return the world plus the demo request R01 and units U01, U02."""
    return world, world["requests"][0], world["units"][0], world["units"][1]


# ---- check 1: compatibility ----
def test_compatible_unit_passes():
    w, r, u1, u2 = get(build_world())
    assert check_compatible(u2, r)[0] is True


def test_wrong_blood_group_fails():
    w, r, u1, u2 = get(build_world())
    ok, reason = check_compatible({**u2, "blood_group": "B+"}, r)
    assert ok is False
    assert "B+" in reason


def test_wrong_component_fails():
    w, r, u1, u2 = get(build_world())
    ok, reason = check_compatible({**u2, "component": "PLATELETS"}, r)
    assert ok is False


# ---- check 2: free ----
def test_available_unit_is_free():
    w, r, u1, u2 = get(build_world())
    assert check_free(u2)[0] is True


def test_reserved_unit_is_not_free():
    w, r, u1, u2 = get(build_world())
    assert check_free({**u2, "status": "RESERVED"})[0] is False


# ---- check 3: routes ----
def test_detour_when_direct_road_blocked():
    w, r, u1, u2 = get(build_world())
    block(w, "B", "C")
    assert find_best_path(w, "B", "C") == (80, ["B", "A", "C"])


def test_no_route_when_every_road_into_c_is_blocked():
    w, r, u1, u2 = get(build_world())
    for route in w["travel"]:
        if route["to_id"] == "C":
            route["blocked"] = True
    assert find_best_path(w, "B", "C") is None
    assert check_route(u1, r, w)[0] is False


def test_unit_already_at_destination_takes_zero_minutes():
    w, r, u1, u2 = get(build_world())
    assert find_best_path(w, "C", "C") == (0, ["C"])


# ---- check 4: timing ----
def test_demo_trap_unit_expires_before_arrival():
    w, r, u1, u2 = get(build_world())
    ok, reason = is_feasible(u1, r, w)
    assert ok is False
    assert "expire" in reason


def test_good_unit_is_feasible():
    w, r, u1, u2 = get(build_world())
    assert is_feasible(u2, r, w)[0] is True


def test_buffer_rejects_tight_expiry():
    w, r, u1, u2 = get(build_world())
    # A to C takes 60 min; expiry at 65 leaves only 5 spare, buffer is 10
    ok, reason = check_timing({**u2, "expires_at": 65}, r, w)
    assert ok is False
    assert "buffer" in reason


def test_late_arrival_fails_deadline():
    w, r, u1, u2 = get(build_world())
    ok, reason = check_timing(u2, {**r, "needed_by": 50}, w)
    assert ok is False
    assert "deadline" in reason


def test_timing_uses_detour_when_road_blocked():
    w, r, u1, u2 = get(build_world())
    block(w, "A", "C")  # direct A to C is 60; A to B to C is 65
    ok, reason = check_timing(u2, r, w)
    assert ok is True
    assert "minute 65" in reason

def test_locked_unit_is_not_free():
    w, r, u1, u2 = get(build_world())
    w["locked"].append({"unit_id": "U02", "request_id": "R02"})
    ok, reason = is_feasible(u2, r, w)
    assert ok is False
    assert "locked" in reason    
