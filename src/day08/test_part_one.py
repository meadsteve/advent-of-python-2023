from day08.part_one import (
    Direction,
    InfiniteDirections,
    Node,
    parse,
    steps_required,
    solve_part_one,
)


def test_it_parses_a_basic_block():
    example = """RL

AAA = (ZZZ, ZZZ)
ZZZ = (ZZZ, ZZZ)""".split(
        "\n"
    )

    assert parse(example) == (
        InfiniteDirections(Direction.right, Direction.left),
        {
            "AAA": Node(label="AAA", left="ZZZ", right="ZZZ"),
            "ZZZ": Node(label="ZZZ", left="ZZZ", right="ZZZ"),
        },
    )


def test_it_calculates_the_number_of_steps_needed_for_the_example():
    directions, nodes = parse(
        """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""".split(
            "\n"
        )
    )

    assert steps_required(directions, nodes) == 2


def test_it_works_for_another_example():
    directions, nodes = parse(
        """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""".split(
            "\n"
        )
    )

    assert steps_required(directions, nodes) == 6


def test_it_solves_part_one():
    assert solve_part_one() == 13939
