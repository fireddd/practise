from typing import Optional

from enums.marker import Marker


class Grid:
    def __init__(self, n: int):
        self._n = n
        self._grid: list[list[Optional[Marker]]] = [[None] * n for _ in range(n)]
        self._moves_made = 0

    @property
    def size(self) -> int:
        return self._n

    def is_valid(self, row: int, col: int) -> bool:
        return 0 <= row < self._n and 0 <= col < self._n and self._grid[row][col] is None

    def mark_cell(self, row: int, col: int, marker: Marker) -> None:
        if not self.is_valid(row, col):
            raise ValueError(f"Invalid move at ({row}, {col})")
        self._grid[row][col] = marker
        self._moves_made += 1

    def is_full(self) -> bool:
        return self._moves_made == self._n * self._n

    def get_cell(self, row: int, col: int) -> Optional[Marker]:
        return self._grid[row][col]

    def __str__(self) -> str:
        rows = []
        for r in range(self._n):
            cells = []
            for c in range(self._n):
                cell = self._grid[r][c]
                cells.append(f" {cell.value if cell else '.'} ")
            rows.append("|".join(cells))
        separator = "-" * (self._n * 4 - 1)
        return f"\n{separator}\n".join(rows)
