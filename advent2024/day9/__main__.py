import itertools

from advent2024.utils import input_raw

raw_data = input_raw(9, "example").strip()


def print_disk(disk: list[int | None], read_pointer=0, write_pointer=0) -> None:
    first, last = min(read_pointer, write_pointer), max(read_pointer, write_pointer)
    if first and last:
        print(" " * first + "w" + " " * (last - first - 1) + "r")
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


def defrag_disk_pt_2(orig_disk: list[int | None]) -> list[int | None]:
    print_disk(orig_disk)
    write_disk = orig_disk.copy()

    write_i = 0
    read_i = len(write_disk)
    for file_contents, group in itertools.groupby(write_disk):
        write_file_len = len(list(group))
        if file_contents is None:
            # found an empty gap

            read_i = len(write_disk)
            # breakpoint()
            for file_contents, group in itertools.groupby(reversed(write_disk)):

                read_file_len = len(list(group))
                read_i -= read_file_len
                if read_i <= write_i + read_file_len:
                    break

                if file_contents is not None and read_file_len <= write_file_len:
                    # if it fits i sits
                    print_disk(write_disk, read_i, write_i)
                    write_disk[write_i : write_i + read_file_len] = list(
                        itertools.repeat(file_contents, read_file_len)
                    )
                    write_disk[read_i : read_i + read_file_len] = list(
                        itertools.repeat(None, read_file_len)
                    )
                    break
        write_i += write_file_len

    print_disk(write_disk, read_i, write_i)
    return write_disk

    # write_i = 0
    # read_i = len(disk) - 1
    # while write_i < read_i:
    #     if disk[write_i] is not None:
    #         write_i += 1
    #         continue
    #     if disk[read_i] is None:
    #         read_i -= 1
    #         continue

    #     # swap elements
    #     disk[write_i], disk[read_i] = disk[read_i], disk[write_i]
    # return disk


def checksum_disk(disk: list[int | None]) -> int:
    return sum(val * i for i, val in enumerate(disk) if val is not None)


data = read_disk(raw_data)

defragged = defrag_disk(data)
alt_defragged = defrag_disk_pt_2(data)

print("pt1", checksum_disk(defragged))
print("pt2", checksum_disk(alt_defragged))
