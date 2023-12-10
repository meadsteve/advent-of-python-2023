from day09.part_one import difference_sequence, all_zeros, next_number, solve_part_one


def test_a_function_that_gets_the_difference_sequence():
    assert difference_sequence([0, 3, 6, 9, 12, 15]) == [3, 3, 3, 3, 3]
    assert difference_sequence([3, 3, 3, 3, 3]) == [0, 0, 0, 0]


def test_a_useful_function_that_tells_us_if_all_of_something_is_zeroes():
    assert all_zeros([0, 0, 0, 0])
    assert not all_zeros([0, 3, 6, 9, 12, 15])


def test_a_function_to_predict_the_next_number():
    assert next_number([3, 3, 3, 3, 3]) == 3
    assert next_number([0, 3, 6, 9, 12, 15]) == 18
    assert next_number([10, 13, 16, 21, 30, 45]) == 68


def test_it_can_solve_part_one():
    assert solve_part_one() == 2043183816
