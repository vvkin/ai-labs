from app.config.types import Point, Vector


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
    return (round(point[0]), round(point[1]))


def add_points(x: Point, y: Point) -> Point:
    return (x[0] + y[0], x[1] + y[1])