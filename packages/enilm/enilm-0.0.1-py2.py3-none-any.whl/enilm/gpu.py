import tensorflow as tf

import enilm


def set_memory_growth():
    """
    Attempts to allocate only as much GPU memory as needed for the runtime allocations:
     it starts out allocating very little memory, and as the program gets run and more GPU memory is needed, we extend
     the GPU memory region allocated to the TensorFlow process.

    https://www.tensorflow.org/guide/gpu#limiting_gpu_memory_growth
    """
    gpus = tf.config.list_physical_devices('GPU')

    if gpus:
        try:
            # Currently, memory growth needs to be the same across GPUs
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as e:
            # Memory growth must be set before GPUs have been initialized
            raise e


def set_memory_limit(limit: int, gpu_id: int = 0, unit: enilm.constants.MemUnit = enilm.constants.MemUnit.GiB):
    """
    Set a hard limit on the total memory to allocate on the GPU

    https://www.tensorflow.org/guide/gpu#limiting_gpu_memory_growth
    """

    limit_mbytes = enilm.convert.size(limit, unit, enilm.constants.MemUnit.MiB)
    gpus = tf.config.list_physical_devices('GPU')

    assert gpu_id < len(gpus)
    if gpus:
        # Restrict TensorFlow to only allocate 1GB of memory on the first GPU
        try:
            tf.config.experimental.set_virtual_device_configuration(
                gpus[0],
                [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=limit_mbytes)])
        except RuntimeError as e:
            # Virtual devices must be set before GPUs have been initialized
            raise e
