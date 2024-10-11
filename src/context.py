import time
import pygame
import typing as tp
from datetime import datetime

from api import make_move
from const import *
from draw.utils import Circle, Dim, Grid, Arrow
from logger import get_logger
from models import *
from utils import IncorrectDataException

logger = get_logger("CONTEXT")

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Context(metaclass=Singleton):
    def __init__(self):
        # From response
        self.anomalies: list[Anomaly] = []
        self.bounties: list[Bounty] = []
        self.enemies: list[Enemy] = []
        self.carpets: list[Carpet] = []
        self.wanted: list[Wanted] = []
        # To make move
        self.moves: list[CarpetMove] = []
        self.feedback: Feedback = Feedback()
        self.interrupt: bool = False
        self.current_carpet: int = 0
        self.maxSpeed: float = 0

    def update_on_time(self):
        try:
            move_resp = make_move(self.moves)

            self.anomalies = move_resp.anomalies
            self.bounties = move_resp.bounties
            self.enemies = move_resp.enemies
            self.carpets = move_resp.transports
            self.wanted = move_resp.wantedList
            self.maxSpeed = move_resp.maxSpeed

        except IncorrectDataException as e:
            print(f"Incorrect data found: {e}")

        # logger.info(self.anomalies)
        # logger.info(self.bounties)
        # logger.info(self.enemies)
        # logger.info(self.carpets)
        # logger.info(self.wanted)

    def get_grids(self) -> list[Grid]:
        grids = []
        for center in self.carpets:
            # center is the carpet this grid is centered to
            cells = []
            circles = []
            arrows = []

            for carpet in self.carpets:
                cells.append({'x': int(carpet.x - center.x) + 150, 'y': int(carpet.y - center.y) + 150, 'type': 'green'})
                coef = MAX_ARROW_LENGTH / self.maxSpeed
                arrow_start = pygame.Vector2(int(carpet.x - center.x) + 150, int(carpet.y - center.y) + 150)
                arrow_end = pygame.Vector2(arrow_start.x + carpet.velocity.x * coef, arrow_start.y + carpet.velocity.y * coef)
                arrows.append(
                    Arrow(
                        start=arrow_start,
                        end=arrow_end,
                        color='green'
                    )
                )

            for enemy in self.enemies:
                cells.append({'x': int(enemy.x - center.x) + 150, 'y': int(enemy.y - center.y) + 150, 'type': 'red'})
                coef = MAX_ARROW_LENGTH / self.maxSpeed
                arrow_start = pygame.Vector2(int(enemy.x - center.x) + 150, int(enemy.y - center.y) + 150)
                arrow_end = pygame.Vector2(arrow_start.x + enemy.velocity.x * coef, arrow_start.y + enemy.velocity.y * coef)
                arrows.append(
                    Arrow(
                        start=arrow_start,
                        end=arrow_end,
                        color='red'
                    )
                )

            for wanted in self.wanted:
                cells.append({'x': int(wanted.x - center.x) + 150, 'y': int(wanted.y - center.y) + 150, 'type': 'yellow'})
                coef = MAX_ARROW_LENGTH / self.maxSpeed
                arrow_start = pygame.Vector2(int(wanted.x - center.x) + 150, int(wanted.y - center.y) + 150)
                arrow_end = pygame.Vector2(arrow_start.x + wanted.velocity.x * coef, arrow_start.y + wanted.velocity.y * coef)
                arrows.append(
                    Arrow(
                        start=arrow_start,
                        end=arrow_end,
                        color='yellow'
                    )
                )

            for bounty in self.bounties:
                circles.append(Circle(int(bounty.x - center.x) + 150, int(bounty.y - center.y) + 150, bounty.radius, 'blue'))

            for anomaly in self.anomalies:
                circles.append(Circle(int(anomaly.x - center.x) + 150, int(anomaly.y - center.y) + 150, anomaly.radius, 'orange'))

            grids.append(
                Grid(
                    Dim(300, 300),
                    cells,
                    circles,
                    arrows
                )
            )
        return grids
