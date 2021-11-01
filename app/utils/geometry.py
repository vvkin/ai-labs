from dataclasses import dataclass
from typing import Generator

from app.config.types import Point, Vector

@dataclass(order=True, unsafe_hash=True)
class Point:
    x: float
    y: float

    def as_int(self) -> "Point":
        return Point(int(self.x), int(self.y))

    def __add__(self, other: "Point") -> "Point":
        return Point(
            self.x + other.x,
            self.y + other.y
        )
    
    def __mul__(self, scalar: float) -> "Point":
        return Point(
            self.x * scalar,
            self.y * scalar
        )
    
    def __truediv__(self, scalar: float) -> "Point":
        return Point(
            self.x / scalar,
            self.y / scalar
        )
    
    def __floordiv__(self, scalar: float) -> "Point":
        return (self / scalar).as_int()
    
    def __iter__(self) -> Generator[float, None, None]:
        yield self.x
        yield self.y


def add_points(x: Point, y: Point) -> Point:
    return (x[0] + y[0], x[1] + y[1])


def divide_point(point: Point, value: float) -> Point:
    x, y = point
    return (x / value, y / value)


def manhattan_distance(this: Point, other: Point) -> float:
    x1, y1 = this
    x2, y2 = other
    return abs(x1 - x2) + abs(y1 - y2)


def get_nearest_point(position: Vector) -> Point:
    (row, col) = position
    grid_row = int(row + 0.5)
    grid_col = int(col + 0.5)
    return (grid_row, grid_col)


def normalize_point(point: Point) -> Point:
    return (int(point[0]), int(point[1]))
