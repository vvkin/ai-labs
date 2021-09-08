import copy
from typing import Optional
from dataclasses import InitVar, dataclass

from app.config.const.geometry import Direction
from app.utils.layout import Layout
from .agent import Agent, AgentState, AgentConfig


@dataclass
class GameStateData:
    state: InitVar["GameStateData"] = None
    _food_eaten: tuple[float, float] = None
    _capsule_eaten: int = None
    _agent_moved: int = None
    _lose: bool = False
    _win: bool = False
    score_change: int = 0

    def __post_init__(self, state: Optional["GameStateData"] = None) -> None:
        if state is not None:
            self.food = copy.copy(state.food)
            self.capsules = state.capsules[:]
            self.agent_states = self.__copy_agent_states(state.agent_states)
            self.layout = state.layout
            self._eaten = state._eaten
            self.score = state.score

    def __copy_agent_states(
        self, agent_states: list[AgentState]
    ) -> list[AgentState]:
        states = []
        for state in agent_states:
            states.append(copy.copy(state))
        return states

    def initialize(self, layout: Layout, num_ghost_agents: int) -> None:
        self.food = copy.deepcopy(layout.food)
        self.capsules = layout.capsules[:]
        self.layout = layout
        self.score = 0
        self.score_change = 0

        self.agent_states = []
        num_ghosts = 0
        for is_pacman, pos in layout.agent_positions:
            if not is_pacman:
                if num_ghosts == num_ghost_agents:
                    continue
                else:
                    num_ghosts += 1
            self.agent_states.append(
                AgentState(AgentConfig(pos, Direction.STOP), is_pacman)
            )
        self._eaten = [False] * len(self.agent_states)


class Game:
    def __init__(self, agents: list[Agent], display, rules) -> None:
        self.agentCrashed = False
        self.agents = agents
        self.display = display
        self.rules = rules
        self.gameOver = False
        self.history = []

    def run(self) -> None:
        self.display.init(self.state.data)
        self.num_moves = 0

        agent_idx = 0
        num_agents = len(self.agents)

        while not self.gameOver:
            agent = self.agents[agent_idx]
            action = agent.get_action(copy.deepcopy(self.state))

            self.history.append((agent_idx, action))
            self.state = self.state.generate_next(agent_idx, action)

            self.display.update(self.state.data)

            self.rules.process(self.state, self)
            if agent_idx == num_agents + 1:
                self.num_moves += 1
            agent_idx = (agent_idx + 1) % num_agents

        self.display.finish()
