import itertools
from collections import defaultdict
from functools import cmp_to_key

from advent2024.utils import input_lines

input_data = input_lines(5)

rule_dict = defaultdict(set)
for first, later in (
    map(int, line.strip().split("|")) for line in itertools.takewhile(bool, input_data)
):
    rule_dict[first].add(later)

updates: list[list[int]] = [list(map(int, line.split(","))) for line in input_data]


def check_update(update: list[int]) -> bool:
    return sorted(update, key=cmp_to_key(is_pairing_valid)) == update


def is_pairing_valid(first, later):
    return later not in rule_dict[first] or -1


def pt1():
    return sum(update[len(update) // 2] for update in updates if check_update(update))


def pt2():
    def middle_pages():
        for update in updates:
            if update != (new := sorted(update, key=cmp_to_key(is_pairing_valid))):
                yield new[len(new) // 2]

    return sum(middle_pages())


print("pt1", pt1())
print("pt2", pt2())
