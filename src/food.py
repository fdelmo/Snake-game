import random


class Food:
    """Food class."""

    def __init__(self, block_size, bounds):
        self.color = (255, 0, 0)
        self.block_size = block_size
        self.bounds = bounds
        self.position = (0, 0)
        self.spawn()

    def draw(self, game, window):
        """Method to draw the food as a rectangle of size size_block
        on the game window."""
        game.draw.rect(
            window, self.color,
            (self.position[0], self.position[1],
             self.block_size, self.block_size)
        )

    def spawn(self):
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
        x = random.randint(0, blocks_x-1)*self.block_size
        y = random.randint(0, blocks_y-1)*self.block_size
        self.position = (x, y)
