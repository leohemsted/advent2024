import copy
import itertools
from dataclasses import dataclass
from typing import Any, Generator, Self


@dataclass(frozen=True)
class Grid:
    grid: list[list[Any]]

    @property
    def x_total(self) -> int:
        return len(self.grid)

    @property
    def y_total(self) -> int:
        return len(self.grid[0])

    def __iter__(self) -> Generator[tuple[Any, Any]]:
        for x in range(self.x_total):
            for y in range(self.y_total):
                yield x, y

    def get(self, x: int, y: int):
        return self.grid[y][x]

    def in_bounds(self, coordinate: "Coordinate") -> bool:
        return (0 <= coordinate.x < self.x_total) and (0 <= coordinate.y < self.y_total)

    def with_amendment(self, coordinate: "Coordinate", new_val: Any) -> Self:
        new_raw = copy.deepcopy(self.grid)
        new_raw[coordinate.y][coordinate.x] = new_val
        return type(self)(new_raw)


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def translate(self, direction: "Direction") -> Self:
        return type(self)(x=self.x + direction.x, y=self.y + direction.y)


class GridCoordinate(Coordinate):
    grid: Grid

    def __init__(self, x: int, y: int, grid: Grid):
        super().__init__(x, y)
        self.grid = grid

    def in_bounds(self) -> bool:
        return (0 <= self.x < self.grid.x_total) and (0 <= self.y < self.grid.y_total)

    def _cell_equal(self, char: str) -> bool:
        return self.in_bounds() and self.grid.get(self.x, self.y) == char

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return super().__eq__(other)
        else:
            return self._cell_equal(other)

    def translate(self, direction: "Direction") -> Self:
        return type(self)(
            x=self.x + direction.x, y=self.y + direction.y, grid=self.grid
        )


class Direction(Coordinate):
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

    def __repr__(self) -> str:
        str_parts = []
        if self.y == -1:
            str_parts.append("North")
        elif self.y == 1:
            str_parts.append("South")

        if self.x == -1:
            str_parts.append("East")
        elif self.x == 1:
            str_parts.append("West")

        return f"Dir({' '.join(str_parts)})"
