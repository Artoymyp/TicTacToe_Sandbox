"""A Script that runs the Tic-Tac-Toe game in a console."""

import os

from tic_tac_toe import PlayerMark
from tic_tac_toe import TicTacToe
from game_runner import GameRunner, GamePresenterBase, GamePlayerBase


class ConsoleGamePlayer(GamePlayerBase):
    """Source of turns for the game that is a console user."""

    def provide_turn(self, game: TicTacToe) -> (int, int):
        """Request a grid cell from a console user."""
        cell_number = int(input('Please use a numpad 1-9 Keys to make the next move:'))
        cell_number -= 1
        return (cell_number % 3, cell_number // 3)


class ConsoleGamePresenter(GamePresenterBase):
    """Presents a game to a console user."""

    def show(self, game: TicTacToe):
        """Draw the game interface in console."""
        os.system('cls||clear')
        print('+-+-+-+')
        for vertical_index in reversed(range(game.grid_size)):
            row_display_values = [
                game.get_cell_mark(horizontal_index, vertical_index).display_value
                for horizontal_index in range(game.grid_size)
                ]
            print('|{0}|{1}|{2}|'.format(*row_display_values))
        print('+-+-+-+')

    def show_winner(self, game: TicTacToe):
        """Displays a result of the game."""
        self.show(game)
        if game.winner == PlayerMark.EMPTY:
            print("The game is draw.")
        else:
            print('winner is ' + game.winner.display_value)


def main():
    """The entry point."""
    game_runner = GameRunner(ConsoleGamePresenter(), ConsoleGamePlayer(), ConsoleGamePlayer())
    game_runner.start_game()


if __name__ == '__main__':
    main()
