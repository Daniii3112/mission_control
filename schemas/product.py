from typing_extensions import TypedDict


class ProductOption(TypedDict):
    id: str
    name: str
    description: str
    target_audience: str
    price_range: str
    time_to_market: str
    key_differentiator: str
