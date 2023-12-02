from __future__ import annotations

import dataclasses
from enum import Enum
from typing import Collection, Mapping

from common import read_lines


class Color(str, Enum):
    red = "red"
    green = "green"
    blue = "blue"


CubeCollection = Mapping[Color, int]


@dataclasses.dataclass
class Game:
    game_id: int
    draws: list[Draw]

    def is_possible_from(self, cube_collection: CubeCollection) -> bool:
        return biggest_draw_possible(self.draws).is_possible_from(cube_collection)

    @property
    def power(self) -> int:
        x = 1
        for _, y in biggest_draw_possible(self.draws).cubes.items():
            x = x * y
        return x


@dataclasses.dataclass
class Draw:
    cubes: CubeCollection

    @classmethod
    def from_raw_string(cls, draw_string: str) -> Draw:
        cubes = {}
        for part in draw_string.split(", "):
            num_string, color_string = part.split(" ")
            cubes[Color(color_string)] = int(num_string)
        return cls(cubes=cubes)

    def is_possible_from(self, collection: CubeCollection) -> bool:
        for color, size in self.cubes.items():
            if color not in collection:
                return False
            if size > collection[color]:
                return False
        return True


def parse_line(line: str) -> Game:
    game_part, draw_part = line.split(": ")
    _, raw_game_id = game_part.split(" ")
    draws = [Draw.from_raw_string(draw) for draw in draw_part.split("; ")]
    return Game(game_id=int(raw_game_id), draws=draws)


def biggest_draw_possible(draws: Collection[Draw]) -> Draw:
    highest: dict[Color, int] = {Color.green: 0, Color.blue: 0, Color.red: 0}
    for draw in draws:
        for color, size in draw.cubes.items():
            if size > highest[color]:
                highest[color] = size
    return Draw(cubes=highest)


def solve_part_one() -> int:
    lines = read_lines("./src/day02/input.txt")
    games = (parse_line(line) for line in lines)
    possible_games = (
        game
        for game in games
        if game.is_possible_from({Color.red: 12, Color.green: 13, Color.blue: 14})
    )
    return sum(game.game_id for game in possible_games)


def solve_part_two() -> int:
    lines = read_lines("./src/day02/input.txt")
    games = (parse_line(line) for line in lines)
    return sum(game.power for game in games)
