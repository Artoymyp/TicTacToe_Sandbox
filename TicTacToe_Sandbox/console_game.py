"""A Script that runs the Tic-Tac-Toe game in a console."""

import os

from tic_tac_toe import TicTacToe


def draw(game: TicTacToe):
    """Draw the game interface in console."""
    print('+-+-+-+')
    for row in game.table:
        print('|{0}|{1}|{2}|'.format(*row))
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
    print('winner is ' + game.winner)


if __name__ == '__main__':
    main()
