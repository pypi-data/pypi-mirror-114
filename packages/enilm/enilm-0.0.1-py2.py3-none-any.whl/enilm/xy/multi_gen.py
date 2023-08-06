import gc
from typing import Optional, Dict, Iterator, Iterable

import enilm
from enilm import nilmtk
import pandas as pd


def _sub_gen(
        apps_elecs,
        first_app_name,
        y_series,
        batch_size,
        first_app_elec_gen,
        load_kwargs,
        mains_elec,
        apps_names) -> Optional[enilm.etypes.xy.XYSeries]:
    # load y and then x with y sections
    first_iter: bool = True
    for app_name, app_elec in apps_elecs.items():
        if first_iter:
            assert app_name == first_app_name
            first_iter = False

            # load until we have at least a batch_size of samples
            curr_y = y_series[app_name]
            while len(curr_y) < batch_size:
                next_y_chunk = next(first_app_elec_gen, None)
                if next_y_chunk is None:  # no data anymore
                    # exit and stop generator for this epoch
                    return
                curr_y = pd.concat((curr_y, next_y_chunk))  # TODO: avoid pd.concat in loop

            # exit if data length is not enough for a batch
            if len(curr_y) < batch_size:
                return

            # save
            y_series[app_name] = curr_y

            # timeframe to load data for next appliances
            load_kwargs['sections'] = [nilmtk.TimeFrame(
                y_series[app_name].index[0],
                y_series[app_name].index[-1],
            )]
        else:
            # load data for each appliance to specified section from first appliance
            should_reload: bool = True

            # if we can do it with current data, then no need to reload!
            if len(y_series[app_name]) > batch_size:
                assert len(load_kwargs['sections']) == 1
                first_app_tf: nilmtk.TimeFrame = load_kwargs['sections'][0]

                if y_series[app_name].index[0] < first_app_tf.start:
                    new_ser = y_series[app_name][y_series[app_name].index > first_app_tf.start]
                    if len(new_ser) > batch_size:
                        y_series[app_name] = new_ser
                        should_reload = False

            # reload data
            if should_reload:
                curr_y = app_elec.power_series_all_data(**load_kwargs)
                if curr_y is None or len(curr_y) < batch_size:
                    # exist if no or not enough data
                    return
                y_series[app_name] = curr_y

    # get data to use in this chunk (batch_size of each loaded data of app)
    # and remove this data from y_series
    y_chunks: Dict[str, pd.Series] = {}
    for app_name in apps_names:
        y_chunks[app_name] = y_series[app_name][:batch_size]

        # delete this data from y_series
        y_series[app_name] = y_series[app_name][batch_size:]

    # load mains (with section of first appliance)
    x: pd.Series = mains_elec.power_series_all_data(**load_kwargs)
    if x is None:
        raise enilm.xy.expections.IsEmpty('x is None')

    # align
    data = pd.concat([x, *y_chunks.values()], axis=1, keys=['x', *apps_names]).dropna()

    # final x
    x = data['x']
    assert x.isna().sum() == 0

    # final y
    y = {}
    for app_name in apps_names:
        curr_y = data[app_name]
        assert curr_y.isna().sum() == 0
        assert len(x) == len(curr_y)
        y[app_name] = curr_y

    # free mem
    del data
    gc.collect()

    return enilm.etypes.xy.XYSeries(x, y)


def get_and_align_gen(
        mains_elec: nilmtk.ElecMeter,
        apps_elecs: Dict[enilm.etypes.AppName, nilmtk.ElecMeter],
        batch_size: int,
        epochs: int,
        load_kwargs: Optional[enilm.load_kwargs.LoadKwargs] = None,
) -> Iterator[enilm.etypes.xy.XYSeries]:
    # load kwargs to dict
    if load_kwargs is not None:
        load_kwargs = load_kwargs.to_dict()
    else:
        load_kwargs = {}

    # sections not supported yet (since it is used in sub_generator)
    if 'sections' in load_kwargs:
        raise NotImplementedError

    # all apps names
    apps_names = list(apps_elecs.keys())

    for epoch in range(epochs):
        # to hold data for each appliance
        y_series: Dict[str, pd.Series] = {app_name: pd.Series() for app_name in apps_names}

        # create generator only for first appliance
        # other apps and mains would be loaded directly utilizing the section parameter
        first_app_name = apps_names[0]
        first_app_elec_gen = apps_elecs[first_app_name].power_series(**load_kwargs)

        while True:
            xy = _sub_gen(apps_elecs, first_app_name, y_series, batch_size, first_app_elec_gen, load_kwargs, mains_elec,
                          apps_names)
            if xy is not None:
                yield xy
            else:
                break

# def compute_steps_per_epoch(gen: Iterable[enilm.etypes.xy.XYSeries], epochs: int):
#     total = len(list(gen))
#     return total // epochs
