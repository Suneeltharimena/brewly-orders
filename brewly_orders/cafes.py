"""Brewly's 120 cafés and who is on shift (practice data)."""

CAFE_IDS = [f"BR{number:03d}" for number in range(1, 121)]

# Most cafés run two baristas; a few busy ones run three.
BARISTAS = {"BR001": 3, "BR017": 3, "BR042": 3}


def check_cafe(cafe_id: str) -> None:
    if cafe_id not in CAFE_IDS:
        raise ValueError(f"no such café: {cafe_id}")


def baristas_on_shift(cafe_id: str) -> int:
    check_cafe(cafe_id)
    return BARISTAS.get(cafe_id, 2)
