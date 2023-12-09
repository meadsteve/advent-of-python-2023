from day08.part_one_and_two import multiverse_steps_required, parse, solve_part_two


def test_it_works_for_another_example():
    directions, nodes = parse(
        """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""".split(
            "\n"
        )
    )

    assert multiverse_steps_required(directions, nodes) == 6


def test_it_solves_part_two():
    assert solve_part_two() == 8906539031197
