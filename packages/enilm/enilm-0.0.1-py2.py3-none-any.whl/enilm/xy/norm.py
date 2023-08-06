from typing import Dict, Optional, Iterable, Tuple, Callable

import enilm
import numpy as np


def compute_mean_std(
        x: np.ndarray,
        y: Dict[enilm.etypes.AppName, np.ndarray],
) -> enilm.etypes.xy.XYNormParams:
    y_mean = {}
    y_std = {}

    for app_name in y.keys():
        y_mean[app_name] = float(np.mean(y[app_name]))
        y_std[app_name] = float(np.std(y[app_name]))
    return enilm.etypes.xy.XYNormParams(
        float(np.mean(x)), float(np.std(x)),
        y_mean, y_std
    )


def _apply(
        fn: Callable[[np.ndarray, float, float], np.ndarray],
        xy: enilm.etypes.xy.XYArray,
        appliances: Iterable[enilm.etypes.AppName],
        *,
        x_mean: Optional[float] = None,
        x_std: Optional[float] = None,
        y_mean: Optional[Dict[enilm.etypes.AppName, float]] = None,
        y_std: Optional[Dict[enilm.etypes.AppName, float]] = None,
) -> enilm.etypes.xy.XYArray:
    # assert providing (mean AND std) or (neither)
    if x_mean is not None:
        assert x_std is not None
    if y_mean is not None:
        assert y_std is not None

    x, y = xy
    x_res: np.ndarray
    y_res: Dict[enilm.etypes.AppName, np.ndarray] = {}
    with enilm.context.sec(header='[de]normalize', mem=True):
        if x_mean is None:
            x_mean = float(np.mean(x))
        if x_std is None:
            x_std = float(np.std(x))
        x_res = fn(x, x_mean, x_std)

        # compute mean and std if not provided
        if y_mean is None:
            _, _, y_mean, y_std = compute_mean_std(x, y)

        for app_name in appliances:
            y_res[app_name] = fn(y[app_name], y_mean[app_name], y_std[app_name])

    return enilm.etypes.xy.XYArray(x_res, y_res)


def norm(xy: enilm.etypes.xy.XYArray,
         appliances: Iterable[enilm.etypes.AppName],
         x_mean: Optional[float] = None,
         x_std: Optional[float] = None,
         y_mean: Optional[Dict[enilm.etypes.AppName, float]] = None,
         y_std: Optional[Dict[enilm.etypes.AppName, float]] = None,
         ) -> enilm.etypes.xy.XYArray:
    return _apply(
        enilm.norm.normalize, xy, appliances,
        x_mean=x_mean,
        x_std=x_std,
        y_mean=y_mean,
        y_std=y_std
    )


def denorm(xy: enilm.etypes.xy.XYArray,
           appliances: Iterable[enilm.etypes.AppName],
           x_mean: Optional[float] = None,
           x_std: Optional[float] = None,
           y_mean: Optional[Dict[enilm.etypes.AppName, float]] = None,
           y_std: Optional[Dict[enilm.etypes.AppName, float]] = None,
           ) -> enilm.etypes.xy.XYArray:
    return _apply(
        enilm.norm.denormalize, xy, appliances,
        x_mean=x_mean,
        x_std=x_std,
        y_mean=y_mean,
        y_std=y_std
    )
