import pytest

from stock_matching_engine.enums import OrderExecutionType, OrderStatus, OrderType
from stock_matching_engine.matching_engine import MatchingEngine
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


class TestBasicMatching:
    def test_exact_match_buy_then_sell(self):
        engine = MatchingEngine()
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 150.0, 100)
        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 150.0, 100)

        engine.place_order(buy)
        trades = engine.place_order(sell)

        assert len(trades) == 1
        assert trades[0].quantity == 100
        assert trades[0].price == 150.0
        assert trades[0].buy_order_id == "B1"
        assert trades[0].sell_order_id == "S1"

    def test_exact_match_sell_then_buy(self):
        engine = MatchingEngine()
        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 140.0, 50)
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 150.0, 50)

        engine.place_order(sell)
        trades = engine.place_order(buy)

        assert len(trades) == 1
        assert trades[0].quantity == 50
        assert trades[0].price == 140.0

    def test_no_match_when_price_doesnt_cross(self):
        engine = MatchingEngine()
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 100.0)
        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 110.0)

        engine.place_order(buy)
        trades = engine.place_order(sell)

        assert len(trades) == 0


class TestPartialFills:
    def test_incoming_larger_than_book_order(self):
        engine = MatchingEngine()
        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 100.0, 50)
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 100.0, 150)

        engine.place_order(sell)
        trades = engine.place_order(buy)

        assert len(trades) == 1
        assert trades[0].quantity == 50
        buy_order = engine.get_order("B1")
        assert buy_order.remaining_quantity == 100
        assert buy_order.status == OrderStatus.PARTIALLY_FILLED

    def test_incoming_smaller_than_book_order(self):
        engine = MatchingEngine()
        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 100.0, 200)
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 100.0, 80)

        engine.place_order(sell)
        trades = engine.place_order(buy)

        assert len(trades) == 1
        assert trades[0].quantity == 80
        sell_order = engine.get_order("S1")
        assert sell_order.remaining_quantity == 120
        assert sell_order.status == OrderStatus.PARTIALLY_FILLED

    def test_multiple_partial_fills(self):
        engine = MatchingEngine()
        s1 = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 100.0, 30)
        s2 = _make_order("S2", OrderType.SELL, OrderExecutionType.LIMIT, 105.0, 50)
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 110.0, 60)

        engine.place_order(s1)
        engine.place_order(s2)
        trades = engine.place_order(buy)

        assert len(trades) == 2
        assert trades[0].quantity == 30
        assert trades[0].price == 100.0
        assert trades[1].quantity == 30
        assert trades[1].price == 105.0
        assert engine.get_order("B1").status == OrderStatus.FILLED
        assert engine.get_order("S1").status == OrderStatus.FILLED
        assert engine.get_order("S2").status == OrderStatus.PARTIALLY_FILLED
        assert engine.get_order("S2").remaining_quantity == 20


class TestPriceTimePriority:
    def test_best_price_matched_first(self):
        engine = MatchingEngine()
        s1 = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 105.0, 100)
        s2 = _make_order("S2", OrderType.SELL, OrderExecutionType.LIMIT, 100.0, 100)
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 110.0, 100)

        engine.place_order(s1)
        engine.place_order(s2)
        trades = engine.place_order(buy)

        assert len(trades) == 1
        assert trades[0].sell_order_id == "S2"
        assert trades[0].price == 100.0

    def test_same_price_earlier_order_matched_first(self):
        engine = MatchingEngine()
        s1 = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 100.0, 100)
        s2 = _make_order("S2", OrderType.SELL, OrderExecutionType.LIMIT, 100.0, 100)
        s1.timestamp = 1.0
        s2.timestamp = 2.0
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 100.0, 100)

        engine.place_order(s1)
        engine.place_order(s2)
        trades = engine.place_order(buy)

        assert len(trades) == 1
        assert trades[0].sell_order_id == "S1"


