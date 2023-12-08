from __future__ import annotations
import dataclasses
from collections import Counter
from enum import Enum, auto
from functools import total_ordering

from common import read_lines


class Card(int, Enum):
    two = auto()
    three = auto()
    four = auto()
    five = auto()
    six = auto()
    seven = auto()
    eight = auto()
    nine = auto()
    T = auto()
    J = auto()
    Q = auto()
    K = auto()
    A = auto()

    @classmethod
    def from_string(cls, c) -> Card:
        match c:
            case "2":
                return Card.two
            case "3":
                return Card.three
            case "4":
                return Card.four
            case "5":
                return Card.five
            case "6":
                return Card.six
            case "7":
                return Card.seven
            case "8":
                return Card.eight
            case "9":
                return Card.nine
            case "T":
                return Card.T
            case "J":
                return Card.J
            case "Q":
                return Card.Q
            case "K":
                return Card.K
            case "A":
                return Card.A
        raise ValueError(f"Symbol doesnt match a card: {c}")


class HandType(int, Enum):
    HighCard = auto()
    OnePair = auto()
    TwoPair = auto()
    ThreeOfAKind = auto()
    FullHouse = auto()
    FourOfAKind = auto()
    FiveOfAKind = auto()


@total_ordering
class Hand:
    _cards: tuple[Card, Card, Card, Card, Card]

    def __init__(self, *args: Card):
        if len(args) != 5:
            raise ValueError(f"Not enough card symbols - expected 5 - got {len(args)}")
        self._cards = args  # type: ignore

    def __iter__(self):
        return iter(self._cards)

    def __repr__(self):
        return f"Hand({','.join(repr(c) for c in self._cards)})"

    def __str__(self):
        return f"{hand_type(self).name} - {''.join(c.name for c in self._cards)}"

    def __eq__(self, other):
        if not isinstance(other, Hand):
            raise RuntimeError("Cant compare another object")
        return self._cards == other._cards

    def __lt__(self, other):
        if not isinstance(other, Hand):
            raise RuntimeError("Hand can only be compared to Hand")
        self_type = hand_type(self)
        other_type = hand_type(other)
        if self_type < other_type:
            return True
        if self_type == other_type:
            for self_card, other_card in zip(self._cards, other._cards):
                if self_card < other_card:
                    return True
                if self_card.value > other_card:
                    break
        return False

    @classmethod
    def from_string(cls, card_part: str) -> Hand:
        return cls(*(Card.from_string(c) for c in card_part))


def hand_type(hand: Hand) -> HandType:
    card_counts = Counter(hand)

    unique_card_count = len(card_counts)
    max_duplicates = max(card_counts.values())

    if unique_card_count == 1:
        return HandType.FiveOfAKind
    if unique_card_count == 2 and max_duplicates == 4:
        return HandType.FourOfAKind
    if unique_card_count == 2 and max_duplicates == 3:
        return HandType.FullHouse
    if unique_card_count == 3 and max_duplicates == 3:
        return HandType.ThreeOfAKind
    if unique_card_count == 3 and max_duplicates == 2:
        return HandType.TwoPair
    if unique_card_count == 4:
        return HandType.OnePair
    if unique_card_count == 5:
        return HandType.HighCard
    raise RuntimeError("This doesn't seem to be a valid hand")


@dataclasses.dataclass
class HandAndBid:
    hand: Hand
    bid: int

    def __str__(self):
        return f"{self.hand} - {self.bid}"


def parse(line: str) -> HandAndBid:
    card_part, raw_bid = line.split(" ")
    return HandAndBid(hand=Hand.from_string(card_part), bid=int(raw_bid))


def solve_part_one() -> int:
    return solve_part_one_for_file("./src/day07/input.txt")


def solve_part_one_for_file(file_path) -> int:
    lines = read_lines(file_path)
    hands = [parse(line) for line in lines]
    hands_and_rank = enumerate(sorted(hands, key=lambda h: h.hand))
    return sum((rank + 1) * hand.bid for rank, hand in hands_and_rank)
