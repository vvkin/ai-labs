import inspect
from functools import partial
from typing import Any, Callable
from app.config.types import Point

from app.pacman.search.problem import AllFoodProblem, PositionProblem, SearchProblem
from app.pacman.search.heuristics import all_food_heuristic, distance_heuristic
from app.pacman.search.algorithms import a_star
from app.pacman.domain.agent import Agent
from app.config.const.geometry import Direction


class SearchAgent(Agent):
    def __init__(
        self,
        search_fn: Callable,
        problem_type: SearchProblem,
        heuristic: Callable = None,
        **problem_kwargs: Any,
    ) -> None:
        self.problem_type = problem_type
        arg_names = inspect.getargs(heuristic)[0]
        self.search_fn =  partial(search_fn, heuristic=heuristic)\
            if "heuristic" in arg_names else search_fn
        self.problem_kwargs = problem_kwargs

    def get_action(self, game_state) -> int:
        if self.action_idx >= len(self.actions):
            return Direction.STOP
        idx = self.action_idx
        self.action_idx += 1
        return self.actions[idx]

    def register_state(self, game_state) -> None:
        kwargs = self.problem_kwargs if hasattr(self, "problem_kwargs") else {}
        problem = self.problem_type(game_state, **kwargs)
        self.action_idx = 0
        self.actions = self.search_fn(problem)

class PositionAgent(SearchAgent):
    def __init__(self, goal: Point) -> None:
        self.search_fn = partial(a_star, heuristic=distance_heuristic)
        self.problem_type = PositionProblem
        self.problem_kwargs = {"goal": goal}

class AllFoodAgent(SearchAgent):
    def __init__(self) -> None:
        self.search_fn = partial(a_star, heuristic=all_food_heuristic)
        self.problem_type = AllFoodProblem
