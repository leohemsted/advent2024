from advent2024.coordinate import Coordinate, Direction, Grid
from advent2024.utils import input_lines

room = Grid([list(l) for l in input_lines(6)])

NORTH = Direction(0, -1)
SOUTH = Direction(0, 1)
EAST = Direction(1, 0)
WEST = Direction(-1, 0)

next_dir = {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH}

obstacles: set[Coordinate] = set()
guard_start_location: Coordinate
guard_start_direction: Direction = NORTH

for x, y in room:
    if (cell_contents := room.get(x, y)) == "#":
        obstacles.add(Coordinate(x, y))
    elif cell_contents != ".":
        guard_start_location = Coordinate(x, y)
        if cell_contents == "^":
            guard_start_direction = NORTH
        elif cell_contents == "v":
            guard_start_direction = SOUTH
        elif cell_contents == "<":
            guard_start_direction = EAST
        elif cell_contents == ">":
            guard_start_direction = WEST
        else:
            raise ValueError(f"unrecognised cell {cell_contents}")


def pt1() -> int:
    tiles_visited = set()
    curr_direction: Direction = guard_start_direction
    curr_location: Coordinate = guard_start_location

    while room.in_bounds(curr_location):
        tiles_visited.add(curr_location)
        if (one_step_forwards := curr_location.translate(curr_direction)) in obstacles:
            curr_direction = next_dir[curr_direction]
        else:
            curr_location = one_step_forwards

    return len(tiles_visited)


print("pt1", pt1())
