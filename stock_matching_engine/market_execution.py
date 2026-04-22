from stock_matching_engine.execution_strategy import OrderExecutionStrategy
from stock_matching_engine.order import Order


class MarketOrderExecutionStrategy(OrderExecutionStrategy):
    def can_match(self, incoming: Order, book_order: Order) -> bool:
        return True
