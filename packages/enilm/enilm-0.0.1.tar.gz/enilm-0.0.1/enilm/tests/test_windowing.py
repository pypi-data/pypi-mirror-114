from unittest import TestCase

import enilm
import numpy as np


class Test(TestCase):
    def test_chunkize(self):
        res = list(enilm.windowing.chunkize(np.arange(7), chunk_size=3))

        self.assertEqual(len(res), 3)
        self.assertTrue(np.all(res[0] == np.array([0, 1, 2])))
        self.assertTrue(np.all(res[1] == np.array([3, 4, 5])))
        self.assertTrue(np.all(res[2] == np.array([6])))
