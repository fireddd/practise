from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from stock_matching_engine.enums import OrderStatus
from stock_matching_engine.order import Order
from stock_matching_engine.ordering_strategy import OrderBookOrderingStrategy


class OrderBook(ABC):
    def __init__(self, ordering_strategy: OrderBookOrderingStrategy):
        self._ordering_strategy = ordering_strategy
        self._orders: Dict[str, Order] = {}

    def add(self, order: Order):
        self._orders[order.order_id] = order

    def cancel(self, order_id: str) -> bool:
        if order_id in self._orders:
            self._orders[order_id].cancel()
            del self._orders[order_id]
            return True
        return False

    def get_sorted_orders(self) -> List[Order]:
        active = [o for o in self._orders.values() if o.status in (OrderStatus.OPEN, OrderStatus.PARTIALLY_FILLED)]
        return self._ordering_strategy.sort(active)

    def get_best_order(self) -> Optional[Order]:
        sorted_orders = self.get_sorted_orders()
        return sorted_orders[0] if sorted_orders else None

    def remove_filled(self):
        filled_ids = [oid for oid, o in self._orders.items() if o.status == OrderStatus.FILLED]
        for oid in filled_ids:
            del self._orders[oid]

    @property
    def orders(self) -> Dict[str, Order]:
        return self._orders


class BuyOrderBook(OrderBook):
    pass


class SellOrderBook(OrderBook):
    pass
