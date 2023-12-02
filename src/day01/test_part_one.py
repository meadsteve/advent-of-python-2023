from .part_one import find_first_number, find_last_number, number_for_input, solve_part_one


def test_finds_the_first_number():
    assert find_first_number("er3fdf1e") == "3"


def test_finds_the_last_number():
    assert find_last_number("er3fdf1e") == "1"


def test_it_can_build_the_number_for_a_string():
    assert number_for_input("er3fdf1e") == 31


def test_it_solves_the_problem():
    assert solve_part_one() == 55002
