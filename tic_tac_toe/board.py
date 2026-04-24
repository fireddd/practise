from tic_tac_toe.marker import Marker


class Board:
    def __init__(self, size: int):
        if size <= 0:
            raise ValueError("Board size must be positive.")
        self.size = size
        self.grid: list[list[Marker | None]] = [[None for _ in range(size)] for _ in range(size)]

    def is_valid_move(self, row: int, col: int) -> bool:
        return 0 <= row < self.size and 0 <= col < self.size and self.grid[row][col] is None

    def mark_cell(self, row: int, col: int, marker: Marker) -> None:
        if not self.is_valid_move(row, col):
            raise ValueError(f"Invalid move at ({row}, {col}).")
        self.grid[row][col] = marker

    def is_full(self) -> bool:
        return all(cell is not None for row in self.grid for cell in row)

    def render(self) -> str:
        rows = []
        for row in self.grid:
            rows.append(" | ".join(cell.value if cell is not None else " " for cell in row))
        separator = "\n" + "-" * (self.size * 4 - 3) + "\n"
        return separator.join(rows)

