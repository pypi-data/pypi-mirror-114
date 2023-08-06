"""
NOTE: Output is expected to be passed to some fit method thus, we can't use the NamedTuple XYArray for the return
 see https://www.tensorflow.org/api_docs/python/tf/keras/Model#fit for explanation
"""
import gc
from typing import Dict, Literal, Tuple, Optional, Iterable, Callable, Iterator

import enilm
from enilm import nilmtk
import numpy as np
import pandas as pd

# function to be called before yielding each x and y pair
PreprocessFn = Callable[
    [pd.Series, Dict[enilm.etypes.AppName, pd.Series]],  # receive pd.Series
    Tuple[np.ndarray, Dict[enilm.etypes.AppName, np.ndarray]]  # must return np.ndarray
]


def _load(
        _set: Literal['train', 'test'],
        config: enilm.config.ExpConfig,
        preprocess: Optional[PreprocessFn] = None) \
        -> Iterator[Tuple[np.ndarray, Dict[enilm.etypes.AppName, np.ndarray]]]:
    selected_data_sel: Iterable[enilm.config.DataSel]
    if _set == 'train':
        selected_data_sel = config.train
    elif _set == 'test':
        selected_data_sel = config.test
    else:
        raise ValueError

    for data_sel in selected_data_sel:
        # repeated variables depending on set
        dataset: enilm.etypes.Datasets = data_sel.dataset
        houses: Iterable[enilm.etypes.HouseNr] = data_sel.houses
        sections: Optional[Dict[enilm.etypes.HouseNr, Iterable[nilmtk.TimeFrame]]] = data_sel.sections

        # load data for each house
        for house in houses:
            # create load kwargs
            load_kwargs = enilm.load_kwargs.LoadKwargs(
                sample_period=config.sample_period,
            )
            if sections is not None:
                load_kwargs.sections = sections[house]

            # load elecs
            mains: nilmtk.ElecMeter
            apps_elecs: Dict[enilm.etypes.AppName, nilmtk.ElecMeter]
            with enilm.context.sec(header=f'loading {_set} elecs for house {house}', mem=True):
                loaded = enilm.datasets.loaders.load(dataset, house)
                mains = loaded.elec.mains()
                apps_elecs = {}
                for app_name in config.appliances:
                    apps_elecs[app_name] = enilm.appliances.get_elec(app_name, loaded.elec)

            # load x for mains, y for each appliance
            with enilm.context.sec(header=f'loading & aligning data for house {house}', mem=True):
                gen = enilm.xy.multi_gen.get_and_align_gen(
                    mains_elec=mains,
                    apps_elecs=apps_elecs,
                    batch_size=config.batch_size,
                    epochs=config.epochs,
                    load_kwargs=load_kwargs,
                )

                # declarations
                x_ser: pd.Series = pd.Series()
                y_ser: Dict[enilm.etypes.AppName, pd.Series] = {}
                x: np.ndarray = np.array([])
                y: Dict[enilm.etypes.AppName, np.ndarray] = {}
                chunk_id = 0
                for x_ser, y_ser in gen:
                    chunk_id += 1

                    # sanity checks
                    for _app_name in y_ser.keys():
                        assert len(x_ser) == len(y_ser[_app_name])

                    # skip if smaller than required window size
                    if len(x_ser) < config.win_size:
                        continue

                    with enilm.context.sec(header=f'Getting chunk {chunk_id} from generator', mem=True):
                        #  preprocessing
                        if preprocess is not None:
                            x, y = preprocess(x_ser, y_ser)
                        else:
                            x = x_ser.to_numpy()
                            y = {app_name: y_ser[app_name].to_numpy() for app_name in config.appliances}

                        # shuffling
                        if config.shuffle:
                            perm = np.random.permutation(len(x))
                            x = x[perm]
                            y = {k: v[perm] for k, v in y.items()}

                        # sanity check
                        for app_y in y.values():
                            assert len(x) == len(app_y)

                        yield x, y

                        del x, y, x_ser, y_ser
                        gc.collect()


def train_from_config(config: enilm.config.ExpConfig, preprocess: Optional[PreprocessFn] = None) \
        -> Iterator[Tuple[np.ndarray, Dict[enilm.etypes.AppName, np.ndarray]]]:
    return _load('train', config, preprocess)


def test_from_config(config: enilm.config.ExpConfig, preprocess: Optional[PreprocessFn] = None) \
        -> Iterator[Tuple[np.ndarray, Dict[enilm.etypes.AppName, np.ndarray]]]:
    return _load('test', config, preprocess)

# def from_exp_config(config: enilm.config.ExpConfig):
#     return enilm.etypes.xy.TrainTestXYArray(
#         train=train_from_config(config),
#         test=test_from_config(config),
#     )
