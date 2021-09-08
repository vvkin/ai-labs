class Direction:
    WEST = -2
    SOUTH = -1
    STOP = 0
    NORTH = 1
    EAST = 2

DIRECTIONS = {
    Direction.NORTH: (0, 1),
    Direction.SOUTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.WEST: (-1, 0),
    Direction.STOP: (0, 0),
}
