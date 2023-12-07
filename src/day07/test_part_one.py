import pytest

from day07.part_one import (
    Card,
    HandAndBid,
    parse,
    hand_type,
    HandType,
    Hand,
    solve_part_one,
    solve_part_one_for_file,
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


def test_it_works_for_the_example():
    assert solve_part_one_for_file("./src/day07/example.txt") == 6440


def test_it_can_solve_part_one():
    assert solve_part_one() != 250944320
    assert solve_part_one() == 0
