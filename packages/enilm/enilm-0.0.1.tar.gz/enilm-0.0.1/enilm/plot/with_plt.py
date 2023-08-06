import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


def visualize_weights(model: tf.keras.Model):
    for layer in model.layers:
        if isinstance(layer, tf.keras.layers.Conv2D):
            name = layer.name
            w, b = layer.get_weights()
            w = w.squeeze()
            print(name)
            print(w.shape)

            if len(w.shape) == 3:
                print('averaging over third axis')
                w = np.average(w, axis=2)

            if len(w.shape) == 2:
                heatmap = plt.pcolor(w)
                plt.colorbar(heatmap)
                plt.imshow(w)
                plt.show()
