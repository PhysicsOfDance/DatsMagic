from models import EPS, Carpet, Vec2
from const import *


from simple_pid import PID
import numpy as np

class PidController:
    def __init__(self, carpet: Carpet):
        self.pid_x: PID = PID(P_COEF, I_COEF, D_COEF, 0)
        self.pid_y: PID = PID(P_COEF, I_COEF, D_COEF, 0)
        self.target: Vec2 | None = None
        self.previous_dist_length = np.inf
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
        dist = self.target - self.carpet.pos
        total = dist.length
        from context import Context
        context = Context()
        coef = context.maxAcceleration / total
        return coef * dist


    def update_target(self, carpet: Carpet):
        from context import Context
        context = Context()
        self.carpet = carpet

        if self.target:
            dist = Vec2(x=(self.target.x - self.carpet.x), y=(self.target.y - self.carpet.y))
            if dist.length < COLLECTED_BOUNTY_DIST or dist.length > self.previous_dist_length:
                # If we are getting futher from target or collected it, change the target
                self.target = None
                self.previous_dist_length = np.inf
            else:
                # Monitor distance to change behavior if we start getting further
                self.previous_dist_length = dist.length

        if self.target is None:
            position = np.array([self.carpet.x, self.carpet.y])
            bounties = np.array([[b.x, b.y] for b in context.bounties])
            from_position_to_bounty = bounties - position
            from_position_to_bounty_distances_sqr = np.sum((bounties - position) ** 2, axis=1)

            # Remove bounties, that are orthogonal or more to our velocity direction
            carpet_velocity = np.array([self.carpet.velocity.x, self.carpet.velocity.y])
            dot_products = np.matmul(from_position_to_bounty, carpet_velocity)
            cosines = dot_products / ((self.carpet.velocity.length + EPS) * from_position_to_bounty_distances_sqr ** 0.5)
            mask = cosines > 0.3

            if np.any(mask):
                bounties = bounties[mask]
                from_position_to_bounty_distances_sqr = from_position_to_bounty_distances_sqr[mask]
            target_bounty = bounties[np.argmin(from_position_to_bounty_distances_sqr)]

            self.target = Vec2(x=target_bounty[0], y=target_bounty[1])
            self.pid_x = PID(P_COEF, I_COEF, D_COEF, self.target.x)
            self.pid_y = PID(P_COEF, I_COEF, D_COEF, self.target.y)
