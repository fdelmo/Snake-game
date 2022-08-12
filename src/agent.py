from gameAI import *
from snake import Direction
import random
import tensorflow as tf
from collections import deque
import numpy as np


MAX_MEMORY = 10**5
BATCH_SIZE = 1000


class Agent:
    def __init__(self) -> None:
        self.n_games = 0
        self.epsilon = 0  # randomness of agent actions
        self.lr = 0.01  # learning rate
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = None  # TODO
        self.trainer = None  # TODO

    def get_state(self, game: GameAI) -> np.array[int]:
        """
        Get the current state of the game and output it as an np.array of integers.

        Parameters outputed (in this order, concatenated):
            - Direction [UP, DOWN, RIGHT, LEFT] (0 or 1 representing the boolean state)
            - Image of the game in "grid" mode: 
                - 0 = empty space
                - 1 = snake's body (not head)
                - 2 = snake's head
                - 5 = food
        """
        du = game.snake.direction == Direction.UP
        dd = game.snake.direction == Direction.DOWN
        dr = game.snake.direction == Direction.RIGHT
        dl = game.snake.direction == Direction.LEFT

        state = [du, dd, dr, dl]
        for col in range(int(BOUNDS[1]/BLOCK_SIZE)):
            for row in range(int(BOUNDS[0]/BLOCK_SIZE)):
                pos = (row*BLOCK_SIZE, col*BLOCK_SIZE)

                if pos == game.snake.body[-1]:
                    cell = 2
                elif pos in game.snake.body:
                    cell = 1
                elif pos == game.food.position:
                    cell = 5
                else:
                    cell = 0

                state.append(cell)

        return np.array(state, dtype=int)

    def get_action(self, state, game: GameAI):
        """
        Method to choose the action that the agent will perform in each
        play_step. The agent will choose to move right (1), left (2) or go
        straight (0). Then this value needs to be transformed acordingly into
        the accepted values of game.snake.direction.

        We include some randomness (which will decrease as we train the agent)
        to make sure we maximize exploration of possibilities, specially at the
        beginning of the training, in order to try to avoid local extrema of the 
        Q function.
        """
        self.epsilon = 100 - self.n_games

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)  # 0=straigth, 1=right, 2=left
        else:
            state_trans = tf.convert_to_tensor(state, dtype=tf.float64)
            prediction = self.model.predict(state_trans)
            move = tf.argmax(prediction).numpy()

        # transform the 3 possible actions into the 4 possible directions
        # (needed for the game logic to work properly)
        return (game.snake.direction + (2**move-1)) % 4

    def remember(self, state, action, reward, next_state, game_over) -> None:
        """
        Stores previous state, action taken, next state, reward obtained and
        game over status of the game in memory.

        Note: if MAX_MEMORY is reached, the most left value will be poped out
        to introduce the newest value on the far right of the deque (append).
        """
        self.memory.append((state, action, reward, next_state, game_over))

    def train_short_memory(self, state, action, reward, new_state, game_over):
        """Implement a one step training cycle."""
        self.trainer.train(state, action, reward, new_state, game_over)

    def train_long_memory(self):
        """
        Implement a longer training cycle (training in a random subset of the
        memory of size BATCH_SIZE).
        """
        if len(self.memory) > BATCH_SIZE:
            mem_subset = random.sample(self.memory, BATCH_SIZE)
        else:
            mem_subset = self.memory

        states, actions, rewards, new_states, game_overs = zip(*mem_subset)
        self.trainer.train(states, actions, rewards, new_states, game_overs)


def train_agent(agent: Agent, n_games: int):
    game = GameAI(max_fps=30)
    for iteration in range(n_games):
        # get state of the game
        state = agent.get_state(game)

        # get action to perform (direction to move)
        action = agent.get_action(game, state)

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

        # trian the agent in short memory
        agent.train_short_memory(
            state=state,
            action=action,
            reward=game.reward,
            next_state=state_new,
            game_over=game.game_over
        )

        # when game is over: train on long memory, plot and update results, and reset the game
        if game.game_over:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
