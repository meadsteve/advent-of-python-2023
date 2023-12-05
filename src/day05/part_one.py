import dataclasses
import re
from typing import Sequence, Protocol, Mapping

from common import blocks_by_blank_line, read_lines

mapper_definition = re.compile(r"([a-z]+)-to-([a-z]+) map:")


@dataclasses.dataclass
class Range:
    source_start: int
    source_end: int
    delta: int

    def contains(self, value: int) -> bool:
        return self.source_start <= value <= self.source_end

    @classmethod
    def from_string(cls, raw_string: str):
        [dest_start, source_start, range_length] = [
            int(n) for n in raw_string.split(" ")
        ]
        assert range_length > 0
        return cls(
            source_start=source_start,
            source_end=source_start + range_length - 1,
            delta=dest_start - source_start,
        )


class MappingFunction(Protocol):
    source: str
    destination: str

    def __call__(self, value: int) -> int:
        pass


class ChainedMapper(MappingFunction):
    source: str
    destination: str
    _first: MappingFunction
    _second: MappingFunction

    def __init__(self, first: MappingFunction, second: MappingFunction):
        self._first = first
        self._second = second
        self.source = self._first.source
        self.destination = self._second.destination

    def __call__(self, value: int) -> int:
        first = self._first
        second = self._second
        return second(first(value))


class Mapper(MappingFunction):
    source: str
    destination: str

    _mappings: Sequence[Range]

    def __init__(self, lines: Sequence[str]):
        [definition_line, *mapping_values] = lines
        definition = re.match(mapper_definition, definition_line)
        if not definition:
            raise ValueError("Invalid header line for mapper")
        self.source = definition.group(1)
        self.destination = definition.group(2)
        self._mappings = [Range.from_string(mapping) for mapping in mapping_values]

    def __call__(self, value: int) -> int:
        for mapping in self._mappings:
            if mapping.contains(value):
                return value + mapping.delta
        return value


class MappingCollection:
    _mappers: Mapping[str, MappingFunction]

    def __init__(self, mappers: Sequence[MappingFunction]):
        self._mappers = {mapper.source: mapper for mapper in mappers}

    def get_mapper_between(self, source: str, destination: str) -> MappingFunction:
        mapper = self._mappers[source]
        while mapper.destination != destination:
            mapper = ChainedMapper(mapper, self._mappers[mapper.destination])
        return mapper


def solve_part_one_for_file(file_path: str) -> int:
    blocks = list(blocks_by_blank_line(read_lines(file_path)))
    [[seed_line], *mapper_blocks] = blocks

    mappers = MappingCollection([Mapper(m) for m in mapper_blocks])
    seeds = [int(s) for s in seed_line.split(" ")[1:]]

    mapper = mappers.get_mapper_between("seed", "location")

    return min(mapper(s) for s in seeds)


def solve_part_one():
    return solve_part_one_for_file("./src/day05/input.txt")
