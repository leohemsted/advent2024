from advent2024.utils import input_lines

wordsearch = [list(l) for l in input_lines(4)]


class Guard:
    heading: Literal[""]
