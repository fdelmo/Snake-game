from gameAI import GameAI
from snake import Direction
import random
import torch
from collections import deque


MAX_MEMORY = 10**5


class Agent:
    def __init__(self) -> None:
        self.n_games = 0
        self.epsilon = 0  # randomness of agent actions
        self.memory = deque(maxlen=MAX_MEMORY)

    def get_state(self, game):
        pass

    def get_action(self, state):
        pass

    def remember(self, state, action, reward, next_state, game_over):
        pass


def train_agent(agent: Agent):
    game = GameAI()
    while True:
        # get state of the game
        state = agent.get_state(game)

        # get action to perform (direction to move)
        action = agent.get_action(state)

        # evolve the game one step further with the chose action and get new state
        game.play_step(direction=action)
        state_new = agent.get_state(game)

        # store info in memory for long term memory training after
        agent.remember(
            state=state,
            action=action,
            reward=game.reward,
            next_state=state_new,
            game_over=game.game_over
        )
