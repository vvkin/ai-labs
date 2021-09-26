import random
import time
from collections import Counter
from typing import Any, Callable

from app.config.types import Distribution, Point


def normalize(counter: Distribution) -> Distribution:
    if isinstance(counter, Counter):
        counter = dict(counter)
    sum_all = sum(counter.values())
    normalized = {}
    for key, value in counter.items():
        normalized[key] = value / sum_all
    return normalized


def sample(dist: Distribution) -> str:
    actions = random.choices(
        population=list(dist.keys()),
        weights=list(dist.values()),
    )
    return actions[0]

def time_it(fn: Callable) -> Callable:
    def timed(*args, **kwargs) -> Any:
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()
        print(f'Time ({fn.__name__}): {(end - start) * 1000} ms')
        return result
    return timed

def add_points(x: Point, y: Point) -> Point:
    return (x[0] + y[0], x[1] + y[1])
