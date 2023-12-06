from __future__ import annotations

import dataclasses
import functools
from typing import Iterable, overload


def read_lines(path: str) -> Iterable[str]:
    with open(path, "r") as file:
        while line := file.readline():
            yield line.strip()


def blocks_by_blank_line(lines: Iterable[str]) -> Iterable[list[str]]:
    chunk: list[str] = []
    for line in lines:
        if line == "":
            yield chunk
            chunk = []
        else:
            chunk.append(line)
    yield chunk


@overload
def multiply_together(ns: Iterable[int]) -> int:
    ...


@overload
def multiply_together(ns: Iterable[float]) -> float:
    ...


def multiply_together(ns: Iterable):
    return functools.reduce(lambda x, y: x * y, ns, 1)


def iterator_length(ns: Iterable) -> int:
    return sum(1 for _ in ns)


@dataclasses.dataclass
class IntRange(Iterable[int]):
    start: int
    stop: int

    def __iter__(self):
        return iter(range(self.start, self.stop))

    def __len__(self) -> int:
        return self.stop - self.start

    @classmethod
    def empty(cls) -> IntRange:
        return IntRange(start=0, stop=0)
