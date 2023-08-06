from typing import Dict
from unittest import TestCase

import enilm
import numpy as np
import pandas as pd

config = enilm.config.ExpConfig(
    exp_n=-1,
    notes='TEST',
    appliances=['fridge'],
    win_size=599,
    sample_period=60,
    repeats=1,
    epochs=20,
    batch_size=1024,
    shuffle=False,
    validation_split=0.2,
    model_id='TEST',
    train=[
        enilm.config.DataSel(
            dataset=enilm.etypes.Datasets.REDD,
            houses=[2],
        ),
    ],
    test=[
        enilm.config.DataSel(
            dataset=enilm.etypes.Datasets.REDD,
            houses=[1],
        ),
    ],
)


class Test(TestCase):
    def test_sae(self):
        app_name = config.appliances[0]
        xy: enilm.etypes.xy.XYArray = enilm.xy.load.train_from_config(config)

        x_norm: np.ndarray
        y_norm: Dict[enilm.etypes.AppName, np.ndarray]
        y_mean, y_std = enilm.xy.norm.compute_mean_std(xy.y, config.appliances)
        x_norm, y_norm = enilm.xy.norm.norm(xy, config.appliances, y_mean=y_mean, y_std=y_std)

        x_chunks: np.ndarray
        y_chunks: Dict[enilm.etypes.AppName, np.ndarray]
        x_chunks = enilm.windowing.rolling(x_norm, config.win_size)
        y_chunks = {
            k.replace(' ', '_'): enilm.windowing.midpoints(v, config.win_size) for k, v in y_norm.items()
        }

        model = enilm.models.test.s2p_seq(config.win_size)
        enilm.tests.common.set_model_weights_to_ones(model)

        sae = enilm.losses.sae.sae(
            xy.y[app_name].flatten(),
            enilm.norm.denormalize(model(x_chunks).numpy().flatten(), y_mean[app_name], y_std[app_name]),
        )

        self.assertAlmostEqual(sae, 6564383000000.0)

    def test_sae_period(self):
        app_name = config.appliances[0]
        xy: enilm.etypes.xy.XYArray = enilm.xy.load.train_from_config(config)

        x_norm: np.ndarray
        y_norm: Dict[enilm.etypes.AppName, np.ndarray]
        y_mean, y_std = enilm.xy.norm.compute_mean_std(xy.y, config.appliances)
        x_norm, y_norm = enilm.xy.norm.norm(xy, config.appliances, y_mean=y_mean, y_std=y_std)

        x_chunks: np.ndarray
        y_chunks: Dict[enilm.etypes.AppName, np.ndarray]
        x_chunks = enilm.windowing.rolling(x_norm, config.win_size)
        y_chunks = {
            k.replace(' ', '_'): enilm.windowing.midpoints(v, config.win_size) for k, v in y_norm.items()
        }

        model = enilm.models.test.s2p_seq(config.win_size)
        enilm.tests.common.set_model_weights_to_ones(model)

        sae = enilm.losses.sae.sae_period(
            xy.y[app_name].flatten(),
            enilm.norm.denormalize(model(x_chunks).numpy().flatten(), y_mean[app_name], y_std[app_name]),
            pd.Timedelta('1D'),
            config.sample_period
        )

        # TODO
        # self.assertAlmostEqual(sae, 6564383000000.0)
