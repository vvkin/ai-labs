from typing import Any, Union
from dataclasses import dataclass, InitVar

from .states import SearchState


@dataclass(eq=False)
class CostFn:
    game_state: InitVar[Any]

    def get_min_cost(self) -> Union[int, float]:
        raise NotImplementedError

    def __call__(self, state: SearchState) -> Union[int, float]:
        raise NotImplementedError


@dataclass(eq=False)
class UniformCostFn(CostFn):
    cost: int = 1

    def get_min_cost(self) -> int:
        return self.cost

    def __call__(self, state: SearchState) -> int:
        return self.cost


@dataclass(eq=False)
class FoodCostFn(CostFn):
    empty_cost: int = 2
    food_cost: int = 1

    def __post_init__(self, game_state: Any) -> None:
        self.food = game_state.get_food()

    def get_min_cost(self) -> int:
        return min(self.food_cost, self.empty_cost)

    def __call__(self, state: SearchState) -> int:
        x, y = state.position
        x_int, y_int = map(int, [x, y])
        return self.food_cost if self.food[x_int][y_int]\
            else self.empty_cost
