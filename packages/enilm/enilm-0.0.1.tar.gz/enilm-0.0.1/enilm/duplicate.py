from itertools import islice, cycle
from typing import List, Iterator, TypeVar

X = TypeVar("X")  # generic


def duplicate_data(data: List[X], duplication_duration: int) -> Iterator[X]:
    """
    Based on itertools, specifically cycle and islice:
        islice(cycle([1,2,3]), 5) -> [1, 2, 3, 4, 5]
    """
    return islice(cycle(data), duplication_duration)
