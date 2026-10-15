# backend/tests/test_metrics.py
from backend.simulator import build_world
from backend.metrics import compute_metrics, compare_baseline_and_optimizer


def test_compute_metrics_empty():
    world = {"requests": [{"request_id": "R01"}], "units": []}
    metrics = compute_metrics(world, [])
    assert metrics["total_requests"] == 1
    assert metrics["fulfilled_requests"] == 0
    assert metrics["fulfillment_rate"] == 0.0
    assert metrics["total_travel_minutes"] == 0


def test_compare_baseline_and_optimizer_runs():
    world = build_world()
    result = compare_baseline_and_optimizer(world)

    assert "baseline" in result
    assert "optimizer" in result
    assert "summary" in result

    base_metrics = result["baseline"]["metrics"]
    opt_metrics = result["optimizer"]["metrics"]

    # Both should successfully fulfill all valid requests
    assert base_metrics["fulfilled_requests"] > 0
    assert opt_metrics["fulfilled_requests"] > 0
    assert "total_travel_minutes" in base_metrics
    assert "total_travel_minutes" in opt_metrics


def test_comparison_preserves_world_isolation():
    # Verify neither strategy mutates the original world
    world = build_world()
    locked_count_before = len(world["locked"])

    compare_baseline_and_optimizer(world)

    assert len(world["locked"]) == locked_count_before