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


def pt1():
    stones = input_stones
    for i in range(26):
        print(i, len(stones))
        stones = iterate_stones(stones)


print("pt1", pt1())
