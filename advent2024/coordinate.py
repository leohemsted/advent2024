import itertools
from dataclasses import dataclass
from typing import Any, Generator, Self


class Grid:
    grid: list[list[Any]]

    x_total: int
    y_total: int

    index = (0, 0)

    def __init__(self, grid: list[list[Any]]):
        self.grid = grid
        self.y_total = len(self.grid)
        self.x_total = len(self.grid[0])

    def __iter__(self) -> Generator[tuple[Any, Any]]:
        for x in range(self.x_total):
            for y in range(self.y_total):
                yield x, y

    def __getitem__(self, index: int) -> list[Any]:
        return self.grid[index]


@dataclass
class BaseCoord:
    x: int
    y: int

    def translate(self, direction: "Direction") -> Self:
        return type(self)(x=self.x + direction.x, y=self.y + direction.y)


class Coordinate(BaseCoord):
    grid: Grid

    def __init__(self, x: int, y: int, grid: Grid):
        super().__init__(x, y)
        self.grid = grid

    def in_bounds(self) -> bool:
        return (0 <= self.x < self.grid.x_total) and (0 <= self.y < self.grid.y_total)

    def _cell_equal(self, char: str) -> bool:
        return self.in_bounds() and self.grid[self.y][self.x] == char

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Coordinate):
            return super().__eq__(other)
        else:
            return self._cell_equal(other)


class Direction(BaseCoord):
    def intersecting_diagonals(self) -> list[Self]:
        # exclude any non-direction coordinates
        assert abs(self.x) == 1 and abs(self.y) == 1
        # returns intersecting diagonals
        return [
            type(self)(x=self.x * -1, y=self.y),
            type(self)(x=self.x, y=self.y * -1),
        ]

    def __mul__(self, val: int) -> Self:
        return type(self)(x=self.x * val, y=self.y * val)

    @classmethod
    def all_directions(cls) -> list[Self]:
        return [cls(x, y) for x, y in itertools.product([-1, 0, 1], [-1, 0, 1])]

    @classmethod
    def diagonals(cls) -> list[Self]:
        return [cls(x, y) for x, y in itertools.product([-1, 1], [-1, 1])]
