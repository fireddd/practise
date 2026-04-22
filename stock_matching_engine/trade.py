from dataclasses import dataclass


@dataclass
class Trade:
    trade_id: str
    buy_order_id: str
    sell_order_id: str
    stock: str
    price: float
    quantity: int
