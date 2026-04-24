from abc import ABC, abstractmethod

from tic_tac_toe.board import Board
from tic_tac_toe.marker import Marker


class WinningStrategy(ABC):
    @abstractmethod
    def is_winner(self, board: Board, row: int, col: int, marker: Marker) -> bool:
        raise NotImplementedError


class HorizontalWinningStrategy(WinningStrategy):
    def is_winner(self, board: Board, row: int, col: int, marker: Marker) -> bool:
        return all(board.grid[row][current_col] == marker for current_col in range(board.size))


class VerticalWinningStrategy(WinningStrategy):
    def is_winner(self, board: Board, row: int, col: int, marker: Marker) -> bool:
        return all(board.grid[current_row][col] == marker for current_row in range(board.size))


class LeftDiagonalWinningStrategy(WinningStrategy):
    def is_winner(self, board: Board, row: int, col: int, marker: Marker) -> bool:
        if row != col:
            return False
        return all(board.grid[index][index] == marker for index in range(board.size))


class RightDiagonalWinningStrategy(WinningStrategy):
    def is_winner(self, board: Board, row: int, col: int, marker: Marker) -> bool:
        if row + col != board.size - 1:
            return False
        return all(board.grid[index][board.size - 1 - index] == marker for index in range(board.size))
