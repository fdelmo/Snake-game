from enum import Enum
from typing import Tuple
import pygame


class Direction(Enum):
    """Class for directions. Directions can be called by
    using commands of the rype 'Direction.DOWN' """
    UP = 0
    DOWN = 2
    RIGHT = 1
    LEFT = 3

    def __sub__(self, other):
        """
        First try works when the player interacts with the game
        via keyboard. The second works when the AI plays the game.
        """
        try:
            result = self.value - other.value
        except:
            result = self.value-other

        return result

    def __add__(self, other_value: int) -> int:
        return self.value + other_value


class Snake:
    """Snake class. The color is hardcoded in the class, all other
    attributes and variables are passed when creating an instance."""

    def __init__(self, block_size: int, bounds: Tuple[int], die_on_edges: bool = False):
        self.block_size = block_size
        self.bounds = bounds
        self.color = (0, 255, 125)
        self.die_on_edges = die_on_edges
        self.spawn()

    def spawn(self) -> None:
        """Resets the snake to the initial state"""
        self.length = 3
        self.direction = Direction.DOWN
        self.body = [
            (10*self.block_size, self.block_size),
            (10*self.block_size, 2*self.block_size),
            (10*self.block_size, 3*self.block_size),
            (10*self.block_size, 4*self.block_size),
            (10*self.block_size, 5*self.block_size),
        ]

    def eat(self) -> None:
        """Method to define the behavior or the snake when it eats a food."""
        self.length += 1

    def check_tail_collision(self) -> None:
        """
        This method checks if the head of the snake is in the same position as
        any other of its body segments and returns True if it is.
        """
        self_collision = False

        for i in range(len(self.body) - 1):
            if self.body[-1] == self.body[i]:
                self_collision = True

        if self.die_on_edges:
            if (self.body[-1][0] >= self.bounds[0]) or (self.body[-1][0] < 0):
                self_collision = True
            elif (self.body[-1][1] >= self.bounds[1]) or (self.body[-1][1] < 0):
                self_collision = True

        return self_collision

    def draw(self, game, window) -> None:
        """Draws Snake in the display using an instance of pygame as 'game'
        and an instance of the surface to be drawn to as ' window' """
        for block in self.body:
            game.draw.rect(
                window, self.color,
                (block[0], block[1], self.block_size, self.block_size))

    def move(self) -> None:
        """
        Checks in what direction the snake looks and 'moves' it on 
        block in that direction by drawing a block in front and removing
        a block from the back of the tail
        """
        curr_head = self.body[-1]
        if self.direction == Direction.DOWN:
            if (curr_head[1]+self.block_size >= self.bounds[1]) & (not self.die_on_edges):
                new_head = (curr_head[0], 0)
            else:
                new_head = (curr_head[0], curr_head[1]+self.block_size)
        elif self.direction == Direction.UP:
            if (curr_head[1]-self.block_size < 0) & (not self.die_on_edges):
                new_head = (curr_head[0], self.bounds[1]-self.block_size)
            else:
                new_head = (curr_head[0], curr_head[1]-self.block_size)
        elif self.direction == Direction.RIGHT:
            if (curr_head[0]+self.block_size >= self.bounds[0]) & (not self.die_on_edges):
                new_head = (0, curr_head[1])
            else:
                new_head = (curr_head[0]+self.block_size, curr_head[1])
        elif self.direction == Direction.LEFT:
            if (curr_head[0]-self.block_size < 0) & (not self.die_on_edges):
                new_head = (self.bounds[0]-self.block_size, curr_head[1])
            else:
                new_head = (curr_head[0]-self.block_size, curr_head[1])

        self.body.append(new_head)

        if self.length < len(self.body):
            self.body.pop(0)

    def steer(self) -> None:
        """This method changes the direction of the snake"""
        keys = pygame.key.get_pressed()
        new_direction = self.direction

        if keys[pygame.K_UP]:
            new_direction = Direction.UP
        elif keys[pygame.K_DOWN]:
            new_direction = Direction.DOWN
        elif keys[pygame.K_RIGHT]:
            new_direction = Direction.RIGHT
        elif keys[pygame.K_LEFT]:
            new_direction = Direction.LEFT

        if abs(self.direction-new_direction) != 2:
            self.direction = new_direction

    def steer_AI(self, new_dir: Direction) -> None:
        """
        This method changes the direction of the snake given the new
        direction as a parameter. This is implemented so that the AI
        agent can play the game.
        """
        if abs(self.direction - new_dir) != 2:
            self.direction = new_dir
