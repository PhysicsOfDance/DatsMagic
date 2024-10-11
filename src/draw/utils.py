import pygame
from collections import namedtuple
from pydantic import BaseModel

Anomaly = namedtuple("Anomaly", ["x", "y", "radius", "color"])
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

    for cell in grid.cells:
        pygame.draw.rect(
            screen,
            color_dict.get(cell['type'], 'black'),
            (
                cell['x'] * cell_width,
                cell['y'] * cell_height,
                cell_width,
                cell_height,
            ),
        )

    for object in grid.objects:
        pygame.draw.circle(
            screen,
            color=color_dict.get(object.color, 'black'),
            center=(object.x * cell_width, object.y * cell_height),
            radius=float(object.radius * int(cell_width)),
            width= int(cell_width)
        )
