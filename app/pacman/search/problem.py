from typing import Callable

from app.config.types import Point, Vector


class Problem:
    def __init__(self, cost_fn: Callable = lambda _: 1) -> None:
        self.cost_fn = cost_fn

    def update(self) -> None:
        raise NotImplemented()

    def get_start(self) -> Vector:
        raise NotImplemented()

    def get_goal(self) -> bool:
        raise NotImplemented()

    def get_neighbors(self) -> list[Point, float]:
        raise NotImplemented()
