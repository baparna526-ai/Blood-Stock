from backend.simulator import build_world
from backend.events import block_route, add_urgent_requests, cancel_request, add_stock


def test_all_events_work_together():
    w = build_world()

    block_route(w, 'A', 'C')
    add_urgent_requests(w, 'A', 'O-', 2, w['now'] + 120)
    cancel_request(w, 'R01')
    add_stock(w, 'A', 'O-', 3, w['now'] + 500)

    texts = [entry['text'] for entry in w['event_log']]
    assert texts == [
        "Transport failure: route A-C blocked",
        "Demand spike: 2 urgent O- request(s) at A",
        "Cancellation: request R01 cancelled",
        "New stock: 3 unit(s) of O- at A",
    ]