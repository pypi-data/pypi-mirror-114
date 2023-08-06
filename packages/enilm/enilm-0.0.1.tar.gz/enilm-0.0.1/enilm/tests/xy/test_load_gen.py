from typing import Dict, Tuple
from unittest import TestCase

import enilm
import numpy as np
import pandas as pd


class Test(TestCase):
    def setUp(self) -> None:
        self.config = enilm.config.ExpConfig(
            exp_n=1,
            appliances=['microwave', 'dish washer'],
            win_size=599,
            sample_period=60,
            repeats=6,
            epochs=2,
            batch_size=1000,
            shuffle=True,
            validation_split=0.2,
            model_id='s2p_seq_mtl4',
            train=[
                enilm.config.DataSel(
                    dataset=enilm.etypes.Datasets.REDD,
                    houses=[1]
                ),
                enilm.config.DataSel(
                    dataset=enilm.etypes.Datasets.REFIT,
                    houses=[2],
                )
            ],
        )

    def test_loading_from_multiple_datasets(self):
        for x, y in enilm.xy.load_gen.train_from_config(self.config):
            for app_name in self.config.appliances:
                self.assertEqual(len(x), len(y[app_name]))

    def test_preprocess(self):
        def preprocess(x_ser: pd.Series, y_ser: Dict[enilm.etypes.AppName, pd.Series]) \
                -> Tuple[np.ndarray, Dict[enilm.etypes.AppName, np.ndarray]]:
            x = x_ser.to_numpy()
            y = {app_name: y_ser[app_name].to_numpy() for app_name in self.config.appliances}

            y_mean, y_std = enilm.xy.norm.compute_mean_std(y, self.config.appliances)
            x_norm, y_norm = enilm.xy.norm.norm(
                enilm.etypes.xy.XYArray(x, y),
                self.config.appliances,
                y_mean=y_mean,
                y_std=y_std
            )

            x_chunks: np.ndarray
            y_chunks: Dict[enilm.etypes.AppName, np.ndarray]
            with enilm.context.sec(header='chunking', mem=True):
                x_chunks = enilm.windowing.rolling(x_norm, self.config.win_size)
                y_chunks = {
                    k.replace(' ', '_'): enilm.windowing.midpoints(v, self.config.win_size) for k, v in y_norm.items()
                }
            return x_chunks, y_chunks

        for x, y in enilm.xy.load_gen.train_from_config(self.config, preprocess):
            for _app_name in y.keys():
                self.assertEqual(x.shape[0], y[_app_name].shape[0])
            self.assertEqual(x.shape[1], self.config.win_size)
