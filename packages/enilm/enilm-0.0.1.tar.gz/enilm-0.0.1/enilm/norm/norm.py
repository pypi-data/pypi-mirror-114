from pathlib import Path
from typing import Union, NamedTuple, Optional, List

import numpy as np
import pandas as pd
import yaml

from enilm.nilmtk import Appliance, ElecMeter, MeterGroup

import enilm


def normalize(x: Union[np.ndarray, pd.Series], mean: Optional[float] = None, std: Optional[float] = None):
    if mean is None:
        mean = np.mean(x)
    if std is None:
        std = np.std(x)

    return (x - mean) / std


def denormalize(x: Union[np.ndarray, pd.Series], mean: float, std: float):
    return (x * std) + mean


class NormParams(NamedTuple):
    mean: float
    std: float


def compute(x: Union[np.ndarray, pd.Series]) -> NormParams:
    return NormParams(float(np.mean(x)), float(np.std(x)))


class NoActivations(RuntimeError):
    pass


def compute_on_power_from_elec(
        elec: Union[ElecMeter, MeterGroup],
        on_power_threshold: Optional[int] = None,
        load_kwargs: Optional[enilm.load_kwargs.LoadKwargs] = None
) -> NormParams:
    """
    If `on_power_threshold` is not provided, then it is extracted from enilm.nilmtk see `nilmtk.appliance.on_power_threshold`
    """
    load_kwargs = load_kwargs.to_dict() if load_kwargs is not None else {}
    activations: List[pd.Series] = enilm.activations.get_appliance_activations(
        elec, on_power_threshold, **load_kwargs
    )
    if len(activations) == 0:
        raise NoActivations
    all_act: np.ndarray = np.concatenate(activations)
    return NormParams(float(np.mean(all_act)), float(np.std(all_act)))


def get_params(dataset: enilm.etypes.DatasetID, appliance: Union[Appliance, str] = None) -> NormParams:
    """
    if appliance is None, normalization params for mains is returned
    """
    config_file_path: Path = Path(__file__).parent.parent / "config.yaml"
    dataset_name = enilm.datasets.id_to_str(dataset)
    norm_params = yaml.safe_load(config_file_path.read_text())['norm']

    if dataset_name not in norm_params:
        raise ValueError

    app_name: str
    if appliance is None:
        app_name = 'mains'
    elif isinstance(appliance, Appliance):
        app_name = appliance.label()
    elif isinstance(appliance, str):
        app_name = appliance
    else:
        raise ValueError

    if app_name not in norm_params[dataset_name]:
        raise ValueError

    return NormParams(
        mean=norm_params[dataset_name][app_name]['mean'],
        std=norm_params[dataset_name][app_name]['std'],
    )
