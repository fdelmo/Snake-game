from doctest import ELLIPSIS_MARKER
import pygame
import pickle
from datetime import date
from pygame.constants import CONTROLLER_BUTTON_MAX
from snake import *
from food import Food
from typing import List, Dict
import numpy as np


#global variables
# BOUNDS = (500, 500)
BOUNDS = (375, 375)
BLOCK_SIZE = 25


class Game:
    """Game class. Game logic and variables are self contained in the object"""

    def __init__(self, max_fps: int = 11, die_on_edges=False, caption: str = "PySnake") -> None:
        # initialization of pygame and window
        pygame.init()
        self.window = pygame.display.set_mode(BOUNDS)
        pygame.display.set_caption(caption)
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()

        # game variables
        self.score = 0
        self.max_fps = max_fps
        self.score_font = pygame.font.Font('freesansbold.ttf', 16)
        self.game_over = False

        # creating of an instance of each object needed
        self.snake = Snake(BLOCK_SIZE, BOUNDS, die_on_edges=die_on_edges)
        self.food = Food(BLOCK_SIZE, BOUNDS, self.snake)

    def print_score(self, pos_x: int, pos_y: int) -> None:
        """
        This method is to  be called in the later method 'draw'. This one takes
        responsability of rendering the score in the screen on each frame.
        """
        score_render = self.score_font.render(
            f'Score: {self.score}', True, (255, 97, 3))

        self.window.blit(score_render, (pos_x, pos_y))

    def read_records(self) -> List[Dict]:
        """
        Method to read historic records of the game from disk. Returns a list
        with dictionaries with info of the top 5 records.
        """
        try:
            with open('records.pck', 'rb') as handle:
                records = pickle.load(handle)

        except FileNotFoundError:
            # TODO: Maybe change this to dict?
            records = []
            print('Empty records file created!')

        return records

    def save_record(self, records: List[Dict], user: str) -> None:
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

        if len(records) > 5:
            records.pop()  # ensure that there are only 5 top records

        # save the records to disk
        with open('records.pck', 'wb') as handle:
            pickle.dump(records, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def check_record(self, user: str = 'Test_user') -> bool:
        """
        This method checks if the current score is in the top 5 record scores.
        If so, it calls the save_record method.
        """

        records = self.read_records()

        if len(records) < 5:
            self.save_record(records, user)
            return True
        elif self.score > records[-1]["record"]:
            self.save_record(records, user)
            return True
        else:
            return False

    def events(self) -> bool:
        """Quits the game if the game need to be stopped"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def check_food(self) -> None:
        """
        This methid checks if the head of the snake is in the position of the
        food. If True, then the snake eats the food and the food respawns.
        Then the score of the game increases by 10.
        """
        if self.snake.body[-1] == self.food.position:
            self.snake.eat()
            self.food.spawn(self.snake)
            self.score += 1
            self.reward = 10

    def evolve(self) -> None:
        """
        This method evolves the state of the game by moving the snake
        and creating new food if the last was eaten. 
        It checks if the game is over and returns the status
        """
        self.snake.steer()
        self.snake.move()
        self.check_food()
        self.game_over = self.snake.check_tail_collision()

    def draw(self) -> None:
        """
        This method draws all elements to the screen. Has to be run every 
        frame and only after all events and game logics have been checked
        """
        self.window.fill((0, 0, 0))

        # draw all objects in screen
        self.snake.draw(pygame, self.window)
        self.food.draw(pygame, self.window)

        # draw score
        self.print_score(pos_x=BOUNDS[1]-100, pos_y=10)

        pygame.display.flip()

    def play_step(self) -> None:
        """
        Step of the game's main loop.
        """
        # pygame.time.delay(self.time)
        self.clock.tick(self.max_fps)
        self.events()
        self.evolve()
        self.draw()


def main():
    """Main function"""
    game = Game(max_fps=12)

    while not game.game_over:
        game.play_step()

    game.check_record()

    print(game.read_records())
    pygame.quit()


# Running the program
if __name__ == '__main__':
    main()
