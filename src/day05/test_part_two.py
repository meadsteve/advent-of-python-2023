import pytest

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


def test_chained_mappers_can_be_reversed():
    mapper = ChainedMapper(
        Mapper.from_text(["seed-to-soil map:", "50 98 2", "52 50 48"]),
        Mapper.from_text(["soil-to-fertilizer map:", "0 15 37", "37 52 2", "39 0 15"]),
    )
    reversed_mapper = mapper.reverse()

    assert mapper(98) == 35
    assert reversed_mapper(35) == 98


def test_it_works_for_the_example_file():
    assert solve_part_two_for_file("./src/day05/example.txt", batch_size=10) == 46


@pytest.mark.skip("WIP: Slooooow - and might not work")
def test_it_solves_part_two():
    assert solve_part_two() is None
