import json
from datetime import datetime, timedelta

from const import MOCK_IGNORE_ANOMALIES, MOCK_START_STILL
from models import *

class MockServer:
    def __init__(self):
        self.state: CarpetMoveResponse | None = None
        self.last_update_time: datetime = datetime.now()

        mock_filename = "mock_still.json" if MOCK_START_STILL else "mock.json"
        with open(mock_filename) as mock_file:
            init_json = json.load(mock_file)
            self.state = CarpetMoveResponse(**init_json)
            
    def update_on_time(self):
        from context import Context
        context = Context()
        delta: float = (datetime.now() - self.last_update_time).total_seconds()

        # Move self
        for index, carpet in enumerate(self.state.transports):
            total_acceleration = Vec2(x=0, y=0) if MOCK_IGNORE_ANOMALIES else carpet.anomalyAcceleration
            maybe_carpet_move = [carpet_move for carpet_move in context.moves if carpet_move.id == carpet.id]
            if maybe_carpet_move:
                control_acceleration = maybe_carpet_move.pop().acceleration
                if control_acceleration.length > context.maxAcceleration:
                    coef = context.maxAcceleration / control_acceleration.length
                    control_acceleration *= coef
                total_acceleration += control_acceleration

            self.state.transports[index].velocity = carpet.velocity + delta * total_acceleration
            if self.state.transports[index].velocity.length > context.maxSpeed:
                coef = context.maxSpeed / self.state.transports[index].velocity.length
                self.state.transports[index].velocity *= coef

            self.state.transports[index].pos = carpet.pos + delta * carpet.velocity + 0.5 * delta ** 2 * total_acceleration

            # Check if coins were collected
            for bounty in self.state.bounties:
                if (carpet.pos - bounty.pos).length < bounty.radius:
                    print(f"CARPET {index + 1} collected a COIN!")

            # Recompute anomaly acceleration
            carpet.anomalyAcceleration = Vec2(x=0, y=0)
            for anomaly in self.state.anomalies:
                from_carpet_to_anomaly = anomaly.pos - carpet.pos
                if from_carpet_to_anomaly.length > anomaly.radius:
                    coef = anomaly.strength * abs(anomaly.strength) / from_carpet_to_anomaly.sqr_length
                    carpet.anomalyAcceleration += coef * from_carpet_to_anomaly

        # Move enemies
        for index, enemy in enumerate(self.state.enemies):
            self.state.enemies[index].pos = enemy.pos + delta * enemy.velocity

        # Move anomalies
        for index, anomaly in enumerate(self.state.anomalies):
            self.state.anomalies[index].pos = anomaly.pos + delta * anomaly.velocity
