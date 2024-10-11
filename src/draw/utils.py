import pygame
from collections import namedtuple
from pydantic import BaseModel

from .arrow import draw_arrow

Circle = namedtuple("Circle", ["x", "y", "radius", "color"])
Dim = namedtuple("Dimension", ["width", "height"])
Grid = namedtuple("Grid", ["dim", "cells", "circles", "arrows"])
Arrow = namedtuple("Arrow", ["start", "end", "color"])

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


def draw_grid(screen: pygame.Surface, grid: Grid) -> None:
    """
        This function draws the game of life on the given
        pygame.Surface object.
    """
    cell_width = screen.get_width() / grid.dim.width
    cell_height = screen.get_height() / grid.dim.height

    for cell in grid.cells:
        pygame.draw.circle(
            screen,
            color=cell['type'],
            center=(cell['x'] * cell_width, cell['y'] * cell_height),
            radius=5
        )

    for circle in grid.circles:
        pygame.draw.circle(
            screen,
            color=circle.color,
            center=(circle.x * cell_width, circle.y * cell_height),
            radius=float(circle.radius * int(cell_width)),
            width= int(cell_width)
        )

    for arrow in grid.arrows:
        draw_arrow(
            screen,
            start=arrow.start * cell_width,
            end=arrow.end * cell_height,
            color=arrow.color
        )
