import pytest

from tic_tac_toe.board import Board
from tic_tac_toe.marker import Marker
from tic_tac_toe.player import Player
from tic_tac_toe.winning_strategies import (
    HorizontalWinningStrategy,
    LeftDiagonalWinningStrategy,
    RightDiagonalWinningStrategy,
    VerticalWinningStrategy,
)


def test_player_defaults_are_extensible():
    player = Player(name="Player 1", marker=Marker.X)
    assert player.name == "Player 1"
    assert player.marker == Marker.X


def test_board_starts_empty():
    board = Board(3)
    assert board.size == 3
    assert board.grid == [[None, None, None], [None, None, None], [None, None, None]]


def test_board_marks_valid_cell():
    board = Board(3)
    board.mark_cell(1, 2, Marker.O)
    assert board.grid[1][2] == Marker.O


def test_board_rejects_out_of_bounds_or_occupied_moves():
    board = Board(3)
    board.mark_cell(0, 0, Marker.X)

    with pytest.raises(ValueError):
        board.mark_cell(0, 0, Marker.O)

    with pytest.raises(ValueError):
        board.mark_cell(3, 0, Marker.O)


def test_horizontal_strategy_detects_winner():
    board = Board(3)
    for col in range(3):
        board.mark_cell(1, col, Marker.X)

    assert HorizontalWinningStrategy().is_winner(board, 1, 2, Marker.X) is True


def test_vertical_strategy_detects_winner():
    board = Board(3)
    for row in range(3):
        board.mark_cell(row, 0, Marker.O)

    assert VerticalWinningStrategy().is_winner(board, 2, 0, Marker.O) is True


def test_left_diagonal_strategy_detects_winner():
    board = Board(3)
    for index in range(3):
        board.mark_cell(index, index, Marker.X)

    assert LeftDiagonalWinningStrategy().is_winner(board, 2, 2, Marker.X) is True


def test_right_diagonal_strategy_detects_winner():
    board = Board(3)
    coordinates = [(0, 2), (1, 1), (2, 0)]
    for row, col in coordinates:
        board.mark_cell(row, col, Marker.O)

    assert RightDiagonalWinningStrategy().is_winner(board, 2, 0, Marker.O) is True


def test_render_shows_placeholders_for_empty_cells():
    board = Board(3)
    board.mark_cell(0, 0, Marker.X)
    rendered = board.render()
    assert "X |" in rendered
    assert " " in rendered
