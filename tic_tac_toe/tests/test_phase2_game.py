import pytest

from tic_tac_toe.board import Board
from tic_tac_toe.game import Game, GameStatus
from tic_tac_toe.marker import Marker
from tic_tac_toe.player import Player
from tic_tac_toe.winning_strategies import (
    HorizontalWinningStrategy,
    LeftDiagonalWinningStrategy,
    RightDiagonalWinningStrategy,
    VerticalWinningStrategy,
)


def build_game() -> Game:
    return Game(
        board=Board(3),
        players=[
            Player(name="Player 1", marker=Marker.X),
            Player(name="Player 2", marker=Marker.O),
        ],
        winning_strategies=[
            HorizontalWinningStrategy(),
            VerticalWinningStrategy(),
            LeftDiagonalWinningStrategy(),
            RightDiagonalWinningStrategy(),
        ],
    )


def test_turns_alternate_after_valid_moves():
    game = build_game()

    assert game.current_player.name == "Player 1"
    game.play_turn(0, 0)
    assert game.current_player.name == "Player 2"
    game.play_turn(1, 1)
    assert game.current_player.name == "Player 1"


def test_horizontal_win_sets_winner_and_stops_game():
    game = build_game()

    game.play_turn(0, 0)
    game.play_turn(1, 0)
    game.play_turn(0, 1)
    game.play_turn(1, 1)
    result = game.play_turn(0, 2)

    assert result.status == GameStatus.WON
    assert result.winner is not None
    assert result.winner.name == "Player 1"
    assert game.status == GameStatus.WON


def test_draw_is_detected_when_board_fills_without_winner():
    game = build_game()

    for row, col in [(0, 0), (0, 1), (0, 2), (1, 1), (1, 0), (1, 2), (2, 1), (2, 0), (2, 2)]:
        result = game.play_turn(row, col)

    assert result.status == GameStatus.DRAW
    assert game.winner is None


def test_invalid_move_does_not_advance_turn():
    game = build_game()
    game.play_turn(0, 0)

    with pytest.raises(ValueError):
        game.play_turn(0, 0)

    assert game.current_player.name == "Player 2"


def test_finished_game_rejects_additional_moves():
    game = build_game()
    game.play_turn(0, 0)
    game.play_turn(1, 0)
    game.play_turn(0, 1)
    game.play_turn(1, 1)
    game.play_turn(0, 2)

    with pytest.raises(ValueError):
        game.play_turn(2, 2)


def test_reset_restores_fresh_board_and_first_turn():
    game = build_game()
    game.play_turn(0, 0)
    game.play_turn(1, 1)

    game.reset()

    assert game.status == GameStatus.IN_PROGRESS
    assert game.winner is None
    assert game.current_player.name == "Player 1"
    assert game.board.grid == [[None, None, None], [None, None, None], [None, None, None]]
