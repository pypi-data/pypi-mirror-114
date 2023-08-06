from unittest import TestCase

import enilm
import numpy as np


class Test(TestCase):
    def setUp(self) -> None:
        float_size = 4
        enilm.esp.http.set_params(enilm.esp.http.Params(
            win_size=199,
            inbuf_size=199 * float_size,
            n_outputs=3,
            outbuf_size=3 * float_size,
            esp_url='http://192.168.178.158/',
        ))

    def test_set_input_buffer(self):
        x = np.random.random(size=(199,))
        x[3] = 12.34
        x = x.astype(np.float32)
        self.assertTrue(enilm.esp.http.set_input_buffer(x))

    def test_get_inference_result(self):
        res = enilm.esp.http.get_inference_result(as_ndarry=True)
        self.assertIsInstance(res, np.ndarray)
        self.assertTrue(len(res), 3)

    def test_both(self):
        x = np.random.random(size=(199,))
        x[3] = 12.34
        x = x.astype(np.float32)
        res = enilm.esp.http.get_inference_result(x, as_ndarry=True)
        self.assertIsInstance(res, np.ndarray)
        self.assertTrue(len(res), 3)
