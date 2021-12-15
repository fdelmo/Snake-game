import pygame
import os
import pickle
from datetime import date
from pygame.constants import CONTROLLER_BUTTON_MAX
from src.snake import *
from src.food import Food

#global variables
BOUNDS = (500, 500)
BLOCK_SIZE = 25


class Game:
    """Game class. Game logic and variables are self contained in the object"""

    def __init__(self):
        # game variables
        self.score = 0
        self.score_font = pygame.font.Font('freesansbold.ttf', 16)
        self.game_over = False

        # creating of an instance of each object needed
        self.snake = Snake(BLOCK_SIZE, BOUNDS)
        self.food = Food(BLOCK_SIZE, BOUNDS, self.snake)

        # check (and create) the 'records' csv file
        path = os.path.join(os.getcwd(), 'Data')
        if not os.path.isdir(path):
            os.mkdir(path)

    def print_score(self, window, pos_x, pos_y):
        """
        This method is to  be called in the later method 'draw'. This one takes
        responsability of rendering the score in the screen on each frame.
        """
        score_render = self.score_font.render(
            f'Score: {self.score}', True, (255, 97, 3))

        window.blit(score_render, (pos_x, pos_y))

    def test_save(self):
        """
        TO REMOVE!!
        """
        test_dics = [{
            'user': 'Ferran',
            'record': 1000,
            'date': date.today()
        },
            {
                'user': 'Jans',
                'record': 800,
                'date': date.today()
        },
            {
                'user': 'Alpha',
                'record': 300,
                'date': date.today()
        }]

        with open('test_records.pck', 'wb') as handle:
            pickle.dump(test_dics, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def read_records(self):
        """
        Method to read historic records of the game from disk.
        """
        with open('test_records.pck', 'rb') as handle:
            test_read_dics = pickle.load(handle)

        print(test_read_dics)

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
            self.score += 10

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

        # draw score
        self.print_score(window, pos_x=BOUNDS[1]-100, pos_y=10)

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
        pygame.time.delay(90)

        stop = game.events(pygame)

        game.evolve(pygame)

        game.draw(pygame, window)

    game.read_records()

    pygame.quit()


# Running the program
if __name__ == '__main__':
    main()
