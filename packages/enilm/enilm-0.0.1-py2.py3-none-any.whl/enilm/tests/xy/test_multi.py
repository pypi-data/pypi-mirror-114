from unittest import TestCase

import enilm
import pandas as pd
import numpy as np


class Test(TestCase):
    def setUp(self) -> None:
        loaded = enilm.datasets.loaders.load(enilm.etypes.Datasets.REDD, 3)

        self.elec = loaded.elec
        self.apps_names = ['fridge', 'washing machine', 'dish washer']
        self.apps_elecs = {}
        for app_name in self.apps_names:
            self.apps_elecs[app_name] = enilm.appliances.get_elec(app_name, self.elec)

    def test_multi(self):
        x, y = enilm.xy.get_and_align_multi_y(
            self.elec.mains(),
            self.apps_elecs,
            sample_period=60
        )

        # series
        self.assertTrue(isinstance(x, pd.Series))
        self.assertTrue(isinstance(y[self.apps_names[0]], pd.Series))

        # as required
        self.assertListEqual(list(y.keys()), self.apps_names)

        # same time indices
        for app_name in self.apps_names:
            self.assertTrue(np.all(x.index == y[app_name].index))

# def test_multi_y_redd(self):
#     elec = enilm.datasets.loaders.load(enilm.etypes.Datasets.REDD, 2).elec
#     app_elec = enilm.appliances.get_elec('fridge', elec)
#     tz = enilm.nilmdt.get_tzinfo_from_ds(enilm.etypes.Datasets.REDD)
#     sec = [enilm.nilmdt.get_month_timeframe(2011, 4, tz)]
#     xy = enilm.xy.get_and_align_multi_y(elec.mains(), {'fridge': app_elec}, sections=sec)
#     print()
