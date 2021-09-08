from utils.vector import Vector
from enum import Enum, auto

# auto() increments by one

class Direction(Enum):
    WEST = -2
    SOUTH = auto()
    STOP = auto()
    NORTH = auto()
    EAST = auto()

DIRECTIONS = {
    Direction.NORTH: Vector(0, 1),
    Direction.SOUTH: Vector(0, -1),
    Direction.STOP: Vector(1, 0),
    Direction.NORTH: Vector(-1, 0),
    Direction.EAST: Vector(0, 0)
}
