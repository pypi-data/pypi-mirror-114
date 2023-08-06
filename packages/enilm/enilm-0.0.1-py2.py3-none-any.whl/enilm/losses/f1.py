import numpy as np
from sklearn.metrics import f1_score

from enilm.losses import LossFunc


def f1score_func_with_power_threshold(on_power_threshold: float) -> LossFunc:
    """
    Create F1 loss function with specified power threshold

    Parameters
    ----------
    on_power_threshold the on power threshold

    Returns
    -------
    The loss function
    """

    def func(app_gt, app_pred):
        gt_temp = np.array(app_gt)
        gt_temp = np.where(gt_temp < on_power_threshold, 0, 1)
        pred_temp = np.array(app_pred)
        pred_temp = np.where(pred_temp < on_power_threshold, 0, 1)
        return f1_score(gt_temp, pred_temp)

    return func
