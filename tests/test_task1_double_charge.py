"""Task 1: a customer must never pay twice for one order. These fail until the bug is fixed."""
from brewly_orders.orders import OrderService
from brewly_orders.payments import FakeGateway
from brewly_orders.store import OrderStore


def test_a_slow_gateway_does_not_charge_twice():
    # The first attempt takes the money, then times out; the service retries.
    gateway = FakeGateway(timeouts_after_charge=1)
    service = OrderService(OrderStore(), gateway)
    order = service.place_order("BR004", ["coffee"], request_id="r-1")
    assert order.status == "paid"
    assert len(gateway.charges) == 1, f"the card was charged {len(gateway.charges)} times for one coffee"


def test_tapping_pay_twice_gives_one_order_and_one_charge(service, gateway):
    first = service.place_order("BR005", ["coffee"], request_id="r-7")
    second = service.place_order("BR005", ["coffee"], request_id="r-7")
    assert second.id == first.id, "the same request_id must return the same order"
    assert len(service.store) == 1
    assert len(gateway.charges) == 1, f"the card was charged {len(gateway.charges)} times for one tap-twice order"


def test_different_requests_are_still_charged(service, gateway):
    service.place_order("BR005", ["coffee"], request_id="r-8")
    service.place_order("BR005", ["coffee"], request_id="r-9")
    assert len(gateway.charges) == 2, "two different orders must be two charges"
