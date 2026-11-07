"""What the service already does. These pass before you start; keep them passing."""
import pytest

from brewly_orders.menu import price
from brewly_orders.orders import OrderService
from brewly_orders.payments import FakeGateway, PaymentFailed
from brewly_orders.store import OrderStore


def test_a_coffee_costs_three_pounds_fifty():
    assert price(["coffee"]) == 350


def test_unknown_items_are_refused():
    with pytest.raises(ValueError):
        price(["coffee", "unicorn latte"])


def test_an_empty_order_is_refused():
    with pytest.raises(ValueError):
        price([])


def test_placing_an_order_charges_the_card_once(service, gateway):
    order = service.place_order("BR001", ["coffee", "croissant"], request_id="r-1")
    assert order.status == "paid"
    assert order.total_pence == 625
    assert [charge.amount_pence for charge in gateway.charges] == [625]


def test_an_unknown_cafe_is_refused(service):
    with pytest.raises(ValueError):
        service.place_order("BR999", ["coffee"], request_id="r-1")


def test_payment_gives_up_when_the_gateway_is_down():
    gateway = FakeGateway(unreachable=True)
    service = OrderService(OrderStore(), gateway)
    with pytest.raises(PaymentFailed):
        service.place_order("BR002", ["tea"], request_id="r-1")
    assert gateway.charges == []
    assert len(service.store) == 0


def test_collecting_an_order(service):
    order = service.place_order("BR003", ["tea"], request_id="r-1")
    assert service.collect(order.id).status == "collected"
    with pytest.raises(ValueError):
        service.collect(order.id)
