import enilm
import six
import tensorflow as tf
from tensorflow.python.keras.metrics import MeanMetricWrapper
from tensorflow.python.keras import backend as K
from tensorflow.python.keras.utils.tf_utils import is_tensor_or_variable
from tensorflow.python.keras.metrics import get


class DenormMAE(MeanMetricWrapper):
    @staticmethod
    def denorm_mae(y_true, y_pred, y_mean, y_std):
        y_true = enilm.norm.denormalize(y_true, y_mean, y_std)
        y_pred = enilm.norm.denormalize(y_pred, y_mean, y_std)
        return tf.keras.losses.mean_absolute_error(y_true, y_pred)

    def __init__(self, y_mean: float, y_std: float, name='denorm_mae', dtype=None):
        super(DenormMAE, self).__init__(self.denorm_mae, name, dtype=dtype, y_mean=y_mean, y_std=y_std)

    # def get_config(self):
    #     config = {}
    #
    #     if type(self) is DenormMAE:  # pylint: disable=unidiomatic-typecheck
    #         config['fn'] = self._fn
    #
    #     for k, v in six.iteritems(self._fn_kwargs):
    #         config[k] = K.eval(v) if is_tensor_or_variable(v) else v
    #     base_config = super(MeanMetricWrapper, self).get_config()
    #     return dict(list(base_config.items()) + list(config.items()))
