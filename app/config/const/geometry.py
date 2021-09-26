class Direction:
    WEST = -2
    SOUTH = -1
    STOP = 0
    NORTH = 1
    EAST = 2
    
    @staticmethod
    def as_list(with_stop: bool = False):
        directions = [
            Direction.WEST,
            Direction.SOUTH,
            Direction.NORTH,
            Direction.EAST,
        ]
        if with_stop:
            directions += [Direction.STOP]
        return directions

DIRECTIONS = {
    Direction.NORTH: (0, 1),
    Direction.SOUTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.WEST: (-1, 0),
    Direction.STOP: (0, 0),
}
