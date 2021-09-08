from dataclasses import dataclass
from typing import Optional

from app.config.const.geometry import Direction, DIRECTIONS
from app.utils.grid import Grid



class Agent:
    def __init__(self, index: int = 0) -> None:
        self.index = index

    def get_action(self, state) -> str:
        raise NotImplementedError


@dataclass(eq=False)
class AgentConfig:
    position: tuple[float, float]
    direction: int

    def get_position(self) -> tuple[float, float]:
        return self.position

    def get_direction(self) -> str:
        return self.direction

    def generate_next(self, vector: tuple[float, float]) -> "AgentConfig":
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

    def get_position(self) -> Optional[tuple[float, float]]:
        if self.configuration == None:
            return None
        return self.configuration.get_position()

    def get_direction(self) -> int:
        return self.configuration.get_direction()


class Actions:
    @staticmethod
    def get_possible_actions(config: AgentConfig, walls: Grid) -> list[int]:
        x, y = config.get_position()
        x_int, y_int = int(x + 0.5), int(y + 0.5)

        if abs(x - x_int) + abs(y - y_int) > 1e-3:
            return [config.get_direction()]

        actions = []
        for direction, (dx, dy) in DIRECTIONS.items():
            next_x = x_int + dx
            next_y = y_int + dy
            if not walls[next_x][next_y]:
                actions.append(direction)

        return actions

    @staticmethod
    def reverse_direction(action: int) -> int:
        return -action

    @staticmethod
    def vector_to_direction(vector: tuple[float, float]) -> int:
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
    def direction_to_vector(direction: int, speed=1.0) -> tuple[float, float]:
        dx, dy = DIRECTIONS[direction]
        return (dx * speed, dy * speed)