from collections import Counter
from typing import Union

from app.config.types import Distribution
from app.config.const.geometry import Direction
from app.utils.helpers import normalize, sample
from app.pacman.domain.rules import GameState
from app.pacman.domain.agent import Agent


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
        return normalize(dist)
