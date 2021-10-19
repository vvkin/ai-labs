import numpy as np

def get_empty_adj_matrix(size: int) -> np.ndarray:
    adj_matrix = np.full((size, size), float("inf"))
    np.fill_diagonal(adj_matrix, 0)
    return adj_matrix
