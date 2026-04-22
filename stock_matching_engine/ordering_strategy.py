from abc import ABC, abstractmethod
from typing import List

from stock_matching_engine.order import Order


class OrderBookOrderingStrategy(ABC):
    @abstractmethod
    def sort(self, orders: List[Order]) -> List[Order]:
        pass
