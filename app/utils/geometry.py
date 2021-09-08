def manhattan_distance(
    point1: tuple[float, float], point2: tuple[float, float]
) -> float:
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)


def get_nearest_point(position: tuple[float, float]) -> tuple[float, float]:
    (row, col) = position
    grid_row = int(row + 0.5)
    grid_col = int(col + 0.5)
    return (grid_row, grid_col)
