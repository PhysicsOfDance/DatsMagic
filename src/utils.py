import typing as tp
import functools

class IncorrectDataException(Exception):
    pass


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
