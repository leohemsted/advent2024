from advent2024.coordinate import Coordinate, Direction, Grid
from advent2024.utils import input_lines

room = Grid([list(l) for l in input_lines(6, "example")])

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


def plot_route(room: Grid) -> list[tuple[Coordinate, Direction]]:
    tiles_visited: list[tuple[Coordinate, Direction]] = []
    curr_direction = guard_start_direction
    curr_location = guard_start_location

    while room.in_bounds(curr_location):
        tiles_visited.append((curr_location, curr_direction))

        if (one_step_forwards := curr_location.translate(curr_direction)) in obstacles:
            curr_direction = next_dir[curr_direction]
        else:
            curr_location = one_step_forwards
    return tiles_visited


def pt2() -> int:
    tiles_visited = plot_route(room)
    infinite_loops = 0

    def _check_for_overlaps(i: int, tile: Coordinate, direction: Direction) -> bool:
        new_direction = next_dir[direction]
        # for any tile, if i turn right and then extend in a line until
        # i hit edge/obstacle, do i go over a tile that i visited
        # earlier in the path
        while room.in_bounds(tile) and tile not in obstacles:
            # for each bit of the route we've done so far
            # (using range rather than slice because slice makes a copy which seems wasteful)
            for previously_visited_tile, previous_direction in tiles_visited[:i]:
                if (
                    tile == previously_visited_tile
                    and new_direction == previous_direction
                ):
                    return True
            # move one step forward and try again
            tile = tile.translate(new_direction)

        return False

    for i, (tile, direction) in enumerate(tiles_visited):
        if _check_for_overlaps(i, tile, direction):
            infinite_loops += 1
    return infinite_loops


print("pt1", pt1())
# print("pt2", pt2())
print("pt2", pt3())
