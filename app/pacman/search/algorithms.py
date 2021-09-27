from collections import deque

from app.utils.helpers import time_it
from app.utils.search import restore_path
from app.utils.structures import Queue, Stack, PriorityQueue
from app.config.types import Path
from app.pacman.search.problem import Problem


INF = float('inf')

@time_it
def bfs(problem: Problem) -> Path:
    start = problem.get_start()
    goal = problem.get_goal()
    
    queue = Queue()
    visited = set()
    memory = dict()
    queue.enque((start, 0))
    
    while not queue.is_empty():
        parent, cost = queue.deque()
        visited.add(parent)
        if parent == goal: break
        
        for node, move_cost in problem.get_neighbors(parent):
            if node not in visited:
                new_cost = cost + move_cost
                memory[node] = parent
                queue.enque((node, new_cost))

    return restore_path(start, goal, memory)

@time_it
def dfs(problem: Problem) -> Path:
    start = problem.get_start()
    goal = problem.get_goal()
    
    costs = {start: 0}
    stack = Stack()
    memory = dict()
    stack.push(start)
    
    while not stack.is_empty():
        parent = stack.pop()
        cost = costs[parent]
        if parent == goal: break
        
        for node, move_cost in problem.get_neighbors(parent):
            new_cost = cost + move_cost
            if new_cost < costs.get(node, INF):
                memory[node] = parent
                costs[node] = new_cost
                stack.push(node)

    return restore_path(start, goal, memory)


@time_it
def ucs(problem: Problem) -> Path:
    start = problem.get_start()
    goal = problem.get_goal()
    
    costs = {start: 0}
    queue = PriorityQueue()
    visited = set()
    memory = dict()
    queue.enque(start, 0)
    
    while not queue.is_empty():
        parent, cost = queue.deque()
        visited.add(parent)
        
        if parent == goal: break
        if cost > costs[parent]: continue
        
        for node, move_cost in problem.get_neighbors(parent):
            if node not in visited:
                new_cost = cost + move_cost
                if new_cost < costs.get(node, INF):
                    costs[node] = new_cost
                    memory[node] = parent
                    queue.enque(node, new_cost)
    
    return restore_path(start, goal, memory)
