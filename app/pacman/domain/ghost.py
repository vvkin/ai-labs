from collections import Counter
from typing import Union
from functools import partial

from app.config.types import Distribution
from app.config.const.geometry import Direction
from app.pacman.search.problem import PositionProblem
from app.utils.geometry import add_points, normalize_point
from app.utils.helpers import normalize, sample
from app.pacman.domain.rules import GameState
from app.pacman.domain.agent import Actions, Agent
from app.pacman.search.algorithms import a_star
from app.pacman.search.heuristics import distance_heuristic


class GhostAgent(Agent):
    def __init__(self, index: int) -> None:
        self.index = index

    def get_action(self, state: GameState) -> Union[str, int]:
        dist = self.get_distribution(state)
        return sample(dist) if dist else Direction.STOP

    def get_distribution(self, state: GameState) -> Distribution:
        raise NotImplementedError


class RandomGhost(GhostAgent):
    def get_distribution(self, state: GameState) -> Distribution:
        dist = Counter(state.get_legal_actions(self.index))
        return normalize(dict(dist))


class GreedyGhost(GhostAgent):
    def __init__(
        self, 
        index: int, 
        search_fn = partial(a_star, heuristic=distance_heuristic, greedy=True)
    ) -> None:
        super().__init__(index)
        self.search_fn = search_fn
    
    def get_distribution(self, state: GameState) -> Distribution:
        ghost_pos = state.get_ghost_position(self.index)
        dist = dict()

        pacman_pos = state.get_pacman_position()
        for action in state.get_legal_actions(self.index):
            move = Actions.direction_to_vector(action)
            next_pos = add_points(ghost_pos, move)
            problem = PositionProblem(state, pacman_pos, next_pos)
            actions = self.search_fn(problem)
            dist[action] = -len(actions)
        
        return normalize(dist)
