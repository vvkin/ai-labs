from collections import defaultdict
from typing import Any

from app.config.const.geometry import Direction
from app.config.types import Action, Point
from app.pacman.domain.agent import Actions
from app.pacman.search.cost_fns import CostFn, UniformCostFn
from app.pacman.search.states import SearchState, AllFoodState
from app.utils.geometry import add_points, normalize_point
from app.utils.structures import IndexDict, Queue
from app.utils.search import get_empty_adj_matrix


class SearchProblem:
    def __init__(
        self,
        state,
        cost_fn: CostFn = UniformCostFn,
        **cost_kwargs: Any
    ) -> None:
        self.history = {}
        self.walls = state.get_walls()
        self.cost_fn = cost_fn(state, **cost_kwargs)  
    
    def get_start(self):
        raise NotImplementedError
    
    def is_goal(self, state: SearchState) -> bool:
        raise NotImplementedError

    def get_neighbor(self, state: SearchState, position: Point, action: Action):
        raise NotImplementedError

    def get_neighbors(self, state: SearchState) -> list[Point, float]:
        neighbors = []
        for action in Direction.as_list():
            vector = Actions.direction_to_vector(action)
            next = normalize_point(add_points(state.position, vector))
            next_x, next_y = next
            if not self.walls[next_x][next_y]:
                neighbor = self.get_neighbor(state, next, action)
                neighbors.append(neighbor)
        return neighbors
    
    def as_adj_list(self):
        start = self.get_start()
        visited, queue = set(), Queue()
        adj_list = defaultdict(list)
        mapping = IndexDict()
        queue.enque(start)
        
        while not queue.is_empty():
            parent = queue.deque()
            prev_idx = mapping[parent.position]
            visited.add(prev_idx)
            for state, _, cost in self.get_neighbors(parent):
                next_idx = mapping[state.position]
                adj_list[prev_idx].append((next_idx, cost))
                if next_idx not in visited:
                    queue.enque(state)

        return adj_list, mapping.as_dict()
    
    def as_adj_matrix(self):
        adj_list, mapping = self.as_adj_list()

        adj_matrix = get_empty_adj_matrix(len(adj_list))
        for p_idx, n_idxs in adj_list.items():
            for n_idx, cost in n_idxs:
                adj_matrix[p_idx, n_idx] = cost

        return adj_matrix, mapping
    
    def get_min_cost(self):
        return self.cost_fn.get_min_cost()

class PositionProblem(SearchProblem):
    def __init__(
        self,
        game_state,
        goal: Point,
        cost_fn: CostFn = UniformCostFn,
        **cost_kwargs: Any,
    ) -> None:
        super().__init__(game_state, cost_fn, **cost_kwargs)
        self.goal = goal
        self.start = SearchState(game_state.get_pacman_position())

    def is_goal(self, state: SearchState) -> bool:
        return state.position == self.goal

    def get_start(self) -> Point:
        return self.start

    def get_goal(self) -> Point:
        return self.goal

    def get_neighbor(self, state: SearchState, position: Point, action: Action):
        next_state = SearchState(position)
        cost = self.cost_fn(next_state)
        return next_state, action, cost

class AllFoodProblem(SearchProblem):
    def __init__(
        self,
        game_state,
        cost_fn: CostFn = UniformCostFn,
        **cost_kwargs: Any,
    ) -> None:
        super().__init__(game_state, cost_fn, **cost_kwargs)
        self.food = game_state.get_food()
        self.start = AllFoodState(
            game_state.get_pacman_position(), frozenset(self.food)
        )

    def get_start(self) -> "AllFoodState":
        return self.start

    def is_goal(self, state: "AllFoodState") -> bool:
        return len(state.rest) == 0

    def get_neighbor(self, state: "AllFoodState", position: Point, action: Action):
        rest = state.rest - set([position])\
            if position in state.rest else state.rest
        next_state = AllFoodState(position, rest)
        cost = self.cost_fn(next_state)
        return next_state, action, cost

    def get_food(self) -> list[Point]:
        return self.food
