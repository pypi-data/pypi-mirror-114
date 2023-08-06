import tensorflow as tf

from enilm.models.seq import shared_conv_params


def dae(win_size: int):
    # TODO
    # https://github1s.com/nilmtk/nilmtk-contrib/blob/HEAD/nilmtk_contrib/disaggregate/dae.py

    dae = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            filters=8,
            kernel_size=(4, 1),
            activation="linear",
            name='conv1',
            input_shape=(1, win_size, 1),
            **shared_conv_params
        ),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(
            units=win_size * 8,
            activation='relu',
        ),
        tf.keras.layers.Dense(
            units=128,
            activation='relu',
        ),
        tf.keras.layers.Dense(
            units=win_size * 8,
            activation='relu',
        ),
        tf.keras.layers.Reshape((1, win_size, 8)),
        tf.keras.layers.Conv2D(
            filters=1,
            kernel_size=(4, 1),
            activation="linear",
            name='conv2',
            input_shape=(1, win_size, 1),
            **shared_conv_params
        ),
    ])

    dae.compile(loss='mse', optimizer='adam')

    print(dae.input_shape)
    dae.summary()