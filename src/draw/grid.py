from models import Carpet
from strategy import attack
from .models import *

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

        # Draw anomaly acceleration vector
        for carpet in context.carpets:
            local_pos = self._to_local(carpet.pos)
            arrow_end = local_pos + self.acceleration_coef * carpet.anomalyAcceleration.clipped(50)
            self.arrows.append(Arrow(start=local_pos, end=arrow_end, color=Color.ORANGE))


    def _add_entities(self, entities: list[tp.Any], color: Color, show_speed: bool = True):
        for entity in entities:
            local_pos = self._to_local(entity.pos)
            attack = None
            if isinstance(entity, Carpet):
                attack = entity.attackCooldownMs / ATTACK_CD
            if show_speed:
                self.cells.append(Cell(x=local_pos.x, y=local_pos.y, color=color, shield=entity.shieldLeftMs / MAX_SHIELD_DURATION, attack=attack))
                # Draw velocity vector
                arrow_end = local_pos + self.speed_coef * entity.velocity
                self.arrows.append(Arrow(start=local_pos, end=arrow_end, color=color))
            else:
                self.circles.append(Circle(x=local_pos.x, y=local_pos.y, radius=entity.radius, color=color))


    def _to_local(self, pos: Vec2) -> Vec2:
        return pos - self.center + Vec2(x=DIM_SIDE_HALF_SIZE, y=DIM_SIDE_HALF_SIZE)
