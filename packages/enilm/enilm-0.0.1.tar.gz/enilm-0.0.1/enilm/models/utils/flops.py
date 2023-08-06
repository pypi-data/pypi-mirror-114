# TODO implement for tflite

from typing import Callable

import tensorflow as tf


def get_flops(model_gen_fn: Callable[..., tf.keras.Model], **kwargs):
    """
    ref https://stackoverflow.com/a/61060485/1617883
    :param model_gen_fn:
    :param kwargs:
    :return:
    """

    session = tf.compat.v1.Session()
    graph = tf.compat.v1.get_default_graph()

    with graph.as_default():
        with session.as_default():
            model = model_gen_fn(**kwargs)
            # model = keras.applications.mobilenet.MobileNet(
            #         alpha=1, weights=None, input_tensor=tf.compat.v1.placeholder('float32', shape=(1, 224, 224, 3)))

            run_meta = tf.compat.v1.RunMetadata()
            opts = tf.compat.v1.profiler.ProfileOptionBuilder.float_operation()

            # Optional: save printed results to file
            # flops_log_path = os.path.join(tempfile.gettempdir(), 'tf_flops_log.txt')
            # opts['output'] = 'file:outfile={}'.format(flops_log_path)
            # print(flops_log_path)

            # We use the Keras session graph in the call to the profiler.
            flops = tf.compat.v1.profiler.profile(graph=graph,
                                                  run_meta=run_meta, cmd='op', options=opts)

    tf.compat.v1.reset_default_graph()
    return flops.total_float_ops


if __name__ == '__main__':
    from enilm.common.tf.models import s2p

    print(get_flops(s2p, win_size=199))
    print(get_flops(s2p, win_size=599))
