from game import *


class GameAI(Game):
    """
    Game environtment for the AI Agent to play, inherits from Game and rewrites the 
    methods that have to do with human input so that the Agent can play.
    """

    def __init__(self, time: int = 60, caption: str = "PySnake - Training AI") -> None:
        super().__init__(time, caption)
        self.reward = 0

    def evolve(self, direction: Direction) -> None:
        """
        This method evolves the state of the game by moving the snake
        and creating new food if the last was eaten.
        It checks if the game is over and returns the status.
        It takes a parameter as direction so that the AI Agent can play.

        Reqwrites the method in Game class.
        """
        self.snake.steer_AI(new_dir=direction)
        self.snake.move()
        self.check_food()
        self.game_over = self.snake.check_tail_collision()

    def play_step(self, direction: Direction) -> None:
        """
        Step of the game's main loop.
        Rewrites the method in Game class.
        """
        pygame.time.delay(self.time)
        self.events()
        self.evolve(direction=direction)
        self.draw()


if __name__ == '__main__':
    game = GameAI()

    while not game.game_over:
        game.play_step(Direction.RIGHT)

    pygame.quit()
