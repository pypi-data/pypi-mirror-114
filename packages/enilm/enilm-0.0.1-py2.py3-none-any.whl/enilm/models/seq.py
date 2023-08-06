import tensorflow as tf

shared_conv_params = dict(
    strides=(1, 1),
    padding='same',
)


def _build_seq_model_basis(win_size: int, with_reshape: bool = False) -> tf.keras.Model:
    model = tf.keras.Sequential()

    if with_reshape:
        # add dummy dimension for each sample for the next Conv layer
        model.add(tf.keras.layers.Reshape((1, win_size, 1), input_shape=(win_size,), name='reshape'))
        model.add(tf.keras.layers.Conv2D(30, (10, 1), activation="relu", name='conv1', **shared_conv_params))
    else:
        model.add(tf.keras.layers.Conv2D(30, (10, 1), activation="relu", name='conv1', input_shape=(1, win_size, 1),
                                         **shared_conv_params))

    model.add(tf.keras.layers.Conv2D(30, (8, 1), activation='relu', name='conv2', **shared_conv_params))
    model.add(tf.keras.layers.Conv2D(40, (6, 1), activation='relu', name='conv3', **shared_conv_params))
    model.add(tf.keras.layers.Conv2D(50, (5, 1), activation='relu', name='conv4', **shared_conv_params))
    model.add(tf.keras.layers.Dropout(.2, name='dropout1'))
    model.add(tf.keras.layers.Conv2D(50, (5, 1), activation='relu', name='conv5', **shared_conv_params))
    model.add(tf.keras.layers.Dropout(.2, name='dropout2'))
    model.add(tf.keras.layers.Flatten(name='flatten'))
    model.add(tf.keras.layers.Dense(1024, activation='relu', name='dense1'))
    model.add(tf.keras.layers.Dropout(.2, name='dropout3'))

    return model


def _build_seq_model_basis_conv1d(win_size: int, with_reshape: bool = False) -> tf.keras.Model:
    model = tf.keras.Sequential()

    if with_reshape:
        # add dummy dimension for each sample for the next Conv layer
        model.add(tf.keras.layers.Reshape((win_size, 1), input_shape=(win_size,), name='reshape'))
        model.add(tf.keras.layers.Conv1D(30, 10, activation="relu", strides=1, name='conv1'))
    else:
        model.add(tf.keras.layers.Conv1D(30, 10, activation="relu", input_shape=(win_size, 1), strides=1, name='conv1'))

    model.add(tf.keras.layers.Conv1D(30, 8, activation='relu', strides=1, name='conv2'))
    model.add(tf.keras.layers.Conv1D(40, 6, activation='relu', strides=1, name='conv3'))
    model.add(tf.keras.layers.Conv1D(50, 5, activation='relu', strides=1, name='conv4'))
    model.add(tf.keras.layers.Dropout(.2, name='dropout1'))
    model.add(tf.keras.layers.Conv1D(50, 5, activation='relu', strides=1, name='conv5'))
    model.add(tf.keras.layers.Dropout(.2, name='dropout2'))
    model.add(tf.keras.layers.Flatten(name='flatten'))
    model.add(tf.keras.layers.Dense(1024, activation='relu', name='dense1'))
    model.add(tf.keras.layers.Dropout(.2, name='dropout3'))

    return model


def s2p(win_size: int, with_reshape: bool = True, _compile: bool = True, use_conv1d: bool = False) -> tf.keras.Model:
    if use_conv1d:
        model = _build_seq_model_basis_conv1d(win_size, with_reshape)
    else:
        model = _build_seq_model_basis(win_size, with_reshape)

    model.add(tf.keras.layers.Dense(1, name='dense2'))

    if _compile:
        # Diff to original: added MAE as another metric
        model.compile(loss='mse', optimizer='adam', metrics=['mae'])

    return model


def s2s(win_size: int, with_reshape: bool = True, _compile: bool = True, use_conv1d: bool = False) -> tf.keras.Model:
    if use_conv1d:
        model = _build_seq_model_basis_conv1d(win_size, with_reshape)
    else:
        model = _build_seq_model_basis(win_size, with_reshape)

    model.add(tf.keras.layers.Dense(win_size, name='dense2'))

    if _compile:
        # Diff to original: added MAE as another metric
        model.compile(loss='mse', optimizer='adam', metrics=['mae'])

    return model


