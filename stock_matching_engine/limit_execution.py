from stock_matching_engine.enums import OrderType
from stock_matching_engine.execution_strategy import OrderExecutionStrategy
from stock_matching_engine.order import Order


class LimitOrderExecutionStrategy(OrderExecutionStrategy):
    def can_match(self, incoming: Order, book_order: Order) -> bool:
        if incoming.order_type == OrderType.BUY:
            return book_order.price <= incoming.price
        return book_order.price >= incoming.price
