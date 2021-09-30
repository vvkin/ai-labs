from dataclasses import dataclass, field
from typing import Callable

from app.pacman.domain.agent import Actions
from app.config.const.geometry import Direction
from app.config.types import Point, Vector
from app.utils.geometry import add_points, normalize_point
from app.pacman.search.algorithms import bfs, dfs, ucs
from app.pacman.search.problem import Problem

class PacmanSearchProblem(Problem):
    def update(self, state) -> None:
        self._walls = state.get_walls()
        self._goal = state.get_food()[0]
        self._start = state.get_pacman_position()
    
    def get_start(self) -> Point:
        return self._start

    def get_goal(self) -> Point:
        return self._goal

    def get_neighbors(self, pos: Point) -> list[Point, float]:
        neighbors = []
        for action in Direction.as_list():
            vector = Actions.direction_to_vector(action)
            next = normalize_point(add_points(pos, vector))
            next_x, next_y = next
            if not self._walls[next_x][next_y]:
                cost = self.cost_fn(next)
                neighbors.append((next, cost))
        return neighbors

@dataclass
class PacmanSearch:
    problem: PacmanSearchProblem
    fns: list[Callable] = field(default_factory=lambda: [bfs, dfs, ucs])
    keys: list[str] = field(default_factory=lambda: ['z', 'Z'])
    path: list[Vector] = field(default_factory=list)
    prev_idx: int = -1
    idx: int = 0

    def key_pressed(self) -> bool:
        return self.prev_idx != self.idx

    def handle_key(self, state) -> None:
        if any(key for key in self.keys if key in state.keys_pressed()):
            self.idx = (self.idx + 1) % len(self.fns)

    def update(self, state) -> None:
        self.problem.update(state)
        if self.problem.get_goal():
            self.prev_idx = self.idx
            self.path = self.fns[self.idx](self.problem)
