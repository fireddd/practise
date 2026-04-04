from abc import ABC, abstractmethod
class evlaution_express(ABC):
    @abstractmethod
    def evaluate(self, request):
        pass