class TestMarketOrders:
    def test_market_buy_matches_best_sell(self):
        engine = MatchingEngine()
        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 100.0, 50)
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.MARKET, 0, 50)

        engine.place_order(sell)
        trades = engine.place_order(buy)

        assert len(trades) == 1
        assert trades[0].price == 100.0
        assert trades[0].quantity == 50

    def test_market_sell_matches_best_buy(self):
        engine = MatchingEngine()
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 200.0, 30)
        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.MARKET, 0, 30)

        engine.place_order(buy)
        trades = engine.place_order(sell)

        assert len(trades) == 1
        assert trades[0].price == 200.0

    def test_market_order_no_liquidity(self):
        engine = MatchingEngine()
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.MARKET, 0, 100)
        trades = engine.place_order(buy)
        assert len(trades) == 0


class TestCancelOrder:
    def test_cancel_open_order(self):
        engine = MatchingEngine()
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 150.0, 100)
        engine.place_order(buy)

        assert engine.cancel_order("B1") is True
        assert engine.get_order("B1").status == OrderStatus.CANCELLED

    def test_cancel_prevents_matching(self):
        engine = MatchingEngine()
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 150.0, 100)
        engine.place_order(buy)
        engine.cancel_order("B1")

        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 140.0, 100)
        trades = engine.place_order(sell)
        assert len(trades) == 0

    def test_cancel_nonexistent_order(self):
        engine = MatchingEngine()
        assert engine.cancel_order("NOPE") is False

    def test_cancel_already_filled(self):
        engine = MatchingEngine()
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 150.0, 100)
        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 150.0, 100)
        engine.place_order(buy)
        engine.place_order(sell)

        assert engine.cancel_order("B1") is False


class TestEmptyBookNoExecution:
    def test_limit_buy_into_empty_sell_book(self):
        engine = MatchingEngine()
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 150.0, 100)
        trades = engine.place_order(buy)

        assert len(trades) == 0
        assert engine.get_order("B1").status == OrderStatus.OPEN
        assert engine.get_buy_book_size("AAPL") == 1
        assert engine.get_sell_book_size("AAPL") == 0

    def test_limit_sell_into_empty_buy_book(self):
        engine = MatchingEngine()
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 150.0, 100)
        trades = engine.place_order(sell)

        assert len(trades) == 0
        assert engine.get_order("S1").status == OrderStatus.OPEN
        assert engine.get_sell_book_size("AAPL") == 1
        assert engine.get_buy_book_size("AAPL") == 0

    def test_market_buy_into_empty_sell_book_cancelled(self):
        engine = MatchingEngine()
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.MARKET, 0, 100)
        trades = engine.place_order(buy)

        assert len(trades) == 0
        assert engine.get_order("B1").status == OrderStatus.CANCELLED
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

    def test_market_sell_into_empty_buy_book_cancelled(self):
        engine = MatchingEngine()
        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.MARKET, 0, 100)
        trades = engine.place_order(sell)

        assert len(trades) == 0
        assert engine.get_order("S1").status == OrderStatus.CANCELLED
        assert engine.get_sell_book_size("AAPL") == 0
        assert engine.get_buy_book_size("AAPL") == 0


