class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    def to_int(self, ceil: bool = False) -> "Vector":
        dx = dy = 0.5 if ceil else 0
        return Vector(int(self.x + dx), int(self.y + dy))
    
    def manhattan(self, other: "Vector") -> float:
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def magnitude(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def nearest(self) -> "Vector":
        return self.to_int(ceil=True)
