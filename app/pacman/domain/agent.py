from dataclasses import dataclass
from typing import Optional

from app.config.types import Vector
from app.config.const.geometry import Direction, DIRECTIONS
from app.utils.grid import Grid


class Agent:
    def __init__(self, index: int = 0) -> None:
        self.index = index

    def get_action(self, state: object) -> str:
        raise NotImplementedError


@dataclass(eq=False)
class AgentConfig:
    position: Vector
    direction: int

    def get_position(self) -> Vector:
        return self.position

    def get_direction(self) -> str:
        return self.direction

    def generate_next(self, vector: Vector) -> "AgentConfig":
        x, y = self.position
        dx, dy = vector
        direction = Actions.vector_to_direction(vector)
        if direction == Direction.STOP:
            direction = self.direction
        return AgentConfig((x + dx, y + dy), direction)


@dataclass(eq=False)
class AgentState:
    configuration: AgentConfig
    is_pacman: bool
    scared_timer: int = 0

    def __post_init__(self) -> None:
        self.start = self.configuration

    def get_position(self) -> Optional[Vector]:
        return None if self.configuration is None\
            else self.configuration.get_position()

    def get_direction(self) -> int:
        return self.configuration.get_direction()


class Actions:
    EPS = 1e-3
    
    @staticmethod
    def get_possible_actions(config: AgentConfig, walls: Grid) -> list[int]:
        x, y = config.get_position()
        if (x % 1) + (y % 1) > Actions.EPS:
            return [config.get_direction()]
        
        x_int, y_int = map(round, (x, y))        
        actions = [direction for direction, (dx, dy)\
            in DIRECTIONS.items()
            if not walls[x_int + dx][y_int + dy]
        ]
        return actions


    @staticmethod
    def reverse_direction(action: int) -> int:
        return -action

    @staticmethod
    def vector_to_direction(vector: Vector) -> int:
        dx, dy = vector
        if dy > 0:
            return Direction.NORTH
        if dy < 0:
            return Direction.SOUTH
        if dx < 0:
            return Direction.WEST
        if dx > 0:
            return Direction.EAST
        return Direction.STOP

    @staticmethod
    def direction_to_vector(direction: int, speed=1.0) -> Vector:
        dx, dy = DIRECTIONS[direction]
        return (dx * speed, dy * speed)
