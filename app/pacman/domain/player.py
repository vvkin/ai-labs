import random

from app.config.const.geometry import Direction
from .game import Agent


class PlayerAgent(Agent):
    def __init__(self, index: int = 0) -> None:
        self.last_move = Direction.STOP
        self.index = index
        self.keys = []

    def get_action(self, state) -> str:
        keys = list(state.keys_waiting()) + list(state.keys_pressed())
        if len(keys) > 0:
            self.keys = keys

        legal = state.get_legal_actions(self.index)
        move = self.get_move(legal)

        if move == Direction.STOP:
            if self.last_move in legal:
                move = self.last_move

        if move not in legal:
            move = random.choice(legal)

        self.last_move = move
        return move

    def get_move(self, legal: list[int]) -> int:
        move = Direction.STOP
        if "Left" in self.keys and Direction.WEST in legal:
            move = Direction.WEST
        if "Right" in self.keys and Direction.EAST in legal:
            move = Direction.EAST
        if "Up" in self.keys and Direction.NORTH in legal:
            move = Direction.NORTH
        if "Down" in self.keys and Direction.SOUTH in legal:
            move = Direction.SOUTH
        return move
