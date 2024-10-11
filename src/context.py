import time
import typing as tp
from datetime import datetime

from models import *

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
 

class Context(metaclass=Singleton):
    def __init__(self):
        self.dynamic_smth: tp.Any | None = None 

        # No need to update static objects
        self.static_smth: tp.Any | None = datetime.now() 

    def update(self):
        self.dynamic_smth = datetime.now()
