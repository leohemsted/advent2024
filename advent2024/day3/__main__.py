import re

from advent2024.utils import input_raw

commands = input_raw(3)


def pt1():
    muls = re.findall(r"mul\((\d+),(\d+)\)", commands)
    return sum(int(x) * int(y) for x, y in muls)


print("pt1", pt1())
