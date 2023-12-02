from day02.part_one import Color, Draw, parse_line, biggest_draw_possible, Game, solve_part_one


def test_a_draw_can_be_parsed():
    assert Draw.from_raw_string("3 blue, 4 red, 1 green") == Draw(
        cubes={Color.red: 4, Color.blue: 3, Color.green: 1}
    )


def test_a_draw_can_be_parsed_without_all_three_colors():
    assert Draw.from_raw_string("3 blue, 4 red") == Draw(
        cubes={Color.red: 4, Color.blue: 3}
    )


def test_a_line_can_be_parsed():
    assert parse_line("Game 34: 3 blue, 4 red; 1 green") == Game(
        game_id=34,
        draws=[
            Draw(cubes={Color.red: 4, Color.blue: 3}),
            Draw(cubes={Color.green: 1}),
        ],
    )


def test_from_a_series_of_draws_the_largest_of_each_number_can_be_found():
    assert biggest_draw_possible(
        [
            Draw(cubes={Color.red: 4, Color.blue: 3}),
            Draw(cubes={Color.green: 1}),
            Draw(cubes={Color.green: 2, Color.blue: 3}),
            Draw(cubes={Color.green: 1, Color.red: 5}),
        ]
    ) == Draw(cubes={Color.green: 2, Color.blue: 3, Color.red: 5})


def test_it_can_indicate_if_a_draw_is_possible_from_a_collection():
    collection = {Color.green: 10, Color.blue: 10, Color.red: 10}
    assert Draw(cubes={Color.green: 2, Color.blue: 3, Color.red: 5}).is_possible_from(
        collection
    )
    assert not Draw(
        cubes={Color.green: 21, Color.blue: 3, Color.red: 5}
    ).is_possible_from(collection)


def test_it_can_indicate_if_a_game_is_possible_from_a_collection():
    some_game = Game(
        game_id=13,
        draws=[
            Draw(cubes={Color.red: 4, Color.blue: 3}),
            Draw(cubes={Color.red: 6, Color.blue: 2}),
            Draw(cubes={Color.green: 1}),
        ],
    )
    assert some_game.is_possible_from({Color.green: 10, Color.blue: 10, Color.red: 10})
    assert not some_game.is_possible_from(
        {Color.green: 10, Color.blue: 10, Color.red: 5}
    )


def test_it_can_solve_part_one():
    assert solve_part_one() == 2771
