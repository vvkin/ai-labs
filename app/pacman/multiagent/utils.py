import random

from app.pacman.multiagent.states import ReflexState
from app.utils.geometry import normalize_point
from app.utils.structures import MazeDistance

EPS = 1e-3
INF = float('inf')


def utility_fn(
    state: ReflexState, maze_dists: MazeDistance, dist_mult=1e2, food_mult=1e4
) -> float:
    game_state = state.game_state

    pacman = normalize_point(game_state.get_pacman_position())
    food_dists = [
        maze_dists.get(pacman, food) for food in game_state.get_food()
    ]
    food_dist = clip(food_dists) if food_dists else EPS

    ghost_dists = []
    for ghost in game_state.get_ghost_positions():
        ghost_dists.append(maze_dists.get(pacman, normalize_point(ghost)))


    # ghost_dists = [
    #     maze_dists.get(pacman, ghost)
    #     for ghost in game_state.get_ghost_positions()
    # ]
    ghost_dist = clip(ghost_dists) if ghost_dists else INF
    num_food = game_state.get_num_food()

    game_score = (
        dist_mult / (food_dist if food_dist < 2 * ghost_dist else -ghost_dist)
        + food_mult / num_food
        + random.randint(-2, 2)
    )
    return game_score


def clip(values: list[float], eps: float = EPS):
    return max(min(values), eps)
