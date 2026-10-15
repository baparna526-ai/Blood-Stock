# backend/api.py
import copy
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.simulator import build_world
from backend.optimizer import run_optimizer
from backend.metrics import compute_metrics, compare_baseline_and_optimizer
from backend.noise import add_dirty_records
from backend.validation import clean_units
from backend import events

app = FastAPI(title="Blood Stock API")

# Allow the frontend on any local port (5173, 5174, ...)
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_methods=["*"],
    allow_headers=["*"],
)

# The one current world. Events change it, /reset rebuilds it.
state = {"world": build_world()}


def run_event(action):
    """Run an event function; turn its ValueError into a clean 400 response."""
    try:
        action()
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
    return state["world"]


# ---------- read ----------
@app.get("/world")
def get_world():
    return state["world"]


@app.get("/compare")
def get_compare():
    return compare_baseline_and_optimizer(state["world"])


@app.post("/plan")
def make_plan():
    world = copy.deepcopy(state["world"])      # plan on a copy, so the state stays untouched
    allocations = run_optimizer(world)
    return {"allocations": allocations,
            "metrics": compute_metrics(world, allocations)}


@app.get("/noise-demo")
def noise_demo():
    dirty, injected = add_dirty_records(build_world())
    hospital_ids = {h["hospital_id"] for h in dirty["hospitals"]}
    clean, report = clean_units(dirty["units"], hospital_ids)
    return {"units_before": len(dirty["units"]), "units_after": len(clean),
            "injected": injected, "cleaner_report": report}


# ---------- change the world ----------
class BlockRoute(BaseModel):
    from_id: str
    to_id: str
    both_directions: bool = True


class UrgentRequest(BaseModel):
    hospital_id: str
    patient_group: str
    count: int = 1
    needed_by: int


class CancelRequest(BaseModel):
    request_id: str


class AddStock(BaseModel):
    hospital_id: str
    blood_group: str
    count: int = 1
    expires_at: int


@app.post("/events/block-route")
def block_route(body: BlockRoute):
    return run_event(lambda: events.block_route(
        state["world"], body.from_id, body.to_id, body.both_directions))


@app.post("/events/urgent-request")
def urgent_request(body: UrgentRequest):
    return run_event(lambda: events.add_urgent_requests(
        state["world"], body.hospital_id, body.patient_group, body.count, body.needed_by))


@app.post("/events/cancel")
def cancel(body: CancelRequest):
    return run_event(lambda: events.cancel_request(state["world"], body.request_id))


@app.post("/events/add-stock")
def add_stock(body: AddStock):
    return run_event(lambda: events.add_stock(
        state["world"], body.hospital_id, body.blood_group, body.count, body.expires_at))


@app.post("/reset")
def reset():
    state["world"] = build_world()
    return state["world"]