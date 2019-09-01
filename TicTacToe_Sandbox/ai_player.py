"""This module contains implementation of the AI player."""

import random
import time

import numpy as np
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
from operator import add
import seaborn as sns
import matplotlib.pyplot as plt

from tic_tac_toe import TicTacToe, PlayerMark
from random_player import RandomPlayer
from game_runner import GamePresenterBase, GamePlayerBase, GameRunner
from console_game import ConsoleGamePlayer, ConsoleGamePresenter

FILENAME = 'weights.hdf5'
TOTAL_GAMES = 20
EPSILON_RAND_MAX = int(0.7 * TOTAL_GAMES)
EPSILON_START = TOTAL_GAMES
REREQUEST_TRESHOLD = 70


class DQNPlayer(GamePlayerBase):
    """A player, that uses Deep Q Network for selecting a cell to mark."""

    def __init__(self, dqn_agent, epsilon, rerequest_treshold):
        self.epsilon = epsilon
        self.dqn_agent = dqn_agent
        self.rerequest_count = 0
        self.total_rerequest_count = 0
        self.rerequest_treshold = rerequest_treshold

    def provide_turn(self, game, is_first_request: bool):
        if is_first_request:
            self.total_rerequest_count += self.rerequest_count
            self.rerequest_count = 0
        else:
            self.rerequest_count += 1

        #perform random actions based on agent.epsilon, or choose the action
        if random.randint(0, EPSILON_RAND_MAX) < self.epsilon or self.rerequest_count > self.rerequest_treshold:
            final_move = (random.randint(0, game.grid_size - 1), random.randint(0, game.grid_size - 1))
        else:
            # predict action based on the old state
            state_old = self.dqn_agent.get_state(game)
            prediction = self.dqn_agent.model.predict(state_old.reshape((1,9)))
            max_prop_index = np.argmax(prediction[0])
            final_move = (max_prop_index % game.grid_size, max_prop_index // game.grid_size)
        return final_move


class DQNAgent(object):
    """Class that concentrates DQN-logic.
    
    Based on the https://github.com/maurock/snake-ga.
    """
    def __init__(self):
        self.reward = 0
        self.gamma = 0.9
        self.short_memory = np.array([])
        self.agent_target = 1
        self.agent_predict = 0
        self.learning_rate = 0.005
        self.model = self.network()
        #self.model = self.network(FILENAME)
        self.epsilon = 0
        self.actual = []
        self.memory = []

    def get_state(self, game: TicTacToe):
        state = [
            game.get_cell_mark(x, y).value
                for x in range(game.grid_size) 
                    for y in range(game.grid_size) 
            ]

        return np.asarray(state)

    def set_reward(self, player: GamePlayerBase, game: TicTacToe, is_good_move: bool):
        if not is_good_move:
            self.reward = -100
            return self.reward

        self.reward = 0
        if game.has_ended():
            if game.winner == player.get_mark():
                self.reward = 10
            elif game.winner == PlayerMark.EMPTY:
                self.reward = -25
            else:
                self.reward = -50
            return self.reward
        self.reward = 5
        return self.reward

    def network(self, weights=None):
        model = Sequential()
        model.add(Dense(100, activation='relu', input_dim=9))
        for layer_index in range(9):
            model.add(Dense(output_dim=100, activation='relu'))
            model.add(Dropout(0.15))
        model.add(Dense(output_dim=9, activation='softmax'))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        if weights:
            model.load_weights(weights)
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay_new(self, memory):
        if len(memory) > 1000:
            minibatch = random.sample(memory, 1000)
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
            target_f = self.model.predict(np.array([state]))
            target_f[0][np.argmax(action)] = target
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        state_len = len(state)
        next_state_array = next_state.reshape((1, state_len))
        state_array = state.reshape((1, state_len))
        if not done:
            target = reward + self.gamma * np.amax(self.model.predict(next_state_array)[0])
        target_f = self.model.predict(state_array)
        target_f[0][np.argmax(action)] = target
        self.model.fit(state_array, target_f, epochs=1, verbose=0)


class AITrainer:
    """This class trains an AI neural network for the ai_player."""
    def __init__(self):
        self.agent = DQNAgent()
        self.state_old = []

    def get_score(self, game: TicTacToe, player: GamePlayerBase) -> int:
        if game.winner == player.get_mark():
            score = 1
        elif game.winner == PlayerMark.EMPTY:
            score = 0
        else:
            score = -1
        return score

    def on_mark_selected_callback(self, game: TicTacToe, player: GamePlayerBase, move, is_good_move: bool):
        #get new state
        state_new = self.agent.get_state(game)

        if self.player == player:
            game_has_ended = game.has_ended()

            #set the reward for the new state
            reward = self.agent.set_reward(player, game, is_good_move)
            
            #train short memory base on the new action and state
            move_array = [0]*(game.grid_size**2)
            move_array[move[0]*game.grid_size+move[1]] = 1
            self.agent.train_short_memory(self.state_old, move_array, reward, state_new, game_has_ended)
            
            # store the new data into a long term memory
            self.agent.remember(self.state_old, move_array, reward, state_new, game_has_ended)

        self.state_old = state_new

    def train(self):
        group_score_plot = []
        game_group_indices_for_a_plot =[]
        game_indices_for_a_plot =[]
        rerequest_plot = []
        group_rerequest_plot = []

        counter_games = 0
        group_size = 10
        group_score = 0
        group_rerequest_score = 0

        while counter_games < TOTAL_GAMES:
            # Collecting data for group plots.
            if counter_games % group_size == 0:
                game_group_indices_for_a_plot.append(counter_games)
                group_score_plot.append(group_score)
                group_score = 0
                group_rerequest_plot.append(group_rerequest_score)
                group_rerequest_score = 0

            # Initialize classes
            # The epsilon argument is set to give randomness to actions.
            self.player = DQNPlayer(self.agent, EPSILON_START - counter_games, REREQUEST_TRESHOLD)

            # Configura a game (DQN_AI vs Random) whithout any presentation.
            game_runner = GameRunner(game_presenter = None, player1 = self.player, player2 = RandomPlayer())
            self.state_old = self.agent.get_state(game_runner.game)
            
            # Configuring DQN-learning function to run after each game turn.
            game_runner.on_mark_selected = self.on_mark_selected_callback

            # Run the game.
            game_runner.start_game()

            # Fit DQN for new data.
            self.agent.replay_new(self.agent.memory)

            score = self.get_score(game_runner.game, self.player)
            group_score += score
            rerequest_plot.append(self.player.total_rerequest_count)
            group_rerequest_score += self.player.total_rerequest_count

            game_indices_for_a_plot.append(counter_games)
            counter_games += 1
            print(f'{counter_games}/{TOTAL_GAMES}')

        # Save model weights for future use.
        self.agent.model.save_weights(FILENAME)
        
        # Prepare learning plots.
        sns.set(color_codes=True)

        # Plot 1: 
        # - score accumulated for each group_size games.
        # - normalized cell rerequest rate for each group_size games.
        plt.figure(1)
        ax = sns.regplot(
            np.array([game_group_indices_for_a_plot])[0], 
            np.array([group_score_plot])[0], 
            color="b", x_jitter=.1, line_kws={'color':'green'})
        ax.set(xlabel='games', ylabel='score')

        group_rerequest_plot = [x / max(group_rerequest_plot) for x in group_rerequest_plot]

        ax = sns.regplot(
            np.array([game_group_indices_for_a_plot])[0], 
            np.array([group_rerequest_plot])[0], 
            color="r", x_jitter=.1, line_kws={'color':'blue'})
        ax.set(xlabel='games', ylabel='rerequest')

        # Plot 2: plain rerequest count plot.
        plt.figure(2)
        bx = sns.regplot(
            np.array([game_indices_for_a_plot])[0], 
            np.array([rerequest_plot])[0], 
            color="b", x_jitter=.1, line_kws={'color':'green'})
        bx.set(xlabel='games', ylabel='rerequest_count')

        # Show plots.
        plt.show()


def main():
    """The entry point."""
    if True:
        trainer = AITrainer()
        trainer.train()
    else:
        agent = DQNAgent()
        agent.model.load_weights(FILENAME)
        player = DQNPlayer(agent, 0, REREQUEST_TRESHOLD)
        while True:
            game_runner = GameRunner(ConsoleGamePresenter(), player, ConsoleGamePlayer())
            game_runner.start_game()
            time.sleep(2)


if __name__ == '__main__':
    main()