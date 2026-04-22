from stock_matching_engine.enums import OrderExecutionType, OrderType
from stock_matching_engine.matching_engine import MatchingEngine
from stock_matching_engine.order import Order


def print_trades(trades, label=""):
    if label:
        print(f"\n--- {label} ---")
    if not trades:
        print("  No trades executed.")
        return
    for t in trades:
        print(f"  Trade {t.trade_id[:8]}.. | {t.stock} | Buy:{t.buy_order_id} Sell:{t.sell_order_id} | {t.quantity} @ {t.price}")


def main():
    engine = MatchingEngine()

    # Scenario 1: exact limit match
    print("=" * 60)
    print("SCENARIO 1: Exact limit order match")
    print("=" * 60)
    b1 = Order("B1", "AAPL", OrderType.BUY, OrderExecutionType.LIMIT, 150.0, 100)
    engine.place_order(b1)
    print(f"Placed BUY  B1: 100 AAPL @ 150.0")

    s1 = Order("S1", "AAPL", OrderType.SELL, OrderExecutionType.LIMIT, 150.0, 100)
    trades = engine.place_order(s1)
    print(f"Placed SELL S1: 100 AAPL @ 150.0")
    print_trades(trades, "Trades")
    print(f"B1 status: {b1.status.value}, S1 status: {s1.status.value}")

    # Scenario 2: partial fills
    print(f"\n{'=' * 60}")
    print("SCENARIO 2: Partial fills across multiple orders")
    print("=" * 60)
    s2 = Order("S2", "GOOG", OrderType.SELL, OrderExecutionType.LIMIT, 200.0, 30)
    s3 = Order("S3", "GOOG", OrderType.SELL, OrderExecutionType.LIMIT, 205.0, 50)
    engine.place_order(s2)
    engine.place_order(s3)
    print(f"Placed SELL S2: 30 GOOG @ 200.0")
    print(f"Placed SELL S3: 50 GOOG @ 205.0")

    b2 = Order("B2", "GOOG", OrderType.BUY, OrderExecutionType.LIMIT, 210.0, 60)
    trades = engine.place_order(b2)
    print(f"Placed BUY  B2: 60 GOOG @ 210.0")
    print_trades(trades, "Trades")
    print(f"B2 status: {b2.status.value} (filled: {b2.filled_quantity})")
    print(f"S2 status: {s2.status.value} (filled: {s2.filled_quantity})")
    print(f"S3 status: {s3.status.value} (filled: {s3.filled_quantity}, remaining: {s3.remaining_quantity})")

    # Scenario 3: market order
    print(f"\n{'=' * 60}")
    print("SCENARIO 3: Market order")
    print("=" * 60)
    s4 = Order("S4", "MSFT", OrderType.SELL, OrderExecutionType.LIMIT, 300.0, 40)
    engine.place_order(s4)
    print(f"Placed SELL S4: 40 MSFT @ 300.0")

    b3 = Order("B3", "MSFT", OrderType.BUY, OrderExecutionType.MARKET, 0, 40)
    trades = engine.place_order(b3)
    print(f"Placed BUY  B3: 40 MSFT @ MARKET")
    print_trades(trades, "Trades")

    # Scenario 4: cancel order
    print(f"\n{'=' * 60}")
    print("SCENARIO 4: Cancel order before match")
    print("=" * 60)
    b4 = Order("B4", "TSLA", OrderType.BUY, OrderExecutionType.LIMIT, 250.0, 100)
    engine.place_order(b4)
    print(f"Placed BUY  B4: 100 TSLA @ 250.0")

    cancelled = engine.cancel_order("B4")
    print(f"Cancel B4: {'success' if cancelled else 'failed'} -> status: {b4.status.value}")

    s5 = Order("S5", "TSLA", OrderType.SELL, OrderExecutionType.LIMIT, 240.0, 100)
    trades = engine.place_order(s5)
    print(f"Placed SELL S5: 100 TSLA @ 240.0")
    print_trades(trades, "Trades (should be none — B4 was cancelled)")

    # Scenario 5: price-time priority
    print(f"\n{'=' * 60}")
    print("SCENARIO 5: Price-time priority")
    print("=" * 60)
    s6 = Order("S6", "AMZN", OrderType.SELL, OrderExecutionType.LIMIT, 120.0, 100)
    s7 = Order("S7", "AMZN", OrderType.SELL, OrderExecutionType.LIMIT, 110.0, 100)
    s8 = Order("S8", "AMZN", OrderType.SELL, OrderExecutionType.LIMIT, 110.0, 100)
    s7.timestamp = 1.0
    s8.timestamp = 2.0
    engine.place_order(s6)
    engine.place_order(s7)
    engine.place_order(s8)
    print(f"Placed SELL S6: 100 AMZN @ 120.0")
    print(f"Placed SELL S7: 100 AMZN @ 110.0 (earlier)")
    print(f"Placed SELL S8: 100 AMZN @ 110.0 (later)")

    b5 = Order("B5", "AMZN", OrderType.BUY, OrderExecutionType.LIMIT, 115.0, 100)
    trades = engine.place_order(b5)
    print(f"Placed BUY  B5: 100 AMZN @ 115.0")
    print_trades(trades, "Trades (should match S7 first — lower price, earlier time)")

    # Summary
    print(f"\n{'=' * 60}")
    print(f"TOTAL TRADES EXECUTED: {len(engine.trades)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
