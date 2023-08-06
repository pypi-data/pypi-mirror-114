import time
from typing import Optional, Union

import tensorflow as tf
import numpy as np

last_duration: Optional[float] = None


# https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/micro/examples/hello_world/main_functions.cc#L96
def quant(val: Union[float, np.ndarray], scale: float, zero_point: int) -> Union[float, np.ndarray]:
    # TODO: vectorize
    if scale != 0:
        return val / scale + zero_point
    else:
        return val + zero_point


# https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/micro/examples/hello_world/main_functions.cc#L111
def dequant(val: Union[float, np.ndarray], scale: float, zero_point: int) -> Union[float, np.ndarray]:
    # TODO: vectorize
    return (val - zero_point) * scale


def pred(lmodel: bytes, x_input: np.ndarray, debug: bool = True, scale: bool = True) -> np.ndarray:
    global last_duration
    interpreter = tf.lite.Interpreter(model_content=lmodel)
    interpreter.allocate_tensors()

    # For now only 1-in 1-out models
    assert len(interpreter.get_input_details()) == 1
    assert len(interpreter.get_output_details()) == 1

    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]

    input_scale, input_zero_point = input_details["quantization"]
    output_scale, output_zero_point = output_details["quantization"]
    need_to_quant_input = input_scale != 0 and input_zero_point != 0
    need_to_quant_output = output_scale != 0 and output_zero_point != 0
    if debug:
        print("Input quantization")
        print(f"\tscale: {input_scale}")
        print(f"\tzero point: {input_zero_point}")
        if not need_to_quant_input:
            print("\tno quantization")
        print("Output quantization")
        print(f"\tscale: {output_scale}")
        print(f"\tzero point: {output_zero_point}")
        if not need_to_quant_output:
            print("\tno quantization")

    input_tensor_index = input_details['index']
    output_tensor_index = output_details['index']
    if debug:
        print(f'Index: {input_tensor_index} --> {output_tensor_index}')

    input_type = input_details['dtype']
    output_type = output_details['dtype']
    if debug:
        print(f'Type: {input_type} --> {output_type}')

    input_signature = input_details['shape_signature']
    output_signature = output_details['shape_signature']
    if debug:
        print(f'Signature: {input_signature} -> {output_signature}')

    n_samples = x_input.shape[0]
    input_shape = (n_samples, *input_signature[1:])
    output_shape = (n_samples, *output_signature[1:])
    if debug:
        print(f'Shape: {input_shape} -> {output_shape}')
    assert x_input.shape == input_shape

    y_pred = np.empty(shape=output_shape, dtype=output_type)
    start_time = time.time()
    for i in range(n_samples):
        curr_input = x_input[i]
        if scale and need_to_quant_input:
            # Check if the input type is quantized, then rescale input data
            input_scale, input_zero_point = input_details["quantization"]
            curr_input = quant(curr_input, input_scale, input_zero_point)

        # convert to expected type
        if curr_input.dtype != input_type:
            curr_input = curr_input.astype(input_type)

        # run inference
        interpreter.set_tensor(input_tensor_index, [curr_input])
        interpreter.invoke()

        # get output
        y_pred[i] = interpreter.get_tensor(output_tensor_index)[0]

    last_duration = time.time() - start_time

    # quantize output
    if scale and need_to_quant_output:
        res = np.zeros(shape=output_shape)
        for i in range(len(y_pred)):
            res[i] = dequant(y_pred[i], output_scale, output_zero_point)
        return res

    return y_pred

# TODO: compute error
#     loss_function = tf.keras.losses.mean_squared_error
#     return (
#         np.mean(loss_function(y_test, y_pred.astype(np.float32)).numpy()),
#         time.time() - start
#     )
