from typing import Iterable

from common import read_lines

CharSequence = str | Iterable[str]


def find_first_number(input_chars: CharSequence) -> str:
    for char in input_chars:
        if char.isdigit():
            return char
    raise RuntimeError("No number found")


def find_last_number(input_chars: str) -> str:
    return find_first_number(reversed(input_chars))


def number_for_input(input_chars: str) -> int:
    return int(f"{find_first_number(input_chars)}{find_last_number(input_chars)}")


def solve_part_one() -> int:
    return sum(number_for_input(line) for line in read_lines("./src/day01/input.txt"))
