from typing import Callable

from app.utils.helpers import time_it
from app.utils.structures import  PriorityQueue
from app.config.types import Action
from app.pacman.search.problem import SearchProblem


INF = float('inf')

@time_it
def a_star(problem: SearchProblem, heuristic: Callable) -> list[Action]:
    start = problem.get_start()
    costs = {start: 0}
    visited = set()
    queue = PriorityQueue()
    queue.enque((start, []), 0)

    while not queue.is_empty():
        (parent, actions), _ = queue.deque()
        visited.add(parent)
        cost = costs[parent]

        if problem.is_goal(parent): # target found
            return actions

        for state, action, move_cost in problem.get_neighbors(parent):
            if state not in visited:
                new_cost = cost + move_cost
                if new_cost < costs.get(state, INF):
                    new_actions = actions + [action]
                    priority = new_cost + heuristic(state, problem)
                    costs[state] = new_cost
                    queue.enque((state, new_actions), priority)

    return [] # no actions for non-existing path
