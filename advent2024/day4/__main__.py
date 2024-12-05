import itertools
from dataclasses import dataclass
from typing import Any, Literal, Self

from advent2024.utils import input_lines

wordsearch = [list(l) for l in input_lines(4)]

y_total = len(wordsearch)
x_total = len(wordsearch[0])


@dataclass
class BaseCoord:
    x: int
    y: int


class Coordinate(BaseCoord):
    def in_bounds(self) -> bool:
        return (0 <= self.x < x_total) and (0 <= self.y < y_total)

    def _char_equal(self, char: str) -> bool:
        return self.in_bounds() and wordsearch[self.y][self.x] == char

    def translate(self, direction: "Direction") -> Self:
        return type(self)(x=self.x + direction.x, y=self.y + direction.y)

    def __eq__(self, other: Any) -> Self:
        if isinstance(other, str):
            return self._char_equal(other)
        else:
            return super().__eq__(other)


class Direction(Coordinate):
    def intersecting_diagonals(self) -> list[Self]:
        # exclude any non-direction coordinates
        assert abs(self.x) == 1 and abs(self.y) == 1
        # returns intersecting diagonals
        return [
            type(self)(x=self.x * -1, y=self.y),
            type(self)(x=self.x, y=self.y * -1),
        ]

    def __mul__(self, val: int) -> Self:
        return type(self)(x=self.x * val, y=self.y * val)

    @classmethod
    def all_directions(cls) -> list[Self]:
        return [cls(x, y) for x, y in itertools.product([-1, 0, 1], [-1, 0, 1])]

    @classmethod
    def diagonals(cls) -> list[Self]:
        return [cls(x, y) for x, y in itertools.product([-1, 1], [-1, 1])]


def check_for_string(coordinate: Coordinate, string: str, direction: Direction) -> bool:
    return (
        not string
        or coordinate == string[0]
        and check_for_string(
            coordinate.translate(direction),
            string[1:],
            direction,
        )
    )


def pt1():
    return sum(
        check_for_string(Coordinate(x, y), string="XMAS", direction=direction)
        for direction in Direction.all_directions
        for x in range(x_total)
        for y in range(y_total)
    )


def check_nearby_char(
    coordinate: Coordinate,
    char_to_check: str,
    direction: Direction,
    forwards_or_back: Literal[-1, 1],
):
    return coordinate.translate(direction * forwards_or_back) == char_to_check


def check_sam(coordinate: Coordinate, direction: Direction):
    return check_nearby_char(coordinate, "S", direction, -1) and check_nearby_char(
        coordinate, "M", direction, 1
    )


def check_for_x_mas(coordinate: Coordinate) -> bool:
    return coordinate == "A" and any(
        check_sam(coordinate, diag)
        for direction in Direction.diagonals
        if check_sam(coordinate, direction)
        for diag in direction.intersecting_diagonals()
    )


def pt2():
    return sum(
        check_for_x_mas(Coordinate(x, y))
        for x in range(x_total)
        for y in range(y_total)
    )


print("pt1", pt1())
print("pt1", pt2())
