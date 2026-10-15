# backend/validation.py

VALID_GROUPS = {"O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"}


def clean_units(units, hospital_ids):
    clean = []
    report = []
    seen = set()

    for original in units:
        unit = dict(original)
        uid = unit["unit_id"]

        # Duplicate: drop the extra copy
        if uid in seen:
            report.append({"unit_id": uid, "action": "DROPPED", "reason": "duplicate record"})
            continue
        seen.add(uid)

        # Fix messy blood group (a+ becomes A+)
        group = unit.get("blood_group")
        if isinstance(group, str):
            fixed = group.strip().upper()
            if fixed != group:
                unit["blood_group"] = fixed
                report.append({"unit_id": uid, "action": "FIXED",
                               "reason": f"blood group '{group}' changed to '{fixed}'"})

        # Things we cannot trust: set aside with a reason
        problem = None
        if unit.get("blood_group") not in VALID_GROUPS:
            problem = f"unknown blood group '{unit.get('blood_group')}'"
        elif unit.get("expires_at") is None:
            problem = "expiry is missing"
        elif unit["expires_at"] <= 0:
            problem = f"expiry is not positive ({unit['expires_at']})"
        elif unit.get("hospital_id") not in hospital_ids:
            problem = f"hospital '{unit.get('hospital_id')}' does not exist"

        if problem:
            report.append({"unit_id": uid, "action": "QUARANTINED", "reason": problem})
            continue

        clean.append(unit)

    return clean, report