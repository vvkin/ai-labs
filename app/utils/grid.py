from app.config.types import Point
import numpy as np

class Grid:
    def __init__(self, width: int, height: int, value: bool = False) -> None:
        self.width = width
        self.height = height
        self.value = value
        self.data = np.full((self.width, self.height), self.value)
    
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
