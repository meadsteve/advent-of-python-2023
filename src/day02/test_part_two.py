from day02.part_one_and_two import (
    Color,
    Draw,
    Game,
    solve_part_two,
)


def test_it_can_get_the_power_of_a_game():
    assert (
        Game(
            game_id=13,
            draws=[
                Draw(cubes={Color.red: 4, Color.blue: 3}),
                Draw(cubes={Color.red: 6, Color.blue: 2}),
                Draw(cubes={Color.green: 2}),
            ],
        ).power
        == 6 * 3 * 2
    )


def test_it_can_solve_part_two():
    assert solve_part_two() == 70924
