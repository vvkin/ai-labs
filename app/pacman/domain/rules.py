import copy
from typing import Optional, Union

from app.config.const.pacman import *
from app.config.const.geometry import Direction
from app.config.types import Action, Point, Vector
from app.utils.layout import Layout
from app.utils.geometry import get_nearest_point, manhattan_distance
from app.utils.grid import Grid
from app.pacman.graphics.ui import UI
from app.pacman.domain.agent import Agent, Actions, AgentState
from app.pacman.domain.game import Game, GameStateData


class GameState:
    def __init__(self, state: Optional["GameState"] = None) -> None:
        self.data = GameStateData(state.data if state else None)

    def get_legal_actions(self, agent_idx: int = 0) -> list[Action]:
        if self.is_game_over(): return []

        if agent_idx == 0:
            return PacmanRules.get_legal_actions(self)

        return GhostRules.get_legal_actions(self, agent_idx)

    def generate_next(self, agent_idx: int, action: int) -> "GameState":
        if self.is_game_over():
            reason = "Can't generate a successor of a terminal state."
            raise Exception(reason)

        state = GameState(self)
        if agent_idx == 0:
            state.data._eaten = [False] * state.get_num_agents()
            PacmanRules.apply_action(state, action)
        else: GhostRules.apply_action(state, action, agent_idx)

        if agent_idx == 0:
            state.data.score_change -= TIME_PENALTY
        else: GhostRules.decrement_timer(state.data.agent_states[agent_idx])
        GhostRules.check_death(state, agent_idx)

        state.data._agent_moved = agent_idx
        state.data.score += state.data.score_change
        return state
    
    def get_walls(self) -> Grid:
        return self.data.layout.walls
    
    def is_game_over(self) -> bool:
        return self.is_lose() or self.is_win()

    def is_lose(self) -> bool:
        return self.data._lose

    def is_win(self) -> bool:
        return self.data._win

    def initialize(
        self, 
        ui: UI, 
        layout: Layout, 
        num_ghost_agents: int = 1000,
    ) -> None:
        GameState.keys_pressed = ui.keys_pressed
        GameState.keys_waiting = ui.keys_waiting
        self.data.initialize(layout, num_ghost_agents)

    def get_pacman_state(self) -> AgentState:
        return copy.copy(self.data.agent_states[0])

    def get_pacman_position(self) -> Vector:
        return self.data.agent_states[0].get_position()

    def get_num_agents(self) -> int:
        return len(self.data.agent_states)

    def get_capsules(self) -> list:
        return self.data.capsules
    
    def get_food(self) -> list[Union[Point, None]]:
        return self.data.food.get_points() or [None]

    def get_num_food(self) -> int:
        return self.data.food.count()

    def get_ghost_state(self, agent_idx: int) -> AgentState:
        if agent_idx == 0 or agent_idx >= self.get_num_agents():
            raise Exception("Invalid index")
        return self.data.agent_states[agent_idx]


class GameRules:
    @staticmethod
    def new_game(
        layout: Layout,
        pacman_agent: list[Agent],
        ghost_agents: list[Agent],
        display,
    ) -> Game:
        agents = [pacman_agent] + ghost_agents[:layout.get_num_ghosts()]
        state = GameState()
        state.initialize(display.ui, layout, len(ghost_agents))
        game = Game(agents, display, GameRules)
        game.state = state
        return game

    @staticmethod
    def process(state: GameState, game: Game) -> None:
        if state.is_win():
            GameRules.win(state, game)
        if state.is_lose():
            GameRules.lose(state, game)

    @staticmethod
    def win(state: GameState, game: Game) -> None:
        print(f"Pacman emerges victorious! Score: {state.data.score}")
        game.game_over = True

    @staticmethod
    def lose(state: GameState, game: Game) -> None:
        print(f"Pacman died! Score: {state.data.score}")
        game.game_over = True

