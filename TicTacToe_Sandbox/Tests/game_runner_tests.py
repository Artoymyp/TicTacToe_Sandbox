"""This module contains tests for the GameRunner class."""

import unittest
from unittest.mock import Mock, call

from game_runner import GameRunner, GamePresenterBase, GamePlayerBase

class TestGameRunner(unittest.TestCase):
    """Class tests logic of the GameRunner class."""

    _game_turn_sequence = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        game_presenter = Mock(create_autospec=GamePresenterBase)
        player1 = Mock(create_autospec=GamePlayerBase)
        player1.provide_turn.side_effect = self._game_turn_sequence_provider

        player2 = Mock(create_autospec=GamePlayerBase)
        player2.provide_turn.side_effect = self._game_turn_sequence_provider

        self._runner = GameRunner(game_presenter, player1, player2)

        self._mock_sequence_manager = Mock()
        self._mock_sequence_manager.attach_mock(game_presenter.show, 'show_game')
        self._mock_sequence_manager.attach_mock(game_presenter.show_winner, 'show_winner')
        self._mock_sequence_manager.attach_mock(player1.provide_turn, 'provide_turn1')
        self._mock_sequence_manager.attach_mock(player2.provide_turn, 'provide_turn2')

    def _game_turn_sequence_provider(self, game, is_first_request):
        return self._game_turn_sequence.pop(0)

    def test_simple_game_call_sequence(self):
        """Test a simple game run."""
        # arrange
        self._game_turn_sequence = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]
        game = self._runner.game

        expected_call_sequence = [
            call.show_game(game),
            call.provide_turn1(game, True),
            call.show_game(game),
            call.provide_turn2(game, True),
            call.show_game(game),
            call.provide_turn1(game, True),
            call.show_game(game),
            call.provide_turn2(game, True),
            call.show_game(game),
            call.provide_turn1(game, True),
            call.show_winner(game)
            ]

        # act
        self._runner.start_game()

        # assert
        self._mock_sequence_manager.assert_has_calls(expected_call_sequence)

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

        game = self._runner.game

        expected_call_sequence = [
            call.show_game(game),
            call.provide_turn1(game, True),
            call.show_game(game),
            call.provide_turn2(game, True),
            call.show_game(game),
            call.provide_turn2(game, False),
            call.show_game(game),
            call.provide_turn2(game, False),
            call.show_game(game),
            call.provide_turn1(game, True),
            call.show_game(game),
            call.provide_turn2(game, True),
            call.show_game(game),
            call.provide_turn1(game, True),
            call.show_winner(game)
            ]

        # act
        self._runner.start_game()

        # assert
        self._mock_sequence_manager.assert_has_calls(expected_call_sequence)


if __name__ == '__main__':
    unittest.main()
