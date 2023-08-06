import tempfile
import os
import zipfile
import bz2

import tensorflow as tf


def get_gzipped_model_size(model: tf.keras.Model) -> int:
    # Returns size of gzipped model, in bytes.
    _, keras_file = tempfile.mkstemp('.h5')
    model.save(keras_file, include_optimizer=False)

    _, zipped_file = tempfile.mkstemp('.zip')
    with zipfile.ZipFile(zipped_file, 'w', compression=zipfile.ZIP_DEFLATED) as f:
        f.write(keras_file)

    return os.path.getsize(zipped_file)


def get_lite_gzipped_model_size(model_bytes: bytes) -> int:
    # Returns size of gzipped model, in bytes.
    _, tflite_file = tempfile.mkstemp('.tflite')
    with open(tflite_file, 'wb') as f:
        f.write(model_bytes)

    _, zipped_file = tempfile.mkstemp('.zip')
    with zipfile.ZipFile(zipped_file, 'w', compression=zipfile.ZIP_DEFLATED) as f:
        f.write(tflite_file)

    return os.path.getsize(zipped_file)


def get_bz2_model_size(model: tf.keras.Model, compresslevel: int = 9) -> int:
    """
    :param model:
    :param compresslevel: can be changed (must be an integer between 1 and 9. The default is 9)
    :return: size of zipped model, in bytes.
    """

    _, keras_file = tempfile.mkstemp('.h5')
    model.save(keras_file, include_optimizer=False)

    with open(keras_file, 'rb') as f:
        tarbz2contents = bz2.compress(f.read(), compresslevel=compresslevel)

    return len(tarbz2contents)


def get_lite_bz2_model_size(model_bytes: bytes, compresslevel: int = 9) -> int:
    return len(bz2.compress(model_bytes, compresslevel=compresslevel))
