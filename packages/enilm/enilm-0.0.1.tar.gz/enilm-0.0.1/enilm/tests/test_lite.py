from unittest import TestCase

import numpy as np
import tensorflow as tf

import enilm


def create_representative_data_gen(win_size, dtype=np.float32, n_samples=1000):
    def representative_data_gen():
        data = np.random.random((n_samples, 1, 1, win_size))
        if data.dtype != dtype:
            data = data.astype(dtype)
        for input_value in tf.data.Dataset.from_tensor_slices(data).batch(1).take(100):
            yield [input_value]

    return representative_data_gen


class Test(TestCase):
    def test_pred_full_int_quant(self):
        # int8 in out
        win_size = 499

        model = enilm.models.test.s2p_sing_ker(win_size, with_reshape=False)
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.representative_dataset = create_representative_data_gen(win_size)
        converter.target_spec.supported_ops = [
            tf.lite.OpsSet.TFLITE_BUILTINS_INT8,
        ]
        converter.inference_input_type = tf.int8
        converter.inference_output_type = tf.int8
        tflite_model = converter.convert()
        pred = enilm.lite.pred(
            tflite_model,
            x_input=np.random.random((1000, 1, 1, win_size)),
        )
        self.assertTrue(sum(pred) != 0)
        self.assertIsInstance(pred, np.ndarray)
        self.assertTrue(pred.shape, (1000, 1))

    def test_pred_default_quant(self):
        # float32 in out
        win_size = 499

        model = enilm.models.test.s2p_sing_ker(win_size, with_reshape=False)
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.representative_dataset = create_representative_data_gen(win_size)
        tflite_model = converter.convert()
        pred = enilm.lite.pred(
            tflite_model,
            x_input=np.random.random((1000, 1, 1, win_size)),
        )
        self.assertTrue(sum(pred) != 0)
        self.assertIsInstance(pred, np.ndarray)
        self.assertTrue(pred.shape, (1000, 1))
