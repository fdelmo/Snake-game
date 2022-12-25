from audioop import maxpp
from lib2to3.pgen2.driver import Driver
from game import *


class GameAI(Game):
    """
    Game environtment for the AI Agent to play, inherits from Game and rewrites the 
    methods that have to do with human input so that the Agent can play.
    """

    def __init__(self, max_fps: int = 20, die_on_edges=True, caption: str = "PySnake - Training AI") -> None:
        super().__init__(max_fps, die_on_edges=die_on_edges, caption=caption)

    def evolve(self, direction: Direction) -> None:
        """
        This method evolves the state of the game by moving the snake
        and creating new food if the last was eaten.
        It checks if the game is over and returns the status.
        It takes a parameter as direction so that the AI Agent can play.

        Rewrites the method in Game class.
        """
        self.snake.steer_AI(new_dir=direction)
        self.snake.move()
        self.check_food()
        self.game_over = self.snake.check_tail_collision()
        if self.game_over:
            self.reward = -50

    def play_step(self, direction: Direction) -> None:
        """
        Step of the game's main loop.
        Rewrites the method in Game class.
        """
        # pygame.time.delay(self.time)
        self.reward = 0
        self.clock.tick(self.max_fps)
        self.events()
        self.evolve(direction=direction)
        self.draw()

    def reset(self) -> None:
        self.score = 0
        self.game_over = False

        self.snake.spawn()
        self.food.spawn(self.snake)


if __name__ == '__main__':
    game = GameAI(max_fps=30)

    while True:
        game.play_step(direction=Direction.RIGHT)

        if game.game_over:
            game.reset()
