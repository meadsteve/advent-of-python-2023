from day04.part_one_and_two import parse_row, solve_part_two, CardScratcher


def test_on_the_given_example():
    scratcher = CardScratcher(
        [
            parse_row("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"),
            parse_row("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19"),
            parse_row("Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1"),
            parse_row("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83"),
            parse_row("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36"),
            parse_row("Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"),
        ]
    )

    assert scratcher.scratch() == 30


def test_a_tweaked_example():
    scratcher = CardScratcher(
        [
            parse_row("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"),
            parse_row("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19"),
            parse_row("Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1"),
            parse_row("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83"),
            parse_row("Card 5: 87 83 26 28 32 | 87 30 70 12 93 22 82 36"),
            parse_row("Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"),
        ]
    )

    assert scratcher.scratch() == 44


def test_it_can_solve_part_two():
    assert solve_part_two() == 6189740
