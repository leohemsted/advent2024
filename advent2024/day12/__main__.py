import itertools
from collections import defaultdict
from typing import Literal

from advent2024.coordinate import (
    CARDINAL_DIRECTIONS,
    EAST,
    NORTH,
    SOUTH,
    WEST,
    Coordinate,
    Direction,
    Grid,
)
from advent2024.utils import input_lines

grid = Grid([list(line) for line in input_lines(12)])


def get_area(coord: Coordinate, val: str, area: set[Coordinate]) -> None:
    if coord in area:
        return

    area.add(coord)

    for next_coord in [coord + dir for dir in CARDINAL_DIRECTIONS]:
        if (
            next_coord not in area
            and grid.in_bounds(next_coord)
            and grid.get_from_coordinate(next_coord) == val
        ):
            get_area(next_coord, val, area)


def calc_fences(area: set[Coordinate], part=Literal["pt1", "pt2"]) -> int:
    # each cardinal direction has a dict of axes (either x or y), each of which has
    # a list of fences. we then loop through the list to see what's what
    # we have directions rather than just two x and y, so that outie fences vs
    # innie fences can be separated (eg: example 5)
    fences: defaultdict[Direction, dict[int, list[int]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for c in area:
        for dir in [NORTH, SOUTH]:
            if c + dir not in area:
                fences[dir][c.y].append(c.x)
        for dir in [EAST, WEST]:
            if c + dir not in area:
                fences[dir][c.x].append(c.y)

    def _count_axes_pt1(fences_dict: dict[int, list[int]]) -> int:
        return sum(len(fence_list) for fence_list in fences_dict.values())

    def _count_axes_pt2(fences_dict: dict[int, list[int]]) -> int:
        fence_count = 0
        for fence_list in fences_dict.values():
            # always have at least one fence in a row
            fence_count += 1
            for first_fence, next_fence in itertools.pairwise(sorted(fence_list)):
                if next_fence - first_fence != 1:
                    # if there's a gap, there must be at least one more fence section
                    fence_count += 1
        return fence_count

    fn = _count_axes_pt1 if part == "pt1" else _count_axes_pt2

    return sum(fn(fence_list_dict) for fence_list_dict in fences.values())


sets: list[set[Coordinate]] = []
pt1_cost = 0
pt2_cost = 0
for x, y in grid:
    coord = Coordinate(x, y)
    if not any(coord in set for set in sets):
        val = grid.get_from_coordinate(coord)
        area: set[Coordinate] = set()
        sets.append(area)
        get_area(coord, val, area)
        side_count = calc_fences(area, "pt1")
        fence_count = calc_fences(area, "pt2")
        pt1_cost += len(area) * side_count
        pt2_cost += len(area) * fence_count


print("pt1", pt1_cost)
print("pt2", pt2_cost)
