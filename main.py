import pygame
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

    def print_score(self, window, pos_x, pos_y):
        """
        This method is to  be called in the later method 'draw'. This one takes
        responsability of rendering the score in the screen on each frame.
        """
        score_render = self.score_font.render(
            f'Score: {self.score}', True, (255, 97, 3))

        window.blit(score_render, (pos_x, pos_y))

    def read_records(self):
        """
        Method to read historic records of the game from disk. Returns a list
        with dictionaries with info of the top 5 records.
        """
        try:
            with open('records.pck', 'rb') as handle:
                records = pickle.load(handle)

        except:
            # TODO: Temporary command.
            records = []
            print('There is no record history')

        return records

    def save_record(self, records, user):
        """
        This method checks if the current score is in the top N records and stores
        it in the correct position if it is. It also stores the date and username.
        """

        records.append({
            "user": user,
            "record": self.score,
            "date": date.today()
        })

        # sort the records
        records = sorted(records, key=lambda k: k['record'], reverse=True)

        if len(records) > 3:
            records.pop()  # ensure that there are only 5 top records

        # save the records to disk
        with open('records.pck', 'wb') as handle:
            pickle.dump(records, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def check_record(self):
        """
        This method checks if the current score is in the top 5 record scores.
        If so, it calls the save_record method.
        """

        records = self.read_records()

        # TODO: change length to 5 after testing
        if len(records) < 3:
            self.save_record(records, 'test_user')
            return True
        elif self.score > records[-1]["record"]:
            self.save_record(records, 'test_user')
            return True
        else:
            return False

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

    # testing record storing
    game.score = 370
    # game.check_record()
    print(game.read_records())
    pygame.quit()


# Running the program
if __name__ == '__main__':
    main()
