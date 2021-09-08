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

    def count(self, value: bool = True) -> int:
        return (self.data == value).sum()
