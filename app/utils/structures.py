import heapq
import numpy as np
from dataclasses import dataclass
from collections import deque
from typing import Mapping, Union, Any

from app.config.types import Point

class BaseDeque:
    def __init__(self) -> None:
        self._data = deque()
    
    def is_empty(self) -> bool:
        return len(self._data) == 0

class Queue(BaseDeque):
    def enque(self, item: Any) -> None:
        self._data.append(item)

    def deque(self) -> Any:
        return self._data.popleft()


class Stack(BaseDeque):
    def push(self, item: Any) -> None:
        self._data.append(item)
    
    def pop(self) -> Any:
        return self._data.pop()


class PriorityQueue:
    def __init__(self) -> None:
        self._heap = []

    def enque(self, item: Any, priority: float) -> None:
        heapq.heappush(self._heap, (priority, item))

    def deque(self) -> tuple[Any, float]:
        priority, item = heapq.heappop(self._heap)
        return item, priority

    def is_empty(self) -> bool:
        return len(self._heap) == 0

@dataclass(eq=False)
class DistanceMemory:
    dist: np.ndarray
    mapping: dict[Point, int]
    goal_idxs: dict[int, int]

    def get(self, start: Point, end: Point) -> Union[float, int]:
        row_idx = self.goal_idxs[self.mapping[end]]
        column_idx = self.mapping[start]
        return self.dist[row_idx, column_idx]

class IndexDict:
    def __init__(self) -> None:
        self.idx = 0
        self.data = dict()

    def __getitem__(self, position: Point) -> int:
        idx = self.data.get(position, self.idx)
        if idx == self.idx:
            self.idx = idx + 1
            self.data[position] = idx
        return idx

    def as_dict(self) -> dict[Point, int]:
        return self.data

class MazeDistance:
    def __init__(self, maze_dists: np.ndarray, mapping, goal_mapping) -> None:
        self.maze_dists = maze_dists
        self.mapping = mapping
        self.goal_mapping = goal_mapping

    def get(self, start: Point, end: Point) -> float:
        end = self.mapping[end]
        if self.goal_mapping is not None:
            end = self.goal_mapping[end]
        start = self.mapping[start]
        return self.maze_dists[end, start]
