import pytest

from brewly_orders.orders import OrderService
from brewly_orders.payments import FakeGateway
from brewly_orders.store import OrderStore


@pytest.fixture
def gateway() -> FakeGateway:
    return FakeGateway()


@pytest.fixture
def service(gateway: FakeGateway) -> OrderService:
    return OrderService(OrderStore(), gateway)
