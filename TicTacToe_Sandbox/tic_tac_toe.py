"""Tic-Tac-Toe game mechanics.

This module contains classes, that define the Tic-Tac-Toe game logic.

Classes:
    TicTacToe - class that defines the Tic-Tac-Toe game logic.
    PlayerMark - enum for valid states of a cell in the game's grid.

"""

from enum import Enum


class PlayerMark(Enum):
    """Enum of possible marks in a Tic-Tac-Toe cell."""

    def __init__(self, value, display_value):
        self._value_ = value
        self.display_value = display_value

    NOUGHT = (1, 'O')
    CROSS = (-1, 'X')
    EMPTY = (0, ' ')


class TicTacToe():
    """Tic-Tac-Toe game mechanics."""

    grid_size = 3

    def __init__(self):
        self._table = [
            [PlayerMark.EMPTY
             for x in range(TicTacToe.grid_size)]
            for y in range(TicTacToe.grid_size)
            ]
        self.next_mark = PlayerMark.NOUGHT
        self._previous_mark = PlayerMark.CROSS
        self.winner = PlayerMark.EMPTY

    @staticmethod
    def _has_winning_potential(mark1: PlayerMark, mark2: PlayerMark, mark3: PlayerMark) -> bool:
        marks_list = [mark1, mark2, mark3]
        marks_count = sum([x != PlayerMark.EMPTY for x in marks_list])
        marks_sum = sum([x.value for x in marks_list])
        return marks_sum in (marks_count, -marks_count)

    def has_ended(self) -> bool:
        """Tell whether the game has ended or not."""
        if self.winner != PlayerMark.EMPTY:
            return True

        for cell_group in self._enumerate_possible_win_cell_groups():
            if self._has_winning_potential(*cell_group):
                return False

        return True

    def _enumerate_possible_win_cell_groups(self) -> list:
        """Return the list of all cell lists, which can cause win"""
        cell_groups = []
        for row in self._table:
            cell_groups.append(row)

        transposed_table = [list(i) for i in zip(*self._table)]
        for row in transposed_table:
            cell_groups.append(row)

        cell_groups.append([self._table[0][0], self._table[1][1], self._table[2][2]])
        cell_groups.append([self._table[0][2], self._table[1][1], self._table[2][0]])

        return cell_groups

    def _evaluate_that_winner_is_determined(self):
        for cell_group in self._enumerate_possible_win_cell_groups():
            if sum([mark.value for mark in cell_group]) in (3, -3):
                return True

        return False

    def mark_cell(self, horizontal_index, vertical_index) -> bool:
        """Put the mark in the grid.

        Put the self.NextMark in the (horizontal_index, vertical_index) grid cell.
        Arguments:
        horizontal_index -- zero-based column index.  Should be in [0, grid_size).
        vertical_index -- zero-based row index.  Should be in [0, grid_size).

        If the cell (horizontal_index, vertical_index) is already marked, then
        game state will not change.

        Return:
        Bool value indicating whether a cell was successfully marked.
        """

        if horizontal_index >= self.grid_size or vertical_index >= self.grid_size:
            return False

        if PlayerMark.EMPTY != self.get_cell_mark(horizontal_index, vertical_index):
            return False

        self._table[horizontal_index][vertical_index] = self.next_mark
        if self._evaluate_that_winner_is_determined():
            self.winner = self.next_mark

        self.next_mark, self._previous_mark = self._previous_mark, self.next_mark

        return True

    def get_cell_mark(self, horizontal_index, vertical_index) -> PlayerMark:
        """Return the mark from the grid cell.

        Returns the mark placed inside the (horizontal_index, vertical_index) grid cell.
        Arguments:
        horizontal_index -- zero-based column index.
        vertical_index -- zero-based row index.

        Exceptions:
        Throws IndexError if horizontal_index or vertical_index are not in the [0, grid_size).
        """
        return self._table[horizontal_index][vertical_index]
