import random
from collections import Counter


def normalize(counter: dict[str, float]) -> dict[str, float]:
    if isinstance(counter, Counter):
        counter = dict(counter)
    sum_all = sum(counter.values())
    normalized = {}
    for key, value in counter.items():
        normalized[key] = value / sum_all
    return normalized


def sample(dist: dict[str, float]) -> str:
    actions = random.choices(
        population=list(dist.keys()),
        weights=list(dist.values()),
    )
    return actions[0]