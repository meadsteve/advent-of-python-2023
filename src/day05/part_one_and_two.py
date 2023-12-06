from __future__ import annotations
import dataclasses
import itertools
import re
from concurrent.futures import ProcessPoolExecutor
from typing import Sequence, Protocol, Mapping, Iterable

from common import blocks_by_blank_line, read_lines, IntRange

MAX_INT_TO_TRY = 100_000_000_000_000

mapper_definition = re.compile(r"([a-z]+)-to-([a-z]+) map:")


@dataclasses.dataclass
class MappedRange:
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

    def apply_for_range(self, ranges: Iterable[IntRange]) -> Iterable[IntRange]:
        pass

    def reverse(self) -> MappingFunction:
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

    def reverse(self) -> ChainedMapper:
        return ChainedMapper(self._second.reverse(), self._first.reverse())

    def apply_for_range(self, ranges: Iterable[IntRange]) -> Iterable[IntRange]:
        first = self._first
        second = self._second
        return second.apply_for_range(first.apply_for_range(ranges))


class Mapper(MappingFunction):
    source: str
    destination: str

    _mappings: Sequence[MappedRange]

    def __init__(
        self, *, source: str, destination: str, mappings: Sequence[MappedRange]
    ):
        self.source = source
        self.destination = destination
        self._mappings = sorted(mappings, key=lambda m: m.source_start)

    @classmethod
    def from_text(cls, lines: Sequence[str]):
        [definition_line, *mapping_values] = lines
        definition = re.match(mapper_definition, definition_line)
        if not definition:
            raise ValueError("Invalid header line for mapper")
        return Mapper(
            source=definition.group(1),
            destination=definition.group(2),
            mappings=[MappedRange.from_string(mapping) for mapping in mapping_values],
        )

    def apply_for_range(self, ranges: Iterable[IntRange]) -> Iterable[IntRange]:
        for input_range in ranges:
            lower = input_range.start
            upper = input_range.stop - 1
            for mapping in self._mappings:
                if upper < mapping.source_start:
                    yield IntRange(start=lower, stop=upper + 1)
                    lower = upper + 1
                    break
                if mapping.contains(lower) and mapping.contains(upper):
                    yield IntRange(
                        start=lower + mapping.delta, stop=upper + mapping.delta + 1
                    )
                    lower = upper + 1
                    break
                if mapping.contains(upper):
                    yield IntRange(start=lower, stop=mapping.source_start)
                    yield IntRange(
                        start=mapping.source_start + mapping.delta,
                        stop=upper + mapping.delta,
                    )
                    lower = upper + 1
                    break
                if mapping.contains(lower):
                    yield IntRange(
                        start=lower + mapping.delta,
                        stop=mapping.source_end + mapping.delta + 1,
                    )
                    lower = mapping.source_end + 1
            if lower <= upper:
                yield IntRange(start=lower, stop=upper + 1)

    def __call__(self, value: int) -> int:
        for mapping in self._mappings:
            if mapping.contains(value):
                return value + mapping.delta
        return value

    def reverse(self) -> Mapper:
        reversed_mappings = [
            MappedRange(
                source_start=old_range.source_start + old_range.delta,
                source_end=old_range.source_end + old_range.delta,
                delta=-old_range.delta,
            )
            for old_range in self._mappings
        ]
        return Mapper(
            source=self.destination, destination=self.source, mappings=reversed_mappings
        )


class MappingCollection:
    _mappers: Mapping[str, MappingFunction]

    def __init__(self, mappers: Iterable[MappingFunction]):
        self._mappers = {mapper.source: mapper for mapper in mappers}

    def get_mapper_between(self, source: str, destination: str) -> MappingFunction:
        mapper = self._mappers[source]
        while mapper.destination != destination:
            mapper = ChainedMapper(mapper, self._mappers[mapper.destination])
        return mapper


def solve_part_one_for_file(file_path: str) -> int:
    mapper, seeds = _mapper_and_seeds(file_path)

    return min(mapper(s) for s in seeds)


def solve_part_two_for_file(file_path: str) -> int:
    mapper, seeds = _mapper_and_seeds(file_path)

    seed_range_min_maxes = [
       IntRange(start=start, stop=start + delta + 1) for (start, delta) in itertools.batched(seeds, 2)
    ]

    results = sorted(list(mapper.apply_for_range(seed_range_min_maxes)), key=lambda r: r.start)

    return results[0].start


def _mapper_and_seeds(file_path):
    blocks = blocks_by_blank_line(read_lines(file_path))
    [seed_line] = next(blocks)
    seeds = (int(s) for s in seed_line.split(" ")[1:])
    mappers = MappingCollection(Mapper.from_text(m) for m in blocks)
    mapper = mappers.get_mapper_between("seed", "location")
    return mapper, seeds


def solve_part_one():
    return solve_part_one_for_file("./src/day05/input.txt")


def solve_part_two():
    return solve_part_two_for_file("./src/day05/input.txt")

