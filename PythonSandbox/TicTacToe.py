class TicTacToe(object):
    """TicTacToe game mechanics"""
    def __init__(self):
        self.table = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
        self.next_mark = 'O'
        self.winner = ''

    def draw(self):
        print('+-+-+-+')
        for row in self.table:
            print('|{0}|{1}|{2}|'.format(*row))
        print('+-+-+-+')

    def has_ended(self):
        return self.winner

    def _is_winner(self, mark):
        for row in self.table:
            if (row[0] == row[1] == row[2] == mark):
                return True;

        ttable = [list(i) for i in zip(*self.table)]
        for row in ttable:
            if (row[0] == row[1] == row[2] == mark):
                return True;

        if (self.table[0][0] == self.table[1][1] == self.table[2][2] == mark):
            return True

        if (self.table[0][2] == self.table[1][1] == self.table[2][0] == mark):
            return True

        return False

    def mark_cell(self, x, y):
        """Put the mark in the grid
        
        Put the self.NextMark in the (x, y) grid cell.
        Arguments:
        x -- zero-based column index
        y -- zero-based row index
        """
        self.table[x][y] = self.next_mark
        if (self._is_winner(self.next_mark)):
            self.winner = self.next_mark
        self.next_mark = 'X' if self.next_mark == 'O' else 'O'


if __name__ == "__main__":
    import os

    game = TicTacToe()
    while not game.has_ended():
        os.system('cls||clear')

        game.draw()
        cellNumber = int(input('Please use a numpad 1-9 Keys to make the next move:'))
        cellNumber -= 1
        x, y = cellNumber // 3, cellNumber % 3
        game.mark_cell(x, y)
    else:
        os.system('cls||clear')

        game.draw()
        print('winner is ' + game.winner)
