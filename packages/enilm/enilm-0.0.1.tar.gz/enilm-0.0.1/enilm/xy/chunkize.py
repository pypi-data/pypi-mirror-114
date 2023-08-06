from typing import Dict

import numpy as np

import enilm


def s2p(xy: enilm.etypes.xy.XYArray, win_size: int) -> enilm.etypes.xy.XYArray:
    x_chunks: np.ndarray
    y_chunks: Dict[enilm.etypes.AppName, np.ndarray]

    x_chunks = enilm.windowing.rolling(xy.x, win_size)
    y_chunks = {
        k.replace(' ', '_'): enilm.windowing.midpoints(v, win_size) for k, v in xy.y.items()
    }

    return enilm.etypes.xy.XYArray(x_chunks, y_chunks)
