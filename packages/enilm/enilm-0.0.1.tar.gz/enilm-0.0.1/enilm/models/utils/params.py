from typing import NamedTuple

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

Model = tf.keras.Model


class ParamsCount(NamedTuple):
    count: int
    total: int


def count_params_below(model: Model, threshold: float) -> ParamsCount:
    count = 0
    total = 0
    for layer in model.layers:
        params = layer.get_weights()
        has_params = len(params) > 0
        has_bias = len(params) > 1
        if has_params:
            weights = params[0].flatten()
            total += len(weights)
            count += np.sum(weights < threshold)
            if has_bias:
                bias = params[1].flatten()
                total += len(bias)
                count += np.sum(bias < threshold)

    # Note: total != model.count_params() if model has non-trainable weights

    return ParamsCount(count, total)


def hist(model: Model):
    for layer in model.layers:
        p = layer.get_weights()
        if len(p) == 2:
            print(layer.name)
            all_p = np.concatenate((p[0].flatten(), p[1].flatten()))
            plt.hist(all_p, bins='auto')
            plt.show()


def hist_two_models(m1: Model, m2: Model):
    for l1, l2 in zip(m1.layers, m2.layers):
        p1 = l1.get_weights()
        p2 = l2.get_weights()
        if len(p1) == 2 and len(p2) == 2 and p1[0].shape == p2[0].shape:
            print(l1.name)
            if l1.name != l2.name:
                print(f'Second model has different layer name of {l2.name}')
            plt.hist(np.concatenate((p1[0].flatten(), p1[1].flatten())), bins='auto', alpha=0.5, label=f'm1')
            plt.hist(np.concatenate((p2[0].flatten(), p2[1].flatten())), bins='auto', alpha=0.5, label=f'm2')
            plt.legend()
            plt.show()
