"""Module defines automated tests for the Tic-Tac-Toe game."""

import unittest

from tic_tac_toe import PlayerMark
from tic_tac_toe import TicTacToe


class TestTicTacToe(unittest.TestCase):
    """Class defines automated tests for the Tic-Tac-Toe game."""

    def test_game_winner(self):
        """Test all winning configurations."""
        # arrange
        game_descriptions = [
            ([(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)], 'A win in the 1st column.'),
            ([(0, 1), (0, 0), (1, 1), (1, 0), (2, 1)], 'A win in the 2nd column.'),
            ([(0, 2), (0, 1), (1, 2), (1, 1), (2, 2)], 'A win in the 3st column.'),

            ([(0, 0), (1, 1), (0, 1), (1, 2), (0, 2)], 'A win in the 1st row.'),
            ([(1, 0), (0, 0), (1, 1), (0, 1), (1, 2)], 'A win in the 2nd row.'),
            ([(2, 0), (0, 1), (2, 1), (1, 1), (2, 2)], 'A win in the 3st row.'),

            ([(0, 0), (1, 0), (1, 1), (0, 1), (2, 2)], 'A win in the main diagonal.'),
            ([(0, 2), (1, 0), (1, 1), (0, 1), (2, 0)], 'A win in the minor diagonal.'),
            ]

        for turn_sequence, win_description in game_descriptions:
            game = TicTacToe()
            expected_winner = game.next_mark

            # assert
            for turn_index, turn in enumerate(turn_sequence):
                self.assertEqual(
                    PlayerMark.EMPTY,
                    game.winner,
                    f'Winner before the turn #{turn_index} of the game "{win_description}"')

                game.mark_cell(*turn)

            self.assertEqual(
                expected_winner,
                game.winner,
                'Winner after the last turn of the game "{win_description}"')

            self.assertTrue(game.has_ended(), "Game has ended")

    def test_game_with_no_winner(self):
        """Test the draw game ending."""
        # arrange
        game = TicTacToe()

        draw_complete_turn_sequence = [
            (0, 0), (1, 1), (2, 2), (0, 1), (2, 1), (2, 0), (0, 2), (1, 2), (1, 0)
            ]

        # assert
        for turn_index, turn in enumerate(draw_complete_turn_sequence):
            self.assertEqual(PlayerMark.EMPTY, game.winner, f'Winner before the turn #{turn_index}')
            game.mark_cell(*turn)

        self.assertEqual(PlayerMark.EMPTY, game.winner, 'Winner after the last turn')

        self.assertTrue(game.has_ended(), "Game has ended")

    def test_prediction_of_the_win_impossibility(self):
        """Test that game declares a draw when there are more moves available but there
        cannot be any winner anymore.
        """
        #arrange
        game = TicTacToe()

        draw_incomplete_turn_sequence = [
            (0, 0), (1, 1), (0, 1), (0, 2), (2, 0), (1, 0), (1, 2), (2, 2)
            ]

        #assert
        for turn_index, turn in enumerate(draw_incomplete_turn_sequence):
            self.assertEqual(PlayerMark.EMPTY, game.winner, f'Winner before the turn #{turn_index}')
            self.assertFalse(
                game.has_ended(),
                f"Game has ended prematurely before the turn #{turn_index}")

            game.mark_cell(*turn)

        self.assertEqual(PlayerMark.EMPTY, game.winner, 'Winner after the last turn')

        self.assertTrue(game.has_ended(), "Game has ended")




if __name__ == '__main__':
    unittest.main()
