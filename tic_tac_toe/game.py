from enums.marker import Marker
from enums.game_status import GameStatus
from models.grid import Grid
from models.player import Player
from strategies.winning_strategy import WinningStrategy


class Game:
    def __init__(self, grid: Grid, players: list[Player],
                 winning_strategies: list[WinningStrategy]):
        self._grid = grid
        self._players = players
        self._winning_strategies = winning_strategies
        self._current_player_index = 0
        self._status = GameStatus.IN_PROGRESS

    @property
    def status(self) -> GameStatus:
        return self._status

    @property
    def current_player(self) -> Player:
        return self._players[self._current_player_index]

    @property
    def grid(self) -> Grid:
        return self._grid

    def play_move(self, row: int, col: int) -> GameStatus:
        if self._status != GameStatus.IN_PROGRESS:
            raise ValueError("Game is already over")

        if not self._grid.is_valid(row, col):
            raise ValueError(f"Invalid move at ({row}, {col})")

        marker = self.current_player.marker
        self._grid.mark_cell(row, col, marker)

        if self._check_winner(row, col, marker):
            self._status = GameStatus.X_WINS if marker == Marker.X else GameStatus.O_WINS
            return self._status

        if self._grid.is_full():
            self._status = GameStatus.DRAW
            return self._status

        self._alternate_turn()
        return self._status

    def _check_winner(self, row: int, col: int, marker: Marker) -> bool:
        return any(
            strategy.check_winner(self._grid, row, col, marker)
            for strategy in self._winning_strategies
        )

    def _alternate_turn(self) -> None:
        self._current_player_index = (self._current_player_index + 1) % len(self._players)
