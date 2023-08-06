import numpy as np
import pandas as pd

import enilm


def sae(app_gt: np.ndarray, app_pred: np.ndarray) -> np.float:
    assert len(app_gt.shape) == 1
    assert len(app_pred.shape) == 1
    assert app_gt.shape[0] == app_pred.shape[0]

    app_gt_sum = np.sum(app_gt)
    app_pred_sum = np.sum(app_pred)
    return np.abs(app_gt_sum - app_pred_sum) / app_gt_sum


def sae_period(app_gt: np.ndarray, app_pred: np.ndarray, period: pd.Timedelta, sample_period: int) -> np.float:
    assert len(app_gt.shape) == 1
    assert len(app_pred.shape) == 1
    assert app_gt.shape[0] == app_pred.shape[0]

    n_samples_per_period = int(period.total_seconds() // sample_period)
    app_gt_chunks = enilm.windowing.chunkize(app_gt, chunk_size=n_samples_per_period)
    app_pred_chunks = enilm.windowing.chunkize(app_pred, chunk_size=n_samples_per_period)

    sae_per_period = []
    for app_gt_chunk, app_pred_chunk in zip(app_gt_chunks, app_pred_chunks):
        sae_per_period.append(sae(app_gt_chunk, app_pred_chunk))

    return np.average(sae_per_period)
