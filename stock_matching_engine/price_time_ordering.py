from typing import List

from stock_matching_engine.enums import OrderType
from stock_matching_engine.order import Order
from stock_matching_engine.ordering_strategy import OrderBookOrderingStrategy


class PriceTimeOrderBookOrderingStrategy(OrderBookOrderingStrategy):
    def __init__(self, order_type: OrderType):
        self._order_type = order_type

    def sort(self, orders: List[Order]) -> List[Order]:
        if self._order_type == OrderType.BUY:
            return sorted(orders, key=lambda o: (-o.price, o.timestamp))
        return sorted(orders, key=lambda o: (o.price, o.timestamp))
