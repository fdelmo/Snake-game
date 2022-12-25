from gameAI import *
from snake import Direction
import random
import tensorflow as tf
from collections import deque
import numpy as np
from model import *
from plotter import plot

MAX_MEMORY = 10**5
BATCH_SIZE = 1000


class Agent:
    def __init__(self) -> None:
        self.n_games = 0
        self.record = 0
        self.epsilon = 0  # randomness of agent actions
        self.lr = 0.001  # learning rate
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = SimpleModel([512, 512, 256], 3)
        # self.model = ConvModel(404, [[32, 32], [256, 256]], 3)
        self.trainer = Trainer(self.model, self.lr, self.gamma)

    def get_state(self, game: GameAI) -> np.array(int):
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

        dang_l, dang_r, dang_u, dang_d = 0, 0, 0, 0

        if (game.snake.body[-1][0]-BLOCK_SIZE == 0):
            dang_l = 1
        elif (game.snake.body[-1][0]+BLOCK_SIZE == BOUNDS[0]):
            dang_r = 1
        elif (game.snake.body[-1][1]-BLOCK_SIZE == 0):
            dang_u = 1
        elif (game.snake.body[-1][1]+BLOCK_SIZE == BOUNDS[1]):
            dang_d = 1

        # x_to_food = (game.food.position[0]-game.snake.body[-1][0])/BLOCK_SIZE
        # y_to_food = (game.food.position[1]-game.snake.body[-1][1])/BLOCK_SIZE

        # state = [dl, dr, du, dd, dang_l, dang_r,
        #          dang_u, dang_d, x_to_food, y_to_food]

        state = [du, dd, dr, dl, dang_u, dang_d, dang_r, dang_l,

                 game.food.position[1] > game.snake.body[-1][1],
                 game.food.position[1] < game.snake.body[-1][1],
                 game.food.position[0] > game.snake.body[-1][0],
                 game.food.position[0] < game.snake.body[-1][0],

                 ]

        # state = [du, dd, dr, dl]
        # for col in range(int(BOUNDS[1]/BLOCK_SIZE)):
        #     for row in range(int(BOUNDS[0]/BLOCK_SIZE)):
        #         pos = (row*BLOCK_SIZE, col*BLOCK_SIZE)

        #         if pos == game.snake.body[-1]:
        #             cell = 2
        #         elif pos in game.snake.body:
        #             cell = 1
        #         elif pos == game.food.position:
        #             cell = -1
        #         else:
        #             cell = 0

        #         state.append(cell)

        # state = [du, dd, dr, dl, game.snake.body[-1][0], game.snake.body[-1][1],
        #          x_to_food, y_to_food]

        return np.array(state, dtype=int)

    def get_action(self, game: GameAI, state):
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

        if random.randint(0, 150) < self.epsilon:
            move = random.randint(0, 2)  # 0=straigth, 1=right, 2=left
        else:
            state_trans = tf.convert_to_tensor(state, dtype=tf.float64)
            state_trans = tf.expand_dims(state_trans, 0)
            prediction = self.model(state_trans)
            move = int(tf.argmax(prediction, axis=1))

        # transform the 3 possible actions into the 4 possible directions
        # (needed for the game logic to work properly)
        return move

    def action_to_direction(self, game: GameAI, move: int) -> Direction:
        """
        Transform the action predicted by the model (0,1,2) =
        (straight, right, left) into a direction for the game input.
        """
        return Direction((game.snake.direction + (2**move-1)) % 4)

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


def get_last_means(scores: List, N: int) -> float:
    """
    Computes the mean of the last N scores.
    """
    vals = scores[-N:]
    return float(sum(vals)/(min(N, len(vals))))


def train_agent(agent: Agent, n_games: int, model_name: str):
    scores = []
    mean_scores = []
    last_mean_scores_20 = []
    game_total_score = 0
    game = GameAI(max_fps=1000, die_on_edges=True)
    iteration = 0
    total_reward = 0
    while True:
        iteration += 1
        # get state of the game
        state = agent.get_state(game)

        # get action to perform (direction to move)
        action = agent.get_action(game=game, state=state)

        # transform the action into direction input
        direction = agent.action_to_direction(game, action)

        # evolve the game one step further with the chose action and get new state
        game.play_step(direction=direction)
        state_new = agent.get_state(game)

        # return the game over status as an integer
        game_over = int(game.game_over)

        if game.reward > 0:
            iteration = 0
        elif (iteration % 1000 == 0):
            game.reward = -50
            game.game_over = True
        # store info in memory for long term memory training after
        agent.remember(
            state=state,
            action=action,
            reward=game.reward,
            next_state=state_new,
            game_over=game_over
        )

        # trian the agent in short memory
        agent.train_short_memory(
            state=state,
            action=action,
            reward=game.reward,
            new_state=state_new,
            game_over=game_over
        )

        total_reward += game.reward
        # when game is over: train on long memory, plot and update results, and reset the game
        if game.game_over:
            agent.n_games += 1
            print(
                f'Game {agent.n_games}. Score: {game.score}. Reward: {total_reward}')
            total_reward = 0
            agent.train_long_memory()

            # save the best version of the model:
            # this might be changed later to include different levels of models
            if game.score > agent.record:
                agent.record = game.score
                agent.model.save_model(model_name)

            scores.append(game.score)
            game_total_score += game.score
            mean_scores.append(game_total_score/agent.n_games)
            last_mean_scores_20.append(get_last_means(scores, 20))
            game.reset()

            plot(scores=scores, mean_scores=mean_scores,
                 last_20_mean=last_mean_scores_20, model_name=model_name)

            if agent.n_games == n_games:
                break


if __name__ == '__main__':
    agent = Agent()
    train_agent(agent=agent, n_games=5000,
                model_name='DirectionalDangSimple_300_100')
