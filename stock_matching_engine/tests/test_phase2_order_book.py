import time

import pytest

from stock_matching_engine.enums import OrderExecutionType, OrderStatus, OrderType
from stock_matching_engine.order import Order
from stock_matching_engine.order_book import BuyOrderBook, SellOrderBook
from stock_matching_engine.price_time_ordering import PriceTimeOrderBookOrderingStrategy


def _make_order(order_id, order_type, price, quantity=100, ts=None):
    o = Order(
        order_id=order_id,
        stock="AAPL",
        order_type=order_type,
        execution_type=OrderExecutionType.LIMIT,
        price=price,
        quantity=quantity,
    )
    if ts is not None:
        o.timestamp = ts
    return o


class TestPriceTimeOrdering:
    def test_buy_orders_sorted_highest_price_first(self):
        strategy = PriceTimeOrderBookOrderingStrategy(OrderType.BUY)
        orders = [
            _make_order("O1", OrderType.BUY, 100.0, ts=1.0),
            _make_order("O2", OrderType.BUY, 150.0, ts=2.0),
            _make_order("O3", OrderType.BUY, 120.0, ts=3.0),
        ]
        sorted_orders = strategy.sort(orders)
        assert [o.order_id for o in sorted_orders] == ["O2", "O3", "O1"]

    def test_buy_orders_same_price_sorted_by_time(self):
        strategy = PriceTimeOrderBookOrderingStrategy(OrderType.BUY)
        orders = [
            _make_order("O1", OrderType.BUY, 150.0, ts=3.0),
            _make_order("O2", OrderType.BUY, 150.0, ts=1.0),
            _make_order("O3", OrderType.BUY, 150.0, ts=2.0),
        ]
        sorted_orders = strategy.sort(orders)
        assert [o.order_id for o in sorted_orders] == ["O2", "O3", "O1"]

    def test_sell_orders_sorted_lowest_price_first(self):
        strategy = PriceTimeOrderBookOrderingStrategy(OrderType.SELL)
        orders = [
            _make_order("O1", OrderType.SELL, 100.0, ts=1.0),
            _make_order("O2", OrderType.SELL, 150.0, ts=2.0),
            _make_order("O3", OrderType.SELL, 80.0, ts=3.0),
        ]
        sorted_orders = strategy.sort(orders)
        assert [o.order_id for o in sorted_orders] == ["O3", "O1", "O2"]

    def test_sell_orders_same_price_sorted_by_time(self):
        strategy = PriceTimeOrderBookOrderingStrategy(OrderType.SELL)
        orders = [
            _make_order("O1", OrderType.SELL, 100.0, ts=3.0),
            _make_order("O2", OrderType.SELL, 100.0, ts=1.0),
            _make_order("O3", OrderType.SELL, 100.0, ts=2.0),
        ]
        sorted_orders = strategy.sort(orders)
        assert [o.order_id for o in sorted_orders] == ["O2", "O3", "O1"]


class TestBuyOrderBook:
    def test_add_and_get_best(self):
        book = BuyOrderBook(PriceTimeOrderBookOrderingStrategy(OrderType.BUY))
        book.add(_make_order("O1", OrderType.BUY, 100.0, ts=1.0))
        book.add(_make_order("O2", OrderType.BUY, 150.0, ts=2.0))
        best = book.get_best_order()
        assert best.order_id == "O2"

    def test_cancel_order(self):
        book = BuyOrderBook(PriceTimeOrderBookOrderingStrategy(OrderType.BUY))
        book.add(_make_order("O1", OrderType.BUY, 100.0))
        assert book.cancel("O1") is True
        assert book.get_best_order() is None

    def test_cancel_nonexistent(self):
        book = BuyOrderBook(PriceTimeOrderBookOrderingStrategy(OrderType.BUY))
        assert book.cancel("NOPE") is False

    def test_empty_book_best_is_none(self):
        book = BuyOrderBook(PriceTimeOrderBookOrderingStrategy(OrderType.BUY))
        assert book.get_best_order() is None

    def test_remove_filled_orders(self):
        book = BuyOrderBook(PriceTimeOrderBookOrderingStrategy(OrderType.BUY))
        o1 = _make_order("O1", OrderType.BUY, 100.0)
        o2 = _make_order("O2", OrderType.BUY, 150.0)
        o1.fill(100)
        book.add(o1)
        book.add(o2)
        book.remove_filled()
        assert "O1" not in book.orders
        assert "O2" in book.orders


class TestSellOrderBook:
    def test_add_and_get_best(self):
        book = SellOrderBook(PriceTimeOrderBookOrderingStrategy(OrderType.SELL))
        book.add(_make_order("O1", OrderType.SELL, 100.0, ts=1.0))
        book.add(_make_order("O2", OrderType.SELL, 80.0, ts=2.0))
        best = book.get_best_order()
        assert best.order_id == "O2"

    def test_sorted_orders_excludes_cancelled(self):
        book = SellOrderBook(PriceTimeOrderBookOrderingStrategy(OrderType.SELL))
        o1 = _make_order("O1", OrderType.SELL, 100.0)
        book.add(o1)
        book.cancel("O1")
        assert book.get_sorted_orders() == []
