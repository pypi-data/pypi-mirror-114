from typing import List

import numpy as np
import tensorflow as tf


def set_model_weights_to_ones(model: tf.keras.Model):
    new_weights: List[np.ndarray] = model.get_weights()
    for i in range(len(new_weights)):
        new_weights[i] = np.ones_like(new_weights[i])
    model.set_weights(new_weights)


def set_model_weights_to_zeros(model: tf.keras.Model):
    new_weights: List[np.ndarray] = model.get_weights()
    for i in range(len(new_weights)):
        new_weights[i] = np.zeros_like(new_weights[i])
    model.set_weights(new_weights)
