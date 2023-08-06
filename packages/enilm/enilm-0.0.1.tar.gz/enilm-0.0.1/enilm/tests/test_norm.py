from unittest import TestCase
import numpy as np

from enilm.norm import normalize, denormalize, get_params
import enilm


class Test(TestCase):
    def test_normalize_denormalize_same_results(self):
        x = np.arange(100)
        mean = 4
        std = 53
        self.assertTrue(all(denormalize(normalize(x, mean, std), mean, std) == x))

    def test_get_norm_params_ukdale_fridge(self):
        mean, std = get_params(enilm.etypes.Datasets.UKDALE, 'fridge freezer')
        self.assertEqual(mean, 200)
        self.assertEqual(std, 400)
