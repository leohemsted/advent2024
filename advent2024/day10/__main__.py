from typing import Generator

from advent2024.coordinate import CARDINAL_DIRECTIONS, Coordinate, Grid
from advent2024.utils import input_lines

grid = Grid([[int(x) for x in line] for line in input_lines(10)])


def get_peaks(coordinate: Coordinate, val: int) -> Generator[Coordinate]:
    if grid.in_bounds(coordinate) and grid.get_from_coordinate(coordinate) == val:
        if val == 9:
            yield coordinate
        else:
            for dir in CARDINAL_DIRECTIONS:
                yield from get_peaks(coordinate + dir, val + 1)


def pt1():
    return sum(
        len(set(get_peaks(Coordinate(x, y), 0))) for x, y in grid if grid.get(x, y) == 0
    )


def pt2():
    return sum(
        len(list(get_peaks(Coordinate(x, y), 0)))
        for x, y in grid
        if grid.get(x, y) == 0
    )


print("pt1", pt1())
print("pt2", pt2())
