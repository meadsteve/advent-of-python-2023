from typing import Sequence, Iterable

from common import read_lines


def difference_sequence(numbers: Sequence[int]) -> list[int]:
    return list(b - a for a, b in zip(numbers, numbers[1:]))


def all_zeros(numbers: Iterable[int]) -> bool:
    return all(n == 0 for n in numbers)


def next_number(numbers: Sequence[int]) -> int:
    diffs = difference_sequence(numbers)
    if all_zeros(diffs):
        return numbers[0]
    return numbers[-1] + next_number(diffs)


def solve_part_one() -> int:
    lines = read_lines("./src/day09/input.txt")
    sequences = (list(map(int, line.split(" "))) for line in lines)
    nexts = (next_number(sequence) for sequence in sequences)
    return sum(nexts)
