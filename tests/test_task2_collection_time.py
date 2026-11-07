"""Task 2: tell the customer when to collect. These fail until the feature is built (see TASKS.md)."""
import pytest

from brewly_orders.orders import OrderService
from brewly_orders.payments import FakeGateway
from brewly_orders.store import OrderStore


def ready(order) -> int:
    minutes = getattr(order, "ready_in_minutes", None)
    assert minutes is not None, "a paid order needs ready_in_minutes (TASKS.md, task 2)"
    return minutes


def test_an_empty_cafe_still_quotes_two_minutes(service):
    # 1 drink x 1.5 minutes / 2 baristas = 0.75, so the 2-minute minimum applies.
    assert ready(service.place_order("BR010", ["coffee"], request_id="r-1")) == 2


def test_drinks_already_waiting_count(service):
    for number in range(5):
        service.place_order("BR010", ["coffee"], request_id=f"ahead-{number}")
    # 5 drinks ahead + 2 in this order = 7 drinks x 1.5 minutes / 2 baristas = 5.25, rounded up to 6.
    assert ready(service.place_order("BR010", ["coffee", "tea"], request_id="r-1")) == 6


def test_food_needs_no_barista(service):
    for number in range(4):
        service.place_order("BR011", ["croissant"], request_id=f"ahead-{number}")
    assert ready(service.place_order("BR011", ["coffee", "croissant"], request_id="r-1")) == 2


def test_only_this_cafes_unfinished_drinks_count(service):
    for number in range(6):
        service.place_order("BR012", ["coffee"], request_id=f"other-cafe-{number}")
    collected = [service.place_order("BR013", ["coffee", "coffee"], request_id=f"done-{n}") for n in range(3)]
    for order in collected:
        service.collect(order.id)
    assert ready(service.place_order("BR013", ["coffee"], request_id="r-1")) == 2


def test_more_baristas_means_a_shorter_wait():
    # BR001 runs three baristas: 8 drinks x 1.5 / 3 = 4 minutes exactly.
    service = OrderService(OrderStore(), FakeGateway())
    for number in range(7):
        service.place_order("BR001", ["tea"], request_id=f"ahead-{number}")
    assert ready(service.place_order("BR001", ["coffee"], request_id="r-1")) == 4


@pytest.mark.parametrize("items", [["croissant"], ["croissant", "croissant"]])
def test_food_only_orders_quote_the_minimum(service, items):
    assert ready(service.place_order("BR014", items, request_id="r-1")) == 2
