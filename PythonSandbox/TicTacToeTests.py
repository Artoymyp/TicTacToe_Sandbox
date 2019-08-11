import unittest
from TicTacToe import TicTacToe

class Test_TicTacToeTests(unittest.TestCase):
    def test_game_winner(self):
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
            expected_winner = game.NextMark

            # assert
            for turn_index, turn in enumerate(turn_sequence):
                self.assertEqual(
                    '', 
                    game.Winner, 
                    f'Winner before the turn #{turn_index} of the game "{win_description}"')

                game.MarkCell(*turn)

            self.assertEqual(
                expected_winner, 
                game.Winner, 
                'Winner after the last turn of the game "{win_description}"')

    def test_game_with_no_winner(self):
        # arrange
        game = TicTacToe()

        draw_turn_sequence = [(0, 0), (1, 1), (2, 2), (0, 1), (2, 1), (2, 0), (0, 2), (1, 0)]

        # assert
        for turn_index, turn in enumerate(draw_turn_sequence):
            self.assertEqual('', game.Winner, f'Winner before the turn #{turn_index}')
            game.MarkCell(*turn)

        self.assertEqual('', game.Winner, 'Winner after the last turn')


if __name__ == '__main__':
    unittest.main()
