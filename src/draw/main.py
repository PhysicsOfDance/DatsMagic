from context import Context
from .utils import *

import sys
import time
import threading
import pygame


STARTING_GRID = Grid(
    Dim(50, 50),
    [
        {'x': 1, 'y': 1, 'type': 'blue'},
    ],
    [
        Circle(10, 10, 5, 'green')
    ]
)


def drawing_routine(ctxt: Context):
    """
        A drawing routine to be called in a separate thread
    """

    pygame.init()
    screen = pygame.display.set_mode((600, 600))

    while not ctxt.interrupt:
        if pygame.QUIT in [e.type for e in pygame.event.get()]:
            sys.exit(0)

        grids = ctxt.get_grids()
        if not grids:
            continue
        grid = grids[ctxt.current_carpet]
        screen.fill((0, 0, 0))
        draw_grid(screen, grid)

        pygame.display.flip()

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w]:
            ctxt.feedback.up += 1

        if pressed_keys[pygame.K_s]:
            ctxt.feedback.down += 1

        if pressed_keys[pygame.K_a]:
            ctxt.feedback.left += 1

        if pressed_keys[pygame.K_d]:
            ctxt.feedback.right += 1

        if pressed_keys[pygame.K_1]:
            ctxt.current_carpet = 0

        if pressed_keys[pygame.K_2]:
            ctxt.current_carpet = 1

        if pressed_keys[pygame.K_3]:
            ctxt.current_carpet = 2

        if pressed_keys[pygame.K_4]:
            ctxt.current_carpet = 3

        if pressed_keys[pygame.K_5]:
            ctxt.current_carpet = 4
