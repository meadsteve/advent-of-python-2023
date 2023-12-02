from day01.part_two import (
    find_first_number,
    find_last_number,
    number_for_input,
    solve_part_two,
)


def test_finds_the_first_number_when_numeric():
    assert find_first_number("er3fdf1e") == "3"


def test_finds_the_first_number_when_spelt_out():
    assert find_first_number("xfour3fdf1e") == "4"


def test_finds_the_last_number():
    assert find_last_number("er3fdf1e") == "1"


def test_finds_the_last_number_when_spelt_out():
    assert find_last_number("er3fdf1twoe") == "2"


def test_it_can_build_the_number_for_a_string():
    assert number_for_input("er3fdf1e") == 31


def test_it_solves_the_problem():
    assert solve_part_two() == 55093
