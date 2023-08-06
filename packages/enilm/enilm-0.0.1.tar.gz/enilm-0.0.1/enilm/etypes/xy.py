from typing import NamedTuple, Dict

import pandas as pd
import numpy as np

from .__main__ import AppName


class XYSeries(NamedTuple):
    x: pd.Series
    y: Dict[AppName, pd.Series]


class XYArray(NamedTuple):
    x: np.ndarray
    y: Dict[AppName, np.ndarray]


class TrainTestXYArray(NamedTuple):
    train: XYArray
    test: XYArray


class XYNormParams(NamedTuple):
    x_mean: float
    x_std: float
    y_mean: Dict[AppName, float]
    y_std: Dict[AppName, float]
