from enums.marker import Marker
from models.grid import Grid
from strategies.winning_strategy import WinningStrategy


class RightDiagonalStrategy(WinningStrategy):
    def check_winner(self, grid: Grid, last_row: int, last_col: int, marker: Marker) -> bool:
        n = grid.size
        if last_row + last_col != n - 1:
            return False
        return all(grid.get_cell(i, n - 1 - i) == marker for i in range(n))