class TestPartialFillBookSizes:
    def test_limit_buy_partial_fill_on_sell_book(self):
        """Buy 150 @ 100, only 50 available on sell side. Buy book gets the remainder."""
        engine = MatchingEngine()
        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 100.0, 50)
        engine.place_order(sell)
        assert engine.get_sell_book_size("AAPL") == 1
        assert engine.get_buy_book_size("AAPL") == 0

        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 100.0, 150)
        trades = engine.place_order(buy)

        assert len(trades) == 1
        assert trades[0].quantity == 50
        assert engine.get_order("B1").status == OrderStatus.PARTIALLY_FILLED
        assert engine.get_order("B1").remaining_quantity == 100
        assert engine.get_order("S1").status == OrderStatus.FILLED
        # S1 fully filled -> removed from sell book, B1 remainder -> added to buy book
        assert engine.get_sell_book_size("AAPL") == 0
        assert engine.get_buy_book_size("AAPL") == 1

    def test_limit_sell_partial_fill_on_buy_book(self):
        """Sell 150 @ 100, only 50 demand on buy side. Sell book gets the remainder."""
        engine = MatchingEngine()
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 100.0, 50)
        engine.place_order(buy)
        assert engine.get_buy_book_size("AAPL") == 1
        assert engine.get_sell_book_size("AAPL") == 0

        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 100.0, 150)
        trades = engine.place_order(sell)

        assert len(trades) == 1
        assert trades[0].quantity == 50
        assert engine.get_order("S1").status == OrderStatus.PARTIALLY_FILLED
        assert engine.get_order("S1").remaining_quantity == 100
        assert engine.get_order("B1").status == OrderStatus.FILLED
        # B1 fully filled -> removed from buy book, S1 remainder -> added to sell book
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 1

    def test_market_buy_partial_fill_on_sell_book(self):
        """Market buy 100, only 40 on sell side. Remainder cancelled, not in book."""
        engine = MatchingEngine()
        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 200.0, 40)
        engine.place_order(sell)
        assert engine.get_sell_book_size("AAPL") == 1

        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.MARKET, 0, 100)
        trades = engine.place_order(buy)

        assert len(trades) == 1
        assert trades[0].quantity == 40
        assert trades[0].price == 200.0
        assert engine.get_order("B1").status == OrderStatus.CANCELLED
        assert engine.get_order("B1").filled_quantity == 40
        assert engine.get_order("B1").remaining_quantity == 60
        assert engine.get_order("S1").status == OrderStatus.FILLED
        assert engine.get_sell_book_size("AAPL") == 0
        assert engine.get_buy_book_size("AAPL") == 0

    def test_market_sell_partial_fill_on_buy_book(self):
        """Market sell 100, only 30 on buy side. Remainder cancelled, not in book."""
        engine = MatchingEngine()
        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 150.0, 30)
        engine.place_order(buy)
        assert engine.get_buy_book_size("AAPL") == 1

        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.MARKET, 0, 100)
        trades = engine.place_order(sell)

        assert len(trades) == 1
        assert trades[0].quantity == 30
        assert trades[0].price == 150.0
        assert engine.get_order("S1").status == OrderStatus.CANCELLED
        assert engine.get_order("S1").filled_quantity == 30
        assert engine.get_order("S1").remaining_quantity == 70
        assert engine.get_order("B1").status == OrderStatus.FILLED
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

    def test_limit_buy_sweeps_multiple_sells_with_book_tracking(self):
        """Buy sweeps 2 sell orders fully and partially fills a 3rd."""
        engine = MatchingEngine()
        s1 = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 100.0, 30)
        s2 = _make_order("S2", OrderType.SELL, OrderExecutionType.LIMIT, 105.0, 40)
        s3 = _make_order("S3", OrderType.SELL, OrderExecutionType.LIMIT, 110.0, 50)
        engine.place_order(s1)
        engine.place_order(s2)
        engine.place_order(s3)
        assert engine.get_sell_book_size("AAPL") == 3
        assert engine.get_buy_book_size("AAPL") == 0

        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 110.0, 90)
        trades = engine.place_order(buy)

        assert len(trades) == 3
        assert trades[0].quantity == 30  # S1 fully filled
        assert trades[1].quantity == 40  # S2 fully filled
        assert trades[2].quantity == 20  # S3 partially filled
        assert engine.get_order("B1").status == OrderStatus.FILLED
        assert engine.get_order("S1").status == OrderStatus.FILLED
        assert engine.get_order("S2").status == OrderStatus.FILLED
        assert engine.get_order("S3").status == OrderStatus.PARTIALLY_FILLED
        assert engine.get_order("S3").remaining_quantity == 30
        # S1, S2 removed; S3 remains with partial
        assert engine.get_sell_book_size("AAPL") == 1
        assert engine.get_buy_book_size("AAPL") == 0

    def test_limit_sell_sweeps_multiple_buys_with_book_tracking(self):
        """Sell sweeps 2 buy orders fully and partially fills a 3rd."""
        engine = MatchingEngine()
        b1 = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 110.0, 30)
        b2 = _make_order("B2", OrderType.BUY, OrderExecutionType.LIMIT, 105.0, 40)
        b3 = _make_order("B3", OrderType.BUY, OrderExecutionType.LIMIT, 100.0, 50)
        engine.place_order(b1)
        engine.place_order(b2)
        engine.place_order(b3)
        assert engine.get_buy_book_size("AAPL") == 3
        assert engine.get_sell_book_size("AAPL") == 0

        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 100.0, 90)
        trades = engine.place_order(sell)

        assert len(trades) == 3
        assert trades[0].quantity == 30  # B1 fully filled (highest price first)
        assert trades[1].quantity == 40  # B2 fully filled
        assert trades[2].quantity == 20  # B3 partially filled
        assert engine.get_order("S1").status == OrderStatus.FILLED
        assert engine.get_order("B1").status == OrderStatus.FILLED
        assert engine.get_order("B2").status == OrderStatus.FILLED
        assert engine.get_order("B3").status == OrderStatus.PARTIALLY_FILLED
        assert engine.get_order("B3").remaining_quantity == 30
        # B1, B2 removed; B3 remains with partial
        assert engine.get_buy_book_size("AAPL") == 1
        assert engine.get_sell_book_size("AAPL") == 0

    def test_market_buy_sweeps_multiple_sells_with_book_tracking(self):
        """Market buy sweeps through sell book, partially consuming the last."""
        engine = MatchingEngine()
        s1 = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 100.0, 20)
        s2 = _make_order("S2", OrderType.SELL, OrderExecutionType.LIMIT, 110.0, 50)
        engine.place_order(s1)
        engine.place_order(s2)
        assert engine.get_sell_book_size("AAPL") == 2

        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.MARKET, 0, 40)
        trades = engine.place_order(buy)

        assert len(trades) == 2
        assert trades[0].quantity == 20
        assert trades[0].price == 100.0
        assert trades[1].quantity == 20
        assert trades[1].price == 110.0
        assert engine.get_order("B1").status == OrderStatus.FILLED
        assert engine.get_order("S1").status == OrderStatus.FILLED
        assert engine.get_order("S2").status == OrderStatus.PARTIALLY_FILLED
        assert engine.get_order("S2").remaining_quantity == 30
        assert engine.get_sell_book_size("AAPL") == 1
        assert engine.get_buy_book_size("AAPL") == 0

    def test_market_sell_sweeps_multiple_buys_with_book_tracking(self):
        """Market sell sweeps through buy book, partially consuming the last."""
        engine = MatchingEngine()
        b1 = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 200.0, 25)
        b2 = _make_order("B2", OrderType.BUY, OrderExecutionType.LIMIT, 190.0, 60)
        engine.place_order(b1)
        engine.place_order(b2)
        assert engine.get_buy_book_size("AAPL") == 2

        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.MARKET, 0, 50)
        trades = engine.place_order(sell)

        assert len(trades) == 2
        assert trades[0].quantity == 25
        assert trades[0].price == 200.0
        assert trades[1].quantity == 25
        assert trades[1].price == 190.0
        assert engine.get_order("S1").status == OrderStatus.FILLED
        assert engine.get_order("B1").status == OrderStatus.FILLED
        assert engine.get_order("B2").status == OrderStatus.PARTIALLY_FILLED
        assert engine.get_order("B2").remaining_quantity == 35
        assert engine.get_buy_book_size("AAPL") == 1
        assert engine.get_sell_book_size("AAPL") == 0


