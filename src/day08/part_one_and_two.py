from __future__ import annotations
import dataclasses
import itertools
from enum import Enum, auto
from functools import cache
from typing import Iterator, Iterable

from common import read_lines


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


def steps_required(directions: InfiniteDirections, node_map: NodeMap) -> int:
    steps_taken = 0
    node = "AAA"
    for direction in directions:
        node = node_map.next_node(node, direction)
        steps_taken += 1
        if steps_taken > 9_000_000_000_000:
            raise RuntimeError("Too tired. Too many steps.")
        if node == "ZZZ":
            return steps_taken
    raise Exception("I'm not sure how we got here")


def multiverse_steps_required(directions: InfiniteDirections, node_map: NodeMap) -> int:
    steps_taken = 0
    nodes = [node for node in node_map.all if node.endswith("A")]
    for direction in directions:
        nodes = [node_map.next_node(node, direction) for node in nodes]
        steps_taken += 1
        if steps_taken > 9_000_000_000_000_000_000:
            raise RuntimeError("Too tired. Too many steps.")
        if all(node.endswith("Z") for node in nodes):
            return steps_taken
    raise Exception("I'm not sure how we got here")


def solve_part_one() -> int:
    lines = read_lines("./src/day08/input.txt")
    directions, nodes = parse(lines)
    return steps_required(directions, nodes)


def solve_part_two() -> int:
    lines = read_lines("./src/day08/input.txt")
    directions, nodes = parse(lines)
    return multiverse_steps_required(directions, nodes)


if __name__ == "__main__":
    print(solve_part_two())
