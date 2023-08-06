import tensorflow as tf

from enilm.models.seq import shared_conv_params


def rnn(win_size: int):
    # https://github1s.com/nilmtk/nilmtk-contrib/blob/HEAD/nilmtk_contrib/disaggregate/rnn.py
    # Suggestion: RNN with another input for time

    model = tf.keras.models.Sequential([
        tf.keras.layers.Reshape(
            (1, win_size, 1),
            input_shape=(win_size,),
            name='reshape'
        ),
        tf.keras.layers.Conv2D(
            filters=16,
            kernel_size=(4, 1),
            activation="linear",
            name='conv',
            **shared_conv_params
        ),
        tf.keras.layers.Reshape(
            (win_size, 16),
        ),
        tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(128, return_sequences=True, stateful=False),
            merge_mode='concat'
        ),
        tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(256, return_sequences=False, stateful=False),
            merge_mode='concat'
        ),
        tf.keras.layers.Dense(
            units=128,
            activation='tanh',
        ),
        tf.keras.layers.Dense(
            units=1,
            activation='linear',
        ),
    ])

    model.compile(loss='mse', optimizer='adam', metrics=['mse'])

    return model