import re

from advent2024.utils import input_raw

commands = input_raw(3)


def pt1():
    muls = re.findall(r"mul\((\d+),(\d+)\)", commands)
    return sum(int(x) * int(y) for x, y in muls)


def pt2():
    parsed_commands = re.finditer(
        "".join(
            [
                r"(?>(?P<mul>mul)\((\d+),(\d+)\))",
                r"|",
                r"(?>(?P<do>do)\(\))",
                r"|",
                r"(?>(?P<dont>don't)\(\))",
            ]
        ),
        commands,
    )
    enabled = True
    running_total = 0
    for command in parsed_commands:
        vals = command.groupdict()
        if vals["do"]:
            enabled = True
        elif vals["dont"]:
            enabled = False
        elif vals["mul"]:
            if enabled:
                running_total += int(command[2]) * int(command[3])
        else:
            breakpoint()
    return running_total


print("pt1", pt1())
print("pt2", pt2())
