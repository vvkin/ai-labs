import numpy as np
import os
from typing import Optional

from .grid import Grid


class Layout:
    def __init__(self, maze: list[list[str]]) -> None:
        self.maze = np.array(maze)
        self.height, self.width = self.maze.shape
        self.walls = Grid(self.width, self.height)
        self.food = Grid(self.width, self.height)
        self.capsules = []
        self.agent_positions = []
        self.num_ghosts = 0
        self.__process_maze()
        self.total_food = self.food.count()

    def get_num_ghosts(self) -> int:
        return self.num_ghosts

    def __process_maze(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self.__process_point(x, y, self.maze[self.height - (y + 1)][x])
        self.agent_positions.sort()

        self.agent_positions = [
            (_index == 0, position)
            for _index, position in self.agent_positions
        ]

    def __process_point(self, x: int, y: int, char: str) -> None:
        if char == "%":
            self.walls[x][y] = True
        elif char == ".":
            self.food[x][y] = True
        elif char == "o":
            self.capsules.append((x, y))
        elif char == "P":
            self.agent_positions.append((0, (x, y)))
        elif char in ["1", "2", "3", "4"]:
            self.num_ghosts += 1
            self.agent_positions.append((int(char), (x, y)))

    @staticmethod
    def get_layout(name: str) -> "Layout":
        base_dir = 'app/assets/layouts'
        file_name = name if name.endswith('.lay') else f"{name}.lay"
        layout_path = os.path.join(base_dir, file_name)
        return Layout.load_layout(layout_path)

    @staticmethod
    def load_layout(path: str) -> Optional["Layout"]:
        try:
            with open(path, mode="r") as file:
                maze = [list(line.strip()) for line in file]
                return Layout(maze)
        except:
            return None
