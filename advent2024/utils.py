from collections.abc import Iterator
from pathlib import Path
from typing import Any


def open_input(day: int, filename: str = "input") -> Iterator[tuple[Any], None, None]:
    path = Path.cwd() / "advent2024" / f"day{day}" / filename
    with path.open() as f:
        while line := f.readline():
            yield tuple(line.split())
