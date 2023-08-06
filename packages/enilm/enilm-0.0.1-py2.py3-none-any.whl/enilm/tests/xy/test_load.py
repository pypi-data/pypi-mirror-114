import datetime
from unittest import TestCase

import enilm
import numpy as np


class Test(TestCase):
    def test_from_config(self):
        ds = enilm.etypes.Datasets.REDD
        tz = enilm.nilmdt.get_tzinfo_from_ds(ds)
        apps_names = ['fridge', 'microwave']

        config = enilm.config.ExpConfig(
            exp_n=1,
            appliances=apps_names,
            win_size=599,
            sample_period=60,
            repeats=6,
            epochs=80,
            batch_size=1000,
            shuffle=True,
            validation_split=0.2,
            model_id='s2p_seq_mtl4',
            train=[enilm.config.DataSel(
                houses=[
                    2,  # TimeFrame(start='2011-04-17 19:18:27-04:00', end='2011-05-22 19:59:16-04:00)
                    3,  # TimeFrame(start='2011-04-16 01:11:27-04:00', end='2011-05-30 20:19:54-04:00')
                ],
                dataset=ds,
                sections={
                    2: [
                        enilm.nilmdt.get_day_timeframe(datetime.date(2011, 4, 18), tz),
                        enilm.nilmdt.get_day_timeframe(datetime.date(2011, 4, 20), tz),
                    ],
                    3: [
                        enilm.nilmdt.get_day_timeframe(datetime.date(2011, 4, 28), tz),
                    ]
                },
            )],

            test=[enilm.config.DataSel(
                dataset=ds,
                houses=[1],  # TimeFrame(start='2011-04-18 09:22:09-04:00', end='2011-05-24 15:57:02-04:00'
            )]
        )

        (x_train, y_train), (x_test, y_test) = enilm.xy.load.from_exp_config(config)

        self.assertIsInstance(x_train, np.ndarray)
        self.assertIsInstance(x_test, np.ndarray)
        self.assertListEqual(list(y_train.keys()), ['fridge', 'microwave'])
        self.assertListEqual(list(y_test.keys()), ['fridge', 'microwave'])

        # since only 3 days for training
        self.assertLess(len(x_train), len(x_test))

    def test_loading_from_multiple_datasets(self):
        tz_redd = enilm.nilmdt.get_tzinfo_from_ds(enilm.etypes.Datasets.REDD)
        tz_refit = enilm.nilmdt.get_tzinfo_from_ds(enilm.etypes.Datasets.REFIT)

        config = enilm.config.ExpConfig(
            exp_n=1,
            appliances=['microwave', 'dish washer'],
            win_size=599,
            sample_period=60,
            repeats=6,
            epochs=80,
            batch_size=1000,
            shuffle=True,
            validation_split=0.2,
            model_id='s2p_seq_mtl4',
            train=[
                enilm.config.DataSel(
                    houses=[
                        2,  # TimeFrame(start='2011-04-17 19:18:27-04:00', end='2011-05-22 19:59:16-04:00)
                        3,  # TimeFrame(start='2011-04-16 01:11:27-04:00', end='2011-05-30 20:19:54-04:00')
                    ],
                    dataset=enilm.etypes.Datasets.REDD,
                    sections={
                        2: [
                            enilm.nilmdt.get_day_timeframe(datetime.date(2011, 4, 18), tz_redd),
                            enilm.nilmdt.get_day_timeframe(datetime.date(2011, 4, 20), tz_redd),
                        ],
                        3: [
                            enilm.nilmdt.get_day_timeframe(datetime.date(2011, 4, 28), tz_redd),
                        ]
                    },
                ),
                enilm.config.DataSel(
                    dataset=enilm.etypes.Datasets.REFIT,
                    houses=[3],
                    sections={
                        3: [
                            enilm.nilmdt.get_month_timeframe(2013, 9, tz_refit),
                        ]
                    }
                )
            ],
        )

        xy = enilm.xy.load.train_from_config(config)
        self.assertEqual(xy.x, 10097)
        self.assertEqual(xy.x, xy.y)
