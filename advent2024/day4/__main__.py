from typing import Literal

from advent2024.coordinate import Direction, Grid, GridCoordinate
from advent2024.utils import input_lines

wordsearch = Grid([list(l) for l in input_lines(4)])


def check_for_string(
    coordinate: GridCoordinate, string: str, direction: Direction
) -> bool:
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
        check_for_string(
            GridCoordinate(x, y, wordsearch), string="XMAS", direction=direction
        )
        for direction in Direction.all_directions()
        for x, y in wordsearch
    )


def check_nearby_char(
    coordinate: GridCoordinate,
    char_to_check: str,
    direction: Direction,
    forwards_or_back: Literal[-1, 1],
):
    return coordinate.translate(direction * forwards_or_back) == char_to_check


def check_sam(coordinate: GridCoordinate, direction: Direction):
    return check_nearby_char(coordinate, "S", direction, -1) and check_nearby_char(
        coordinate, "M", direction, 1
    )


def check_for_x_mas(coordinate: GridCoordinate) -> bool:
    return coordinate == "A" and any(
        check_sam(coordinate, diag)
        for direction in Direction.diagonals()
        if check_sam(coordinate, direction)
        for diag in direction.intersecting_diagonals()
    )


def pt2():
    return sum(check_for_x_mas(GridCoordinate(x, y, wordsearch)) for x, y in wordsearch)


print("pt1", pt1())
print("pt1", pt2())
