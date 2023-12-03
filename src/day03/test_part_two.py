from day03.part_one_and_two import (
    Grid,
    get_part_number_neighbours,
    parse_schematic,
    solve_part_two,
)


def test_the_number_of_part_number_neighbours_can_be_counted():
    grid: Grid = [
        [1, 1, "."],
        [".", "*", "."],
        [".", 3, 3],
    ]

    assert get_part_number_neighbours(grid, (1, 1)) == {1, 3}


def test_it_finds_all_the_gear_ratios():
    schematic = parse_schematic(
        [
            "41.",
            ".*.",
            ".22",
        ]
    )

    assert list(schematic.get_gears()) == [(41, 22)]


def test_it_can_solve_part_two():
    assert solve_part_two() == 93994191
