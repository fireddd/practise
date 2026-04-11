from abc import ABC, abstractmethod


class DiscountCalculator(ABC):

    @abstractmethod
    def calculate(self, current_amount: float, discount_value: float) -> float:
        pass
