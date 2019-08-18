"""This module contains tests for the GameRunner class."""

import unittest
from unittest.mock import Mock, call

from game_runner import GameRunner, GamePresenterBase, GamePlayerBase

class TestGameRunner(unittest.TestCase):
    """Class tests logic of the GameRunner class."""

    _game_turn_sequence = []

    def _game_turn_sequence_provider(self, game):
        return self._game_turn_sequence.pop(0)

    def test_simple_game_call_sequence(self):
        """Test a simple game run."""

        # arrange
        self._game_turn_sequence = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]

        mock_sequence_manager = Mock()
        game_presenter = Mock(create_autospec=GamePresenterBase)
        player1 = Mock(create_autospec=GamePlayerBase)
        player1.provide_turn.side_effect = self._game_turn_sequence_provider

        player2 = Mock(create_autospec=GamePlayerBase)
        player2.provide_turn.side_effect = self._game_turn_sequence_provider

        mock_sequence_manager.attach_mock(game_presenter.show, 'show_game')
        mock_sequence_manager.attach_mock(game_presenter.show_winner, 'show_winner')
        mock_sequence_manager.attach_mock(player1.provide_turn, 'provide_turn1')
        mock_sequence_manager.attach_mock(player2.provide_turn, 'provide_turn2')

        runner = GameRunner(game_presenter, player1, player2)
        game = runner.game

        expected_call_sequence = [
            call.show_game(game),
            call.provide_turn1(game),
            call.show_game(game),
            call.provide_turn2(game),
            call.show_game(game),
            call.provide_turn1(game),
            call.show_game(game),
            call.provide_turn2(game),
            call.show_game(game),
            call.provide_turn1(game),
            call.show_winner(game)
            ]

        # act
        runner.start_game()

        # assert
        mock_sequence_manager.assert_has_calls(expected_call_sequence)

    def test_game_with_wrong_moves_call_sequence(self):
        """Test that providing wrong cell numbers will not affect the flow of a game."""

        # arrange
        self._game_turn_sequence = [
            (0, 0),
            (0, 0),  # Duplicated move
            (100, 0),  # Out of range move
            (0, 1),
            (1, 0),
            (1, 1),
            (2, 0)
            ]

        mock_sequence_manager = Mock()
        game_presenter = Mock(create_autospec=GamePresenterBase)
        player1 = Mock(create_autospec=GamePlayerBase)
        player1.provide_turn.side_effect = self._game_turn_sequence_provider

        player2 = Mock(create_autospec=GamePlayerBase)
        player2.provide_turn.side_effect = self._game_turn_sequence_provider

        mock_sequence_manager.attach_mock(game_presenter.show, 'show_game')
        mock_sequence_manager.attach_mock(game_presenter.show_winner, 'show_winner')
        mock_sequence_manager.attach_mock(player1.provide_turn, 'provide_turn1')
        mock_sequence_manager.attach_mock(player2.provide_turn, 'provide_turn2')

        runner = GameRunner(game_presenter, player1, player2)
        game = runner.game

        expected_call_sequence = [
            call.show_game(game),
            call.provide_turn1(game),
            call.show_game(game),
            call.provide_turn2(game),
            call.show_game(game),
            call.provide_turn2(game),
            call.show_game(game),
            call.provide_turn2(game),
            call.show_game(game),
            call.provide_turn1(game),
            call.show_game(game),
            call.provide_turn2(game),
            call.show_game(game),
            call.provide_turn1(game),
            call.show_winner(game)
            ]

        # act
        runner.start_game()

        # assert
        mock_sequence_manager.assert_has_calls(expected_call_sequence)


if __name__ == '__main__':
    unittest.main()
