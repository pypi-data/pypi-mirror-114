import gc
from typing import Optional, Dict

import enilm
from enilm import nilmtk
import pandas as pd


def get_and_align(
        mains_elec: nilmtk.ElecMeter,
        apps_elecs: Dict[enilm.etypes.AppName, nilmtk.ElecMeter],
        load_kwargs: Optional[enilm.load_kwargs.LoadKwargs] = None) -> enilm.etypes.xy.XYSeries:
    # load kwargs
    if load_kwargs is None:
        load_kwargs = enilm.load_kwargs.LoadKwargs()

    # load y and then x with y sections
    y_series: Dict[str, pd.Series] = {}
    y_timeframe: Optional[nilmtk.TimeFrame] = None
    for app_name, app_elec in apps_elecs.items():
        # load
        curr_y = app_elec.power_series_all_data(**load_kwargs.to_dict())

        # check
        if curr_y is None:
            if y_timeframe is None:
                raise enilm.xy.expections.IsEmpty(f'y for {app_elec} is None')
            else:
                raise enilm.xy.expections.IsEmpty(f'y for {app_elec} is None for {y_timeframe}')

        # save
        y_series[app_name] = curr_y

        # add timeframe to load args
        if y_timeframe is None:
            y_timeframe = nilmtk.TimeFrame(
                start=curr_y.index[0],
                end=curr_y.index[-1]
            )
            load_kwargs.sections = [y_timeframe]

    # section
    x: pd.Series = mains_elec.power_series_all_data(**load_kwargs.to_dict())
    if x is None:
        raise enilm.xy.expections.IsEmpty('x is None')

    # align
    data = pd.concat([x, *y_series.values()], axis=1, keys=['x', *y_series.keys()]).dropna()

    # x
    x = data['x']
    assert x.isna().sum() == 0

    # y
    y = {}
    for app_name in apps_elecs.keys():
        curr_y = data[app_name]
        assert curr_y.isna().sum() == 0
        assert len(x) == len(curr_y)
        y[app_name] = curr_y

    # free mem
    del data
    gc.collect()

    return enilm.etypes.xy.XYSeries(x, y)
