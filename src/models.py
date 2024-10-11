from pydantic import BaseModel


class Vec2(BaseModel):
    x: int = 0
    y: int = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def pos(self):
        return (self.x, self.y)
    
    @pos.setter
    def pos(self, new_pos: tuple[int, int]):
        assert isinstance(new_pos.x, int)
        assert isinstance(new_pos.y, int)
        self.x = new_pos.x
        self.y = new_pos.y


class CarpetMove(BaseModel):
    acceleration: Vec2
    activateShield: bool = False
    attack: Vec2
    id: str

class CarperRequest(BaseModel):
    transports: list[CarpetMove]

class CarpetResponse(Vec2):
    anomalyAcceleration: Vec2
    attackCooldownMs: int
    deathCount: int
    health: int
    id: str
    selfAcceleration: int
    shieldCooldownMs: int
    shieldLeftMs: int
    status: str
    velocity: Vec2


class Anomaly(Vec2):
    effectiveRadius: int
    id: str
    radius: int
    strength: int
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

class MoveResponse(BaseModel):
    anomalies: list[Anomaly]
    attackCooldownMs: int
    attackDamage: int
    attackExplosionRadius: int
    attackRange: int
    bounties: list[Bounty]
    enemies: list[Enemy]
    mapSize: Vec2
    maxAccel: int
    maxSpeed: int
    name: str
    points: int
    reviveTimeoutSec: int
    shieldCooldownMs: int
    shieldTimeMs: int
    transportRadius: int
    transports: list[CarpetResponse]
    wantedList: list[Wanted]