class PacmanRules:
    @staticmethod
    def get_legal_actions(state: GameState) -> list[Action]:
        return Actions.get_possible_actions(
            state.get_pacman_state().configuration,
            state.data.layout.walls,
        )

    @staticmethod
    def apply_action(state: GameState, action: int) -> None:
        legal = PacmanRules.get_legal_actions(state)
        if action not in legal:
            raise Exception(f"Illegal action {action}")

        pacman_state = state.data.agent_states[0]
        vector = Actions.direction_to_vector(action, PACMAN_SPEED)
        pacman_state.configuration = pacman_state.configuration.generate_next(vector)
        next = pacman_state.configuration.get_position()
        nearest = get_nearest_point(next)
        
        if manhattan_distance(nearest, next) <= 0.5:
            PacmanRules.consume(nearest, state)

    @staticmethod
    def consume(position: Vector, state: GameState) -> None:
        x, y = position

        if state.data.food[x][y]:
            state.data.score_change += 10
            state.data.food[x][y] = False
            state.data._food_eaten = position

            if state.get_num_food() == 0 and not state.data._lose:
                state.data.score_change += 500
                state.data._win = True

        if position in state.get_capsules():
            state.data.capsules.remove(position)
            state.data._capsule_eaten = position

            for idx in range(1, len(state.data.agent_states)):
                state.data.agent_states[idx].scared_timer = SCARED_TIME


class GhostRules:
    @staticmethod
    def get_legal_actions(state: GameState, ghost_idx: int) -> list[int]:
        configuration = state.get_ghost_state(ghost_idx).configuration
        reverse = Actions.reverse_direction(configuration.get_direction())
        actions = [action for action in\
            Actions.get_possible_actions(configuration, state.data.layout.walls)
            if action != Direction.STOP
        ]
        
        if reverse in actions and len(actions) > 1:
            actions.remove(reverse)
        return actions

    @staticmethod
    def apply_action(state: GameState, action: Action, ghost_idx: int) -> None:
        legal = GhostRules.get_legal_actions(state, ghost_idx)
        if action not in legal:
            raise Exception(f"Illegal action {action}")

        ghost_state = state.data.agent_states[ghost_idx]
        vector = Actions.direction_to_vector(
            action,
            GHOST_SPEED / 2 if ghost_state.scared_timer > 0 else GHOST_SPEED,
        )
        ghost_state.configuration = ghost_state.configuration.generate_next(
            vector
        )

    @staticmethod
    def decrement_timer(ghost_state: AgentState) -> None:
        timer = ghost_state.scared_timer
        if timer == 1:
            ghost_state.configuration.pos = get_nearest_point(
                ghost_state.configuration.get_position()
            )
        ghost_state.scared_timer = max(0, timer - 1)

    @staticmethod
    def check_death(state: GameState, agent_idx: int) -> None:
        pacman = state.get_pacman_position()
        if agent_idx == 0:
            for idx in range(1, len(state.data.agent_states)):
                ghost_state = state.data.agent_states[idx]
                ghost = ghost_state.configuration.get_position()

                if GhostRules.can_kill(pacman, ghost):
                    GhostRules.collide(state, ghost_state, idx)
        else:
            ghost_state = state.data.agent_states[agent_idx]
            ghost = ghost_state.configuration.get_position()

            if GhostRules.can_kill(pacman, ghost):
                GhostRules.collide(state, ghost_state, agent_idx)

    @staticmethod
    def collide(
        state: GameState, ghost_state: AgentState, agent_idx: int
    ) -> None:
        if ghost_state.scared_timer <= 0:
            if state.data._win is False:
                state.data.score_change -= 500
                state.data._lose = True
        else:
            state.data.score_change += 200
            ghost_state.configuration = ghost_state.start
            state.data._eaten[agent_idx] = True
            ghost_state.scared_timer = 0

    @staticmethod
    def can_kill(pacman: Point, ghost: Point) -> bool:
        return manhattan_distance(pacman, ghost) <= COLLISION_TOLERANCE
