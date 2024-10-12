from models import Carpet, Vec2
from const import *


from simple_pid import PID
import numpy as np

class PidController:
    def __init__(self, carpet: Carpet):
        self.pid_x: PID = PID(P_COEF, I_COEF, D_COEF, 0)
        self.pid_y: PID = PID(P_COEF, I_COEF, D_COEF, 0)
        self.target: Vec2 = Vec2(x=0, y=0)
        self.carpet: Carpet = carpet

    def get_acceleration(self) -> Vec2:
        acc_x = self.pid_x(self.carpet.x)
        if acc_x is None:
            acc_x = 0

        acc_y = self.pid_y(self.carpet.y)
        if acc_y is None:
            acc_y = 0

        anomaly = self.carpet.anomalyAcceleration
        print(Vec2(x=acc_x - anomaly.x, y=acc_y - anomaly.y))
        return Vec2(x=acc_x - anomaly.x, y=acc_y - anomaly.y)

    def update_target(self, carpet: Carpet):
        from context import Context
        context = Context()
        self.carpet = carpet
        position = np.array([self.carpet.x, self.carpet.y])
        bounties = np.array([[b.x, b.y] for b in context.bounties])

        distances = np.sum((bounties - position) ** 2, axis=1)
        target_bounty = bounties[np.argmin(distances)]
        target = Vec2(x=target_bounty[0], y=target_bounty[1])

        if target != self.target:
            self.target = target
            self.pid_x = PID(P_COEF, I_COEF, D_COEF, target.x)
            self.pid_y = PID(P_COEF, I_COEF, D_COEF, target.y)
