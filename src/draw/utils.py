import pygame
from collections import namedtuple
from pydantic import BaseModel

Circle = namedtuple("Circle", ["radius", ])
Dim = namedtuple("Dimension", ["width", "height"])
Grid = namedtuple("Grid", ["dim", "cells", "objects"])

class Feedback(BaseModel):
    up: int
    down: int
    left: int
    right: int

    def flush(self):
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0


def draw_grid(screen: pygame.Surface, grid: Grid, color_dict: dict) -> None:
    """
        This function draws the game of life on the given
        pygame.Surface object.
    """
    cell_width = screen.get_width() / grid.dim.width
    cell_height = screen.get_height() / grid.dim.height
    border_size = 2

    for cell in grid.cells:
        pygame.draw.rect(
            screen,
            color_dict.get(cell['type'], 'black'),
            (
                cell['x'] * cell_width + border_size,
                cell['y'] * cell_height + border_size,
                cell_width - border_size,
                cell_height - border_size,
            ),
        )
