class TicTacToe(object):
    """TicTacToe game mechanics"""
    def __init__(self):
        self.table = [['1','2','3'],['4','5','6'],['7','8','9']]
        self.NextMark = 'O'
        self.Winner = ''

    def Draw(self):
        print('+-+-+-+')
        for row in self.table:
            print('|{0}|{1}|{2}|'.format(*row))
        print('+-+-+-+')

    def IsEnded(self):
        return self.Winner

    def _IsWinner(self, playerMark):
        for row in self.table:
            if (row[0] == row[1] == row[2] == playerMark):
                return True;

        ttable = [list(i) for i in zip(*self.table)]
        for row in ttable:
            if (row[0] == row[1] == row[2] == playerMark):
                return True;

        if (self.table[0][0]==self.table[1][1]==self.table[2][2]==playerMark):
            return True

        if (self.table[0][2]==self.table[1][1]==self.table[2][0]==playerMark):
            return True

        return False

    def MarkCell(self, x, y):
        self.table[x][y]=self.NextMark
        if (self._IsWinner(self.NextMark)):
            self.Winner = self.NextMark
        self.NextMark = 'X' if self.NextMark == 'O' else 'O'


if __name__ == "__main__":
    import os

    game = TicTacToe()
    while not game.IsEnded():
        os.system('cls||clear')

        game.Draw()
        cellNumber = int(input('Please use a numpad 1-9 Keys to make the next move:'))
        cellNumber-=1
        x, y = cellNumber//3, cellNumber%3
        game.MarkCell(x,y)
    else:
        os.system('cls||clear')

        game.Draw()
        print('winner is '+game.Winner)
