from dataclasses import dataclass
from app.config.types import Point


@dataclass(unsafe_hash=True, frozen=True)
class SearchState:
    position: Point

    def __lt__(self, other: "SearchState") -> bool:
        return self.position < other.position


@dataclass(unsafe_hash=True, frozen=True)
class AllFoodState(SearchState):
    rest: frozenset[Point]

    def __lt__(self, other: "AllFoodState") -> bool:
        return len(self.rest) < len(other.rest)
