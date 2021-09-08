from enum import Enum
from app.utils.graphics import format_color, color_to_vector

class Color:
    WHITE = format_color(1.0, 1.0, 1.0)
    BLACK = format_color(0.0, 0.0, 0.0)
    RED = format_color(0.9, 0.0, 0.0)
    BLUE = format_color(0.0, 0.3, 0.9)
    ORANGE = format_color(0.98, 0.41, 0.07)
    GREEN = format_color(0.1, 0.75, 0.7)
    GRAY = format_color(0.9, 0.9, 0.9)
    DARK_GREEN = format_color(0.4, 0.4, 0)
    LIGHT_BLUE = format_color(0.0, 0.2, 1.0)
    LIGHT_YELLOW = format_color(1.0, 1.0, 0.24) 


class Ghost:
    SIZE = 0.65
    SPEED = 1.0
    
    SCARED_COLOR = Color.WHITE
    COLORS = [Color.RED, Color.BLUE, Color.ORANGE, Color.GREEN]
    VEC_COLORS = [color_to_vector(color) for color in COLORS]
    
    SHAPE = [
        (0, 0.3),
        (0.25, 0.75),
        (0.5, 0.3),
        (0.75, 0.75),
        (0.75, -0.5),
        (0.5, -0.75),
        (-0.5, -0.75),
        (-0.75, -0.5),
        (-0.75, 0.75),
        (-0.5, 0.3),
        (-0.25, 0.75),
    ]
    
class Pacman:
    COLOR = Color.LIGHT_YELLOW
    SCALE = 0.5
    SPEED = 1.0
    OUTLINE_WIDTH = 2.0


class Food:
    FOOD_COLOR = Color.WHITE
    FOOD_SIZE = 0.1
    CAPSULE_COLOR = Color.WHITE
    CAPSULE_SIZE = 0.25


class Interface:
    DEFAULT_GRID_SIZE = 30.0
    INFO_PANEL_HEIGHT = 35
    
    BACKGROUND_COLOR = Color.BLACK
    WALL_COLOR = Color.LIGHT_BLUE
    INFO_PANE_COLOR = Color.DARK_GREEN
    SCORE_COLOR = Color.GRAY
    
    WALL_RADIUS = 0.15
    FRAMES = 4.0
