import typing as tp

from pydantic import BaseModel


class Vec2(BaseModel):
    x: float = 0.0
    y: float = 0.0

    @property
    def pos(self):
        return (self.x, self.y)
    
    @pos.setter
    def pos(self, new_pos: tuple[int, int]):
        assert isinstance(new_pos[0], int)
        assert isinstance(new_pos[1], int)
        self.x = new_pos.x
        self.y = new_pos.y


class CarpetMove(BaseModel):
    acceleration: Vec2
    activateShield: bool = False
    attack: Vec2
    id: str

class CarpetMoveRequest(BaseModel):
    transports: list[CarpetMove]


class Carpet(Vec2):
    anomalyAcceleration: Vec2
    attackCooldownMs: int
    deathCount: int
    health: int
    id: str
    selfAcceleration: Vec2
    shieldCooldownMs: int
    shieldLeftMs: int
    status: str
    velocity: Vec2


class Anomaly(Vec2):
    effectiveRadius: float
    id: str
    radius: float
    strength: float
    velocity: Vec2


class Bounty(Vec2):
    points: int
    radius: int

class Enemy(Vec2):
    health: int
    killBounty: int
    shieldLeftMs: int
    status: str
    velocity: Vec2

class Wanted(Vec2):
    health: int
    killBounty: int
    shieldLeftMs: int
    status: str
    velocity: Vec2

class CarpetMoveResponse(BaseModel):
    anomalies: list[Anomaly]
    attackCooldownMs: int
    attackDamage: int
    attackExplosionRadius: float
    attackRange: float
    bounties: list[Bounty]
    enemies: list[Enemy]
    errors: tp.Any
    mapSize: Vec2
    maxAccel: float
    maxSpeed: float
    name: str
    points: int
    reviveTimeoutSec: int
    shieldCooldownMs: int
    shieldTimeMs: int
    transportRadius: int
    transports: list[Carpet]
    wantedList: list[Wanted]
