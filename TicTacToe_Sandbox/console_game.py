"""A Script that runs the Tic-Tac-Toe game in a console."""

import os

from tic_tac_toe import Player
from tic_tac_toe import TicTacToe


def draw(game: TicTacToe):
    """Draw the game interface in console."""
    print('+-+-+-+')
    for row in reversed(game.table):
        print('|{0}|{1}|{2}|'.format(*[mark.display_value for mark in row]))
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
    if game.winner == Player.EMPTY:
        print("The game is draw.")
    else:
        print('winner is ' + game.winner.display_value)


if __name__ == '__main__':
    main()
