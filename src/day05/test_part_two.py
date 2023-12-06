import pytest

from common import IntRange
from day05.part_one_and_two import (
    solve_part_two_for_file,
    solve_part_two,
    Mapper,
    ChainedMapper,
)


def test_a_basic_mapper_can_be_reversed():
    mapper = Mapper.from_text(["seed-to-soil map:", "50 98 2", "52 50 48"])
    reversed_mapper = mapper.reverse()

    assert mapper(98) == 50
    assert reversed_mapper(50) == 98


def test_a_whole_range_can_be_matched():
    mapper = Mapper.from_text(["seed-to-soil map:", "50 98 2", "52 50 48"])

    assert list(mapper.apply_for_range([IntRange(start=98, stop=100)])) == [
        IntRange(start=50, stop=52)
    ]


def test_a_whole_range_can_be_matched_and_gets_split_if_needed_a():
    mapper = Mapper.from_text(["seed-to-soil map:", "50 98 2", "52 50 48"])

    assert list(mapper.apply_for_range([IntRange(start=98, stop=101)])) == [
        IntRange(start=50, stop=52),
        IntRange(start=100, stop=101),
    ]


def test_a_whole_range_can_be_matched_and_gets_split_if_needed_b():
    mapper = Mapper.from_text(["seed-to-soil map:", "50 98 2", "52 50 48"])

    assert list(mapper.apply_for_range([IntRange(start=96, stop=99)])) == [
        IntRange(start=98, stop=100),
        IntRange(start=50, stop=51),
    ]


def test_a_whole_range_can_be_matched_and_gets_split_if_needed_c():
    mapper = Mapper.from_text(["seed-to-soil map:", "50 98 2", "52 50 48"])

    assert list(
        mapper.apply_for_range(
            [IntRange(start=1, stop=3), IntRange(start=98, stop=101)]
        )
    ) == [
        IntRange(start=1, stop=3),
        IntRange(start=50, stop=52),
        IntRange(start=100, stop=101),
    ]


def test_a_whole_range_can_be_matched_and_gets_split_if_needed_d():
    mapper = Mapper.from_text(["seed-to-soil map:", "50 98 2", "52 50 48"])

    assert list(mapper.apply_for_range([IntRange(start=1000, stop=1002)])) == [
        IntRange(start=1000, stop=1002)
    ]


def test_chained_mappers_can_be_called_with_a_range():
    mapper = ChainedMapper(
        Mapper.from_text(["seed-to-soil map:", "50 98 2", "52 50 48"]),
        Mapper.from_text(["soil-to-fertilizer map:", "0 15 37", "37 52 2", "39 0 15"]),
    )

    assert mapper(96) == 98
    assert mapper(97) == 99
    assert mapper(98) == 35

    assert list(mapper.apply_for_range([IntRange(start=96, stop=99)])) == [
        IntRange(start=98, stop=100),
        IntRange(start=35, stop=36),
    ]


def test_chained_mappers_can_be_reversed():
    mapper = ChainedMapper(
        Mapper.from_text(["seed-to-soil map:", "50 98 2", "52 50 48"]),
        Mapper.from_text(["soil-to-fertilizer map:", "0 15 37", "37 52 2", "39 0 15"]),
    )
    reversed_mapper = mapper.reverse()

    assert mapper(98) == 35
    assert reversed_mapper(35) == 98


def test_it_works_for_the_example_file():
    assert solve_part_two_for_file("./src/day05/example.txt") == 46


def test_it_solves_part_two():
    assert solve_part_two() == 52510809
