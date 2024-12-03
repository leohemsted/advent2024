from collections.abc import Iterator
from pathlib import Path


def input_tuples_per_line(day: int, filename: str = "input") -> Iterator[tuple[str]]:
    path = Path.cwd() / "advent2024" / f"day{day}" / filename
    with path.open() as f:
        while line := f.readline():
            yield tuple(line.split())


def input_lines(day: int, filename: str = "input") -> Iterator[str]:
    path = Path.cwd() / "advent2024" / f"day{day}" / filename
    with path.open() as f:
        while line := f.readline():
            yield line


def input_raw(day: int, filename: str = "input") -> str:
    path = Path.cwd() / "advent2024" / f"day{day}" / filename
    with path.open() as f:
        return f.read().strip()
