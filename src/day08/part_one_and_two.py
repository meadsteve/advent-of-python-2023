from __future__ import annotations
import dataclasses
import itertools
from enum import Enum, auto
from functools import cache
from typing import Iterator, Iterable, Callable

from common import read_lines
from common_maths import smallest_common_multiple


class Direction(Enum):
    left = auto()
    right = auto()


@dataclasses.dataclass
class InfiniteDirections:
    looped: tuple[Direction, ...]

    def __init__(self, *args: Direction):
        self.looped = args

    def __iter__(self) -> Iterator[Direction]:
        return itertools.cycle(self.looped)


NodeId = str


@dataclasses.dataclass
class Node:
    label: NodeId
    left: NodeId
    right: NodeId

    def __hash__(self):
        return hash(self.label)

    @classmethod
    def from_string(cls, raw_string: str) -> Node:
        # NNN = (LLL, RRR)
        (label, raw_links) = raw_string.split(" = ")
        left, right = raw_links.strip("()").split(", ")
        return cls(label=label, left=left, right=right)


class NodeMap:
    _map: dict[NodeId, Node]

    def __init__(self, *args: Node):
        self._map = {n.label: n for n in args}

    def add_node(self, node: Node):
        self._map[node.label] = node

    def __getitem__(self, label):
        return self._map[label]

    def __eq__(self, other):
        return isinstance(other, NodeMap) and self._map == other._map

    @property
    def all(self) -> Iterable[NodeId]:
        return [n.label for n in self._map.values()]

    def __hash__(self):
        return id(self)

    @cache
    def next_node(self, node_id: NodeId, direction: Direction) -> NodeId:
        node = self._map[node_id]
        match direction:
            case Direction.left:
                return self._map[node.left].label
            case Direction.right:
                return self._map[node.right].label
        raise Exception("Not sure how we got here")


def parse(input_data: Iterable[str]) -> tuple[InfiniteDirections, NodeMap]:
    lines = iter(input_data)
    direction_part = next(lines)
    directions = [
        Direction.left if d == "L" else Direction.right for d in direction_part
    ]
    next(lines)  # the blank line
    nodes = NodeMap()
    for node_string in lines:
        nodes.add_node(Node.from_string(node_string))
    return InfiniteDirections(*directions), nodes


def steps_required(
    directions: InfiniteDirections,
    node_map: NodeMap,
    *,
    from_start: str = "AAA",
    end_condition: Callable[[NodeId], bool] = lambda n: n == "ZZZ",
) -> tuple[int, NodeId]:
    steps_taken = 0
    node = from_start
    for direction in directions:
        node = node_map.next_node(node, direction)
        steps_taken += 1
        if steps_taken > 9_000_000_000_000:
            raise RuntimeError("Too tired. Too many steps.")
        if end_condition(node):
            return steps_taken, node
    raise Exception("I'm not sure how we got here")


def multiverse_steps_required(directions: InfiniteDirections, node_map: NodeMap) -> int:
    nodes = [node for node in node_map.all if node.endswith("A")]
    first_end_met = [
        steps_required(
            directions,
            node_map,
            from_start=node,
            end_condition=lambda n: n.endswith("Z"),
        )
        for node in nodes
    ]
    loop_lengths = [
        steps_required(
            directions,
            node_map,
            from_start=final_node,
            end_condition=lambda n: n == final_node,
        )
        for _, final_node in first_end_met
    ]
    if not all(
        first == loop for ((first, _), (loop, _)) in zip(first_end_met, loop_lengths)
    ):
        raise RuntimeError(
            "Case where the loop isn't the same length as getting to the loop not implemented"
        )
    return smallest_common_multiple(n for n, _ in loop_lengths)


def solve_part_one() -> int:
    lines = read_lines("./src/day08/input.txt")
    directions, nodes = parse(lines)
    steps, _final_node = steps_required(directions, nodes)
    return steps


def solve_part_two() -> int:
    lines = read_lines("./src/day08/input.txt")
    directions, nodes = parse(lines)
    return multiverse_steps_required(directions, nodes)
