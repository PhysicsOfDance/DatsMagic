import typing as tp

from pydantic import BaseModel


class Vec2(BaseModel):
    x: float = 0.0
    y: float = 0.0

    def __hash__(self):
        return hash(str(self))
    
    def __add__(self, other):
        if not isinstance(other, Vec2):
            raise ValueError("Operand must be instance of Vec2")
        return Vec2(x=self.x+other.x, y=self.y+other.y)
    
    def __sub__(self, other):
        if not isinstance(other, Vec2):
            raise ValueError("Operand must be instance of Vec2")
        return Vec2(x=self.x-other.x, y=self.y-other.y)
    
    def __mul__(self, scalar):
        if not isinstance(scalar, int):
            raise ValueError("Operand must be a numeric value")
        return Vec2(x=self.x*scalar, y=self.y*scalar)

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
    attack: Vec2 = Vec2()
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
