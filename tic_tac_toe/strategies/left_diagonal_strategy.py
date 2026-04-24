from enums.marker import Marker
from models.grid import Grid
from strategies.winning_strategy import WinningStrategy


class LeftDiagonalStrategy(WinningStrategy):
    def check_winner(self, grid: Grid, last_row: int, last_col: int, marker: Marker) -> bool:
        if last_row != last_col:
            return False
        return all(grid.get_cell(i, i) == marker for i in range(grid.size))
