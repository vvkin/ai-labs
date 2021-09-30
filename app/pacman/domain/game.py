import copy
from dataclasses import InitVar, dataclass
from typing import Optional

from app.config.const.geometry import Direction
from app.utils.layout import Layout
from app.pacman.domain.agent import Agent, AgentState, AgentConfig


@dataclass
class GameStateData:
    state: InitVar["GameStateData"] = None
    score_change: int = 0
    _food_eaten: Optional[tuple[float, float]] = None
    _capsule_eaten: int = None
    _agent_moved: int = None
    _lose: bool = False
    _win: bool = False

    def __post_init__(self, state: Optional["GameStateData"] = None) -> None:
        if state is not None:
            self.pacman_search = copy.deepcopy(state.pacman_search)
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
        pacman_search = None,
    ) -> None:
        self.food = copy.deepcopy(layout.food)
        self.pacman_search = copy.deepcopy(pacman_search)
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
    def __init__(self, agents: list[Agent], display, rules) -> None:
        self.agent_crashed = False
        self.agents = agents
        self.display = display
        self.rules = rules
        self.game_over = False
        self.history = []

    def run(self) -> None:
        self.display.init(self.state.data)
        num_agents = len(self.agents)
        agent_idx = 0
        
        while not self.game_over:
            agent = self.agents[agent_idx]
            state = copy.deepcopy(self.state)
            action = agent.get_action(state)

            self.history.append((agent_idx, action))
            self.state = self.state.generate_next(agent_idx, action)
            
            if self.state.data.pacman_search and agent_idx == 0:
                pacman_search = self.state.data.pacman_search
                pacman_search.handle_key(self.state)
                if pacman_search.key_pressed() or action != Direction.STOP:
                    pacman_search.update(self.state)
                    self.display.draw_path(self.state.data)
            
            self.display.update(self.state.data)
            self.rules.process(self.state, self)
            
            if agent_idx == num_agents + 1:
                self.num_moves += 1
            agent_idx = (agent_idx + 1) % num_agents

        self.display.finish()
