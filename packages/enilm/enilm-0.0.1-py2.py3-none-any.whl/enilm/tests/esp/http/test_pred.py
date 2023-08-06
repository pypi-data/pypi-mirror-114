from pathlib import Path
from unittest import TestCase

import enilm
import numpy as np


class Test(TestCase):
    def setUp(self) -> None:
        self.win_size = 499
        self.n_outputs = 1

        enilm.esp.http.interface.set_params(enilm.esp.http.interface.Params(
            esp_url='http://192.168.178.158/',
        ))

    def test_pred_full_int_quant(self):
        x = np.random.random((10, self.win_size))
        tflite_model = Path('./models/stl_full_int_quant.tflite').read_bytes()
        esp_pred = enilm.esp.http.pred.pred(x, tflite_model, self.n_outputs)
        self.assertTrue(len(esp_pred == x.shape[0]))

    def test_pred_default_quant(self):
        x = np.random.random((10, self.win_size))
        tflite_model = Path('./models/stl_default_quant.tflie').read_bytes()
        esp_pred = enilm.esp.http.pred.pred(x, tflite_model, self.n_outputs)
        self.assertTrue(len(esp_pred == x.shape[0]))
