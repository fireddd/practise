from enums.marker import Marker
from enums.game_status import GameStatus
from models.grid import Grid
from models.player import Player
from strategies.left_diagonal_strategy import LeftDiagonalStrategy
from strategies.right_diagonal_strategy import RightDiagonalStrategy
from strategies.horizontal_strategy import HorizontalStrategy
from strategies.vertical_strategy import VerticalStrategy
from game import Game

BOARD_SIZE = 3


def create_game() -> Game:
    grid = Grid(BOARD_SIZE)
    players = [Player("Player 1", Marker.X), Player("Player 2", Marker.O)]
    strategies = [
        LeftDiagonalStrategy(),
        RightDiagonalStrategy(),
        HorizontalStrategy(),
        VerticalStrategy(),
    ]
    return Game(grid, players, strategies)


def print_instructions():
    print("\n=== Tic Tac Toe ===")
    print(f"Board size: {BOARD_SIZE}x{BOARD_SIZE}")
    print("Player 1: X | Player 2: O")
    print("Enter moves as row,col (0-indexed). Example: 0,2 for top-right corner.")
    print("Win by completing a row, column, or diagonal. Game ends in a draw if the board is full.")
    print("Press Ctrl+C to quit at any time.")


def main():
    print_instructions()
    while True:
        game = create_game()
        print(f"\n--- New Game ---")
        print(game.grid)

        while game.status == GameStatus.IN_PROGRESS:
            player = game.current_player
            print(f"\n{player}'s turn.")

            try:
                raw = input("Enter row,col (e.g. 0,1): ").strip()
                row_str, col_str = raw.split(",")
                row, col = int(row_str.strip()), int(col_str.strip())
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                return
            except ValueError:
                print("Invalid input. Enter as row,col (e.g. 0,1)")
                continue

            try:
                game.play_move(row, col)
            except ValueError as e:
                print(f"Error: {e}")
                continue

            print(game.grid)

        if game.status == GameStatus.DRAW:
            print("\nIt's a draw!")
        else:
            winner = "X" if game.status == GameStatus.X_WINS else "O"
            print(f"\n{winner} wins!")

        try:
            replay = input("\nPlay again? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if replay != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
