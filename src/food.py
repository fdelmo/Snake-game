import random
from snake import Snake
from typing import Tuple


class Food:
    """Food class."""

    def __init__(self, block_size: int, bounds: Tuple[int], snake: Snake):
        self.color = (255, 0, 0)
        self.block_size = block_size
        self.bounds = bounds
        self.position = (0, 0)
        self.spawn(snake)

    def draw(self, game, window) -> None:
        """Method to draw the food as a rectangle of size size_block
        on the game window."""
        game.draw.rect(
            window, self.color,
            (self.position[0], self.position[1],
             self.block_size, self.block_size)
        )

    def spawn(self, snake: Snake) -> None:
        """
        Method to spawn the Food in a random position in the screen.
        blocks_x and blocks_y count how many numbers of block fit in
        the screen. Then we update the position of the Food to a random
        (x,y) coordinate chosen from all the possible coordinated that
        align with the blocks in the screen.
        """
        blocks_x = self.bounds[0]/self.block_size
        blocks_y = self.bounds[1]/self.block_size
        # the -1 is to compensate that the first pixel is 0 and not 1

        # spawn a new food checking that the posiition does not overlap with the snake
        ok = False
        while not ok:
            x = random.randint(0, blocks_x-1)*self.block_size
            y = random.randint(0, blocks_y-1)*self.block_size
            if (x, y) not in snake.body:
                self.position = (x, y)
                ok = True
            #self.position = (x, y)
