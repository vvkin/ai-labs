from dataclasses import dataclass

from app.pacman.rl.dqn.model import Model


@dataclass(eq=False)
class EpsParams:
    start: float
    end: float
    step: float


@dataclass(eq=False)
class DQNAgentConfig:
    model: Model
    train: bool
    eps_params: EpsParams
