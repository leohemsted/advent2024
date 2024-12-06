import functools
import itertools
from collections import defaultdict
from dataclasses import dataclass
from typing import Self

from advent2024.utils import input_lines

grid = [list(l) for l in input_lines(6)]
x_max = len(grid[0])
y_max = len(grid)


@dataclass(frozen=True)
class BaseCoord:
    x: int
    y: int


class Coordinate(BaseCoord):

    @functools.cache
    def in_bounds(self) -> bool:
        return (0 <= self.x < x_max) and (0 <= self.y < y_max)

    @functools.cache
    def __add__(self, direction: "Direction") -> Self:
        return type(self)(x=self.x + direction.x, y=self.y + direction.y)


class Direction(BaseCoord):
    pass


NORTH = Direction(0, -1)
SOUTH = Direction(0, 1)
EAST = Direction(1, 0)
WEST = Direction(-1, 0)

next_dir = {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH}

obstacles: set[Coordinate] = set()
guard_start_location: Coordinate
guard_start_direction: Direction = NORTH

for x, y in itertools.product(range(x_max), range(y_max)):
    if (cell_contents := grid[y][x]) == "#":
        obstacles.add(Coordinate(x, y))
    elif cell_contents != ".":
        guard_start_location = Coordinate(x, y)


def plot_route(obstacles: set[Coordinate]) -> set[Coordinate]:
    tiles_visited: dict[Coordinate, set[Direction]] = defaultdict(set)
    curr_direction: Direction = guard_start_direction
    curr_location: Coordinate = guard_start_location

    while curr_location.in_bounds():
        tiles_visited[curr_location].add(curr_direction)
        if (one_step_forwards := curr_location + curr_direction) in obstacles:
            curr_direction = next_dir[curr_direction]
        else:
            curr_location = one_step_forwards

        if curr_direction in tiles_visited[curr_location]:
            return set()

    return set(tiles_visited.keys())


tiles_visited = plot_route(obstacles)

pt1 = len(tiles_visited)
pt2 = sum(bool(not plot_route(obstacles | {tile})) for tile in tiles_visited)


print("pt1", pt1)
print("pt2", pt2)
