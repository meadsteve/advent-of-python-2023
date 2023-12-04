import pytest

from day04.part_one import Row, parse_row, solve_part_one


def test_it_can_parse_a_row():
    assert parse_row("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53") == Row(
        card_id=1,
        numbers=[41, 48, 83, 86, 17],
        winning_numbers=[83, 86, 6, 31, 17, 9, 48, 53],
    )


@pytest.mark.parametrize(
    "row_string, expected_score",
    [
        ("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53", 8),
        ("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19", 2),
        ("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83", 1),
        ("Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11", 0),
    ],
)
def test_it_scores_correctly(row_string, expected_score):
    assert parse_row(row_string).score == expected_score


def test_it_can_solve_part_one():
    assert solve_part_one() == 15205
