"""A Tic-Tac-Toe game running infrastructure.

This module contains classes that allow to run the Tic-Tac-Toe game.

Classes:
    GamePresenterBase - base for classes that present a game's state.
    GamePlayerBase - base class for objects that select game cells to mark.
    GameRunner - class that describes Tic-Tac-Toe game sequence.
"""

from tic_tac_toe import TicTacToe


class GamePresenterBase():
    """Base class for any object that presents a game."""

    def show(self, game: TicTacToe):
        """Show a game state."""
        raise NotImplementedError

    def show_winner(self, game: TicTacToe):
        """Show a game winner."""
        raise NotImplementedError


class GamePlayerBase():
    """The base class for any source of turns for the game."""

    def provide_turn(self, game: TicTacToe) -> (int, int):
        """Provide a game grid cell coordinates."""
        raise NotImplementedError


class GameRunner():
    """The class that controls a Tic-Tac-Toe game sequence.

    The class helps to abstract the game logic from a game representation and
    from a cell selection logic.
    """

    def __init__(
            self,
            game_presenter: GamePresenterBase,
            player1: GamePlayerBase,
            player2: GamePlayerBase):
        self.game_presenter = game_presenter
        self._current_player = player1
        self._next_player = player2
        self.game = TicTacToe()

    def start_game(self):
        """Start main game cycle."""

        while not self.game.has_ended():
            while True:
                self.game_presenter.show(self.game)
                turn = self._current_player.provide_turn(self.game)
                success = self.game.mark_cell(*turn)
                if success:
                    break

            self._current_player, self._next_player = self._next_player, self._current_player

        self.game_presenter.show_winner(self.game)
