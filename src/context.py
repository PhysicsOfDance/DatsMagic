import time
import pygame
import typing as tp
from datetime import datetime

from const import *
from logger import get_logger
from mock_server import MockServer
from models import *
from utils import IncorrectDataException
from pid import PidController

logger = get_logger("CONTEXT")

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Context(metaclass=Singleton):
    def __init__(self):
        # Mock server
        self.mock_server = MockServer()
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
        self.maxSpeed: float = 1.0
        self.maxAcceleration: float = 1.0
        # Private variables
        self.__current_carpet_index: int = 0
        self.__left_corner_text: str = str(self.__current_carpet_index + 1)
        if USE_MOCK:
            self.__left_corner_text += " MOCK Server"

        self.pids: list[PidController] = []

    ####################################################################

    @property
    def current_carpet_index(self) -> int:
        return self.__current_carpet_index

    @property
    def left_corner_text(self) -> str:
        return self.__left_corner_text

    @current_carpet_index.setter
    def current_carpet_index(self, new_index: int) -> None:
        self.__current_carpet_index = new_index
        self.__left_corner_text = str(self.__current_carpet_index + 1)
        if USE_MOCK:
            self.__left_corner_text += " MOCK Server"

    ####################################################################

    def update_on_time(self):
        try:
            from api import make_move
            move_resp = make_move(self.moves)

            self.anomalies = move_resp.anomalies
            self.bounties = move_resp.bounties
            self.enemies = move_resp.enemies
            self.carpets = move_resp.transports
            self.wanted = move_resp.wantedList
            self.maxSpeed = move_resp.maxSpeed

        except IncorrectDataException as e:
            print(f"Incorrect data found: {e}")