class TestEndToEndLimitBuyLimitSell:
    def test_exact_match_both_books_empty(self):
        engine = MatchingEngine()
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 150.0, 100)
        trades = engine.place_order(buy)
        assert len(trades) == 0
        assert engine.get_buy_book_size("AAPL") == 1
        assert engine.get_sell_book_size("AAPL") == 0

        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 150.0, 100)
        trades = engine.place_order(sell)
        assert len(trades) == 1
        assert trades[0].quantity == 100
        assert trades[0].price == 150.0
        assert engine.get_order("B1").status == OrderStatus.FILLED
        assert engine.get_order("S1").status == OrderStatus.FILLED
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

    def test_no_match_one_in_each_book(self):
        engine = MatchingEngine()
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 100.0, 100)
        trades = engine.place_order(buy)
        assert len(trades) == 0
        assert engine.get_buy_book_size("AAPL") == 1
        assert engine.get_sell_book_size("AAPL") == 0

        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 110.0, 100)
        trades = engine.place_order(sell)
        assert len(trades) == 0
        assert engine.get_order("B1").status == OrderStatus.OPEN
        assert engine.get_order("S1").status == OrderStatus.OPEN
        assert engine.get_buy_book_size("AAPL") == 1
        assert engine.get_sell_book_size("AAPL") == 1

    def test_partial_match_remainder_in_buy_book(self):
        engine = MatchingEngine()
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 100.0, 50)
        trades = engine.place_order(sell)
        assert len(trades) == 0
        assert engine.get_sell_book_size("AAPL") == 1
        assert engine.get_buy_book_size("AAPL") == 0

        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 100.0, 120)
        trades = engine.place_order(buy)
        assert len(trades) == 1
        assert trades[0].quantity == 50
        assert trades[0].price == 100.0
        assert engine.get_order("S1").status == OrderStatus.FILLED
        assert engine.get_order("B1").status == OrderStatus.PARTIALLY_FILLED
        assert engine.get_order("B1").remaining_quantity == 70
        assert engine.get_sell_book_size("AAPL") == 0
        assert engine.get_buy_book_size("AAPL") == 1


