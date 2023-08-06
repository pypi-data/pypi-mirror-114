from typing import Callable

import enilm
import numpy as np
from sklearn.metrics import mean_absolute_error


def denrom_mae(pred_fn: Callable[[np.ndarray], np.ndarray], x_chunks: np.ndarray, y_chunks: np.ndarray, y_mean: float,
               y_std: float) -> float:
    n = len(x_chunks)
    n_splits = 10
    while not (n / n_splits).is_integer():
        n_splits -= 1
        if n_splits < 0:
            raise ValueError

    x_splits = np.split(x_chunks, n_splits)
    y_splits = np.split(y_chunks, n_splits)
    model_mae = []
    for x, y in zip(x_splits, y_splits):
        model_mae.append(mean_absolute_error(
            # enilm.norm.denormalize(y.squeeze(), y_mean, y_std),
            enilm.norm.denormalize(y, y_mean, y_std),
            # enilm.norm.denormalize(model(np.expand_dims(x, axis=2)).numpy(), y_mean, y_std),
            # enilm.norm.denormalize(model(x).numpy(), y_mean, y_std),
            enilm.norm.denormalize(pred_fn(x), y_mean, y_std),
        ))

    return np.average(model_mae)
