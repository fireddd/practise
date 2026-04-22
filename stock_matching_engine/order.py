import time
from dataclasses import dataclass, field

from stock_matching_engine.enums import OrderExecutionType, OrderStatus, OrderType


@dataclass
class Order:
    order_id: str
    stock: str
    order_type: OrderType
    execution_type: OrderExecutionType
    price: float
    quantity: int
    status: OrderStatus = OrderStatus.OPEN
    filled_quantity: int = 0
    timestamp: float = field(default_factory=time.time)

    @property
    def remaining_quantity(self) -> int:
        return self.quantity - self.filled_quantity

    def fill(self, qty: int):
        self.filled_quantity += qty
        if self.filled_quantity >= self.quantity:
            self.status = OrderStatus.FILLED
        else:
            self.status = OrderStatus.PARTIALLY_FILLED

    def cancel(self):
        self.status = OrderStatus.CANCELLED
