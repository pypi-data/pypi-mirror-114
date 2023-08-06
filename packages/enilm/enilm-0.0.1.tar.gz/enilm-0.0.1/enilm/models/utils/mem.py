from typing import Union, Dict

import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K

from enilm.constants import MemUnit
from enilm import convert


def get_memory_usage(batch_size: int, model: tf.keras.Model, to: MemUnit = MemUnit.GiB, pro_layer=False) \
        -> Union[np.float, Dict]:
    """
    ref: https://stackoverflow.com/a/46216013/1617883
    returned dict:
        key = total, value = mem usage in given unit (`to`)
        key = layer name, value = mem usage
    """
    res = {}

    number_size = 4.0  # size of float32 in bytes
    if K.floatx() == 'float16':
        number_size = 2.0
    if K.floatx() == 'float64':
        number_size = 8.0

    shapes_mem_count = 0
    internal_model_mem_count = 0
    for l in model.layers:
        layer_type = l.__class__.__name__
        if layer_type == 'Model':
            internal_model_mem_count += get_memory_usage(batch_size, l)
        single_layer_mem = 1
        out_shape = l.output_shape
        if type(out_shape) is list:
            out_shape = out_shape[0]
        for s in out_shape:
            if s is None:
                continue
            single_layer_mem *= s
        if pro_layer:
            layer_mem_bytes = number_size * batch_size * single_layer_mem
            res[l.name] = convert.size(layer_mem_bytes, MemUnit.B, to)

        shapes_mem_count += single_layer_mem

    trainable_count = np.sum([K.count_params(p) for p in model.trainable_weights])
    non_trainable_count = np.sum([K.count_params(p) for p in model.non_trainable_weights])

    total_memory = number_size * (batch_size * shapes_mem_count + trainable_count + non_trainable_count)
    res['total'] = convert.size(total_memory, MemUnit.B, to) + internal_model_mem_count
    if not pro_layer: return res['total']
    return res


if __name__ == '__main__':
    from enilm.models import s2p

    model = s2p(599)
    print(get_memory_usage(1024, model, pro_layer=True, to=MemUnit.GiB))
