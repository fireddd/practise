import pytest

from stock_matching_engine.enums import OrderExecutionType, OrderStatus, OrderType
from stock_matching_engine.order import Order


class TestEnums:
    def test_order_types(self):
        assert OrderType.BUY.value == "BUY"
        assert OrderType.SELL.value == "SELL"

    def test_execution_types(self):
        assert OrderExecutionType.LIMIT.value == "LIMIT"
        assert OrderExecutionType.MARKET.value == "MARKET"

    def test_order_statuses(self):
        assert OrderStatus.OPEN.value == "OPEN"
        assert OrderStatus.FILLED.value == "FILLED"
        assert OrderStatus.PARTIALLY_FILLED.value == "PARTIALLY_FILLED"
        assert OrderStatus.CANCELLED.value == "CANCELLED"


class TestOrder:
    def _make_order(self, **kwargs):
        defaults = {
            "order_id": "O1",
            "stock": "AAPL",
            "order_type": OrderType.BUY,
            "execution_type": OrderExecutionType.LIMIT,
            "price": 150.0,
            "quantity": 100,
        }
        defaults.update(kwargs)
        return Order(**defaults)

    def test_order_creation(self):
        order = self._make_order()
        assert order.order_id == "O1"
        assert order.stock == "AAPL"
        assert order.order_type == OrderType.BUY
        assert order.execution_type == OrderExecutionType.LIMIT
        assert order.price == 150.0
        assert order.quantity == 100
        assert order.status == OrderStatus.OPEN
        assert order.filled_quantity == 0

    def test_remaining_quantity(self):
        order = self._make_order(quantity=100)
        assert order.remaining_quantity == 100

    def test_partial_fill(self):
        order = self._make_order(quantity=100)
        order.fill(40)
        assert order.filled_quantity == 40
        assert order.remaining_quantity == 60
        assert order.status == OrderStatus.PARTIALLY_FILLED

    def test_full_fill(self):
        order = self._make_order(quantity=100)
        order.fill(100)
        assert order.filled_quantity == 100
        assert order.remaining_quantity == 0
        assert order.status == OrderStatus.FILLED

    def test_multi_step_fill(self):
        order = self._make_order(quantity=100)
        order.fill(30)
        assert order.status == OrderStatus.PARTIALLY_FILLED
        order.fill(70)
        assert order.status == OrderStatus.FILLED

    def test_cancel(self):
        order = self._make_order()
        order.cancel()
        assert order.status == OrderStatus.CANCELLED

    def test_timestamp_auto_set(self):
        order = self._make_order()
        assert order.timestamp > 0
