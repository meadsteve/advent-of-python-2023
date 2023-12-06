from __future__ import annotations
import dataclasses
import itertools
import re
from concurrent.futures import ProcessPoolExecutor
from typing import Sequence, Protocol, Mapping, Iterable

from common import blocks_by_blank_line, read_lines

MAX_INT_TO_TRY = 100_000_000_000_000

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


class Mapper(MappingFunction):
    source: str
    destination: str

    _mappings: Sequence[Range]

    def __init__(self, *, source: str, destination: str, mappings: Sequence[Range]):
        self.source = source
        self.destination = destination
        self._mappings = mappings

    @classmethod
    def from_text(cls, lines: Sequence[str]):
        [definition_line, *mapping_values] = lines
        definition = re.match(mapper_definition, definition_line)
        if not definition:
            raise ValueError("Invalid header line for mapper")
        return Mapper(
            source=definition.group(1),
            destination=definition.group(2),
            mappings=[Range.from_string(mapping) for mapping in mapping_values],
        )

    def __call__(self, value: int) -> int:
        for mapping in self._mappings:
            if mapping.contains(value):
                return value + mapping.delta
        return value

    def reverse(self) -> Mapper:
        reversed_mappings = [
            Range(
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


def solve_part_two_for_file(file_path: str, *, batch_size: int = 1000) -> int | None:
    mapper, seeds = _mapper_and_seeds(file_path)
    reversed_mapper = mapper.reverse()

    seed_range_min_maxes = [
        (start, start + delta) for (start, delta) in itertools.batched(seeds, 2)
    ]

    location_validator = _LocationValidator(reversed_mapper, seed_range_min_maxes)

    with ProcessPoolExecutor() as executor:
        for possible_minimums in itertools.batched(
            range(0, MAX_INT_TO_TRY), batch_size
        ):
            print(f"Trying: {possible_minimums[0]}")
            results = executor.map(location_validator, possible_minimums)
            non_null_results = [r for r in results if r is not None]
            if len(non_null_results) > 0:
                return min(non_null_results)
    print(f"No value found under {MAX_INT_TO_TRY}")
    return None


@dataclasses.dataclass
class _LocationValidator:
    reversed_mapper: MappingFunction
    seed_range_min_maxes: list[tuple[int, int]]

    def __call__(self, possible_minimum):
        possible_seed = self.reversed_mapper(possible_minimum)

        for start, end in self.seed_range_min_maxes:
            if start <= possible_seed <= end:
                return possible_minimum
        return None


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


if __name__ == "__main__":
    print(solve_part_two())
