import itertools

from advent2024.utils import input_raw

raw_data = input_raw(9).strip()


def print_disk(
    disk: list[int | None], read_pointer=0, write_pointer=0, compressed=True
) -> None:
    first, last = min(read_pointer, write_pointer), max(read_pointer, write_pointer)
    if first and last:
        print(" " * first + "w" + " " * (last - first - 1) + "r")
    if (first and last) or not compressed:
        for item in disk:
            print(item if item is not None else ".", end="")
    else:
        for item, group in itertools.groupby(disk):
            file_len = len(list(group))
            print(
                f"[{item} * {file_len}]" if item is not None else "." * file_len,
                end="",
            )
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
    write_disk = orig_disk.copy()

    read_i = len(write_disk)
    for read_contents, group in itertools.groupby(reversed(write_disk)):
        read_file_len = len(list(group))
        read_i -= read_file_len
        if read_contents is not None:
            # found some data we want to move
            write_i = 0
            for write_contents, group in itertools.groupby(write_disk):
                write_file_len = len(list(group))
                # dont overwrite stuff
                if read_contents is None and write_file_len >= read_file_len:
                    # if it fits i sits
                    # print_disk(write_disk, read_i, write_i, compressed=False)
                    write_disk[write_i : write_i + read_file_len] = list(
                        itertools.repeat(read_contents, read_file_len)
                    )
                    write_disk[read_i : read_i + read_file_len] = list(
                        itertools.repeat(None, read_file_len)
                    )

                    if write_i > read_i:
                        # dont move further out - we cant put this anywhere, give up
                        break
                write_i += write_file_len

    return write_disk


def checksum_disk(disk: list[int | None]) -> int:
    return sum(val * i for i, val in enumerate(disk) if val is not None)


# -------------------------------


def defrag_disk_pt_2_attempt_2(in_data: list[int | None]) -> list[int | None]:
    data = in_data.copy()
    read_i = len(data) - 1
    while read_i > 0:
        read_val = data[read_i]
        end_read_block = read_i + 1
        while data[read_i] == read_val:
            read_i -= 1
        start_read_block = read_i + 1
        read_len = end_read_block - start_read_block
        # print("read", start_read_block, end_read_block, read_val, read_len)

        if read_val is not None:
            write_i = 0
            while write_i < read_i:
                while data[write_i] is not None:
                    write_i += 1
                # found start of an empty block
                start_write_block = write_i
                while data[write_i] is None and write_i - start_write_block < read_len:
                    write_i += 1
                end_write_block = write_i

                if write_i < read_i and end_write_block - start_write_block == read_len:
                    # print("writeable", start_write_block, end_write_block)
                    # print_disk(data, start_write_block, start_read_block)

                    data[start_write_block:end_write_block] = [read_val] * read_len
                    data[start_read_block:end_read_block] = [None] * read_len
                    break

                write_i += 1

    return data


data = read_disk(raw_data)

defragged = defrag_disk(data)
print_disk(data, compressed=False)
alt_defragged = defrag_disk_pt_2_attempt_2(data)
print_disk(alt_defragged, compressed=False)

print("pt1", checksum_disk(defragged))
print("pt2", checksum_disk(alt_defragged))
