import functools

from advent2024.utils import input_raw

stones = [int(x) for x in input_raw(11).split()]


@functools.cache
def count_stones(stone: int, blinks_remaining: int) -> int:
    if blinks_remaining == 0:
        return 1
    blinks_remaining -= 1

    if stone == 0:
        return count_stones(1, blinks_remaining)
    elif len(string := str(stone)) % 2 == 0:
        first = count_stones(int(string[: len(string) // 2]), blinks_remaining)
        second = count_stones(int(string[len(string) // 2 :]), blinks_remaining)
        return first + second
    else:
        return count_stones(stone * 2024, blinks_remaining)


print("pt1", sum(count_stones(stone, blinks_remaining=25) for stone in stones))
print("pt2", sum(count_stones(stone, blinks_remaining=75) for stone in stones))
