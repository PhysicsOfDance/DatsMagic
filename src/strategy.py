from models import *
from context import Context
import numpy as np
from const import UPDATE_TIME

# def __div__(self, scalar):
#         if not isinstance(scalar, int) and not isinstance(scalar, float):
#             raise ValueError("Operand must be a numeric value")
#         if scalar == 0:
#             raise ValueError("Cannot divide by zero value")
#         return Vec2(x=self.x/scalar, y=self.y/scalar)
        
# def __truediv__(self, scalar):
#     if not isinstance(scalar, int) and not isinstance(scalar, float):
#         raise ValueError("Operand must be a numeric value")
#     if self.x == 0 or self.y == 0:
#         raise ValueError("Cannot divide by zero value")
#     return Vec2(x=scalar/self.x, y=scalar/self.y)


def sign(x: float):
    if x == 0:
        return 1
    return x/abs(x)


def vec_len(vec: Vec2):
    return (vec.x**2 + vec.y**2)**0.5


def dist(obj1: Vec2, obj2: Vec2):
    return vec_len(obj1 - obj2)


def scalar_mul(obj1: Vec2, obj2: Vec2):
    return obj1.x*obj2.x + obj1.y*obj2.y


def calculate_dists(obj: Vec2, objects: list[Vec2]):
    return [dist(obj, obj_) for obj_ in objects]


def n_closest_with_dist(objects: list[Vec2], dists: list[float], number: int):
    dist_obj_list = list(sorted(zip(dists, objects)))
    if number == 1:
        return dist_obj_list[0]
    return dist_obj_list[:number]


def acceleration(carpet: Carpet, bounty: Vec2):
    context = Context()
    R = bounty - carpet    

    # S minimal
    v_end = R / vec_len(R) * context.maxSpeed * 0.1
    acc_temp = Vec2(
        x = (v_end.x**2 - carpet.velocity.x**2)/(2 * R.x),
        y = (v_end.y**2 - carpet.velocity.y**2)/(2 * R.y)
    ) # - carpet.anomalyAcceleration
    # acc_temp = (v_end**2 - vec_len(carpet.velocity)**2)/(2 * (bounty - carpet)) - carpet.anomalyAcceleration
    # acc_module = np.clip(abs(vec_len(acc_temp)), 0, context.maxAcceleration)
    return Vec2(
        x = context.maxAcceleration * acc_temp.x / vec_len(acc_temp),
        y = context.maxAcceleration * acc_temp.y / vec_len(acc_temp)
        )

    # return Vec2(
    #     x = -1,
    #     y = -1
    #     )

def activate_shield(carpet: Carpet, closest_dist_enemy: tuple[float, Enemy]):
    if carpet.shieldLeftMs == 0 and carpet.shieldCooldownMs <= UPDATE_TIME and closest_dist_enemy[0] <= 230:
        return True
    return False


def attack(carpet: Carpet, n_closest_dist_enemy: list[tuple[float, Enemy]]):
    if carpet.attackCooldownMs <= UPDATE_TIME:
        # kill if one-shot
        for dist_, enemy in n_closest_dist_enemy:
            if enemy.health <= 30 and dist_ <= 220:
                enemy_next_pos = enemy + enemy.velocity*UPDATE_TIME
                carpet_next_pos = carpet + carpet.velocity*UPDATE_TIME
                if dist(enemy_next_pos, carpet_next_pos) <= 220:
                    return carpet_next_pos + (enemy_next_pos - carpet_next_pos)/vec_len(enemy - carpet)*199
        # attack closest
        if n_closest_dist_enemy[0][0] <= 200:
            return n_closest_dist_enemy[0][1].pos

def carpet_strategy(carpet: Carpet):
    context = Context()
    # enemies_dists = calculate_dists(carpet, context.enemies)
    # n_closest_dist_enemy = n_closest_with_dist(context.enemies, enemies_dists,  2)
    bounties_dists = calculate_dists(carpet, context.bounties)
    closest_bounty = n_closest_with_dist(context.bounties, bounties_dists,  1)[1]

    
    context.moves.append(
        CarpetMove(
            acceleration = acceleration(carpet, closest_bounty),
            # activateShield = activate_shield(carpet, n_closest_dist_enemy[0]),
            # attack = attack(carpet, n_closest_dist_enemy),
            id = carpet.id
        )
    )


