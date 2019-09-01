"""A Tic-Tac-Toe game running infrastructure.

This module contains classes that allow to run the Tic-Tac-Toe game.

Classes:
    GamePresenterBase - base for classes that present a game's state.
    GamePlayerBase - base class for objects that select game cells to mark.
    GameRunner - class that describes Tic-Tac-Toe game sequence.
"""

from tic_tac_toe import TicTacToe, PlayerMark


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

    def provide_turn(self, game: TicTacToe, is_first_request: bool) -> (int, int):
        """Provide a game grid cell coordinates."""
        raise NotImplementedError

    def get_mark(self) -> PlayerMark:
        return self.mark

    def set_mark(self, mark: PlayerMark):
        self.mark = mark


class GameRunner():
    """The class that controls a Tic-Tac-Toe game sequence.

    The class helps to abstract the game logic from a game representation and
    from a cell selection logic.

    on_mark_selected(game, current_player, selected_cell, is_valid_cell_selected) - a method to be called after each mark set attempt.
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

        self._current_player.set_mark(self.game.next_mark)
        self._next_player.set_mark(self.game._previous_mark)

        self.on_mark_selected = None

    def start_game(self):
        """Start main game cycle."""

        while not self.game.has_ended():
            is_first_request = True
            while True:
                if self.game_presenter != None:
                    self.game_presenter.show(self.game)
                turn = self._current_player.provide_turn(self.game, is_first_request)
                success = self.game.mark_cell(*turn)

                if self.on_mark_selected != None:
                    self.on_mark_selected(self.game, self._current_player, turn, success)

                if success:
                    break

                is_first_request = False

            self._current_player, self._next_player = self._next_player, self._current_player

        if self.game_presenter != None:
            self.game_presenter.show_winner(self.game)
