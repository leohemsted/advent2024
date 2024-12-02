import itertools

from advent2024.utils import open_input

reports = [[int(level) for level in report] for report in open_input(2)]


def is_safe(report: list[int]):
    is_going_up = report[0] < report[1]
    for x, y in itertools.pairwise(report):
        if is_going_up != (x < y):
            return False

        if not (0 < abs(x - y) <= 3):
            return False

    return True


def is_safe_with_margin_for_error(report: list[int]):
    is_going_up = report[0] < report[1]

    def check_pair(x, y):
        if is_going_up != (x < y):
            return False

        if not (0 < abs(x - y) <= 3):
            return False

    for x, y in itertools.pairwise(report):
        if not check_pair(x, y):
            return any(
                is_safe(report[:i] + report[i + 1 :]) for i in range(len(report))
            )

    return True


def pt1():
    print("pt1", sum(is_safe(report) for report in reports))


def pt2():
    print("pt2", sum(is_safe_with_margin_for_error(report) for report in reports))


pt1()
pt2()
