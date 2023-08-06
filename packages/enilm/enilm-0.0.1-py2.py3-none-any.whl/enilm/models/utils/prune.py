from typing import Dict, List, Set

import numpy as np
import tensorflow as tf

import enilm as eml


def _is_conv_layer(layer: tf.keras.layers.Layer) -> bool:
    if isinstance(layer, tf.keras.layers.Conv1D):
        return True
    if isinstance(layer, tf.keras.layers.Conv2D):
        return True
    return False


def set_weights(layer: tf.keras.layers.Layer, dim: int, value: float):
    """
    set params of last dimension in layer to value
    """
    params = layer.get_weights()

    # weights
    weights = params[0]
    weights[..., dim] = value

    # biases
    if len(params) == 2:
        biases = params[1]
        biases[dim] = value

    layer.set_weights(params)


def to_prune(layer: tf.keras.layers.Layer, threshold: float) -> Set[int]:
    """
    if params of filter are < threshold => must be pruned
    """
    result = set()
    params = layer.get_weights()
    for id in range(params[0].shape[-1]):
        # check weights
        weights = params[0]
        if np.all(np.abs(weights[..., id]) < threshold):
            # check bias
            if len(params) == 1:  # no bias
                result.add(id)
            else:  # at least with bias
                if np.abs(params[1][id]) < threshold:
                    result.add(id)

    return result


# def prune_conv(model: tf.keras.Model, threshold: float) -> tf.keras.Model:
#     # create config
#     config = model.get_config().copy()
#     filters_to_keep = {}
#     for layer_config in config['layers']:
#         if layer_config['class_name'] in ['Conv1D', 'Conv2D']:
#             layer_name = layer_config['name']
#             layer = model.get_layer(layer_name)
#             filters_to_keep[layer_name] = list(
#                 set(range(layer.filters)) - to_prune(layer, threshold)
#             )
#             layer_config['config']['filters'] = len(filters_to_keep[layer_name])
#
#     # create new model
#     pruned_model = tf.keras.Sequential.from_config(config)
#
#     # copy params
#     prev_conv_layer_name = None
#     for layer in pruned_model.layers:
#         if _is_conv_layer(layer):
#             original_params = model.get_layer(layer.name).get_weights()
#
#             # copy weights
#             if prev_conv_layer_name is not None:
#                 new_weights = original_params[0][..., filters_to_keep[prev_conv_layer_name], :]
#                 new_weights = new_weights[..., filters_to_keep[layer.name]]
#             else:
#                 new_weights = original_params[0][..., filters_to_keep[layer.name]]
#
#             # copy bias
#             if len(original_params) > 1:
#                 new_bias = original_params[1][filters_to_keep[layer.name]]
#                 layer.set_weights([new_weights, new_bias])
#             else:
#                 layer.set_weights([new_weights])
#
#             prev_conv_layer_name = layer.name
#         else:
#             layer.set_weights(model.get_layer(layer.name).get_weights())
#
#     return pruned_model
#
#
# def prune_dense(model: tf.keras.Model, threshold: float) -> tf.keras.Model:
#     # create config
#     config = model.get_config().copy()
#     units_to_keep = {}
#     for layer_config in config['layers']:
#         if layer_config['class_name'] == 'Dense':
#             layer_name = layer_config['name']
#             layer = model.get_layer(layer_name)
#             units_to_keep[layer_name] = list(
#                 set(range(layer.units)) - to_prune(layer, threshold)
#             )
#             layer_config['config']['units'] = len(units_to_keep[layer_name])
#
#     # create new model
#     pruned_model = tf.keras.Sequential.from_config(config)
#
#     # copy params
#     prev_dense_layer_name = None
#     for layer in pruned_model.layers:
#         if isinstance(layer, tf.keras.layers.Dense):
#             original_params = model.get_layer(layer.name).get_weights()
#
#             # copy weights
#             if prev_dense_layer_name is not None:
#                 new_weights = original_params[0][..., units_to_keep[prev_dense_layer_name], :]
#                 new_weights = new_weights[..., units_to_keep[layer.name]]
#             else:
#                 new_weights = original_params[0][..., units_to_keep[layer.name]]
#
#             # copy bias
#             if len(original_params) > 1:
#                 new_bias = original_params[1][units_to_keep[layer.name]]
#                 layer.set_weights([new_weights, new_bias])
#             else:
#                 layer.set_weights([new_weights])
#
#             prev_dense_layer_name = layer.name
#         else:
#             layer.set_weights(model.get_layer(layer.name).get_weights())
#
#     return pruned_model


def prune(model: tf.keras.Model, threshold: float) -> tf.keras.Model:
    # create config
    config = model.get_config().copy()
    units_to_keep = {}
    for layer_config in config['layers']:
        if layer_config['class_name'] == 'Dense':
            layer_name = layer_config['config']['name']
            layer = model.get_layer(layer_name)
            units_to_keep[layer_name] = list(
                set(range(layer.units)) - to_prune(layer, threshold)
            )
            layer_config['config']['units'] = len(units_to_keep[layer_name])
        elif layer_config['class_name'] in ['Conv1D', 'Conv2D']:
            layer_name = layer_config['config']['name']
            layer = model.get_layer(layer_name)
            units_to_keep[layer_name] = list(
                set(range(layer.filters)) - to_prune(layer, threshold)
            )
            layer_config['config']['filters'] = len(units_to_keep[layer_name])

    # create new model
    pruned_model = tf.keras.Sequential.from_config(config)

    # copy params
    prev_layer_name = None
    prev_layer_type = None
    for layer in pruned_model.layers:
        if isinstance(layer, tf.keras.layers.Dense) or _is_conv_layer(layer):
            original_params = model.get_layer(layer.name).get_weights()

            # copy weights
            if prev_layer_type in [
                tf.keras.layers.Conv1D,
                tf.keras.layers.Conv2D
            ] and isinstance(layer, tf.keras.layers.Dense):
                # conv -> flat -> dense
                # https://colab.research.google.com/drive/1jQwyTV7mRdfdWYN4X8n65rG9uI7t7V51?usp=sharing
                old_weights = original_params[0]

                r_mask = np.array(units_to_keep[prev_layer_name])
                c_mask = np.array(units_to_keep[layer.name])

                old_n = model.get_layer(prev_layer_name).filters
                # new_n = pruned_model.get_layer(prev_layer_name).filters

                old_n_filters = int(old_weights.shape[0] / old_n)
                full_r_mask = np.array([r_mask + (i * old_n) for i in range(old_n_filters)]).flatten()

                new_weights = old_weights[full_r_mask]  # rows
                new_weights = new_weights[:, c_mask]  # cols
            elif prev_layer_name is not None and prev_layer_type == type(layer):
                # conv -> conv OR dense -> dense
                new_weights = original_params[0][..., units_to_keep[prev_layer_name], :]
                new_weights = new_weights[..., units_to_keep[layer.name]]
            else:
                new_weights = original_params[0][..., units_to_keep[layer.name]]

            # copy bias
            if len(original_params) > 1:
                new_bias = original_params[1][units_to_keep[layer.name]]
                layer.set_weights([new_weights, new_bias])
            else:
                layer.set_weights([new_weights])

            # for next layer
            prev_layer_name = layer.name
            prev_layer_type = type(layer)
        else:
            layer.set_weights(model.get_layer(layer.name).get_weights())

    return pruned_model
