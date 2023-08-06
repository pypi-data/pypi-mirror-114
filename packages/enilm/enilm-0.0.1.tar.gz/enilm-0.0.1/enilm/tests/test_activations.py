import datetime
from typing import List
from unittest import TestCase

import enilm
import pandas as pd
import plotly.graph_objects as go


class TestActivations(TestCase):
    def test_get_known_on_power_threshold(self):
        ds = enilm.etypes.Datasets.REDD
        e = enilm.datasets.loaders.load(ds, 1).elec

        # from config.yaml
        should = {
            'sockets': 20,
        }

        for an, thr in should.items():
            ae = enilm.appliances.get_elec(an, e)
            app = enilm.appliances.get_appliance(ae)
            self.assertEqual(enilm.activations.get_known_on_power_threshold(ds, app), thr)

    def test_get_activation_for_series(self):
        ds = enilm.etypes.Datasets.REDD
        l = enilm.datasets.loaders.load(ds, 1)
        e = l.elec
        an = 'fridge'
        ae = enilm.appliances.get_elec(an, e)
        ser: pd.Series = ae.power_series_all_data(sample_period=60, sections=[
            enilm.nilmdt.get_day_timeframe(datetime.date(2011, 4, 28), l.tz)
        ])
        activations: List[pd.Series] = enilm.activations.get_activation_for_series(ser, ae)

        self.assertIsInstance(activations, List)
        self.assertIsInstance(activations[0], pd.Series)
        self.assertEqual(len(activations), 21)
