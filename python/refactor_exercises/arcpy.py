from dataclasses import dataclass
from typing import List, Union


@dataclass
class Point:
    ID: int
    X: float
    Y: float


@dataclass
class Array:
    items: List[Point]


@dataclass
class Polygon:
    inputs: Union[Point, Array]
