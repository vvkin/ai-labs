from dataclasses import dataclass

from app.pacman.domain.rules import GameState
from app.config.types import Action


@dataclass(eq=False)
class ReflexState:
    game_state: GameState
    agent: int = 0
    depth: int = 0

    @property
    def action(self) -> Action:
        return self.game_state.get_last_action()