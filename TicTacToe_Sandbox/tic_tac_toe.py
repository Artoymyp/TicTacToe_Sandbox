"""Tic-Tac-Toe game mechanics.

This module contains classes, that define the Tic-Tac-Toe game logic.

Classes:
    TicTacToe - class that defines the Tic-Tac-Toe game logic.

"""

from enum import Enum


class Player(Enum):
    """Enum of possible marks in a Tic-Tac-Toe cell."""

    def __init__(self, value, display_value):
        self._value_ = value
        self.display_value = display_value

    NOUGHT = (1, 'O')
    CROSS = (-1, 'X')
    EMPTY = (0, ' ')


class TicTacToe():
    """Tic-Tac-Toe game mechanics."""

    def __init__(self):
        self.table = [
            [Player.EMPTY, Player.EMPTY, Player.EMPTY],
            [Player.EMPTY, Player.EMPTY, Player.EMPTY],
            [Player.EMPTY, Player.EMPTY, Player.EMPTY]
            ]
        self.next_mark = Player.NOUGHT
        self.winner = Player.EMPTY

    @staticmethod
    def _has_winning_potential(mark1: Player, mark2: Player, mark3: Player) -> bool:
        marks_list = [mark1, mark2, mark3]
        marks_count = sum([x != Player.EMPTY for x in marks_list])
        marks_sum = sum([x.value for x in marks_list])
        return marks_sum in (marks_count, -marks_count)

    def has_ended(self) -> bool:
        """Tell whether the game has ended or not."""
        if self.winner != Player.EMPTY:
            return True

        for cell_group in self._enumerate_possible_win_cell_groups():
            if self._has_winning_potential(*cell_group):
                return False

        return True

    def _enumerate_possible_win_cell_groups(self) -> list:
        """Return the list of all cell lists, which can cause win"""
        cell_groups = []
        for row in self.table:
            cell_groups.append(row)

        transposed_table = [list(i) for i in zip(*self.table)]
        for row in transposed_table:
            cell_groups.append(row)

        cell_groups.append([self.table[0][0], self.table[1][1], self.table[2][2]])
        cell_groups.append([self.table[0][2], self.table[1][1], self.table[2][0]])

        return cell_groups

    def _evaluate_that_winner_is_determined(self):
        for cell_group in self._enumerate_possible_win_cell_groups():
            if sum([mark.value for mark in cell_group]) in (3, -3):
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
        if self._evaluate_that_winner_is_determined():
            self.winner = self.next_mark
        self.next_mark = Player.CROSS if self.next_mark == Player.NOUGHT else Player.NOUGHT