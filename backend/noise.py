# backend/noise.py
import copy
import random


def add_dirty_records(world, seed=7):
    rng = random.Random(seed)
    dirty = copy.deepcopy(world)
    units = dirty["units"]
    log = []

    # Pick 5 different units to damage. Skip U01 and U02 (positions 0 and 1)
    # so the demo trap stays intact.
    missing, dup, fmt, negative, bad_hosp = rng.sample(range(2, len(units)), 5)

    # 1. Missing value
    units[missing]["expires_at"] = None
    log.append(f"{units[missing]['unit_id']}: expires_at is missing")

    # 2. Inconsistent format
    units[fmt]["blood_group"] = units[fmt]["blood_group"].lower()
    log.append(f"{units[fmt]['unit_id']}: blood_group written as '{units[fmt]['blood_group']}'")

    # 3. Wrong value
    units[negative]["expires_at"] = -15
    log.append(f"{units[negative]['unit_id']}: expires_at is negative (-15)")

    # 4. Unknown hospital
    units[bad_hosp]["hospital_id"] = "Z"
    log.append(f"{units[bad_hosp]['unit_id']}: hospital_id 'Z' does not exist")

    # 5. Duplicate record (added last so the positions above stay valid)
    units.append(copy.deepcopy(units[dup]))
    log.append(f"{units[dup]['unit_id']}: record is duplicated")

    return dirty, log