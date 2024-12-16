from advent2024.coordinate import CARDINAL_DIRECTIONS, Coordinate, Grid
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


print("pt1", pt1())
# A region of I plants with price 14 * 22 = 308.


# I Coordinate(x=1, y=7) 13 22
# I Coordinate(x=2, y=7) 14 22
