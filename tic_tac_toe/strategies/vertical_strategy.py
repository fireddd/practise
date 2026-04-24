from enums.marker import Marker
from models.grid import Grid
from strategies.winning_strategy import WinningStrategy


class VerticalStrategy(WinningStrategy):
    def check_winner(self, grid: Grid, last_row: int, last_col: int, marker: Marker) -> bool:
        return all(grid.get_cell(r, last_col) == marker for r in range(grid.size))
