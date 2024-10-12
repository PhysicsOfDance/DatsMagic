from models import Carpet, Vec2
from const import *


from simple_pid import PID
import numpy as np

class PidController:
    def __init__(self, carpet: Carpet):
        self.pid_x: PID = PID(P_COEF, I_COEF, D_COEF, 0)
        self.pid_y: PID = PID(P_COEF, I_COEF, D_COEF, 0)
        self.target: Vec2 | None = None
        self.carpet: Carpet = carpet

    def get_acceleration(self) -> Vec2:
        acc_x = self.pid_x(self.carpet.x)
        if acc_x is None:
            acc_x = 0

        acc_y = self.pid_y(self.carpet.y)
        if acc_y is None:
            acc_y = 0

        anomaly = self.carpet.anomalyAcceleration
        acc_x = acc_x / 200
        return Vec2(x=acc_x - anomaly.x, y=acc_y - anomaly.y)


    def get_acceleration_2(self) -> Vec2:
        if self.target is None:
            return Vec2(x=0, y=0)
        dist = Vec2(x=(self.target.x - self.carpet.x), y=(self.target.y - self.carpet.y))
        total = np.sqrt( dist.x** 2 + dist.y ** 2)
        coef = 10 / total
        return Vec2(x=dist.x * coef , y=dist.y * coef)


    def update_target(self, carpet: Carpet):
        from context import Context
        context = Context()
        self.carpet = carpet

        if self.target:
            dist = Vec2(x=(self.target.x - self.carpet.x), y=(self.target.y - self.carpet.y))
            if dist.length < 4:
                self.target = None

        if self.target is None:
            position = np.array([self.carpet.x, self.carpet.y])
            bounties = np.array([[b.x, b.y] for b in context.bounties])

            distances = np.sum((bounties - position) ** 2, axis=1)
            target_bounty = bounties[np.argmin(distances)]
            self.target = Vec2(x=target_bounty[0], y=target_bounty[1])
            self.pid_x = PID(P_COEF, I_COEF, D_COEF, self.target.x)
            self.pid_y = PID(P_COEF, I_COEF, D_COEF, self.target.y)
