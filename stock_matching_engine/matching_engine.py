import uuid
from typing import Dict, List

from stock_matching_engine.enums import OrderExecutionType, OrderStatus, OrderType
from stock_matching_engine.execution_strategy_factory import ExecutionStrategyFactory
from stock_matching_engine.order import Order
from stock_matching_engine.order_book import BuyOrderBook, OrderBook, SellOrderBook
from stock_matching_engine.price_time_ordering import PriceTimeOrderBookOrderingStrategy
from stock_matching_engine.trade import Trade


class MatchingEngine:
    def __init__(self):
        self._buy_books: Dict[str, BuyOrderBook] = {}
        self._sell_books: Dict[str, SellOrderBook] = {}
        self._trades: List[Trade] = []
        self._all_orders: Dict[str, Order] = {}

    def _get_buy_book(self, stock: str) -> BuyOrderBook:
        if stock not in self._buy_books:
            self._buy_books[stock] = BuyOrderBook(PriceTimeOrderBookOrderingStrategy(OrderType.BUY))
        return self._buy_books[stock]

    def _get_sell_book(self, stock: str) -> SellOrderBook:
        if stock not in self._sell_books:
            self._sell_books[stock] = SellOrderBook(PriceTimeOrderBookOrderingStrategy(OrderType.SELL))
        return self._sell_books[stock]

    def place_order(self, order: Order) -> List[Trade]:
        self._all_orders[order.order_id] = order
        trades = self._try_match(order)
        if order.remaining_quantity > 0 and order.status != OrderStatus.CANCELLED:
            if order.execution_type == OrderExecutionType.MARKET:
                order.cancel()
            else:
                book = self._get_buy_book(order.stock) if order.order_type == OrderType.BUY else self._get_sell_book(order.stock)
                book.add(order)
        return trades

    def cancel_order(self, order_id: str) -> bool:
        order = self._all_orders.get(order_id)
        if order is None or order.status in (OrderStatus.FILLED, OrderStatus.CANCELLED):
            return False
        book = self._get_buy_book(order.stock) if order.order_type == OrderType.BUY else self._get_sell_book(order.stock)
        return book.cancel(order_id)

    def _try_match(self, incoming: Order) -> List[Trade]:
        trades = []
        opposite_book: OrderBook = (
            self._get_sell_book(incoming.stock) if incoming.order_type == OrderType.BUY
            else self._get_buy_book(incoming.stock)
        )
        execution_strategy = ExecutionStrategyFactory.get(incoming.execution_type)

        while incoming.remaining_quantity > 0:
            best = opposite_book.get_best_order()
            if best is None:
                break
            if not execution_strategy.can_match(incoming, best):
                break

            fill_qty = min(incoming.remaining_quantity, best.remaining_quantity)
            trade_price = best.price

            incoming.fill(fill_qty)
            best.fill(fill_qty)

            trade = Trade(
                trade_id=str(uuid.uuid4()),
                buy_order_id=incoming.order_id if incoming.order_type == OrderType.BUY else best.order_id,
                sell_order_id=incoming.order_id if incoming.order_type == OrderType.SELL else best.order_id,
                stock=incoming.stock,
                price=trade_price,
                quantity=fill_qty,
            )
            trades.append(trade)
            self._trades.append(trade)

            if best.status == OrderStatus.FILLED:
                opposite_book.remove_filled()

        return trades

    @property
    def trades(self) -> List[Trade]:
        return list(self._trades)

    def get_order(self, order_id: str):
        return self._all_orders.get(order_id)

    def get_buy_book_size(self, stock: str) -> int:
        return len(self._get_buy_book(stock).orders)

    def get_sell_book_size(self, stock: str) -> int:
        return len(self._get_sell_book(stock).orders)
