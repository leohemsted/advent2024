from advent2024.coordinate import Coordinate, Direction, Grid
from advent2024.utils import input_lines

grid = Grid([[int(x) for x in line] for line in input_lines(10)])


def find_accessible_peaks(coordinate: Coordinate, val: int) -> set[Coordinate]:
    s = set()
    if grid.in_bounds(coordinate) and grid.get_from_coordinate(coordinate) == val:
        if val == 9:
            return {coordinate}
        else:
            next = val + 1
            for dir in [
                Direction(0, -1),
                Direction(0, 1),
                Direction(1, 0),
                Direction(-1, 0),
            ]:
                s |= find_accessible_peaks(coordinate + dir, next)
    return s


def pt1():
    total = 0
    for x, y in grid:
        coord = Coordinate(x, y)
        if grid.get_from_coordinate(coord) == 0:
            total += len(find_accessible_peaks(coord, 0))
    return total


print("pt1", pt1())
# print("pt1", pt2())
