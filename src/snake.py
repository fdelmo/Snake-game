from enum import Enum


class Direction(Enum):
    """Class for directions. Directions can be called by
    using commands of the rype 'Direction.DOWN' """
    UP = 2
    DOWN = 3
    RIGHT = -2
    LEFT = -3

    def __sub__(self, other):
        return self.value - other.value


class Snake:
    """Snake class. The color is hardcoded in the class, all other
    attributes and variables are passed when creating an instance."""

    def __init__(self, block_size, bounds):
        self.block_size = block_size
        self.bounds = bounds
        self.color = (0, 255, 125)
        self.spawn()

    def spawn(self):
        """Resets the snake to the initial state"""
        self.length = 3
        self.direction = Direction.DOWN
        self.body = [(20, 20), (20, 40), (20, 60)]

    def draw(self, game, window):
        """Draws Snake in the display using an instance of pygame as 'game'
        and an instance of the surface to be drawn to as ' window' """
        for block in self.body:
            game.draw.rect(
                window, self.color,
                (block[0], block[1], self.block_size, self.block_size))

    def move(self):
        """
        Checks in what direction the snake looks and 'moves' it on 
        block in that direction by drawing a block in front and removing
        a block from the back of the tail
        """
        curr_head = self.body[-1]
        if self.direction == Direction.DOWN:
            new_head = (curr_head[0], curr_head[1]+self.block_size)
        elif self.direction == Direction.UP:
            new_head = (curr_head[0], curr_head[1]-self.block_size)
        elif self.direction == Direction.RIGHT:
            new_head = (curr_head[0]+self.block_size, curr_head[1])
        elif self.direction == Direction.LEFT:
            new_head = (curr_head[0]-self.block_size, curr_head[1])

        self.body.append(new_head)

        if self.length < len(self.body):
            self.body.pop(0)

    def steer(self, game):
        """This method changes the direction of the snake"""
        keys = game.key.get_pressed()
        new_direction = self.direction

        if keys[game.K_UP]:
            new_direction = Direction.UP
        elif keys[game.K_DOWN]:
            new_direction = Direction.DOWN
        elif keys[game.K_RIGHT]:
            new_direction = Direction.RIGHT
        elif keys[game.K_LEFT]:
            new_direction = Direction.LEFT

        if abs(self.direction-new_direction) != 1:
            self.direction = new_direction
