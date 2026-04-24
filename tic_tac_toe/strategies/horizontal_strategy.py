from enums.marker import Marker
from models.grid import Grid
from strategies.winning_strategy import WinningStrategy


class HorizontalStrategy(WinningStrategy):
    def check_winner(self, grid: Grid, last_row: int, last_col: int, marker: Marker) -> bool:
        return all(grid.get_cell(last_row, c) == marker for c in range(grid.size))
