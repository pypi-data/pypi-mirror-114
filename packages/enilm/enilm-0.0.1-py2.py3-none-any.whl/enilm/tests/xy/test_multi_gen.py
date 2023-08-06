from unittest import TestCase

import enilm
import numpy as np


class Test(TestCase):
    def setUp(self) -> None:
        loaded = enilm.datasets.loaders.load(enilm.etypes.Datasets.REDD, 3)

        self.elec = loaded.elec
        self.apps_names = ['fridge', 'washing machine', 'dish washer']
        self.apps_elecs = {}
        for app_name in self.apps_names:
            self.apps_elecs[app_name] = enilm.appliances.get_elec(app_name, self.elec)

    def test_multi_gen(self):
        batch_size = 1_000
        gen = enilm.xy.multi_gen.get_and_align_gen(
            mains_elec=self.elec.mains(),
            apps_elecs=self.apps_elecs,
            batch_size=batch_size,
            epochs=2,
        )

        for xy in gen:
            self.assertLessEqual(len(xy.x), batch_size)
            for app_name in self.apps_names:
                self.assertLessEqual(len(xy.y[app_name]), batch_size)
                self.assertTrue(np.all(xy.y[app_name].index == xy.x.index))