class TestEndToEndMarketBuyMarketSell:
    def test_both_cancelled_no_trade(self):
        """Market buy placed first gets cancelled (no sells). Market sell also cancelled (no buys)."""
        engine = MatchingEngine()
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.MARKET, 0, 100)
        trades = engine.place_order(buy)
        assert len(trades) == 0
        assert engine.get_order("B1").status == OrderStatus.CANCELLED
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.MARKET, 0, 100)
        trades = engine.place_order(sell)
        assert len(trades) == 0
        assert engine.get_order("S1").status == OrderStatus.CANCELLED
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

    def test_both_cancelled_regardless_of_price(self):
        """Even with different prices, both market orders get cancelled — neither rests in book."""
        engine = MatchingEngine()
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.MARKET, 50.0, 100)
        trades = engine.place_order(buy)
        assert len(trades) == 0
        assert engine.get_order("B1").status == OrderStatus.CANCELLED
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.MARKET, 200.0, 100)
        trades = engine.place_order(sell)
        assert len(trades) == 0
        assert engine.get_order("S1").status == OrderStatus.CANCELLED
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

    def test_both_cancelled_no_partial_possible(self):
        """Market sell placed first gets cancelled. Market buy also cancelled. No trades at all."""
        engine = MatchingEngine()
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.MARKET, 0, 50)
        trades = engine.place_order(sell)
        assert len(trades) == 0
        assert engine.get_order("S1").status == OrderStatus.CANCELLED
        assert engine.get_sell_book_size("AAPL") == 0
        assert engine.get_buy_book_size("AAPL") == 0

        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.MARKET, 0, 120)
        trades = engine.place_order(buy)
        assert len(trades) == 0
        assert engine.get_order("B1").status == OrderStatus.CANCELLED
        assert engine.get_sell_book_size("AAPL") == 0
        assert engine.get_buy_book_size("AAPL") == 0


