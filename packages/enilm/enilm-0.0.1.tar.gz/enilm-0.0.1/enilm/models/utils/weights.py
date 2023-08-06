from typing import Optional

import numpy as np
import pandas as pd
import tensorflow as tf

Model = tf.keras.Model


def per_layer_stats(model: Model) -> pd.DataFrame:
    data = []
    for layer in model.layers:
        weights = layer.get_weights()
        if len(weights) == 0:
            continue
        all_w = []
        for w in weights:
            all_w.extend(list(w.flatten()))
        data.append({
            'layer': layer.name,
            'min': min(all_w),
            'max': max(all_w),
            'mean': np.mean(all_w),
            'std': np.std(all_w),
        })

    return pd.DataFrame(data)


# def per_layer_stats(model: tf.keras.Model):
#     for layer in model.layers:
#         if len(layer.get_weights()) >= 1:
#             w = layer.get_weights()[0].flatten()
#             print(f'{layer.name:<6}: {np.mean(w):+.4f} ± {np.std(w):.4f}')


def per_layer_sparsity(model: tf.keras.Model, threshold: float):
    for layer in model.layers:
        if len(layer.get_weights()) >= 1:
            w = layer.get_weights()[0].flatten()
            print(f'{layer.name:<6}: {np.sum(np.abs(w < threshold)) / len(w) * 100:.2f}%')


def density(model: Model, filter_empty_layers: bool = True,
            density_format: Optional[str] = '{0:.2f}%') -> pd.DataFrame:
    data = []
    total_n_params = 0
    for layer in model.layers:
        # n_params = np.sum(([np.prod(w.shape) for w in layer.get_weights()]), dtype=np.int64)
        n_params = layer.count_params()
        if filter_empty_layers and n_params == 0:
            continue
        total_n_params += n_params
        data.append({
            'layer': layer.name,
            'n_params': n_params
        })

    # add percentages
    for data_point in data:
        weights_rate = (data_point['n_params'] * 100) / total_n_params
        if density_format is not None:
            data_point['percentage'] = density_format.format(weights_rate)
        else:
            data_point['percentage'] = weights_rate

    return pd.DataFrame(data)
