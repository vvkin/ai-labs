from typing import Callable

from app.pacman.domain.agent import Actions
from app.config.const.geometry import Direction
from dataclasses import dataclass, field


from app.config.types import Vector
from app.pacman.search.algorithms import bfs, dfs, ucs
from app.pacman.search.problem import Problem


class PacmanSearchProblem(Problem):
    def update(self, state) -> None:
        self._walls = state.get_walls()
        self._goal = state.get_food()[0]
        self._start = state.get_pacman_position()
        print(self._goal)
    
    def get_start(self) -> Vector:
        return self._start

    def get_goal(self) -> bool:
        return self._goal
    
    def get_neighbors(self, position) -> list:
        neighbors = []
        for action in Direction.as_list():
            vector = Actions.direction_to_vector(action)
            next = (round(position[0] + vector[0]), round(position[1] + vector[1]))
            x, y = next
            if not self._walls[x][y]:
                cost = self.cost_fn(next)
                neighbors.append((next, cost))
        return neighbors

@dataclass
class PacmanSearch:
    problem: PacmanSearchProblem
    fns: list[Callable] = field(default_factory=lambda: [bfs, dfs, ucs])
    keys: list[str] = field(default_factory=lambda: ['z', 'Z'])
    path: list[Vector] = field(default_factory=list)
    idx: int = 0
    
    def key_pressed(self, state) -> bool:
        if any(key for key in self.keys if key in state.keys_pressed()):
            self.idx = (self.idx + 1) % len(self.fns)
            return True
        else: return False

    def update(self, state) -> None:
        self.problem.update(state)
        self.path = self.fns[self.idx](self.problem)
