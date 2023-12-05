from typing import Iterable


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
