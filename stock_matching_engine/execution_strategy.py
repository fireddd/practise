from abc import ABC, abstractmethod

from stock_matching_engine.order import Order


class OrderExecutionStrategy(ABC):
    @abstractmethod
    def can_match(self, incoming: Order, book_order: Order) -> bool:
        pass
