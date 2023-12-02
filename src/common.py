from typing import Iterable


def read_lines(path: str) -> Iterable[str]:
    with open(path, "r") as file:
        while line := file.readline():
            yield line.strip()
