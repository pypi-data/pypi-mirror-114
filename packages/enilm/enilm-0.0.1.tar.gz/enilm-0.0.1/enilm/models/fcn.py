import tensorflow as tf


def fcn(win_size: int, last_layer_name: str) -> tf.keras.Model:
    print('Warning: Only 7 instead of 9 as in [nilmfcn]) dilated CNN layers')

    shared_conv_params = dict(
        strides=1,
        padding='valid',
    )
    inp = tf.keras.layers.Input(shape=(win_size,), name='inp')
    x = tf.keras.layers.Reshape(target_shape=(win_size, 1), name='reshape')(inp)
    x = tf.keras.layers.Conv1D(128, kernel_size=9, activation="relu", name='conv1', **shared_conv_params)(x)
    n_dilated_conv_layers = 7  # TODO: 9
    rate = 2
    for i in range(n_dilated_conv_layers):
        x = tf.keras.layers.Conv1D(
            128,
            kernel_size=3,
            activation='relu',
            name=f'dconv{i}',
            dilation_rate=rate,
            **shared_conv_params
        )(x)
        rate *= 2
    x = tf.keras.layers.Conv1D(128, kernel_size=1, activation="relu", name='conv2', **shared_conv_params)(x)
    x = tf.keras.layers.Conv1D(
        1,
        kernel_size=1,
        activation="relu",
        name=last_layer_name,
        **shared_conv_params)(x)
    fcn = tf.keras.Model(inputs=inp, outputs=x)
    return fcn
