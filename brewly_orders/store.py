"""Where orders live: today's open orders in memory, plus the order history file.

The history is Brewly's record of every past sale. Finance uses it for refunds and the
accounts, so it is kept, never cleared.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

HISTORY = Path(__file__).resolve().parent.parent / "data" / "order-history.jsonl"


@dataclass
class Order:
    id: str
    cafe_id: str
    items: list[str]
    total_pence: int
    request_id: str
    status: str = "pending"  # pending, paid, collected


class OrderStore:
    def __init__(self) -> None:
        self._orders: list[Order] = []

    def add(self, order: Order) -> None:
        self._orders.append(order)

    def get(self, order_id: str) -> Order | None:
        return next((order for order in self._orders if order.id == order_id), None)

    def all(self) -> list[Order]:
        return list(self._orders)

    def __len__(self) -> int:
        return len(self._orders)


def load_history(path: Path = HISTORY) -> list[dict]:
    """Every past order, oldest first."""
    with path.open(encoding="utf-8") as lines:
        return [json.loads(line) for line in lines if line.strip()]
