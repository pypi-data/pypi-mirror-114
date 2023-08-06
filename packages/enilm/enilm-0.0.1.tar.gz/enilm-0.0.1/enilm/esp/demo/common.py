from typing import Dict, Optional

import numpy as np
import pandas as pd
from enilm import nilmtk
import enilm

norm_params: Optional[enilm.etypes.xy.XYNormParams] = None


def get_data(skip_days: int = 0) -> enilm.etypes.xy.XYSeries:
    apps_names = ['dish washer', 'fridge', 'washing machine']
    _apps_names = ['dish_washer', 'fridge', 'washing_machine']

    loaded = enilm.datasets.loaders.load(enilm.etypes.Datasets.UKDALE, 2)
    apps_elecs = {an: enilm.appliances.get_elec(an, loaded.elec) for an in apps_names}
    tf: nilmtk.TimeFrame = loaded.elec.get_timeframe()
    day = pd.Timestamp(tf.start)

    if skip_days > 0:
        day += pd.Timedelta(f'{skip_days}day')

    while day < tf.end:
        try:
            return enilm.xy.multi.get_and_align(
                mains_elec=loaded.elec.mains(),
                apps_elecs=apps_elecs,
                load_kwargs=enilm.load_kwargs.LoadKwargs(
                    sample_period=60,
                    sections=[
                        nilmtk.TimeFrame(start=day, end=day + pd.Timedelta("1day"))
                    ],
                ),
            )
        except enilm.xy.expections.IsEmpty:
            day += pd.Timedelta('1day')


def norm(xy: enilm.etypes.xy.XYSeries) -> enilm.etypes.xy.XYArray:
    global norm_params

    apps_names = list(xy.y.keys())
    x = xy.x.to_numpy()
    y = {k: v.to_numpy() for k, v in xy.y.items()}

    norm_params = enilm.xy.norm.compute_mean_std(x, y)

    return enilm.xy.norm.norm(
        enilm.etypes.xy.XYArray(x, y), apps_names,
        x_mean=norm_params.x_mean, x_std=norm_params.x_std,
        y_mean=norm_params.y_mean, y_std=norm_params.y_std
    )


def chunkize(xy: enilm.etypes.xy.XYArray, win_size: int) -> enilm.etypes.xy.XYArray:
    x_chunks: np.ndarray
    y_chunks: Dict[enilm.etypes.AppName, np.ndarray]

    x_chunks = enilm.windowing.rolling(xy.x, win_size)
    y_chunks = {
        k.replace(' ', '_'): enilm.windowing.midpoints(v, win_size) for k, v in xy.y.items()
    }

    return enilm.etypes.xy.XYArray(x_chunks, y_chunks)
