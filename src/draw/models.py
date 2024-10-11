import pygame
import typing as tp
from pydantic import BaseModel
from enum import Enum

from context import Context
from models import Vec2
from .const import *


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

class Color(Enum):
    BLACK = pygame.Color('black')
    WHITE = pygame.Color('white')
    RED = pygame.Color('red')
    GREEN = pygame.Color('green')
    BLUE = pygame.Color('blue')
    YELLOW = pygame.Color('yellow')
    ORANGE = pygame.Color('orange')

class Cell(Vec2):
    color: Color

class Circle(Vec2):
    radius: float
    color: Color

class Arrow(BaseModel):
    start: Vec2
    end: Vec2
    color: Color

class Dimension(BaseModel):
    width: int
    height: int

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

class Grid:
    def __init__(self, center: Vec2, dim: Dimension = Dimension(width=DIM_SIDE_SIZE, height=DIM_SIDE_SIZE)):
        self.dim: Dimension = dim
        self.center = center
        context = Context()

        self.speed_coef = MAX_SPEED_ARROW_LENGTH / context.maxSpeed
        self.acceleration_coef = MAX_ACCELERATION_ARROW_LENGTH / context.maxAcceleration

        self.cells: list[Cell] = []
        self.circles: list[Circle] = []
        self.arrows: list[Arrow] = []

        self._add_entities(context.carpets, Color.GREEN)
        self._add_entities(context.enemies, Color.RED)
        self._add_entities(context.wanted, Color.YELLOW)
        self._add_entities(context.bounties, Color.BLUE, show_speed=False)
        self._add_entities(context.anomalies, Color.ORANGE, show_speed=False)

        # Draw own acceleration vector
        for carpet in context.carpets:
            maybe_carpet_move = [carpet_move for carpet_move in context.moves if carpet_move.id == carpet.id]
            if maybe_carpet_move:
                local_pos = self._to_local(carpet.pos)
                arrow_end = local_pos + self.acceleration_coef * maybe_carpet_move.pop().acceleration
                self.arrows.append(Arrow(start=local_pos, end=arrow_end, color=Color.WHITE))


    def _add_entities(self, entities: list[tp.Any], color: Color, show_speed: bool = True):
        for entity in entities:
            local_pos = self._to_local(entity.pos)
            if show_speed:
                self.cells.append(Cell(x=local_pos.x, y=local_pos.y, color=color))
                # Draw velocity vector
                arrow_end = local_pos + self.speed_coef * entity.velocity
                self.arrows.append(Arrow(start=local_pos, end=arrow_end, color=color))
            else:
                self.circles.append(Circle(x=local_pos.x, y=local_pos.y, radius=entity.radius, color=color))


    def _to_local(self, pos: Vec2) -> Vec2:
        return pos - self.center + Vec2(x=DIM_SIDE_HALF_SIZE, y=DIM_SIDE_HALF_SIZE)

