import os
import random
import numpy as np
from typing import Optional

from app.utils.grid import Grid
from app.utils.geometry import Point
from app.config.types import MazeText
from app.config.const.layout import Cell
from app.utils.helpers import to_odd

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
        
    @classmethod
    def from_text(cls: "Layout", maze: list[list[str]]) -> "Layout":
        instance = cls(maze)
        return instance

    def get_num_ghosts(self) -> int:
        return self.num_ghosts

    def __process_maze(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                value = self.maze[self.height - (y + 1)][x]
                self.__process_point(x, y, value)
        self.agent_positions.sort()

        self.agent_positions = [
            (_index == 0, position)
            for _index, position in self.agent_positions
        ]

    def __process_point(self, x: int, y: int, value: str) -> None:
        if value == Cell.WALL:
            self.walls[x][y] = True
        elif value == Cell.FOOD:
            self.food[x][y] = True
        elif value == Cell.CAPSULE:
            self.capsules.append((x, y))
        elif value == Cell.PACMAN:
            self.agent_positions.append((False, (x, y)))
        elif value in Cell.GHOST:
            self.num_ghosts += 1
            self.agent_positions.append((True, (x, y)))

    @staticmethod
    def get_layout(name: str) -> Optional["Layout"]:
        base_dir = 'app/assets/layouts'
        file_name = name if name.endswith('.lay') else f'{name}.lay'
        layout_path = os.path.join(base_dir, file_name)
        if (layout := Layout.load_layout(layout_path)) is None:
            raise Exception(f"The layout {name} cannot be found")
        else: return layout

    @staticmethod
    def load_layout(path: str) -> Optional["Layout"]:
        try:
            with open(path, mode='r') as file:
                maze = [list(line.strip()) for line in file]
                return Layout(maze)
        except:
            return None

class MazeGenerator:
    @staticmethod
    def generate(
        height: int,
        width: int,
        num_ghosts: int,
        num_capsules: int = 0,
        num_food: int = 0
    ) -> list[list[str]]:
        maze = MazeGenerator.__get_maze(height, width)
        MazeGenerator.__fill_walls(maze)
        MazeGenerator.__fill_items(maze, num_ghosts, num_food, num_capsules)
        return maze

    def __get_maze(height: int, width: int) -> MazeText:
        height, width = map(to_odd, (height, width))
        return np.full((height, width), Cell.WALL)
    
    def __get_source(height: int, width: int) -> Point:
        return Point(
            random.randrange(1, width, 2),
            random.randrange(1, height, 2)
        )

    def __fill_walls(maze: MazeText) -> None:
        height, width = maze.shape
        source = MazeGenerator.__get_source(height, width)
        maze[source.y, source.x] = Cell.EMPTY
        stack = [source]
    
        while stack:
            current = stack[-1]
            neighbors = MazeGenerator.__get_neighbors(current, maze)

            if neighbors:
                next = neighbors[-1]
                center = (current + next) // 2
                maze[next.y, next.x] = Cell.EMPTY
                maze[center.y, center.x] = Cell.EMPTY
                stack.append(next)
            else: stack.pop()
            
    def __get_neighbors(current: Point, maze: MazeText) -> list[Point]:
        height, width = maze.shape
        neighbors = []

        move_conditions = {
            Point(-2, 0): current.x > 1,
            Point(2, 0): current.x < width - 2,
            Point(0, 2): current.y < height - 2,
            Point(0, -2): current.y > 1,
        }

        for move, condition in move_conditions.items():
            next = current + move
            if condition and maze[next.y, next.x] == Cell.WALL:
                neighbors.append(next)

        random.shuffle(neighbors)
        return neighbors
    
    def __get_free(maze: np.ndarray) -> list[Point]:
        points = []
        height, width = maze.shape
        
        for x in range(height):
            for y in range(width):
                value = maze[x, y]
                if value == Cell.EMPTY:
                    points.append((x, y))

        return points
    
    def __fill_value(maze: np.ndarray, points: list[Point], value: Cell) -> None:
        for x, y in points:
            maze[x, y] = value 
    
    def __fill_items(maze: np.ndarray, ghosts: int, food: int, capsules: int) -> None:
        free_points = MazeGenerator.__get_free(maze)
        to_fill = food + capsules + ghosts + 1

        if len(free_points) < to_fill:
            raise Exception('Unable to locate all objects')
        
        chosen = random.choices(free_points, k=to_fill)
        MazeGenerator.__fill_value(maze, chosen[:food], Cell.FOOD)
        MazeGenerator.__fill_value(maze, chosen[food:food + capsules], Cell.CAPSULE)

        pacman_x, pacman_y = chosen[food + capsules]
        maze[pacman_x, pacman_y] = Cell.PACMAN

        for idx in range(1, ghosts + 1):
            x, y = chosen[food + capsules + idx]
            maze[x, y] = str(idx)
