from collections.abc import Iterator
from pathlib import Path
from typing import Any


def open_input(day: int) -> Iterator[tuple[Any], None, None]:
    path = Path.cwd() / "advent2024" / f"day{day}" / "input"
    with path.open() as f:
        while line := f.readline():
            yield tuple(line.split())
