import re

from advent2024.utils import input_raw

for command in input_raw(3):
    muls = re.findall("mul\((\d+),(\d+)\)", command)
    print(sum(x * y for x, y in muls))
