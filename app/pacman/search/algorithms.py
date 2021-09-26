from collections import deque

from app.utils.helpers import time_it
from app.config.types import Path
from app.pacman.search.problem import Problem

def find_path(start, goal, memory):
    path = []
    while goal in memory:
        parent = memory[goal]
        if parent == start:
            break
        goal = parent
        path.append(parent)
    path.reverse()
    return path

@time_it
def dfs(problem: Problem) -> Path:
    start = problem.get_start()
    goal = problem.get_goal()
    stack = [(start, 0)]
    visited = set()
    memory = dict()
    
    while stack:
        parent, cost = stack.pop()
        visited.add(parent)
        if parent == goal: break
        
        for node, move_cost in problem.get_neighbors(parent):
            if node not in visited:
                new_cost = cost + move_cost
                memory[node] = parent
                stack.append((node, new_cost))

    return find_path(start, goal, memory)
   
@time_it
def bfs(problem: Problem) -> Path:
    return []

@time_it
def ucs(problem: Problem) -> Path:
    return []
