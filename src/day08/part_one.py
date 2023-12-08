from __future__ import annotations
import dataclasses
import itertools
from enum import Enum
from typing import Mapping, Iterator, Iterable

from common import read_lines


class Direction(str, Enum):
    left = "left"
    right = "right"


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

    @classmethod
    def from_string(cls, raw_string: str) -> Node:
        # NNN = (LLL, RRR)
        (label, raw_links) = raw_string.split(" = ")
        left, right = raw_links.strip("()").split(", ")
        return cls(label=label, left=left, right=right)


Nodes = Mapping[NodeId, Node]


def parse(input_data: Iterable[str]) -> tuple[InfiniteDirections, Nodes]:
    lines = iter(input_data)
    direction_part = next(lines)
    directions = [
        Direction.left if d == "L" else Direction.right for d in direction_part
    ]
    next(lines)  # the blank line
    nodes = {}
    for node_string in lines:
        node = Node.from_string(node_string)
        nodes[node.label] = node
    return InfiniteDirections(*directions), nodes


def steps_required(directions: InfiniteDirections, nodes: Nodes) -> int:
    steps_taken = 0
    node = nodes["AAA"]
    for direction in directions:
        match direction:
            case Direction.left:
                node = nodes[node.left]
            case Direction.right:
                node = nodes[node.right]
        steps_taken += 1
        if steps_taken > 9_000_000_000_000:
            raise RuntimeError("Too tired. Too many steps.")
        if node.label == "ZZZ":
            return steps_taken
    raise Exception("I'm not sure how we got here")


def solve_part_one() -> int:
    lines = read_lines("./src/day08/input.txt")
    directions, nodes = parse(lines)
    return steps_required(directions, nodes)
