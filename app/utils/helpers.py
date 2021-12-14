import random
import time
import inspect
import torch
import numpy as np
from typing import Any, Callable

from app.config.types import Distribution


def normalize(
    mapping: dict[str, float]
) -> dict[str, float]:
    keys, values = zip(*mapping.items())
    values = np.array(values)
    values_sum = np.sum(values)

    if values_sum == 0: 
        return mapping

    values = values / values_sum
    normalized = dict(zip(keys, values.tolist()))
    return normalized


def sample(dist: Distribution) -> str:
    population = list(dist.keys())
    weights = list(dist.values())
    if sum(weights) != 0:
        actions = random.choices(
            population=population,
            weights=weights,
        )
        return actions[0]
    else: return population[0]


def time_it(fn: Callable) -> Callable:
    def timed(*args, **kwargs) -> Any:
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        end = time.perf_counter()
        print(f'Time ({fn.__name__}): {(end - start) * 1000} ms')
        return result
    return timed


def to_odd(value: int) -> int:
    return value if value & 1 else value + 1

def get_arg_names(fn: Callable) -> list[str]:
    return list(inspect.signature(fn).parameters.keys())

def to_numpy(tensor: torch.Tensor) -> np.ndarray:
    return tensor.cpu().detach().numpy()
