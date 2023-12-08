import pytest

from common import read_lines
from day07.part_one_and_two import (
    Card,
    HandAndBid,
    parse,
    hand_type,
    HandType,
    Hand,
    solve_part_one,
    solve_for_file,
)


def test_a_row_gets_parsed_into_a_hand_and_bid():
    expected = HandAndBid(
        hand=Hand(Card.three, Card.two, Card.T, Card.three, Card.K), bid=765
    )

    parsed = parse("32T3K 765")

    assert parsed == expected


def test_card_sequence():
    assert (
        Card.two
        < Card.three
        < Card.four
        < Card.five
        < Card.six
        < Card.seven
        < Card.eight
        < Card.nine
        < Card.T
        < Card.J
        < Card.Q
        < Card.K
        < Card.A
    )


def test_hand_sequence():
    assert (
        HandType.HighCard
        < HandType.OnePair
        < HandType.TwoPair
        < HandType.ThreeOfAKind
        < HandType.FullHouse
        < HandType.FourOfAKind
        < HandType.FiveOfAKind
    )


@pytest.mark.parametrize(
    "hand,expected_rank",
    [
        ("23456", HandType.HighCard),
        ("22456", HandType.OnePair),
        ("22446", HandType.TwoPair),
        ("QQQJA", HandType.ThreeOfAKind),
        ("22444", HandType.FullHouse),
        ("24444", HandType.FourOfAKind),
        ("AAAAA", HandType.FiveOfAKind),
    ],
)
def test_it_get_the_hand_type_properly(hand, expected_rank):
    assert hand_type(Hand.from_string(hand)) == expected_rank


@pytest.mark.parametrize(
    "better_hand,worse_hand",
    [
        ("22456", "23456"),
        ("22456", "A3456"),
        ("22256", "AA456"),
        ("22A56", "22456"),
        ("QQQJA", "KK677"),
        ("QQQJA", "T55J5"),
    ],
)
def test_the_hands_compare_properly_based_on_rank(better_hand, worse_hand):
    worse = Hand.from_string(worse_hand)
    better = Hand.from_string(better_hand)
    assert worse < better
    assert better > worse


def test_the_hands_in_the_example_can_be_sorted_as_expected():
    a = Hand.from_string("32T3K")
    b = Hand.from_string("T55J5")
    c = Hand.from_string("KK677")
    d = Hand.from_string("KTJJT")
    e = Hand.from_string("QQQJA")
    assert sorted([a, b, c, d, e]) == [a, d, c, b, e]


def test_a_random_example():
    a = Hand.from_string("23456")
    b = Hand.from_string("34567")
    c = Hand.from_string("45678")
    d = Hand.from_string("56789")
    e = Hand.from_string("A2345")
    hand = [a, b, c, d, e]
    sorted_hand = sorted(hand)
    assert sorted_hand == hand


def test_sorting_the_input_behaves_as_expected():
    lines = read_lines("./src/day07/input.txt")
    hands = [parse(line).hand for line in lines]

    sorted_once = list(sorted(hands))
    sorted_twice = list(sorted(sorted_once))

    assert sorted_once[0:10] == sorted_twice[0:10]


def test_it_works_for_the_example():
    assert solve_for_file("./src/day07/example.txt") == 6440


def test_it_can_solve_part_one():
    assert solve_part_one() == 251806792
