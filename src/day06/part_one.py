import dataclasses
import math
from typing import Collection, Iterable

from common import multiply_together, iterator_length


@dataclasses.dataclass
class RaceData:
    time_allowed: int
    distance_record: int


def winning_acceleration_times(race: RaceData) -> Iterable[int]:
    winning_distance = race.distance_record + 1  # We've got to beat it by one

    # Thanks quadratic formula
    try:
        sqrt_part = math.sqrt((race.time_allowed**2) - (4 * winning_distance))
    except ValueError:
        return []
    lower_bound = math.ceil((race.time_allowed - sqrt_part) / 2)
    upper_bound = math.floor((race.time_allowed + sqrt_part) / 2)

    # These help with debugging but can be removed
    _validate_answer(lower_bound, race)
    _validate_answer(lower_bound, race)

    return range(lower_bound, upper_bound + 1)


def _validate_answer(acceleration_time: int, race: RaceData):
    if acceleration_time <= 0:
        raise ValueError("Negative acceleration time - whoops")
    if acceleration_time >= race.time_allowed:
        raise ValueError("Spent too long accelerating")
    speed = acceleration_time
    distance_covered = speed * (race.time_allowed - acceleration_time)
    if distance_covered <= race.distance_record:
        raise ValueError("We didn't go far enough")


# TODO: use human hands to update input if it changes
# Time:        41     66     72     66
# Distance:   244   1047   1228   1040
input_data: Collection[RaceData] = (
    RaceData(time_allowed=41, distance_record=244),
    RaceData(time_allowed=66, distance_record=1047),
    RaceData(time_allowed=72, distance_record=1228),
    RaceData(time_allowed=66, distance_record=1040),
)


def solve_part_one() -> int:
    winning_options = (
        iterator_length(winning_acceleration_times(race)) for race in input_data
    )
    return multiply_together(winning_options)
