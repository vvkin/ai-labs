import heapq
from collections import deque
from typing import Any

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
