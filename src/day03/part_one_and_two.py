import dataclasses
from typing import Iterator, Sequence, Mapping, Iterable

from common import read_lines

SchematicCell = int | str
Grid = Sequence[Sequence[SchematicCell]]
Position = tuple[int, int]

PartLocationId = int
PartNumber = int


@dataclasses.dataclass
class Schematic:
    grid: Grid
    part_lookup: Mapping[PartLocationId, PartNumber]

    def get_part_ids_next_to_symbol(self) -> list[int]:
        part_location_ids = set()
        for piece, position in self._pieces(pick_if=is_symbol):
            neighbours = get_neighbours(self.grid, position)
            for neighbour in neighbours:
                if isinstance(neighbour, int) and neighbour in self.part_lookup:
                    part_location_ids.add(neighbour)
        return [self.part_lookup[location_id] for location_id in part_location_ids]

    def get_gears(self) -> Iterable[tuple[int, int]]:
        for piece, position in self._pieces(pick_if=is_gear_symbol):
            part_number_neighbours = get_part_number_neighbours(self.grid, position)
            if len(part_number_neighbours) == 2:
                yield tuple(self.part_lookup[x] for x in part_number_neighbours)  # type: ignore

    def _pieces(
        self, *, pick_if=lambda piece: True
    ) -> Iterable[tuple[SchematicCell, Position]]:
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[0])):
                piece = self.grid[y][x]
                if pick_if(piece):
                    yield piece, (x, y)


def is_symbol(piece: SchematicCell):
    if isinstance(piece, int):
        return False
    if piece == ".":
        return False
    return True


def is_gear_symbol(piece: SchematicCell):
    return piece == "*"


def parse_schematic(lines: Iterable[str]) -> Schematic:
    grid = []
    part_lookup = {}
    current_part_location = 0
    for line in lines:
        grid_row: list[str | int] = []
        current_part_number = ""
        for char in line:
            if char.isdigit():
                grid_row.append(current_part_location)
                current_part_number = current_part_number + char
            else:
                grid_row.append(char)
                if current_part_number != "":
                    part_lookup[current_part_location] = int(current_part_number)
                    current_part_number = ""
                    current_part_location += 1
        if current_part_number != "":
            part_lookup[current_part_location] = int(current_part_number)
            current_part_location += 1
        grid.append(grid_row)
    return Schematic(grid=grid, part_lookup=part_lookup)


def get_neighbours(grid: Grid, position: Position) -> Iterator[SchematicCell]:
    base_x, base_y = position
    for offset_x in range(-1, 2):
        for offset_y in range(-1, 2):
            x = base_x + offset_x
            y = base_y + offset_y
            # This is the square itself - skip it
            if x == base_x and y == base_y:
                continue
            # we've fallen off the grid - skip it
            if x < 0 or y < 0 or y >= len(grid) or x >= len(grid[y]):
                continue
            yield grid[y][x]


def get_part_number_neighbours(grid: Grid, position: Position) -> set[int]:
    neighbours = get_neighbours(grid, position)
    return set(neighbour for neighbour in neighbours if isinstance(neighbour, int))


def solve_part_one() -> int:
    lines = read_lines("./src/day03/input.txt")
    schema = parse_schematic(lines)
    return sum(schema.get_part_ids_next_to_symbol())


def solve_part_two() -> int:
    lines = read_lines("./src/day03/input.txt")
    schema = parse_schematic(lines)
    return sum(x * y for (x, y) in schema.get_gears())
