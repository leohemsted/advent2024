import itertools
from collections import defaultdict

from advent2024.coordinate import (
    CARDINAL_DIRECTIONS,
    EAST,
    NORTH,
    SOUTH,
    WEST,
    Coordinate,
    Grid,
)
from advent2024.utils import input_lines

grid = Grid([list(line) for line in input_lines(12)])


def process_area(
    coord: Coordinate,
    val: str,
    area: set[Coordinate],
    perimiter: int,
) -> int:
    area.add(coord)

    new_fences = 0
    for dir in CARDINAL_DIRECTIONS:
        next_coord = coord + dir

        if next_coord not in area:
            if (
                not grid.in_bounds(next_coord)
                or grid.get_from_coordinate(next_coord) != val
            ):
                # add one fence
                new_fences += 1
            else:
                new_fences += process_area(next_coord, val, area, perimiter)

    return new_fences


def pt1():
    sets = []
    cost = 0
    for x, y in grid:
        coord = Coordinate(x, y)
        if not any(coord in set for set in sets):
            area = set()
            sets.append(area)
            val = grid.get_from_coordinate(coord)
            # if val == "I" and coord == Coordinate(2, 7):
            #     breakpoint()
            perimiter = process_area(coord, val, area, 0)
            print(val, coord, len(area), perimiter)
            cost += len(area) * perimiter
    return cost


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


def get_num_sides(area: set[Coordinate]) -> int:
    coords_by_row: dict[int, list[Coordinate]] = defaultdict(list)
    coords_by_col: dict[int, list[Coordinate]] = defaultdict(list)

    # lists of x-indexes of fences above that row index
    fences_by_row: dict[int, list[int]] = defaultdict(list)
    # lists of y-indexes of fences to the left of that col index
    fences_by_col: dict[int, list[int]] = defaultdict(list)

    for c in area:
        coords_by_row[c.y].append(c)
        coords_by_col[c.x].append(c)
        if c + NORTH not in area:
            fences_by_row[c.y].append(c.x)
        if c + SOUTH not in area:
            fences_by_row[c.y + 1].append(c.x)
        if c + WEST not in area:
            fences_by_col[c.x].append(c.y)
        if c + EAST not in area:
            fences_by_col[c.x + 1].append(c.y)

    def _count_axes(fences_dict: dict[int, list[int]]) -> int:
        fence_count = 0
        for fence_list in fences_dict.values():
            fence_count += 1
            for first_fence, next_fence in itertools.pairwise(sorted(fence_list)):
                if next_fence - first_fence != 1:
                    fence_count += 1
        return fence_count

    return _count_axes(fences_by_col) + _count_axes(fences_by_row)


def pt2():
    sets = []
    cost = 0
    for x, y in grid:
        coord = Coordinate(x, y)
        if not any(coord in set for set in sets):
            val = grid.get_from_coordinate(coord)
            area = set()
            sets.append(area)
            get_area(coord, val, area)
            perimeter = get_num_sides(area)
            print(val, coord, len(area), "sides", perimeter)
            cost += len(area) * perimeter
    return cost


print("pt1", pt1())
print("pt2", pt2())
