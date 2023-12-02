from typing import Iterable

from common import read_lines

CharSequence = str | Iterable[str]

number_words = (
    ("one", "1"),
    ("two", "2"),
    ("three", "3"),
    ("four", "4"),
    ("five", "5"),
    ("six", "6"),
    ("seven", "7"),
    ("eight", "8"),
    ("nine", "9"),
)

reversed_number_words = tuple((x[::-1], y) for x, y in number_words)


def find_first_number(input_chars: CharSequence, *, word_lookup=number_words) -> str:
    working_string = ""
    for char in input_chars:
        if char.isdigit():
            return char
        working_string += char
        for number_word, value in word_lookup:
            if number_word in working_string:
                return value
    raise RuntimeError("No number found")


def find_last_number(input_chars: str) -> str:
    return find_first_number(reversed(input_chars), word_lookup=reversed_number_words)


def number_for_input(input_chars: str) -> int:
    return int(f"{find_first_number(input_chars)}{find_last_number(input_chars)}")


def solve_part_two():
    return sum(number_for_input(line) for line in read_lines("./src/day01/input.txt"))
