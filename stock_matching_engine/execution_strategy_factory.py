from stock_matching_engine.enums import OrderExecutionType
from stock_matching_engine.execution_strategy import OrderExecutionStrategy
from stock_matching_engine.limit_execution import LimitOrderExecutionStrategy
from stock_matching_engine.market_execution import MarketOrderExecutionStrategy


class ExecutionStrategyFactory:
    _strategies = {
        OrderExecutionType.LIMIT: LimitOrderExecutionStrategy,
        OrderExecutionType.MARKET: MarketOrderExecutionStrategy,
    }

    @classmethod
    def get(cls, execution_type: OrderExecutionType) -> OrderExecutionStrategy:
        strategy_cls = cls._strategies.get(execution_type)
        if strategy_cls is None:
            raise ValueError(f"Unknown execution type: {execution_type}")
        return strategy_cls()
