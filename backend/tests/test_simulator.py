# backend/tests/test_simulator.py
from backend.simulator import build_world

# for u in build_world()["units"]:
#     if u["hospital_id"] == "C":
#         print(u["unit_id"], u["component"], u["blood_group"])

# Blood groups that can safely give red cells to an A+ patient
COMPATIBLE_WITH_A_POS = {"O-", "O+", "A-", "A+"}

from backend.simulator import build_world


def test_world_has_expected_counts():
    world = build_world()
    assert world["now"] == 0
    assert len(world["hospitals"]) == 5
    assert len(world["travel"]) == 20
    assert len(world["units"]) == 30
    assert len(world["requests"]) == 5


def test_world_is_repeatable():
    assert build_world() == build_world()


def test_unit_ids_are_unique():
    ids = [u["unit_id"] for u in build_world()["units"]]
    assert len(ids) == len(set(ids))


def test_demo_trap_unit_expires_before_arrival():
    world = build_world()
    units = {u["unit_id"]: u for u in world["units"]}
    minutes = {(r["from_id"], r["to_id"]): r["minutes"] for r in world["travel"]}

    u01 = units["U01"]
    u02 = units["U02"]
    assert minutes[(u01["hospital_id"], "C")] > u01["expires_at"]
    assert minutes[(u02["hospital_id"], "C")] < u02["expires_at"]


def test_no_compatible_unit_already_at_hospital_c():
    units = build_world()["units"]
    at_c = [u for u in units
            if u["hospital_id"] == "C" and u["blood_group"] in COMPATIBLE_WITH_A_POS]
    assert at_c == []