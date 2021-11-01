import random
import time
import numpy as np
from collections import Counter
from typing import Any, Callable, Optional

from app.config.types import Distribution


def normalize(
    mapping: dict[str, float], softmax: bool = False
) -> dict[str, float]:
    keys, values = zip(*mapping.items())

    values = np.array(values)
    if softmax is True:
        values = np.exp(values - np.max(values))
    values = values / np.sum(values)

    normalized = dict(zip(keys, values.tolist()))
    return normalized


def sample(dist: Distribution) -> str:
    actions = random.choices(
        population=list(dist.keys()),
        weights=list(dist.values()),
    )
    return actions[0]


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