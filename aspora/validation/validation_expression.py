from abc import ABC, abstractmethod


class ValidationExpression(ABC):
    @abstractmethod
    def evaluate(self, context):
        pass
'''
amoutn < 100

tier = "gold' and amoutn > 100
'''