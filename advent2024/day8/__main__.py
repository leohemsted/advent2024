import itertools
from collections import defaultdict

from advent2024.coordinate import Coordinate, Grid
from advent2024.utils import input_lines

grid = Grid([list(l) for l in input_lines(8)])


antennae_groups: dict[str, set[Coordinate]] = defaultdict(set)

for x, y in grid:
    if (cell_contents := grid.get(x, y)) != ".":
        antennae_groups[cell_contents].add(Coordinate(x, y))


def get_antinodes() -> set[Coordinate]:
    antinodes = set()
    for antennae in antennae_groups.values():
        for first, second in itertools.permutations(antennae, 2):
            vector = first.diff(second)
            if grid.in_bounds(antinode := (first + vector)):
                antinodes.add(antinode)
    return antinodes


def get_harmonic_antinodes() -> set[Coordinate]:
    antinodes = set()
    for antennae in antennae_groups.values():
        for first, second in itertools.permutations(antennae, 2):
            vector = first.diff(second)
            antinode = first
            while grid.in_bounds(antinode):
                antinodes.add(antinode)
                antinode = antinode + vector

    return antinodes


print("pt1", len(get_antinodes()))
print("pt2", len(get_harmonic_antinodes()))
