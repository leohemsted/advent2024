import itertools
from contextlib import suppress
from dataclasses import dataclass

from advent2024.utils import input_lines


@dataclass
class PageOrderingRule:
    first: int
    later: int


input_data = input_lines(5)
rules = [
    PageOrderingRule(*map(int, line.strip().split("|")))
    for line in itertools.takewhile(str.strip, input_data)
]
updates: list[int] = [list(map(int, line.strip().split(","))) for line in input_data]


def check_update(update: list[int]) -> bool:
    for rule in rules:
        with suppress(ValueError):
            if f_index := update.index(rule.first):
                if update.index(rule.later, 0, f_index):
                    return False
    return True


def pt1():
    return sum(update[len(update) // 2] for update in updates if check_update(update))


print("pt1", pt1())
