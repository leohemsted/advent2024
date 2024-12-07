import functools
import itertools
from typing import Generator

from advent2024.utils import input_tuples_per_line


def parse_input() -> Generator[tuple[int, list[int]]]:
    for raw_result, *raw_inputs in input_tuples_per_line(7):
        result = int(raw_result[:-1])
        inputs = list(map(int, raw_inputs))
        yield result, inputs


tot = 0
for result, inputs in parse_input():
    num_operators = len(inputs) - 1
    permutations_of_operators = list(
        itertools.product([int.__add__, int.__mul__], repeat=num_operators)
    )
    for operators in permutations_of_operators:
        operator_iterator = iter(operators)
        applied_result = functools.reduce(
            (lambda acc, x: next(operator_iterator)(acc, x)),
            inputs,
        )
        if applied_result == result:
            tot += result
            break
print(tot)
