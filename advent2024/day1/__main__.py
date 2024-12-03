import functools
import itertools
from collections import Counter

from advent2024.utils import input_tuples_per_line

lhs = []
rhs = []
for x, y in input_tuples_per_line(1):
    lhs.append(int(x))
    rhs.append(int(y))
lhs.sort()
rhs.sort()


def pt1():

    res = functools.reduce(
        lambda running_total, curr_value: running_total
        + abs(curr_value[1] - curr_value[0]),
        itertools.zip_longest(lhs, rhs),
        # initial value for running total
        0,
    )
    print("pt1", res)


def pt2():
    lhs_counter = Counter(lhs)
    rhs_counter = Counter(rhs)
    similarity_score = 0
    for number, count in lhs_counter.items():
        rhs_count = rhs_counter[number]
        similarity_score += number * rhs_count
    print("pt2", similarity_score)


pt1()
pt2()
