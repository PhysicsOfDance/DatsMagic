import sys
import pygame

from context import Context
from .arrow import draw_arrow
from .const import *
from .grid import *
from .models import *

def draw_loop():
    """
        A drawing routine to be called in a separate thread
    """
    context = Context()

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((DISPLAY_SIDE_SIZE, DISPLAY_SIDE_SIZE))

    while not context.interrupt:
        if pygame.QUIT in [e.type for e in pygame.event.get()]:
            sys.exit(0)

        if not context.carpets:
            continue

        screen.fill(color=Color.BLACK.value)

        font = pygame.font.SysFont('arial', 30)
        text = font.render(context.left_corner_text, True, 'white')
        screen.blit(text, (10, 10))

        carpet = context.carpets[context.current_carpet_index]
        grid = Grid(center=carpet.pos)
        draw_grid(screen, grid)
        pygame.display.flip()

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w]:
            context.feedback.up += 1

        if pressed_keys[pygame.K_s]:
            context.feedback.down += 1

        if pressed_keys[pygame.K_a]:
            context.feedback.left += 1

        if pressed_keys[pygame.K_d]:
            context.feedback.right += 1

        if pressed_keys[pygame.K_1]:
            context.current_carpet_index = 0

        if pressed_keys[pygame.K_2]:
            context.current_carpet_index = 1

        if pressed_keys[pygame.K_3]:
            context.current_carpet_index = 2

        if pressed_keys[pygame.K_4]:
            context.current_carpet_index = 3

        if pressed_keys[pygame.K_5]:
            context.current_carpet_index = 4


def draw_grid(screen: pygame.Surface, grid: Grid) -> None:
    """
        This function draws the game of life on the given
        pygame.Surface object.
    """
    # cell_width = screen.get_width() / grid.dim.width
    # cell_height = screen.get_height() / grid.dim.height

    for cell in grid.cells:
        cell.x *= CELL_WIDTH
        cell.y *= CELL_WIDTH
        if cell.shield != 0:
            pygame.draw.circle(
                screen,
                color=Color.GRAY.value,
                center=(cell.x, cell.y),
                radius=(CELL_RADIUS + (SHIELD_RADIUS - CELL_RADIUS) * cell.shield) * CELL_WIDTH
            )

        pygame.draw.circle(
            screen,
            color=cell.color.value,
            center=(cell.x, cell.y),
            radius=CELL_RADIUS * CELL_WIDTH
        )


    for circle in grid.circles:
        circle.x *= CELL_WIDTH
        circle.y *= CELL_WIDTH
        circle.radius *= CELL_WIDTH
        pygame.draw.circle(
            screen,
            color=circle.color.value,
            center=(circle.x, circle.y),
            radius=float(circle.radius),
            width=0
        )

    for arrow in grid.arrows:
        arrow.start *= CELL_WIDTH
        arrow.end *= CELL_WIDTH
        delta = arrow.start - arrow.end
        delta_len_sqr = delta.x ** 2 + delta.y ** 2
        if delta_len_sqr > MIN_DRAW_LENGTH ** 2:
            draw_arrow(
                screen,
                start=pygame.Vector2(arrow.start.x, arrow.start.y),
                end=pygame.Vector2(arrow.end.x, arrow.end.y),
                color=arrow.color.value
            )
