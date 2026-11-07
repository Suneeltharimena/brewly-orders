"""Brewly's menu, in pence (practice data)."""

PRICES = {
    "coffee": 350,
    "tea": 300,
    "croissant": 275,
}

# Drinks need a barista; food comes from the counter.
DRINKS = {"coffee", "tea"}


def price(items: list[str]) -> int:
    """Total price of an order in pence. Unknown items are refused, never priced at zero."""
    if not items:
        raise ValueError("an order needs at least one item")
    unknown = [item for item in items if item not in PRICES]
    if unknown:
        raise ValueError(f"not on the menu: {', '.join(unknown)}")
    return sum(PRICES[item] for item in items)


def drink_count(items: list[str]) -> int:
    return sum(1 for item in items if item in DRINKS)
