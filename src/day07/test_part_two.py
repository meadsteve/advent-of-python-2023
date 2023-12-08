import pytest

from day07.part_one_and_two import (
    Card,
    parse,
    Hand,
    hand_type,
    HandType,
    solve_for_file,
    solve_part_two,
)


def test_a_line_can_be_parsed_with_and_without_jokers():
    line = "32T3J 765"
    with_jokers = parse(line, jokers_exist=True)
    without_jokers = parse(line)

    assert without_jokers.hand[4] == Card.J
    assert with_jokers.hand[4] == Card.joker


@pytest.mark.parametrize(
    "hand,expected_rank",
    [
        ("J3456", HandType.OnePair),
        ("22J56", HandType.ThreeOfAKind),
        ("2244J", HandType.FullHouse),
        ("QQQJA", HandType.FourOfAKind),
        ("J4444", HandType.FiveOfAKind),
    ],
)
def test_a_single_joker_bumps_the_hand_type(hand, expected_rank):
    assert hand_type(Hand.from_string(hand, jokers_exist=True)) == expected_rank


@pytest.mark.parametrize(
    "hand,expected_rank",
    [
        ("J345J", HandType.ThreeOfAKind),
        ("22J5J", HandType.FourOfAKind),
        ("QQQJJ", HandType.FiveOfAKind),
    ],
)
def test_multiple_jokers_bump_the_hand_type(hand, expected_rank):
    assert hand_type(Hand.from_string(hand, jokers_exist=True)) == expected_rank


def test_five_jokers_is_five_of_a_kind():
    assert (
        hand_type(Hand.from_string("JJJJJ", jokers_exist=True)) == HandType.FiveOfAKind
    )


def test_jokers_are_ranked_the_lowest_when_the_hand_type_is_the_same():
    lower = Hand.from_string("J2345", jokers_exist=True)
    higher = Hand.from_string("22345", jokers_exist=True)

    assert higher > lower


def test_it_works_for_the_example():
    assert solve_for_file("./src/day07/example.txt", jokers_exist=True) == 5905


def test_it_can_solve_part_two():
    assert solve_part_two() == 252113488
