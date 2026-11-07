"""Taking an order: price it, charge the card, keep it until the customer collects."""
from __future__ import annotations

import uuid

from brewly_orders.cafes import check_cafe
from brewly_orders.menu import price
from brewly_orders.payments import FakeGateway, PaymentFailed, PaymentTimeout
from brewly_orders.store import Order, OrderStore

MAX_ATTEMPTS = 3


class OrderService:
    def __init__(self, store: OrderStore, gateway: FakeGateway) -> None:
        self.store = store
        self.gateway = gateway

    def place_order(self, cafe_id: str, items: list[str], request_id: str) -> Order:
        """Price the order and take payment, retrying if the gateway is slow.

        ``request_id`` comes from the app: it is the same each time the customer taps Pay
        for the same basket.
        """
        check_cafe(cafe_id)
        total = price(items)
        order = Order(id=f"ord-{len(self.store) + 1}", cafe_id=cafe_id, items=list(items), total_pence=total, request_id=request_id)
        for _ in range(MAX_ATTEMPTS):
            try:
                self.gateway.charge(key=uuid.uuid4().hex, order_id=order.id, amount_pence=total)
                break
            except PaymentTimeout:
                continue
        else:
            raise PaymentFailed(f"could not take payment for {order.id}")
        order.status = "paid"
        self.store.add(order)
        return order

    def collect(self, order_id: str) -> Order:
        """The customer has picked up their order."""
        order = self.store.get(order_id)
        if order is None:
            raise KeyError(order_id)
        if order.status != "paid":
            raise ValueError(f"{order_id} is {order.status}, not ready to collect")
        order.status = "collected"
        return order
