import itertools
from dataclasses import dataclass

from advent2024.utils import input_lines

wordsearch = [list(l) for l in input_lines(4)]

y_total = len(wordsearch)
x_total = len(wordsearch[0])


@dataclass
class Coordinate:
    x: int
    y: int


all_directions = [
    Coordinate(x, y) for x, y in itertools.product([-1, 0, 1], [-1, 0, 1])
]


def char_equal(x: int, y: int, char: str) -> bool:
    return in_bounds(x, y) and wordsearch[y][x] == char


def in_bounds(x: int, y: int) -> bool:
    return (0 <= x < x_total) and (0 <= y < y_total)


def check_for_string(x: int, y: int, string: str, direction: Coordinate) -> bool:
    return (
        not string
        or char_equal(x, y, string[0])
        and check_for_string(x + direction.x, y + direction.y, string[1:], direction)
    )


def pt1():
    return sum(
        check_for_string(x, y, string="XMAS", direction=direction)
        for direction in all_directions
        for x in range(x_total)
        for y in range(y_total)
    )


print("pt1", pt1())
