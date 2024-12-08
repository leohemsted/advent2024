import itertools
from collections import defaultdict

from advent2024.coordinate import Coordinate, Grid
from advent2024.utils import input_lines

grid = Grid([list(l) for l in input_lines(8)])


antinodes: set[Coordinate] = set()
antennae_groups: dict[str, set[Coordinate]] = defaultdict(set)

for x, y in grid:
    if (cell_contents := grid.get(x, y)) != ".":
        antennae_groups[cell_contents].add(Coordinate(x, y))

for channel, antennae in antennae_groups.items():
    for first, second in itertools.permutations(antennae, 2):
        vector = first.diff(second)
        antinode = first + vector
        if grid.in_bounds(antinode):
            antinodes.add(antinode)
print(len(antinodes))
