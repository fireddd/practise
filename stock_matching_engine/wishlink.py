'''
Implement a stock order matching engine.
It should support the following operations:
1) Place buy and sell order
2) Cancel buy and sell order
3) The orders should be matched by price time priority
4) Support partial fills for a given order
5) Two types of orders,
    a) limit - for buying, buy at a given price or below and for selling, sell at a given price or above
    b) market - match with the current latest price


OrderType:
    SELL
    BUY

OrderExecutionType:
    LIMIT
    MARKET

OrderExecutionSTrategy(ABC):
    1) LimitOrderExecutionSTrategy
    2) MarketOrderExecutionStrategy

Order:
    stock
    order_type
    order_execution_type
    price
    quantity

OrderBookOrderingStrategy(ABC):
    @abstractmethod
    def order(orders):
        pass
PriceTimeOrderBookOrderingStrategy(OrderBookOrderingStrategy):

OrderBook(ABC):
    list<orders>
    order_book_ordering_strategy

    def add(order)

    def cancel(order)



BuyOrderBook(OrderBook):
    def __init__(self, orderbookorderingstreagting):
        self.orderbookorderingstreagting = orderbookorderingstreagting)
SellOrderBook(OrderBook):
    def __init__(self, orderbookorderingstreagting):
        self.orderbookorderingstreagting = orderbookorderingstreagting)
StockBroker():
 def __init__(self):
    self.buyOrderBook = BuyOrderBook(PriceTimeOrderBookOrderingStrategy())
    self.sellOrderBook = SellOrderBook(PriceTimeOrderBookOrderingStrategy())

let's define exercise as :
    1 buy 1 sell at same price and quantity, 1 trade, both books empty
    1 buy 1 sell which buying price and selling price don't match, no execution, 0 trade, 1 order in each book
    1 buy 1 sell, price match for buying quantity is more, so 1 trade, 1 order in buy book
    n buy 1 sell, for price matching case
    1 buy n sell, for price matching case
for both limit and market to this exercise
then make limit as buy and market as sell and redo the exercise
then make market as buy and limit as sell and redo the exercise



'''
if __name__ == "__main__":
    print("hello")