from typing import List, Iterable, Union, Optional

import tensorflow as tf

import enilm


def s2p_in5(win_size: int) -> tf.keras.Model:
    shared_conv_params = dict(
        strides=(1, 1),
        padding='same',
    )
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Reshape(
        (1, 5, win_size),
        input_shape=(5, win_size),
        name='reshape')
    )
    model.add(tf.keras.layers.Conv2D(30, (10, 1), activation="relu", name='conv1', **shared_conv_params))
    model.add(tf.keras.layers.Conv2D(30, (8, 1), activation='relu', name='conv2', **shared_conv_params))
    model.add(tf.keras.layers.Conv2D(40, (6, 1), activation='relu', name='conv3', **shared_conv_params))
    model.add(tf.keras.layers.Conv2D(50, (5, 1), activation='relu', name='conv4', **shared_conv_params))
    model.add(tf.keras.layers.Dropout(.2, name='dropout1'))
    model.add(tf.keras.layers.Conv2D(50, (5, 1), activation='relu', name='conv5', **shared_conv_params))
    model.add(tf.keras.layers.Dropout(.2, name='dropout2'))
    model.add(tf.keras.layers.Flatten(name='flatten'))
    model.add(tf.keras.layers.Dense(1024, activation='relu', name='dense1'))
    model.add(tf.keras.layers.Dropout(.2, name='dropout3'))
    model.add(tf.keras.layers.Dense(1, name='dense2'))

    model.compile(loss='mse', optimizer='adam', metrics=['mae'])
    return model


def s2p_seq(win_size: int, _compile: bool = True, output_layer_name: Optional[str] = None) -> tf.keras.Model:
    shared_conv_params = dict(
        strides=(1, 1),
        padding='same',
    )
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Reshape(
        (1, 1, win_size),
        input_shape=(win_size,),
        name='reshape')
    )
    model.add(tf.keras.layers.Conv2D(30, (10, 1), activation="relu", name='conv1', **shared_conv_params))
    model.add(tf.keras.layers.Conv2D(30, (8, 1), activation='relu', name='conv2', **shared_conv_params))
    model.add(tf.keras.layers.Conv2D(40, (6, 1), activation='relu', name='conv3', **shared_conv_params))
    model.add(tf.keras.layers.Conv2D(50, (5, 1), activation='relu', name='conv4', **shared_conv_params))
    model.add(tf.keras.layers.Dropout(.2, name='dropout1'))
    model.add(tf.keras.layers.Conv2D(50, (5, 1), activation='relu', name='conv5', **shared_conv_params))
    model.add(tf.keras.layers.Dropout(.2, name='dropout2'))
    model.add(tf.keras.layers.Flatten(name='flatten'))
    model.add(tf.keras.layers.Dense(1024, activation='relu', name='dense1'))
    model.add(tf.keras.layers.Dropout(.2, name='dropout3'))

    if output_layer_name is not None:
        model.add(tf.keras.layers.Dense(1, name=output_layer_name))
    else:
        model.add(tf.keras.layers.Dense(1, name='dense2'))

    if _compile:
        model.compile(loss='mse', optimizer='adam', metrics=['mae'])

    return model


def s2p_ks1(win_size: int) -> tf.keras.Model:
    shared_conv_params = dict(
        strides=(1, 1),
        padding='same',  # ATTENTION: this is not totally "sinnvoll"
    )
    model = tf.keras.Sequential()

    model.add(tf.keras.layers.Reshape((1, 1, win_size), input_shape=(win_size,), name='reshape'))
    model.add(tf.keras.layers.Conv2D(30, (1, 1), activation="relu", name='conv1', **shared_conv_params))
    model.add(tf.keras.layers.Conv2D(30, (8, 1), activation='relu', name='conv2', **shared_conv_params))
    model.add(tf.keras.layers.Conv2D(40, (6, 1), activation='relu', name='conv3', **shared_conv_params))
    model.add(tf.keras.layers.Conv2D(50, (5, 1), activation='relu', name='conv4', **shared_conv_params))
    model.add(tf.keras.layers.Dropout(.2, name='dropout1'))
    model.add(tf.keras.layers.Conv2D(50, (5, 1), activation='relu', name='conv5', **shared_conv_params))
    model.add(tf.keras.layers.Dropout(.2, name='dropout2'))
    model.add(tf.keras.layers.Flatten(name='flatten'))
    model.add(tf.keras.layers.Dense(1024, activation='relu', name='dense1'))
    model.add(tf.keras.layers.Dropout(.2, name='dropout3'))
    model.add(tf.keras.layers.Dense(1, name='dense2'))

    model.compile(loss='mse', optimizer='adam', metrics=['mae'])
    return model


