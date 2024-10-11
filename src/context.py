import time
import typing as tp
from datetime import datetime

from api import make_move
from logger import get_logger
from models import *

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

    def update_on_time(self):
        move_resp = make_move(self.moves)

        self.anomalies = move_resp.anomalies
        self.bounties = move_resp.bounties
        self.enemies = move_resp.enemies
        self.carpets = move_resp.transports
        self.wanted = move_resp.wantedList

        # logger.info(self.anomalies)
        # logger.info(self.bounties)
        # logger.info(self.enemies)
        # logger.info(self.carpets)
        # logger.info(self.wanted)
