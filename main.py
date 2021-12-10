import pygame
from src.snake import *
from src.food import Food

#global variables
BOUNDS = (500, 500)
BLOCK_SIZE = 25


class Game:
    """Game class. Game logic and variables are self contained in the object"""

    def __init__(self):
        # game variables
        self.points = 0
        self.game_over = False

        # creating of an instance of each object needed
        self.snake = Snake(BLOCK_SIZE, BOUNDS)
        self.food = Food(BLOCK_SIZE, BOUNDS, self.snake)

    def events(self, game):
        """Returns True if the game need to be stopped"""
        for event in game.event.get():
            if event.type == game.QUIT:
                return True

    def check_food(self):
        """
        This methid checks if the head of the snake is in the position of the
        food. If True, then the snake eats the food and the food respawns.
        Then the score of the game increases by 10.
        """
        if self.snake.body[-1] == self.food.position:
            self.snake.eat()
            self.food.spawn(self.snake)
            self.points += 10

    def evolve(self, game):
        """
        This method evolves the state of the game by moving the snake
        and creating new food if the last was eaten. 
        It checks if the gamee is over and returns the status
        """
        self.snake.steer(game)
        self.snake.move()
        self.check_food()
        self.game_over = self.snake.check_tail_collision()

        return self.game_over

    def draw(self, game, window):
        """
        This method draws all elements to the screen. Has to be run every 
        frame and only after all events and game logics have been checked
        """
        window.fill((0, 0, 0))

        # draw all objects in screen
        self.snake.draw(game, window)
        self.food.draw(game, window)

        game.display.flip()


def main():
    """Main function"""
    # initialization of pygame and creation of the window
    pygame.init()
    window = pygame.display.set_mode(BOUNDS)
    pygame.display.set_caption("PySnake")
    pygame.mouse.set_visible(False)

    game = Game()

    stop = False

    while (not stop) & (game.game_over == False):
        pygame.time.delay(80)

        stop = game.events(pygame)

        game.evolve(pygame)

        game.draw(pygame, window)

    pygame.quit()


# Running the program
if __name__ == '__main__':
    main()