def s2p_sing_ker(win_size: int,
                 _compile: bool = True,
                 output_layer_name: Optional[str] = None,
                 with_reshape: bool = True) -> tf.keras.Model:
    shared_conv_params = dict(
        strides=(1, 1),
        padding='valid',  # Should not make any difference, even if it was 'same'
        kernel_size=(1, 1),  # NEW
    )
    model = tf.keras.Sequential()

    if with_reshape:
        model.add(tf.keras.layers.Reshape((1, 1, win_size), input_shape=(win_size,), name='reshape'))
    else:
        model.add(tf.keras.layers.Input(shape=(1, 1, win_size)))
    model.add(tf.keras.layers.Conv2D(30, activation="relu", name='conv1', **shared_conv_params))
    model.add(tf.keras.layers.Conv2D(30, activation='relu', name='conv2', **shared_conv_params))
    model.add(tf.keras.layers.Conv2D(40, activation='relu', name='conv3', **shared_conv_params))
    model.add(tf.keras.layers.Conv2D(50, activation='relu', name='conv4', **shared_conv_params))
    model.add(tf.keras.layers.Dropout(.2, name='dropout1'))
    model.add(tf.keras.layers.Conv2D(50, activation='relu', name='conv5', **shared_conv_params))
    model.add(tf.keras.layers.Dropout(.2, name='dropout2'))
    model.add(tf.keras.layers.Flatten(name='flatten'))
    model.add(tf.keras.layers.Dense(1024, activation='relu', name='dense1'))
    model.add(tf.keras.layers.Dropout(.2, name='dropout3'))

    if output_layer_name is not None:
        model.add(tf.keras.layers.Dense(1, name=output_layer_name))
    else:
        model.add(tf.keras.layers.Dense(1, name='dense2'))

    if _compile:
        model.compile(loss='mse', optimizer='adam', metrics=['mae'])

    return model


def s2p_dconv(win_size: int) -> tf.keras.Model:
    shared_conv_params = dict(
        strides=(1, 1),
        padding='same',
    )

    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Reshape(
        target_shape=(1, win_size, 1),
        input_shape=(win_size,),
        name='reshape'
    ))

    # model.add(tf.keras.layers.Conv2D(30, (10, 1), activation="relu", name='conv1', **shared_conv_params))
    model.add(tf.keras.layers.DepthwiseConv2D(
        kernel_size=10,
        activation="relu",
        name='dconv1',
        depth_multiplier=1,
        **shared_conv_params
    ))

    # model.add(tf.keras.layers.Conv2D(30, (8, 1), activation='relu', name='conv2', **shared_conv_params))
    model.add(tf.keras.layers.DepthwiseConv2D(
        kernel_size=8,
        activation="relu",
        name='dconv2',
        depth_multiplier=1,
        **shared_conv_params
    ))

    # model.add(tf.keras.layers.Conv2D(40, (6, 1), activation='relu', name='conv3', **shared_conv_params))
    model.add(tf.keras.layers.DepthwiseConv2D(
        kernel_size=6,
        activation="relu",
        name='dconv3',
        depth_multiplier=1,
        **shared_conv_params
    ))

    # model.add(tf.keras.layers.Conv2D(50, (5, 1), activation='relu', name='conv4', **shared_conv_params))
    model.add(tf.keras.layers.DepthwiseConv2D(
        kernel_size=5,
        activation="relu",
        name='dconv4',
        depth_multiplier=1,
        **shared_conv_params
    ))

    model.add(tf.keras.layers.Dropout(
        rate=.2,
        name='dropout1'
    ))

    # model.add(tf.keras.layers.Conv2D(50, (5, 1), activation='relu', name='conv5', **shared_conv_params))
    model.add(tf.keras.layers.DepthwiseConv2D(
        kernel_size=5,
        activation="relu",
        name='dconv5',
        depth_multiplier=1,
        **shared_conv_params
    ))

    model.add(tf.keras.layers.Dropout(
        rate=.2,
        name='dropout2'
    ))

    model.add(tf.keras.layers.Flatten(
        name='flatten'
    ))

    model.add(tf.keras.layers.Dense(
        units=1024,
        activation='relu',
        name='dense1'
    ))

    model.add(tf.keras.layers.Dropout(
        rate=.2,
        name='dropout3'
    ))

    model.add(tf.keras.layers.Dense(
        units=1,
        name='dense2'
    ))

    model.compile(loss='mse', optimizer='adam', metrics=['mae'])
    return model


