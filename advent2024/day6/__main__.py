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


def print_room(
    room: Grid,
    obstacles: set[Coordinate],
    tiles_visited: set[tuple[Coordinate, Direction]] = set(),
    notable_obstacle: Coordinate = Coordinate(-1, -1),
):
    visits = {c for c, d in tiles_visited}
    for y in range(len(room.grid[0])):
        for x in range(len(room.grid)):
            to_print = "."
            if Coordinate(x, y) in obstacles:
                to_print = "#"
            if Coordinate(x, y) in visits:
                to_print = "/"
            if Coordinate(x, y) == guard_start_location:
                to_print = "^"
            if Coordinate(x, y) == notable_obstacle:
                to_print = "O"
            print(to_print, end="")
        print("")
    print(notable_obstacle)


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

    # print_room(
    #     room=room,
    #     obstacles=obstacles,
    #     tiles_visited={(x, Direction(0, 0)) for x in tiles_visited},
    #     notable_obstacle=curr_location,
    # )

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


def detect_infinite_loop(
    room: Grid, obstacles: set[Coordinate], notable: Coordinate
) -> bool:
    curr_direction = guard_start_direction
    curr_location = guard_start_location

    tiles_visited: set[tuple[Coordinate, Direction]] = set()

    while room.in_bounds(curr_location):
        tiles_visited.add((curr_location, curr_direction))

        if (one_step_forwards := curr_location.translate(curr_direction)) in obstacles:
            curr_direction = next_dir[curr_direction]
        else:
            curr_location = one_step_forwards

        if (curr_location, curr_direction) in tiles_visited:
            # print_room(room, obstacles, tiles_visited, notable_obstacle=notable)
            return True
    return False


def pt2() -> int:
    tiles_visited = plot_route(room)
    extra_obstacles: set[Coordinate] = set()

    for tile, _ in tiles_visited:
        if tile in extra_obstacles or tile == guard_start_location:
            continue
        modified_obstacles = obstacles | {tile}
        if detect_infinite_loop(room, modified_obstacles, tile):
            extra_obstacles.add(tile)

    return len(extra_obstacles)


print("pt1", pt1())
print("pt2", pt2())
