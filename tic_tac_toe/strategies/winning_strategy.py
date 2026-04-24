from abc import ABC, abstractmethod

from enums.marker import Marker
from models.grid import Grid


class WinningStrategy(ABC):
    @abstractmethod
    def check_winner(self, grid: Grid, last_row: int, last_col: int, marker: Marker) -> bool:
        pass
