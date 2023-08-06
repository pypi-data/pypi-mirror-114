import datetime
from unittest import TestCase
from typing import Dict, List

import enilm
import numpy as np


class TestMetrics(TestCase):
    def setUp(self) -> None:
        tz = enilm.nilmdt.get_tzinfo_from_ds(enilm.etypes.Datasets.REDD)
        self.config: enilm.config.ExpConfig = enilm.config.ExpConfig(
            exp_n=37,
            appliances=['fridge'],

            win_size=599,
            sample_period=60,
            repeats=6,
            epochs=80,
            batch_size=1000,
            shuffle=False,
            validation_split=0.2,

            model_id='s2p_seq_mtl4',

            train_houses=[2, 3],
            train_dataset=enilm.etypes.Datasets.REDD,
            train_sections={
                2: [enilm.nilmdt.get_day_timeframe(datetime.date(2011, 4, 25), tz)],
                3: [enilm.nilmdt.get_day_timeframe(datetime.date(2011, 4, 25), tz)],
            },

            test_houses=[1],
            test_dataset=enilm.etypes.Datasets.REDD,
        )

        xy = enilm.xy.load.train_from_config(self.config)

        # norm
        x_mean, x_std = float(np.mean(xy.x)), float(np.std(xy.x))
        self.y_mean, self.y_std = enilm.xy.norm.compute_mean_std(xy.y, self.config.appliances)
        x_norm, y_norm = enilm.xy.norm.norm(xy, self.config.appliances)

        # chunks
        self.x_chunks: np.ndarray = enilm.windowing.rolling(x_norm, self.config.win_size)
        self.y_chunks: Dict[enilm.etypes.AppName, np.ndarray] = {
            k.replace(' ', '_'): enilm.windowing.midpoints(v, self.config.win_size) for k, v in y_norm.items()
        }

    def test_denrom_mae_s2p_sing_ker(self):
        model = enilm.models.test.s2p_sing_ker(self.config.win_size)
        enilm.tests.common.set_model_weights_to_ones(model)
        should = 457305300664320.0

        for app_name in self.config.appliances:
            curr_denorm_mae = enilm.metrics.denrom_mae(
                lambda _x: model(_x).numpy(),
                self.x_chunks,
                self.y_chunks[app_name],
                self.y_mean[app_name],
                self.y_std[app_name]
            )
            self.assertAlmostEqual(curr_denorm_mae, should)

    def test_denorm_mae_s2p_seq_mtl(self):
        model = enilm.models.test.s2p_seq_mtl(self.config.win_size, ['a', 'b'], _compile=False)
        enilm.tests.common.set_model_weights_to_zeros(model)
        should = 78.27717

        for id, app_name in enumerate(self.config.appliances):
            curr_denorm_mae = enilm.metrics.denrom_mae(
                lambda _x: model(_x)[id].numpy(),
                self.x_chunks,
                self.y_chunks[app_name],
                self.y_mean[app_name],
                self.y_std[app_name]
            )
            self.assertLessEqual(abs(should - curr_denorm_mae), 0.1)
