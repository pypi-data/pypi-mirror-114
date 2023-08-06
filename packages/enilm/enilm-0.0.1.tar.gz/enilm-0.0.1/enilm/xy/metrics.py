from typing import Dict, Iterable, Optional

import numpy as np
import tensorflow as tf
import pandas as pd
import wandb.sdk

import enilm


def denorm_mae(
        model: tf.keras.Model,
        appliances: Iterable[enilm.etypes.AppName],
        x_chunks: np.ndarray,
        y_chunks: Dict[enilm.etypes.AppName, np.ndarray],
        y_mean: Dict[enilm.etypes.AppName, float],
        y_std: Dict[enilm.etypes.AppName, float],
        run: Optional[wandb.sdk.wandb_run.Run] = None,
        run_prefix: Optional[str] = ''
) -> pd.DataFrame:
    denorm_mae: Dict[enilm.etypes.AppName, float] = {}
    for id, app_name in enumerate(appliances):
        _app_name = app_name.replace(" ", "_")
        denorm_mae[app_name] = enilm.metrics.denrom_mae(
            lambda _x: model(_x)[_app_name].numpy(),
            x_chunks,
            y_chunks[_app_name],
            y_mean[app_name],
            y_std[app_name]
        )
        if run is not None:
            run.summary[f"{run_prefix}denorm_mae_{app_name}"] = denorm_mae[app_name]
    denorm_mae_df = pd.DataFrame({k: [v] for k, v in denorm_mae.items()})
    denorm_mae_df.index = ['denorm_mae']
    return denorm_mae_df
