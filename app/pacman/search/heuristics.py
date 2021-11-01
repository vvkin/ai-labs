from numpy import positive
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path

from app.pacman.search.states import AllFoodState, SearchState
from app.pacman.search.problem import AllFoodProblem, PositionProblem
from app.utils.geometry import manhattan_distance
from app.utils.structures import DistanceMemory


def distance_heuristic(
    state: SearchState,
    problem: PositionProblem,
    greedy: bool = False,
) -> float:
    if problem.is_goal(state): return 0

    scaler = 1e3 if greedy else 1
    goal = problem.get_goal()
    cost = manhattan_distance(state.position, goal)
    return scaler * problem.get_min_cost() * cost


def all_food_heuristic(state: AllFoodState, problem: AllFoodProblem) -> float:
    if problem.is_goal(state): return 0

    memory = problem.history.get("memory")
    if memory is None:
        adj_matrix, mapping = problem.as_adj_matrix()
        adj_matrix = csr_matrix(adj_matrix)
        goal_idxs = {mapping[goal]: idx for idx, goal in enumerate(problem.get_food())}
        dist = shortest_path(
            adj_matrix,
            directed=False,
            return_predecessors=False,
            indices=list(goal_idxs.keys()),
        )
        memory = DistanceMemory(dist, mapping, goal_idxs)
        problem.history["memory"] = memory

    return min([
        problem.get_min_cost() * memory.get(state.position, goal)
        for goal in [*state.rest]
    ])


def suboptimal_all_food_heuristic(
    state: AllFoodState, 
    problem: AllFoodProblem,
) -> float:
    if problem.is_goal(state): return 0
    distances = [
        problem.get_min_cost() * manhattan_distance(state.position, goal)
        for goal in [*state.rest]
    ]
    return min(distances)
