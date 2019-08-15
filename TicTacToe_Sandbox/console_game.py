"""A Script that runs the Tic-Tac-Toe game in a console."""

import os

from tic_tac_toe import PlayerMark
from tic_tac_toe import TicTacToe


def draw(game: TicTacToe):
    """Draw the game interface in console."""
    print('+-+-+-+')
    for vertical_index in reversed(range(game.grid_size)):
        row_display_values = [
            game.get_cell_mark(horizontal_index, vertical_index).display_value
            for horizontal_index in range(game.grid_size)
            ]
        print('|{0}|{1}|{2}|'.format(*row_display_values))
    print('+-+-+-+')


def main():
    """The entry point."""
    game = TicTacToe()
    while not game.has_ended():
        os.system('cls||clear')

        draw(game)
        cell_number = int(input('Please use a numpad 1-9 Keys to make the next move:'))
        cell_number -= 1
        game.mark_cell(cell_number // 3, cell_number % 3)

    os.system('cls||clear')

    draw(game)
    if game.winner == PlayerMark.EMPTY:
        print("The game is draw.")
    else:
        print('winner is ' + game.winner.display_value)


if __name__ == '__main__':
    main()