class TestEndToEndLimitBuyMarketSell:
    def test_exact_match_both_books_empty(self):
        engine = MatchingEngine()
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 150.0, 100)
        trades = engine.place_order(buy)
        assert len(trades) == 0
        assert engine.get_buy_book_size("AAPL") == 1
        assert engine.get_sell_book_size("AAPL") == 0

        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.MARKET, 0, 100)
        trades = engine.place_order(sell)
        assert len(trades) == 1
        assert trades[0].quantity == 100
        assert trades[0].price == 150.0
        assert engine.get_order("B1").status == OrderStatus.FILLED
        assert engine.get_order("S1").status == OrderStatus.FILLED
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

    def test_market_sell_always_matches_limit_buy(self):
        """Market sell incoming always matches — no 'no match' even with different prices."""
        engine = MatchingEngine()
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 100.0, 100)
        trades = engine.place_order(buy)
        assert len(trades) == 0
        assert engine.get_buy_book_size("AAPL") == 1
        assert engine.get_sell_book_size("AAPL") == 0

        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.MARKET, 0, 100)
        trades = engine.place_order(sell)
        assert len(trades) == 1
        assert trades[0].quantity == 100
        assert trades[0].price == 100.0
        assert engine.get_order("B1").status == OrderStatus.FILLED
        assert engine.get_order("S1").status == OrderStatus.FILLED
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

    def test_partial_match_remainder_in_buy_book(self):
        engine = MatchingEngine()
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.LIMIT, 150.0, 120)
        trades = engine.place_order(buy)
        assert len(trades) == 0
        assert engine.get_buy_book_size("AAPL") == 1
        assert engine.get_sell_book_size("AAPL") == 0

        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.MARKET, 0, 50)
        trades = engine.place_order(sell)
        assert len(trades) == 1
        assert trades[0].quantity == 50
        assert trades[0].price == 150.0
        assert engine.get_order("S1").status == OrderStatus.FILLED
        assert engine.get_order("B1").status == OrderStatus.PARTIALLY_FILLED
        assert engine.get_order("B1").remaining_quantity == 70
        assert engine.get_buy_book_size("AAPL") == 1
        assert engine.get_sell_book_size("AAPL") == 0


class TestEndToEndMarketBuyLimitSell:
    def test_exact_match_both_books_empty(self):
        engine = MatchingEngine()
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 150.0, 100)
        trades = engine.place_order(sell)
        assert len(trades) == 0
        assert engine.get_sell_book_size("AAPL") == 1
        assert engine.get_buy_book_size("AAPL") == 0

        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.MARKET, 0, 100)
        trades = engine.place_order(buy)
        assert len(trades) == 1
        assert trades[0].quantity == 100
        assert trades[0].price == 150.0
        assert engine.get_order("B1").status == OrderStatus.FILLED
        assert engine.get_order("S1").status == OrderStatus.FILLED
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

    def test_no_match_market_buy_cancelled_limit_sell_rests(self):
        """Market buy cancelled immediately (no sells). Limit sell rests in sell book."""
        engine = MatchingEngine()
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.MARKET, 0, 100)
        trades = engine.place_order(buy)
        assert len(trades) == 0
        assert engine.get_order("B1").status == OrderStatus.CANCELLED
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 110.0, 100)
        trades = engine.place_order(sell)
        assert len(trades) == 0
        assert engine.get_order("S1").status == OrderStatus.OPEN
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 1

    def test_partial_match_remainder_cancelled(self):
        """Market buy fills 50 from sell book, remaining 70 cancelled — not in buy book."""
        engine = MatchingEngine()
        assert engine.get_buy_book_size("AAPL") == 0
        assert engine.get_sell_book_size("AAPL") == 0

        sell = _make_order("S1", OrderType.SELL, OrderExecutionType.LIMIT, 100.0, 50)
        trades = engine.place_order(sell)
        assert len(trades) == 0
        assert engine.get_sell_book_size("AAPL") == 1
        assert engine.get_buy_book_size("AAPL") == 0

        buy = _make_order("B1", OrderType.BUY, OrderExecutionType.MARKET, 0, 120)
        trades = engine.place_order(buy)
        assert len(trades) == 1
        assert trades[0].quantity == 50
        assert trades[0].price == 100.0
        assert engine.get_order("S1").status == OrderStatus.FILLED
        assert engine.get_order("B1").status == OrderStatus.CANCELLED
        assert engine.get_order("B1").filled_quantity == 50
        assert engine.get_order("B1").remaining_quantity == 70
        assert engine.get_sell_book_size("AAPL") == 0
        assert engine.get_buy_book_size("AAPL") == 0


class TestMultiStockIsolation:
    def test_different_stocks_dont_match(self):
        engine = MatchingEngine()
        buy = Order(
            order_id="B1", stock="AAPL", order_type=OrderType.BUY,
            execution_type=OrderExecutionType.LIMIT, price=150.0, quantity=100,
        )
        sell = Order(
            order_id="S1", stock="GOOG", order_type=OrderType.SELL,
            execution_type=OrderExecutionType.LIMIT, price=140.0, quantity=100,
        )
        engine.place_order(buy)
        trades = engine.place_order(sell)
        assert len(trades) == 0
