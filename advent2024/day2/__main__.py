import itertools

from advent2024.utils import input_tuples_per_line

reports = [[int(level) for level in report] for report in input_tuples_per_line(2)]


def check_pair(is_going_up, x, y):
    if is_going_up != (x < y):
        return False

    if not (0 < abs(x - y) <= 3):
        return False
    return True


def is_safe(report: list[int]):
    is_going_up = report[0] < report[1]
    return all(check_pair(is_going_up, x, y) for x, y in itertools.pairwise(report))


def is_safe_with_margin_for_error(report: list[int]):
    is_going_up = report[0] < report[1]

    for x, y in itertools.pairwise(report):
        if not check_pair(is_going_up, x, y):
            return any(
                is_safe(report[:i] + report[i + 1 :]) for i in range(len(report))
            )

    return True


def pt1():
    return sum(is_safe(report) for report in reports)


def pt2():
    return sum(is_safe_with_margin_for_error(report) for report in reports)


print(pt1())  # 432
print(pt2())  # 488
