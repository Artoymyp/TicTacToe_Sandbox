"""Tic-Tac-Toe game mechanics.

This module contains classes, that define the Tic-Tac-Toe game logic.

Classes:
    TicTacToe - class that defines the Tic-Tac-Toe game logic.
"""


class TicTacToe():
    """Tic-Tac-Toe game mechanics."""
    def __init__(self):
        self.table = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
        self.next_mark = 'O'
        self.winner = ''

    def has_ended(self) -> bool:
        """Tell whether the game has ended or not."""
        return self.winner

    def _is_winner(self, mark):
        for row in self.table:
            if row[0] == row[1] == row[2] == mark:
                return True

        ttable = [list(i) for i in zip(*self.table)]
        for row in ttable:
            if row[0] == row[1] == row[2] == mark:
                return True

        if self.table[0][0] == self.table[1][1] == self.table[2][2] == mark:
            return True

        if self.table[0][2] == self.table[1][1] == self.table[2][0] == mark:
            return True

        return False

    def mark_cell(self, horizontal_index, vertical_index):
        """Put the mark in the grid.

        Put the self.NextMark in the (horizontal_index, y) grid cell.
        Arguments:
        horizontal_index -- zero-based column index.
        vertical_index -- zero-based row index.
        """
        self.table[horizontal_index][vertical_index] = self.next_mark
        if self._is_winner(self.next_mark):
            self.winner = self.next_mark
        self.next_mark = 'X' if self.next_mark == 'O' else 'O'
