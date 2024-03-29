import copy
from dataclasses import InitVar, dataclass
from typing import Optional, Union

from app.config.const.geometry import Direction
from app.config.types import Action
from app.utils.layout import Layout
from app.pacman.domain.agent import Agent, AgentState, AgentConfig
from app.utils.logger import Logger
from app.utils.timer import Timer


@dataclass
class GameStateData:
    state: InitVar["GameStateData"] = None
    score_change: int = 0
    _food_eaten: Optional[tuple[float, float]] = None
    _capsule_eaten: int = None
    _agent_moved: int = None
    _last_action: Action = None
    _lose: bool = False
    _win: bool = False

    def __post_init__(self, state: Optional["GameStateData"] = None) -> None:
        if state is not None:
            self.food = copy.copy(state.food)
            self.capsules = state.capsules[:]
            self.agent_states = [copy.copy(el) for el in state.agent_states]
            self.layout = state.layout
            self._eaten = state._eaten
            self.score = state.score

    def initialize(
        self, 
        layout:  Layout, 
        num_ghost_agents: int,
    ) -> None:
        self.food = copy.deepcopy(layout.food)
        self.capsules = layout.capsules[:]
        self.layout = layout
        self.score = 0
        self.score_change = 0
        self.agent_states = []
        num_ghosts = 0

        for is_pacman, pos in layout.agent_positions:
            if not is_pacman:
                if num_ghosts != num_ghost_agents:
                    num_ghost_agents += 1
                else: continue
            state = AgentState(AgentConfig(pos, Direction.STOP), is_pacman)
            self.agent_states.append(state)

        self._eaten = [False] * len(self.agent_states)


class Game:
    def __init__(self, agents: list[Agent], display, rules, log_path) -> None:
        self.agent_crashed = False
        self.agents = agents
        self.display = display
        self.rules = rules
        self.game_over = False
        self.history = []
        self.timer = Timer()
        self.logger = Logger(log_path)

    def run(self) -> None:
        self.display.init(self.state.data)
        self.num_moves = 0

        self.timer.start()
        for agent in self.agents:
            if hasattr(agent, "register_state"):
                agent.register_state(self.state)

        agent_idx = 0
        num_agents = len(self.agents)

        while self.game_over is False:
            agent = self.agents[agent_idx]
            action = agent.get_action(copy.deepcopy(self.state))

            self.history.append((agent_idx, action))
            self.state = self.state.generate_next(agent_idx, action)
            
            self.display.update(self.state.data)
            self.rules.process(self.state, self)
           
            if agent_idx == num_agents + 1:
                self.num_moves += 1
            agent_idx = (agent_idx + 1) % num_agents

        self.timer.stop()
        self.display.finish()

        if (stats := self.__get_stats()) is not None:
            self.logger.log_object(stats)
    
    def __get_stats(self) -> dict[str, Union[bool, str, float]]:
        return {
            "win": self.state.is_win(),
            "elapsed": self.timer.elapsed,
            "score": self.state.get_score(),
            "algorithm": self.agents[0].get_algorithm()
        } if self.game_over else None
