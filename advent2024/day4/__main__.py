import itertools
from dataclasses import dataclass
from typing import Literal, Self

from advent2024.utils import input_lines

wordsearch = [list(l) for l in input_lines(4)]

y_total = len(wordsearch)
x_total = len(wordsearch[0])


@dataclass
class Coordinate:
    x: int
    y: int

    def intersecting_diagonals(self) -> list[Self]:
        # exclude any non-direction coordinates
        assert abs(self.x) == 1 and abs(self.y) == 1
        # returns intersecting diagonals
        return [
            type(self)(x=self.x * -1, y=self.y),
            type(self)(x=self.x, y=self.y * -1),
        ]


all_directions = [
    Coordinate(x, y) for x, y in itertools.product([-1, 0, 1], [-1, 0, 1])
]

diagonals = [Coordinate(x, y) for x, y in itertools.product([-1, 1], [-1, 1])]


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


def check_nearby_char(
    x: int,
    y: int,
    char_to_check: str,
    direction: Coordinate,
    forwards_or_back: Literal[-1, 1],
):
    return char_equal(
        x + (forwards_or_back * direction.x),
        y + (forwards_or_back * direction.y),
        char_to_check,
    )


def check_sam(x, y, direction):
    return check_nearby_char(x, y, "S", direction, -1) and check_nearby_char(
        x, y, "M", direction, 1
    )


def check_for_x_mas(x, y) -> bool:
    if char_equal(x, y, "A"):
        for direction in diagonals:
            if check_sam(x, y, direction):
                for diag in direction.intersecting_diagonals():
                    if check_sam(x, y, diag):
                        return True
    return False


def pt2():
    return sum(check_for_x_mas(x, y) for x in range(x_total) for y in range(y_total))


print("pt1", pt1())
print("pt1", pt2())
