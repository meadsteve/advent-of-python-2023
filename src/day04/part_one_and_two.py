import dataclasses
from typing import Sequence, Mapping

from common import read_lines

CardId = int

NumberCollection = Sequence[int]


@dataclasses.dataclass
class Row:
    card_id: CardId
    numbers: NumberCollection
    winning_numbers: NumberCollection
    score: int
    number_of_matches: int

    def __init__(
        self,
        *,
        card_id: int,
        numbers: NumberCollection,
        winning_numbers: NumberCollection,
    ):
        self.card_id = card_id
        self.numbers = numbers
        self.winning_numbers = winning_numbers

        # Pre-calc some stuff
        _winning_set = set(winning_numbers)
        self.number_of_matches = sum(1 for n in self.numbers if n in _winning_set)
        self.score = (
            2 ** (self.number_of_matches - 1) if self.number_of_matches > 0 else 0
        )


@dataclasses.dataclass
class CardStack:
    card: Row
    number: int


class CardScratcher:
    cards: Mapping[CardId, CardStack]

    def __init__(self, cards: Sequence[Row]):
        self.cards = {c.card_id: CardStack(card=c, number=1) for c in cards}

    def scratch(self) -> int:
        cards_scratched = 0
        for card_id in range(1, len(self.cards) + 1):
            stack = self.cards[card_id]
            cards_scratched += stack.number
            for winner_id in self._get_winnings(stack.card):
                self.cards[winner_id].number += stack.number
        return cards_scratched

    def _get_winnings(self, card: Row) -> Sequence[CardId]:
        amount = card.number_of_matches
        after = card.card_id
        if amount == 0:
            return []
        start = after + 1
        end = min(start + amount, len(self.cards) + 1)
        return range(start, end)


def parse_row(row: str) -> Row:
    id_part, number_part = row.split(": ")
    raw_card_id = id_part.split(" ")[-1]
    raw_card_numbers, raw_winning_numbers = number_part.split("|")
    return Row(
        card_id=int(raw_card_id),
        numbers=_parse_number_string(raw_card_numbers),
        winning_numbers=_parse_number_string(raw_winning_numbers),
    )


def solve_part_one() -> int:
    lines = read_lines("./src/day04/input.txt")
    rows = (parse_row(line) for line in lines)
    return sum(row.score for row in rows)


def solve_part_two() -> int:
    lines = read_lines("./src/day04/input.txt")
    rows = [parse_row(line) for line in lines]
    scratcher = CardScratcher(rows)
    return scratcher.scratch()


def _parse_number_string(number_string: str) -> list[int]:
    raw_numbers = (n.strip() for n in number_string.split(" "))
    filtered_numbers = (n for n in raw_numbers if n != "")
    return list(int(n) for n in filtered_numbers)