def s2p_seq_mtl(win_size: int, apps_names: List[str], _compile: bool) -> tf.keras.Model:
    shared_conv_params = dict(
        strides=(1, 1),
        padding='same',
    )

    inp = tf.keras.layers.Input(
        shape=(win_size,),
        name='inp',
    )

    reshape = tf.keras.layers.Reshape(
        target_shape=(1, 1, win_size),
        name='reshape'
    )(inp)

    conv1 = tf.keras.layers.Conv2D(30, (10, 1), activation="relu", name='conv1', **shared_conv_params)(reshape)
    conv2 = tf.keras.layers.Conv2D(30, (8, 1), activation='relu', name='conv2', **shared_conv_params)(conv1)
    conv3 = tf.keras.layers.Conv2D(40, (6, 1), activation='relu', name='conv3', **shared_conv_params)(conv2)
    conv4 = tf.keras.layers.Conv2D(50, (5, 1), activation='relu', name='conv4', **shared_conv_params)(conv3)
    dropout1 = tf.keras.layers.Dropout(.2, name='dropout1')(conv4)
    conv5 = tf.keras.layers.Conv2D(50, (5, 1), activation='relu', name='conv5', **shared_conv_params)(dropout1)
    dropout2 = tf.keras.layers.Dropout(.2, name='dropout2')(conv5)
    flatten = tf.keras.layers.Flatten(name='flatten')(dropout2)
    dense1 = tf.keras.layers.Dense(1024, activation='relu', name='dense1')(flatten)
    dropout3 = tf.keras.layers.Dropout(.2, name='dropout3')(dense1)

    outputs = []
    for app_name in apps_names:
        outputs.append(
            tf.keras.layers.Dense(1, name=f"{app_name.replace(' ', '_')}")(dropout3)
        )

    model = tf.keras.Model(
        inputs=inp,
        outputs=outputs
    )

    if _compile: raise NotImplementedError

    return model


def s2p_sing_ker_mtl(win_size: int,
                     apps_names: Iterable[Union[enilm.appliances.Appliance, enilm.etypes.AppName]],
                     _compile: bool) -> tf.keras.Model:
    apps_names = enilm.appliances.to_str(apps_names)

    shared_conv_params = dict(
        strides=(1, 1),
        padding='valid',
        kernel_size=(1, 1),
    )

    inp = tf.keras.layers.Input(
        shape=(win_size,),
        name='inp',
    )

    reshape = tf.keras.layers.Reshape(
        target_shape=(1, 1, win_size),
        name='reshape'
    )(inp)

    conv1 = tf.keras.layers.Conv2D(30, activation="relu", name='conv1', **shared_conv_params)(reshape)
    conv2 = tf.keras.layers.Conv2D(30, activation='relu', name='conv2', **shared_conv_params)(conv1)
    conv3 = tf.keras.layers.Conv2D(40, activation='relu', name='conv3', **shared_conv_params)(conv2)
    conv4 = tf.keras.layers.Conv2D(50, activation='relu', name='conv4', **shared_conv_params)(conv3)
    dropout1 = tf.keras.layers.Dropout(.2, name='dropout1')(conv4)
    conv5 = tf.keras.layers.Conv2D(50, activation='relu', name='conv5', **shared_conv_params)(dropout1)
    dropout2 = tf.keras.layers.Dropout(.2, name='dropout2')(conv5)
    flatten = tf.keras.layers.Flatten(name='flatten')(dropout2)
    dense1 = tf.keras.layers.Dense(1024, activation='relu', name='dense1')(flatten)
    dropout3 = tf.keras.layers.Dropout(.2, name='dropout3')(dense1)

    outputs = {}
    for app_name in apps_names:
        _app_name = app_name.replace(' ', '_')
        outputs[_app_name] = tf.keras.layers.Dense(1, name=f"{_app_name}")(dropout3)

    model = tf.keras.Model(
        inputs=inp,
        outputs=outputs
    )

    if _compile: raise NotImplementedError

    return model
