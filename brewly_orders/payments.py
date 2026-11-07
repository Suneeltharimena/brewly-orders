"""A pretend card payment gateway that behaves like real ones.

Like real gateways, it treats a repeated idempotency key as the same request: the second call
returns the first charge instead of charging again. It can also be told to time out *after*
taking the money, which is what slow networks do in real life, or be down altogether.
"""
from __future__ import annotations

from dataclasses import dataclass


class PaymentTimeout(Exception):
    """The gateway did not answer in time. The charge may or may not have gone through."""


class PaymentFailed(Exception):
    """Every attempt to take payment failed."""


@dataclass(frozen=True)
class Charge:
    key: str
    order_id: str
    amount_pence: int


class FakeGateway:
    def __init__(self, timeouts_after_charge: int = 0, unreachable: bool = False) -> None:
        self.charges: list[Charge] = []
        self._by_key: dict[str, Charge] = {}
        self._timeouts_left = timeouts_after_charge
        self._unreachable = unreachable

    def charge(self, key: str, order_id: str, amount_pence: int) -> Charge:
        if self._unreachable:
            raise PaymentTimeout("the gateway is down")
        if key in self._by_key:
            return self._by_key[key]
        charge = Charge(key=key, order_id=order_id, amount_pence=amount_pence)
        self.charges.append(charge)
        self._by_key[key] = charge
        if self._timeouts_left:
            self._timeouts_left -= 1
            raise PaymentTimeout("no answer from the gateway")
        return charge
