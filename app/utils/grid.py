import numpy as np
from collections import defaultdict
from numpy.lib.function_base import copy

from app.config.const.geometry import Direction
from app.config.types import Point
from app.utils.structures import Queue
from app.utils.geometry import add_points, normalize_point
from app.utils.geometry import adjlist_to_adjmatrix


TO_VECTOR = {
    Direction.NORTH: (0, 1),
    Direction.SOUTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.WEST: (-1, 0),
    Direction.STOP: (0, 0),
}

class Grid:
    def __init__(self, width: int, height: int, value: bool = False) -> None:
        self.width = width
        self.height = height
        self.value = value
        self.data = np.full((self.width, self.height), self.value)
    
    @classmethod
    def from_data(cls, data: np.ndarray) -> None:
        width, height = data.shape
        instance = Grid(width, height)
        instance.data = data
        return instance
    
    def __getitem__(self, idx: int) -> bool:
        return self.data[idx]

    def __setitem__(self, key: int, item: bool) -> None:
        self.data[key] = item
    
    def is_valid_coord(self, x: int, y: int) -> bool:
        return (x >= 0 and y >= 0) and\
            (x < self.width and y < self.height)
    
    def get_points(self, value: bool = True) -> list[Point]:
        return [(x, y) for x in range(self.width)
            for y in range(self.height)
            if self.data[x][y] == value
        ]
    
    def count(self, value: bool = True) -> int:
        return (self.data == value).sum()
    
    def get_adjlist(self):
        adjlist = defaultdict(list)
        visited = set()

        for start in self.get_points(False):
            queue = Queue()
            queue.enque(start)

            while not queue.is_empty():
                parent = queue.deque()
                if parent in visited:
                    continue
                visited.add(parent)

                for neighbor in self.get_neighbors(parent):
                    queue.enque(neighbor)
                    adjlist[parent].append((neighbor, 1))
        return adjlist
    
    def get_neighbors(self, position: Point) -> list[Point]:
        neighbors = []
        for move in TO_VECTOR.values():
            x, y = normalize_point(add_points(position, move))
            if not self.data[x][y]:
                neighbors.append((x, y))
        return neighbors
  
    def get_adjmatrix(self):
        adjlist = self.get_adjlist()
        return adjlist_to_adjmatrix(adjlist)
