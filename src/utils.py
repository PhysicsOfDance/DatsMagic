import typing as tp
import functools

from context import Context
from draw.utils import Circle, Dim, Grid

def turncache(func):
    """
    Декоратор, навешиваем на функции для вычисления кода
    если входные данные такие же, то позволяет не пересчитывать всё
    заново, вместо этого вернуть последнее значение

    ВАЖНО: первым аргументом принимает номер текущего хода

    @turncache
    def func(turn_index: int, ...): ...
    """
    last_turn_index: int = -1
    last_value: tp.Any = None

    @functools.wraps(func)  # to save function docstring
    def modified_function(*args: tp.Any, **kwargs: tp.Any) -> tp.Any:
        nonlocal last_turn_index
        nonlocal last_value

        turn_index = args[0]
        if turn_index == last_turn_index:
            return last_value

        value = func(*args, **kwargs)
        last_turn_index = turn_index
        last_value = value
        return value
    return modified_function


def get_grids(ctxt: Context) -> list[Grid]:
    grids = []
    for center in ctxt.carpets:
        # center is the carpet this grid is centered to
        cells = []
        objects = []
        for carpet in ctxt.carpets:
            cells.append({'x': int(carpet.x - center.x) + 150, 'y': int(carpet.y - center.y) + 150, 'type': 'green'})

        for enemy in ctxt.enemies:
            cells.append({'x': int(enemy.x - center.x) + 150, 'y': int(enemy.y - center.y) + 150, 'type': 'red'})

        for wanted in ctxt.wanted:
            cells.append({'x': int(wanted.x - center.x) + 150, 'y': int(wanted.y - center.y) + 150, 'type': 'yellow'})

        for bounty in ctxt.bounties:
            objects.append(Circle(int(bounty.x - center.x) + 150, int(bounty.y - center.y) + 150, bounty.radius, 'blue'))

        for anomaly in ctxt.anomalies:
            objects.append(Circle(int(anomaly.x - center.x) + 150, int(anomaly.y - center.y) + 150, anomaly.radius, 'orange'))

        grids.append(
            Grid(
                Dim(300, 300),
                cells,
                objects
            )
        )
    return grids
