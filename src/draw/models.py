import pygame
import typing as tp
from pydantic import BaseModel
from enum import Enum

from context import Context
from models import Vec2
from .const import *


class Color(Enum):
    BLACK = pygame.Color('black')
    WHITE = pygame.Color('white')
    RED = pygame.Color('red')
    GREEN = pygame.Color('green')
    BLUE = pygame.Color('blue')
    YELLOW = pygame.Color('yellow')
    ORANGE = pygame.Color('orange')
    GRAY = pygame.Color('gray')

class Cell(Vec2):
    color: Color
    shield: float
    attack: float | None

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
