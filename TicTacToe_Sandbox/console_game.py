import os

from tic_tac_toe import TicTacToe

def main():
    game = TicTacToe()
    while not game.has_ended():
        os.system('cls||clear')

        game.draw()
        cell_number = int(input('Please use a numpad 1-9 Keys to make the next move:'))
        cell_number -= 1
        game.mark_cell(cell_number // 3, cell_number % 3)

    os.system('cls||clear')

    game.draw()
    print('winner is ' + game.winner)

if __name__ == '__main__':
    main()
