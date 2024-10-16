import typing as tp
from pydantic import BaseModel

EPS = 1e-3

class Feedback(BaseModel):
    up: int = 0
    down: int = 0
    left: int = 0
    right: int = 0

    def flush(self):
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0


class IVec2(BaseModel):
    x: int
    y: int


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
        if not isinstance(scalar, int) and not isinstance(scalar, float):
            raise ValueError("Operand must be a numeric value")
        return Vec2(x=self.x*scalar, y=self.y*scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __div__(self, scalar):
            if not isinstance(scalar, int) and not isinstance(scalar, float):
                raise ValueError("Operand must be a numeric value")
            if scalar == 0:
                raise ValueError("Cannot divide by zero value")
            return Vec2(x=self.x/scalar, y=self.y/scalar)
            
    def __truediv__(self, scalar):
        if not isinstance(scalar, int) and not isinstance(scalar, float):
            raise ValueError("Operand must be a numeric value")
        if self.x == 0 or self.y == 0:
            raise ValueError("Cannot divide by zero value")
        return Vec2(x=scalar/self.x, y=scalar/self.y)
    
    def __div__(self, scalar):
        if not isinstance(scalar, int) and not isinstance(scalar, float):
            raise ValueError("Operand must be a numeric value")
        return Vec2(x=self.x/scalar, y=self.y/scalar)

    @property
    def length(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    @property
    def sqr_length(self) -> float:
        return self.x ** 2 + self.y ** 2

    def clipped(self, max_value: float) -> "Vec2":
        if self.x < EPS and self.y < EPS:
            return Vec2(x=0, y=0)
        if self.length > max_value:
            coef = max_value / self.length
            return coef * self
        return self
    
    @property
    def as_int(self) -> IVec2:
        return IVec2(x=int(self.x), y=int(self.y))

    @property
    def pos(self) -> "Vec2":
        return Vec2(**self.model_dump())

    @pos.setter
    def pos(self, new_pos: "Vec2") -> None:
        self.x = new_pos.x
        self.y = new_pos.y


class CarpetMove(BaseModel):
    acceleration: Vec2
    activateShield: bool = False
    attack: IVec2 | None = None
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
