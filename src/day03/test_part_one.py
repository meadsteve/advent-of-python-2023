from day03.part_one_and_two import (
    Grid,
    get_neighbours,
    parse_schematic,
    Schematic,
    solve_part_one,
)


def test_all_neighbours_can_be_loaded_for_a_position():
    schematic: Grid = [
        ["A", "B", "C"],
        ["D", "E", "F"],
        ["G", "H", "I"],
    ]

    assert set(get_neighbours(schematic, (1, 1))) == {
        "A",
        "B",
        "C",
        "D",
        "F",
        "G",
        "H",
        "I",
    }


def test_it_works_for_the_corners():
    schematic: Grid = [
        ["A", "B", "C"],
        ["D", "E", "F"],
        ["G", "H", "I"],
    ]

    assert set(get_neighbours(schematic, (0, 0))) == {
        "B",
        "D",
        "E",
    }

    assert set(get_neighbours(schematic, (2, 0))) == {
        "B",
        "E",
        "F",
    }

    assert set(get_neighbours(schematic, (2, 2))) == {
        "E",
        "F",
        "H",
    }


def test_part_location_ids_get_parsed_into_the_scheme():
    raw_input = ["123...", "...456"]
    assert parse_schematic(raw_input) == Schematic(
        grid=[[0, 0, 0, ".", ".", "."], [".", ".", ".", 1, 1, 1]],
        part_lookup={0: 123, 1: 456},
    )


def test_a_schema_can_return_the_part_ids_next_to_a_symbol_when_there_are_none():
    schematic = parse_schematic(["123...", "...456"])

    assert schematic.get_part_ids_next_to_symbol() == []


def test_a_schema_can_return_the_part_ids_next_to_a_symbol():
    schematic = parse_schematic(["123*....", ".....456"])

    assert schematic.get_part_ids_next_to_symbol() == [123]


def test_a_schema_can_return_the_part_ids_next_to_a_symbol_when_there_are_dupes():
    schematic = parse_schematic(["123*....", "....*123"])

    assert schematic.get_part_ids_next_to_symbol() == [123, 123]


def test_it_can_solve_part_one():
    assert solve_part_one() == 553825
