from typing import Literal, Iterator, TypeVar, Iterable

import numpy as np
from numba import njit

from enilm.constants import ModelType


@njit
def rolling(x: np.ndarray, window_size: int) -> np.ndarray:
    """
    split x and y into chunks each of size window_size by using a rolling window
    if strategy is not SAME, some other operation is applied to the chunks (e.g. mean)

    >>> rolling(np.arange(5), 3)
    array([[0, 1, 2],
           [1, 2, 3],
           [2, 3, 4]])

    See: https://stackoverflow.com/a/6811241/1617883
    """
    shape = x.shape[:-1] + (x.shape[-1] - window_size + 1, window_size)
    strides = x.strides + (x.strides[-1],)
    return np.lib.stride_tricks.as_strided(x, shape=shape, strides=strides)


def midpoints(x: np.ndarray, window_size: int) -> np.ndarray:
    """
    return midpoints while accounting for window size disregarding points on both ends

    >>> midpoints(np.arange(10), 5)
    array([[2],
           [3],
           [4],
           [5],
           [6],
           [7]])
    """
    assert window_size % 2 == 1
    return x[window_size // 2:-window_size // 2 + 1].reshape(-1, 1)


def chunkize(arr: np.ndarray, chunk_size: int) -> Iterator[np.ndarray]:
    for i in range(0, len(arr), chunk_size):
        yield arr[i:i + chunk_size]


def for_model(data: np.ndarray, window_size: int, xy: Literal['x', 'y'], model_type: ModelType) -> np.ndarray:
    assert xy in ['x', 'y']  # input/mains or output/target/ground truth/appliance

    # S2S produce sequences for both x and y
    if model_type == ModelType.S2S:
        return rolling(data, window_size)

    # S2P maps a sequence to midpoint
    if model_type == ModelType.S2P:
        if xy == 'x':
            return rolling(data, window_size)
        if xy == 'y':
            return midpoints(data, window_size)
