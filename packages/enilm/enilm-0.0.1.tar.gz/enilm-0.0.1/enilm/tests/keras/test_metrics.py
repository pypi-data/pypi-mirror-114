import datetime
import os
import sys
from io import StringIO
from pathlib import Path
from typing import Dict
from unittest import TestCase

import enilm
import numpy as np
import tensorflow as tf
import tensorflow.python.framework.ops


class TestMetrics(TestCase):
    def setUp(self) -> None:
        tz = enilm.nilmdt.get_tzinfo_from_ds(enilm.etypes.Datasets.REDD)
        self.config: enilm.config.ExpConfig = enilm.config.ExpConfig(
            exp_n=999,
            appliances=['fridge', 'dish washer'],
            win_size=199,
            sample_period=60,
            repeats=6,
            epochs=80,
            batch_size=1000,
            shuffle=False,
            validation_split=0.2,
            model_id='TESTING',
            train=[enilm.config.DataSel(
                houses=[2, 3],
                dataset=enilm.etypes.Datasets.REDD,
                sections={
                    2: [enilm.nilmdt.get_day_timeframe(datetime.date(2011, 4, 25), tz)],
                    3: [enilm.nilmdt.get_day_timeframe(datetime.date(2011, 4, 25), tz)],
                },
            )],
            test=[enilm.config.DataSel(
                houses=[1],
                dataset=enilm.etypes.Datasets.REDD,
            )],
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

    def test_denorm_mae_single_appliance(self):
        model = enilm.models.test.s2p_sing_ker(self.config.win_size, _compile=False)
        model.compile(
            loss='mse',
            optimizer='adam',
            metrics=[
                enilm.keras.metrics.DenormMAE(self.y_mean['fridge'], self.y_std['fridge'])
            ],
        )

        old_stdout = sys.stdout
        result = StringIO()
        sys.stdout = result

        model.fit(self.x_chunks, self.y_chunks['fridge'], epochs=5)

        sys.stdout = old_stdout
        printed = result.getvalue()

        self.assertIn('denorm_mae', printed)

    def test_denorm_mae_multi_appliance(self):
        model = enilm.models.test.s2p_sing_ker_mtl(self.config.win_size, self.config.appliances, _compile=False)

        metrics: Dict[enilm.etypes.AppName, enilm.keras.metrics.DenormMAE] = {}
        for app_name in self.config.appliances:
            _app_name = app_name.replace(' ', '_')
            metrics[_app_name] = enilm.keras.metrics.DenormMAE(self.y_mean[app_name], self.y_std[app_name])

        model.compile(
            loss='mse',
            optimizer='adam',
            metrics=metrics,
        )

        old_stdout = sys.stdout
        result = StringIO()
        sys.stdout = result

        model.fit(self.x_chunks, self.y_chunks, epochs=5)

        sys.stdout = old_stdout
        printed = result.getvalue()

        self.assertIn('dish_washer_denorm_mae', printed)
        self.assertIn('fridge_denorm_mae', printed)

    def test_loading_saving_with_custom_metric(self):
        model = enilm.models.test.s2p_sing_ker_mtl(self.config.win_size, self.config.appliances, _compile=False)

        metrics: Dict[enilm.etypes.AppName, enilm.keras.metrics.DenormMAE] = {}
        for app_name in self.config.appliances:
            _app_name = app_name.replace(' ', '_')
            metrics[_app_name] = enilm.keras.metrics.DenormMAE(self.y_mean[app_name], self.y_std[app_name])

        model.compile(
            loss='mse',
            optimizer='adam',
            metrics=metrics,
        )

        enilm.models.utils.file.save_model(model, Path('model.h5'))
        loaded_model = enilm.models.utils.file.load_model(
            Path('model.h5'),
            custom_objects={'DenormMAE': enilm.keras.metrics.DenormMAE}
        )

        # assert same output
        x = np.random.random((100, self.config.win_size))
        y1: Dict[enilm.etypes.AppName, tensorflow.python.framework.ops.EagerTensor] = model(x)
        y2: Dict[enilm.etypes.AppName, tensorflow.python.framework.ops.EagerTensor] = loaded_model(x)

        for app_name in y1.keys():
            self.assertTrue(np.all(np.all(y1[app_name].numpy() == y2[app_name].numpy())))

        # delete model
        os.remove(Path('model.h5'))
