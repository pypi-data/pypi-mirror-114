import time
from typing import Optional

import numpy as np
import tensorflow as tf
from tqdm import trange

import enilm

last_pred_dur: Optional[float] = None


def pred(x: np.ndarray, tflite_model: bytes, n_outputs: int) -> np.ndarray:
    global last_pred_dur

    assert len(x.shape) > 1
    interpreter = tf.lite.Interpreter(model_content=tflite_model)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]

    input_scale, input_zero_point = input_details["quantization"]
    output_scale, output_zero_point = output_details["quantization"]
    need_to_quant_input = input_scale != 0 and input_zero_point != 0
    need_to_quant_output = output_scale != 0 and output_zero_point != 0

    input_type = input_details['dtype']
    output_type = output_details['dtype']

    n_samples = len(x)
    pred = np.zeros((n_samples, n_outputs), dtype=output_type)
    start_time = time.perf_counter()
    for i in trange(n_samples):
        sample: np.ndarray = x[i]
        if need_to_quant_input:
            sample = enilm.lite.quant(sample, input_scale, input_zero_point)
        sample = sample.astype(input_type)
        y: bytes = enilm.esp.http.interface.get_inference_result(bytes(sample))
        y: np.ndarray = np.frombuffer(y, dtype=output_type)
        if need_to_quant_output:
            y: np.ndarray = enilm.lite.dequant(y, output_scale, output_zero_point)
        pred[i] = y
    last_pred_dur = time.perf_counter() - start_time

    return pred
