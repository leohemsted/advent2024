from collections import defaultdict

from advent2024.coordinate import (
    CARDINAL_DIRECTIONS,
    EAST,
    RIGHT_TURN,
    Coordinate,
    Grid,
)
from advent2024.utils import input_lines

grid = Grid([list(line) for line in input_lines(12, "example1")])


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
    by_row: dict[int, list[Coordinate]] = defaultdict(list)
    by_col: dict[int, list[Coordinate]] = defaultdict(list)

    for c in area:
        by_row[c.y].append(c)
        by_col[c.x].append(c)
    for row in by_row.values():
        row.sort(key=lambda c: c.x)
    for col in by_col.values():
        col.sort(key=lambda c: c.y)

    # find leftmost coordinate in top row of area
    first_coordinate = by_row[min(by_row.keys())][0]

    back_at_start = False
    directions_used = []
    curr_coord = first_coordinate
    direction = first_direction = EAST
    print(area)
    while not back_at_start:
        next_coord = curr_coord + direction
        while next_coord in area:
            print("walking", curr_coord, direction)
            next_coord = next_coord + direction
        # go back one as if we failed while statement, we've just overshot
        curr_coord = next_coord - direction
        print(curr_coord, direction)
        directions_used.append(direction)

        direction = RIGHT_TURN[direction]

        # until we're back at the start and pointing the same way we started
        back_at_start = curr_coord == first_coordinate and direction == first_direction

    print(directions_used)
    return len(directions_used)


def pt2():
    sets = []
    cost = 0
    for x, y in grid:
        coord = Coordinate(x, y)
        if not any(coord in set for set in sets):
            val = grid.get_from_coordinate(coord)
            area = set()
            if val != "C":
                continue
            sets.append(area)
            get_area(coord, val, area)
            perimeter = get_num_sides(area)
            print(val, coord, len(area), "sides", perimeter)
            cost += len(area) * perimeter
    return cost


print("pt1", pt1())
print("pt2", pt2())
