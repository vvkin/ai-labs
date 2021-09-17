from app.config.types import Image, Point, Vector
import math
from tkinter import Grid
from typing import Optional

from app.config.const.graphics import Pacman, Interface, Ghost, Item
from app.config.const.geometry import Direction
from app.pacman.domain.rules import GameState
from app.pacman.domain.agent import Agent, AgentState
from app.utils.layout import Layout
from .ui import UI


class InfoPanel:
    def __init__(self, ui: UI, layout: Layout, grid_size: int):
        self.ui = ui
        self.grid_size = grid_size
        self.base = (layout.height + 1) * grid_size
        self.font_size = 24
        self.text_color = Pacman.COLOR
        self.score_length = 4
        self.draw_panel()

    def to_screen(self, position: Point) -> Point:
        dx, dy = position
        return self.grid_size + dx, self.base + dy

    def draw_panel(self) -> None:
        self.score_text = self.ui.text(
            position=self.to_screen((0, 0)),
            color=self.text_color,
            contents="SCORE:    0",
            font="Times",
            size=self.font_size,
            style="bold",
        )

    def update_score(self, score: int) -> None:
        updated_text = f'SCORE: {score: >{self.score_length}}'
        self.ui.change_text(self.score_text, updated_text)


class PacmanGraphics:
    def __init__(self, ui: UI, zoom=1.0, frame_time=0.0) -> None:
        self.ui = ui
        self.have_window = 0
        self.current_ghost_images = {}
        self.pacman_image = None
        self.zoom = zoom
        self.grid_size = Interface.DEFAULT_GRID_SIZE * zoom
        self.frame_time = frame_time

    def init(self, state: GameState) -> None:
        self.__start_graphics(state)
        self.__draw_static_objects()
        self.__draw_agents(state)
        self.previous_state = state

    def __start_graphics(self, state: GameState) -> None:
        self.layout = state.layout
        self.width = self.layout.width
        self.height = self.layout.height
        self.__make_window(self.width, self.height)
        self.info_panel = InfoPanel(self.ui, self.layout, self.grid_size)
        self.current_state = self.layout

    def __draw_static_objects(self) -> None:
        layout = self.layout
        self.__draw_walls(layout.walls)
        self.food = self.__draw_food(layout.food)
        self.capsules = self.__draw_capsules(layout.capsules)
        self.ui.refresh()

    def __draw_agent(self, agent: Agent, idx: Optional[int]) -> Image:
        return self.__draw_pacman(agent) if agent.is_pacman\
            else self.__draw_ghost(agent, idx)

    def __draw_agents(self, state: GameState) -> None:
        self.agent_images = [
            (agent, self.__draw_agent(agent, idx))
            for idx, agent in enumerate(state.agent_states)
        ]
        self.ui.refresh()
    
    def __swap_images(self, agent_idx: int, new_state: AgentState) -> None:
        previous_image = self.agent_images[agent_idx][1]
        
        for item in previous_image:
            self.ui.remove_from_screen(item)

        agent_image = self.__draw_agent(new_state, agent_idx)
        self.agent_images[agent_idx] = (new_state, agent_image)
        self.ui.refresh()

    def update(self, new_state: GameState) -> None:
        agent_idx = new_state._agent_moved
        agent_state = new_state.agent_states[agent_idx]

        if self.agent_images[agent_idx][0].is_pacman != agent_state.is_pacman:
            self.__swap_images(agent_idx, agent_state)
        prev_state, prev_image = self.agent_images[agent_idx]

        if agent_state.is_pacman:
            self.__animate_pacman(agent_state, prev_state, prev_image)
        else:
            self.__move_ghost(agent_state, agent_idx, prev_image)
        self.agent_images[agent_idx] = (agent_state, prev_image)

        if new_state._capsule_eaten is not None:
            self.__remove_capsules(new_state._capsule_eaten, self.capsules)
        if new_state._food_eaten is not None:
            self.__remove_food(new_state._food_eaten, self.food)

        self.info_panel.update_score(new_state.score)

    def __make_window(self, width: int, height: int) -> None:
        offset = 2 * self.grid_size
        grid_height = self.grid_size * (height - 1)
        grid_width = self.grid_size * (width - 1)
        
        self.ui.init_ui(
            width=grid_width + offset,
            height=grid_height + offset + Interface.INFO_PANEL_HEIGHT,
            color=Interface.BACKGROUND_COLOR,
            title="Pacman",
        )

    def __draw_pacman(self, pacman: AgentState) -> Image:
        return [self.ui.circle(
            position=self.to_screen(self.__get_position(pacman)),
            radius=Pacman.SCALE * self.grid_size,
            outline_color=Pacman.COLOR,
            fill_color=Pacman.COLOR,
            endpoints=self.get_endpoints(self.__get_direction(pacman)),
            width=Pacman.OUTLINE_WIDTH,
        )]

    def get_endpoints(self, direction: int, position=(0.0, 0.0)) -> Vector:
        shift = position[0] % 1 + position[1] % 1
        width = 30 + 80 * math.sin(math.pi * shift)
        delta = width / 2
        return {
            Direction.WEST: (180 + delta, 180 - delta),
            Direction.NORTH: (90 + delta, 90 - delta),
            Direction.STOP: (delta, -delta),
            Direction.SOUTH: (270 + delta, 270 - delta),
            Direction.EAST: (delta, -delta),
        }[direction]
    
    def move_pacman(self, position: Vector, direction: int, image: Image) -> None:
        screen_pos = self.to_screen(position)
        endpoints = self.get_endpoints(direction, position)
        radius = Pacman.SCALE * self.grid_size
        self.ui.move_circle(image[0], screen_pos, radius, endpoints)
        self.ui.refresh()

    def __animate_pacman(
        self, pacman: AgentState, prev_pacman: AgentState, image: Image
    ) -> None:
        if self.frame_time > 0.01 or self.frame_time < 0:
            FRAMES = Interface.FRAMES
            x, y = self.__get_position(pacman)
            xx, yy = self.__get_position(prev_pacman)

            for idx in range(1, int(FRAMES) + 1):
                position = (
                    x * idx / FRAMES + xx * (FRAMES - idx) / FRAMES,
                    y * idx / FRAMES + yy * (FRAMES - idx) / FRAMES,
                )
                self.move_pacman(position, self.__get_direction(pacman), image)
                self.ui.refresh()
                self.ui.sleep(abs(self.frame_time) / FRAMES)
        else:
            self.move_pacman(
                self.__get_position(pacman),
                self.__get_direction(pacman),
                image,
            )
        self.ui.refresh()

    def __get_ghost_color(self, ghost: AgentState, ghost_idx: int) -> int:
        return Ghost.SCARED_COLOR if ghost.scared_timer > 0\
            else Ghost.COLORS[ghost_idx]

    def __draw_ghost(self, ghost, agent_idx: int) -> Image:
        screen_x, screen_y = self.to_screen(self.__get_position(ghost))
        coords = [
            (
                x * self.grid_size * Ghost.SIZE + screen_x,
                y * self.grid_size * Ghost.SIZE + screen_y,
            )
            for x, y in Ghost.SHAPE
        ]
        color = self.__get_ghost_color(ghost, agent_idx)
        return [self.ui.polygon(coords, color, filled=1)]

    def __move_ghost(
        self, ghost: AgentState, ghost_idx: int, image_parts: list[Image]
    ) -> None:
        new_x, new_y = self.to_screen(self.__get_position(ghost))

        for image_part in image_parts:
            self.ui.move_to(image_part, new_x, new_y)
        self.ui.refresh()

        color = self.__get_ghost_color(ghost, ghost_idx)
        self.ui.edit(image_parts[0], fill=color, outline=color)
        self.ui.refresh()

    def __get_position(self, agent_state: AgentState) -> tuple[float, float]:
        if agent_state.configuration is None:
            return (-1000, -1000)
        return agent_state.get_position()

    def __get_direction(self, agent_state: AgentState) -> int:
        if agent_state.configuration == None:
            return Direction.STOP
        return agent_state.configuration.get_direction()

    def finish(self) -> None:
        self.ui.end_graphics()

    def to_screen(self, point: tuple[float, float]) -> tuple[float, float]:
        x, y = point
        x = (x + 1) * self.grid_size
        y = (self.height - y) * self.grid_size
        return x, y

    def __draw_walls(self, walls: Grid) -> None:
        for x, row in enumerate(walls):
            for y, cell in enumerate(row):
                if cell:
                    screen = self.to_screen((x, y))

                    west_is_wall = self.__is_wall(x - 1, y, walls)
                    east_is_wall = self.__is_wall(x + 1, y, walls)
                    north_is_wall = self.__is_wall(x, y + 1, walls)
                    south_is_wall = self.__is_wall(x, y - 1, walls)

                    if (
                        (south_is_wall and north_is_wall)
                        or (south_is_wall and north_is_wall)
                        or (west_is_wall and south_is_wall)
                        or south_is_wall
                    ):
                        self.ui.line(
                            screen,
                            add(screen, (0, self.grid_size)),
                            Interface.WALL_COLOR,
                        )
                    if (
                        (east_is_wall and west_is_wall)
                        or (south_is_wall and east_is_wall)
                        or (east_is_wall and north_is_wall)
                        or east_is_wall
                    ):
                        self.ui.line(
                            screen,
                            add(screen, (self.grid_size, 0)),
                            Interface.WALL_COLOR,
                        )

    def __is_wall(self, x: int, y: int, walls: Grid) -> bool:
        if x < 0 or y < 0:
            return False
        if x >= walls.width or y >= walls.height:
            return False
        return walls[x][y]

    def __draw_food(self, food: Grid) -> list[list[Optional[int]]]:
        food_images = []
        for x, row in enumerate(food):
            image_row = []
            food_images.append(image_row)
            for y, cell in enumerate(row):
                if cell:
                    screen = self.to_screen((x, y))
                    point = self.ui.circle(
                        screen,
                        Item.FOOD_SIZE * self.grid_size,
                        Item.FOOD_COLOR,
                        Item.FOOD_COLOR,
                        width=1,
                    )
                    image_row.append(point)
                else:
                    image_row.append(None)
        return food_images

    def __draw_capsules(self, capsules: list) -> dict:
        capsule_images = {}
        for capsule in capsules:
            screen = self.to_screen(capsule)
            point = self.ui.circle(
                screen,
                Item.CAPSULE_SIZE * self.grid_size,
                Item.CAPSULE_COLOR,
                Item.CAPSULE_COLOR,
                width=1,
            )
            capsule_images[capsule] = point
        return capsule_images

    def __remove_food(self, cell: tuple[int, int], foodImages):
        x, y = cell
        self.ui.remove_from_screen(foodImages[x][y])

    def __remove_capsules(self, cell: tuple[int, int], capsuleImages):
        x, y = cell
        self.ui.remove_from_screen(capsuleImages[(x, y)])


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])
