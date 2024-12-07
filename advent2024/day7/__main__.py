import functools
import itertools
from typing import Callable, Iterable

from advent2024.utils import input_tuples_per_line

rows = [
    (int(raw_result[:-1]), list(map(int, raw_inputs)))
    for raw_result, *raw_inputs in input_tuples_per_line(7)
]


def check_validity(
    result: int, inputs: list[int], operators: Iterable[Callable[[int, int], int]]
):
    return any(
        functools.reduce((lambda acc, x: next(op_iter)(acc, x)), inputs) == result
        for op_iter in map(iter, itertools.product(operators, repeat=len(inputs) - 1))
    )


pt1 = sum(
    result
    for result, inputs in rows
    if check_validity(result, inputs, [int.__add__, int.__mul__])
)


print("pt1", pt1)
