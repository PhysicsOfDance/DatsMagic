from .utils import *

import sys
import time
import threading
import pygame

COLOR_MAP = {0: 'green', 1: 'blue', 2: 'yellow', 3: 'red'}

STARTING_GRID = Grid(
    Dim(50, 50),
    [
        {'x': 1, 'y': 1, 'type': 0},
    ],
    [
        Anomaly(10, 10, 5, 1)
    ]
)


def updating_routine(grid: Grid, feedback: Feedback):
    """
        Just an example
    """
    while True:
        if pygame.QUIT in [e.type for e in pygame.event.get()]:  # should be keyboard interrupt here instead
            sys.exit(0)

        # feedback is accumulated during these calculations
        for cell in grid.cells:
            cell.update({'x': (cell['x'] + feedback.right - feedback.left) % grid.dim.width ,
                'y': (cell['y'] + feedback.down - feedback.up) % grid.dim.height})

        feedback.flush() # flushing it afterwards




def drawing_routine(grid: Grid, color_map: dict, hook: Feedback):
    """
        A drawing routine to be called in a separate thread
    """

    pygame.init()
    screen = pygame.display.set_mode((600, 600))

    while True:
        if pygame.QUIT in [e.type for e in pygame.event.get()]:
            sys.exit(0)

        screen.fill((0, 0, 0))
        draw_grid(screen, grid, color_map)

        pygame.display.flip()
        time.sleep(0.1)

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w]:
            hook.up += 1

        if pressed_keys[pygame.K_s]:
            hook.down += 1

        if pressed_keys[pygame.K_a]:
            hook.left += 1

        if pressed_keys[pygame.K_d]:
            hook.right += 1



if __name__ == "__main__":
    grid = STARTING_GRID

    hook = Feedback(up=0, down=0, left=0, right=0)
    thread = threading.Thread(target=drawing_routine, args=[grid, COLOR_MAP, hook])
    thread.start()
    updating_routine(grid, hook)
