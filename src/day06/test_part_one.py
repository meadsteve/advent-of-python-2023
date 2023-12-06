from day06.part_one import RaceData, winning_acceleration_times, solve_part_one


def test_it_calculates_the_winning_values():
    assert list(
        winning_acceleration_times(RaceData(time_allowed=7, distance_record=9))
    ) == [
        2,
        3,
        4,
        5,
    ]
    assert list(
        winning_acceleration_times(RaceData(time_allowed=15, distance_record=40))
    ) == [
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
    ]


def test_it_will_never_exceed_the_time():
    assert (
        max(winning_acceleration_times(RaceData(time_allowed=100, distance_record=3)))
        <= 100
    )


def test_an_impossible_race_is_just_an_empty_result():
    assert (
        winning_acceleration_times(RaceData(time_allowed=1, distance_record=30)) == []
    )


def test_it_can_solve_part_one():
    assert solve_part_one() == 74698
