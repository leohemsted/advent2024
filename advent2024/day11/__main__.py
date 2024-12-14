import functools

from advent2024.utils import input_raw

input_stones = [int(x) for x in input_raw(11).split()]


def iterate_stones(stones: list[int]) -> list[int]:
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif len(string := str(stone)) % 2 == 0:
            new_stones.append(int(string[: len(string) // 2]))
            new_stones.append(int(string[len(string) // 2 :]))
        else:
            new_stones.append(stone * 2024)
    return new_stones


@functools.cache
def count_stones(stone: int, blinks_remaining: int) -> int:
    if blinks_remaining == 0:
        return 1

    if stone == 0:
        return count_stones(1, blinks_remaining - 1)
    elif len(string := str(stone)) % 2 == 0:
        return count_stones(
            int(string[: len(string) // 2]), blinks_remaining - 1
        ) + count_stones(int(string[len(string) // 2 :]), blinks_remaining - 1)

    else:
        return count_stones(stone * 2024, blinks_remaining - 1)


def pt1():
    stones = input_stones
    for i in range(26):
        print(i, len(stones))
        stones = iterate_stones(stones)


def pt2():
    return sum(count_stones(stone, blinks_remaining=75) for stone in input_stones)


print("pt1", pt1())
print("pt2", pt2())
