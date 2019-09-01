"""The module for the random player implementation."""

from random import randint

from tic_tac_toe import TicTacToe
from game_runner import GamePlayerBase


class RandomPlayer(GamePlayerBase):
    """A player that selects a cell to be marked randomly."""

    def provide_turn(self, game: TicTacToe, is_first_request: bool):
        return (randint(0, game.grid_size - 1), randint(0, game.grid_size - 1))
