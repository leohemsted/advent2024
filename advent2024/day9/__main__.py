import itertools

from advent2024.utils import input_raw

raw_data = input_raw(9).strip()


def print_disk(disk: list[int | None]) -> None:
    for item in disk:
        print(item if item is not None else ".", end="")
    print()


def read_disk(raw_data: str) -> list[int | None]:
    data: list[int | None] = []
    file_id = 0

    def unpack_file(val: int):
        nonlocal file_id
        for _ in range(val):
            data.append(file_id)
        file_id += 1

    def unpack_free_space(val: int):
        for _ in range(val):
            data.append(None)

    unpackers = itertools.cycle([unpack_file, unpack_free_space])

    for char in raw_data:
        unpacker = next(unpackers)
        unpacker(int(char))
    return data


def defrag_disk(orig_disk: list[int | None]) -> list[int | None]:
    disk = orig_disk.copy()
    write_i = 0
    read_i = len(disk) - 1
    while write_i < read_i:
        if disk[write_i] is not None:
            write_i += 1
            continue
        if disk[read_i] is None:
            read_i -= 1
            continue

        # swap elements
        disk[write_i], disk[read_i] = disk[read_i], disk[write_i]
    return disk


def defrag_disk_pt_2(disk: list[int | None]) -> None:
    write_i = 0
    read_i = len(disk) - 1
    while write_i < read_i:
        if disk[write_i] is not None:
            write_i += 1
            continue
        if disk[read_i] is None:
            read_i -= 1
            continue

        # swap elements
        disk[write_i], disk[read_i] = disk[read_i], disk[write_i]


def checksum_disk(disk: list[int | None]) -> int:
    return sum(val * i for i, val in enumerate(disk) if val is not None)


data = read_disk(raw_data)

defragged = defrag_disk(data)

print("pt1", checksum_disk(defragged))
