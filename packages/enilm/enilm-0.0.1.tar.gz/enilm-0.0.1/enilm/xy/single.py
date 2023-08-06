import gc
from typing import Tuple

import enilm
from enilm import nilmtk
import pandas as pd


def get_and_align(mains_elec: nilmtk.ElecMeter, app_elec: nilmtk.ElecMeter, **load_kwargs) \
        -> Tuple[pd.Series, pd.Series]:
    x: pd.Series
    y: pd.Series

    # load y and then x with y sections
    y = app_elec.power_series_all_data(**load_kwargs)
    if y is None:
        raise enilm.xy.expections.IsEmpty('y is None')

    load_kwargs['sections'] = [nilmtk.TimeFrame(
        start=y.index[0],
        end=y.index[-1]
    )]
    x = mains_elec.power_series_all_data(**load_kwargs)
    if x is None:
        raise enilm.xy.expections.IsEmpty('x is None')

    # align
    data = pd.concat([x, y], axis=1, keys=['x', 'y']).dropna()
    x, y = data.x, data.y
    del data
    gc.collect()

    assert len(x) == len(y)
    assert x.isna().sum() == y.isna().sum() == 0

    return x, y
