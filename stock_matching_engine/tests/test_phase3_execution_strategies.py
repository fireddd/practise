import pytest

from stock_matching_engine.enums import OrderExecutionType, OrderType
from stock_matching_engine.execution_strategy_factory import ExecutionStrategyFactory
from stock_matching_engine.limit_execution import LimitOrderExecutionStrategy
from stock_matching_engine.market_execution import MarketOrderExecutionStrategy
from stock_matching_engine.order import Order


def _make_order(order_id, order_type, execution_type, price, quantity=100):
    return Order(
        order_id=order_id,
        stock="AAPL",
        order_type=order_type,
        execution_type=execution_type,
        price=price,
        quantity=quantity,
    )


class TestLimitExecution:
    def setup_method(self):
        self.strategy = LimitOrderExecutionStrategy()

    def test_buy_matches_sell_at_lower_price(self):
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 150.0)
        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 140.0)
        assert self.strategy.can_match(buy, sell) is True

    def test_buy_matches_sell_at_equal_price(self):
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 150.0)
        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 150.0)
        assert self.strategy.can_match(buy, sell) is True

    def test_buy_does_not_match_sell_at_higher_price(self):
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 150.0)
        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 160.0)
        assert self.strategy.can_match(buy, sell) is False

    def test_sell_matches_buy_at_higher_price(self):
        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 140.0)
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 150.0)
        assert self.strategy.can_match(sell, buy) is True

    def test_sell_matches_buy_at_equal_price(self):
        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 150.0)
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 150.0)
        assert self.strategy.can_match(sell, buy) is True

    def test_sell_does_not_match_buy_at_lower_price(self):
        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 150.0)
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 140.0)
        assert self.strategy.can_match(sell, buy) is False


class TestMarketExecution:
    def setup_method(self):
        self.strategy = MarketOrderExecutionStrategy()

    def test_market_buy_always_matches(self):
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.MARKET, 0)
        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 999.0)
        assert self.strategy.can_match(buy, sell) is True

    def test_market_sell_always_matches(self):
        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.MARKET, 0)
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 50.0)
        assert self.strategy.can_match(sell, buy) is True


class TestExecutionStrategyFactory:
    def test_returns_limit_strategy(self):
        strategy = ExecutionStrategyFactory.get(OrderExecutionType.LIMIT)
        assert isinstance(strategy, LimitOrderExecutionStrategy)

    def test_returns_market_strategy(self):
        strategy = ExecutionStrategyFactory.get(OrderExecutionType.MARKET)
        assert isinstance(strategy, MarketOrderExecutionStrategy)
