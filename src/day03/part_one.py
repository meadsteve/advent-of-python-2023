import dataclasses
from typing import Iterator, Sequence, Mapping, Iterable

SchematicCell = int | str
Grid = Sequence[Sequence[SchematicCell]]
Position = tuple[int, int]

PartLocationId = int
PartNumber = int


def is_symbol(piece: SchematicCell):
    if isinstance(piece, int):
        return False
    if piece == ".":
        return False
    return True


@dataclasses.dataclass
class Schematic:
    grid: Grid
    part_lookup: Mapping[PartLocationId, PartNumber]

    def get_part_ids_next_to_symbol(self) -> set[int]:
        results = set()
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[0])):
                piece = self.grid[y][x]
                if is_symbol(piece):
                    neighbours = get_neighbours(self.grid, (x, y))
                    for neighbour in neighbours:
                        if isinstance(neighbour, int) and neighbour in self.part_lookup:
                            results.add(self.part_lookup[neighbour])
        return results


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
