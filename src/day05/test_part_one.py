from day05.part_one_and_two import (
    Mapper,
    ChainedMapper,
    MappingCollection,
    solve_part_one_for_file,
    solve_part_one,
)


def test_a_mapper_can_be_built_from_text():
    lines = ["seed-to-soil map:", "50 98 2", "52 50 48"]
    mapper = Mapper.from_text(lines)
    assert mapper.source == "seed"
    assert mapper.destination == "soil"


def test_a_mapper_uses_the_explicitly_defined_maps():
    mapper = Mapper.from_text(["seed-to-soil map:", "50 98 2", "52 50 48"])

    assert mapper(98) == 50
    assert mapper(99) == 51

    assert mapper(50) == 52
    assert mapper(51) == 53


def test_a_mapper_leaves_the_value_unchanged_if_not_defined():
    mapper = Mapper.from_text(["seed-to-soil map:", "50 98 2", "52 50 48"])

    assert mapper(100) == 100
    assert mapper(49) == 49


def test_two_mapping_functions_can_be_chained_together():
    mapper_one = Mapper.from_text(["seed-to-soil map:", "50 98 2", "52 50 48"])
    mapper_two = Mapper.from_text(
        ["soil-to-fertilizer map:", "0 15 37", "37 52 2", "39 0 15"]
    )
    mapper = ChainedMapper(mapper_one, mapper_two)

    assert mapper.source == "seed"
    assert mapper.destination == "fertilizer"

    assert mapper(100) == 100
    assert mapper(98) == 35


def test_a_mapping_collection_can_give_the_correct_mappings():
    mapping_collection = MappingCollection(
        [
            Mapper.from_text(["seed-to-soil map:", "50 98 2", "52 50 48"]),
            Mapper.from_text(
                ["soil-to-fertilizer map:", "0 15 37", "37 52 2", "39 0 15"]
            ),
        ]
    )
    mapper = mapping_collection.get_mapper_between("seed", "fertilizer")

    assert mapper.source == "seed"
    assert mapper.destination == "fertilizer"


def test_it_works_for_the_example_file():
    assert solve_part_one_for_file("./src/day05/example.txt") == 35


def test_it_solves_part_one():
    assert solve_part_one() == 662197086
