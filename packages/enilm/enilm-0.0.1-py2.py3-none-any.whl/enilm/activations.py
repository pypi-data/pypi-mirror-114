from pathlib import Path
from typing import List, Optional, Union, Iterator

import enilm
import enilm.nilmtk.electric
import numpy as np
import pandas as pd
import yaml
from enilm.nilmtk import Appliance, ElecMeter, MeterGroup
from enilm.nilmtk.electric import Electric
from enilm.nilmtk.utils import timedelta64_to_secs


def get_known_on_power_threshold(dataset: enilm.etypes.DatasetID, appliance: Appliance) -> Optional[float]:
    """
    Returns on power threshold from known appliances as specified in `on_power_thresholds.toml`

    Parameters
    ----------
    dataset dataset name
    appliance appliance name

    Returns
    -------
    On power threshold if defined, None otherwise.
    """
    assert isinstance(appliance, Appliance)

    config_file_path: Path = Path(__file__).parent.parent / "config.yaml"
    thresholds = yaml.safe_load(config_file_path.read_text())['on_power_thresholds']

    dataset_name: str = dataset.name if isinstance(dataset, enilm.etypes.Datasets) else dataset
    if dataset_name in thresholds:
        app_id_str = appliance.label(True)
        if app_id_str in thresholds[dataset_name]:
            return thresholds[dataset_name][app_id_str]


def get_appliance_activations(
        appliance_elec: Union[ElecMeter, MeterGroup], on_power_threshold: Optional[int] = None, **kwargs
) -> List[pd.Series]:
    """
    Uses nilmtk.electric.Electric.get_activations to extract activations ranges for an appliance.
    If `on_power_threshold` is not provided, then it is extracted from enilm.nilmtk see `nilmtk.appliance.on_power_threshold`

    Parameters
    ----------
    appliance_elec ElecMeter or MeterGroup of the appliance
    on_power_threshold on power threshold in watts
    kwargs passed to `nilmtk.electric.ElecMeter.get_activations`

    Returns
    -------
    list of activations, each as pandas series
    """
    # type check
    if on_power_threshold is not None:
        assert isinstance(on_power_threshold, int)
    assert isinstance(appliance_elec, ElecMeter) or isinstance(appliance_elec, MeterGroup)

    # if len(appliance_elec.appliances) != 1:
    #     raise ValueError("Provided meter must include one appliance only")

    if on_power_threshold is None:
        app: Appliance = enilm.appliances.get_appliance(appliance_elec)
        on_power_threshold = get_known_on_power_threshold(appliance_elec.dataset(), app)
        if on_power_threshold is None:
            # fallback to nilmtk metadata
            on_power_threshold = app.on_power_threshold()
    return appliance_elec.get_activations(on_power_threshold=on_power_threshold, **kwargs)


def get_activation_for_series(
        series: pd.Series,
        appliance_elec: Union[ElecMeter, MeterGroup],
        on_power_threshold: Optional[int] = None
) -> List[pd.Series]:
    if on_power_threshold is None:
        app: Appliance = enilm.appliances.get_appliance(appliance_elec)
        on_power_threshold = get_known_on_power_threshold(appliance_elec.dataset(), app)
        if on_power_threshold is None:
            # fallback to nilmtk metadata
            on_power_threshold = app.on_power_threshold()

    return nilmtk.electric.get_activations(
        series,
        min_off_duration=appliance_elec.min_off_duration(),
        min_on_duration=appliance_elec.min_on_duration(),
        on_power_threshold=on_power_threshold,
    )


def _get_appliance_activations_generator(
        elec: Electric, min_off_duration=None, min_on_duration=None, border=1, on_power_threshold=None, **kwargs
) -> Iterator[pd.Series]:
    """The same function as `nilmtk.Electric.get_appliance_activations` and `nilmtk.electric.get_activates` but as a
    generator"""
    if on_power_threshold is None:
        on_power_threshold = elec.on_power_threshold()

    if min_off_duration is None:
        min_off_duration = elec.min_off_duration()

    if min_on_duration is None:
        min_on_duration = elec.min_on_duration()

    kwargs.setdefault("resample", True)
    for chunk in elec.power_series(**kwargs):
        when_on = chunk >= on_power_threshold

        # Find state changes
        state_changes = when_on.astype(np.int8).diff()
        del when_on
        switch_on_events = np.where(state_changes == 1)[0]
        switch_off_events = np.where(state_changes == -1)[0]
        del state_changes

        if len(switch_on_events) == 0 or len(switch_off_events) == 0:
            return []

        # Make sure events align
        if switch_off_events[0] < switch_on_events[0]:
            switch_off_events = switch_off_events[1:]
            if len(switch_off_events) == 0:
                return []
        if switch_on_events[-1] > switch_off_events[-1]:
            switch_on_events = switch_on_events[:-1]
            if len(switch_on_events) == 0:
                return []
        assert len(switch_on_events) == len(switch_off_events)

        # Smooth over off-durations less than min_off_duration
        if min_off_duration > 0:
            off_durations = chunk.index[switch_on_events[1:]].values - chunk.index[switch_off_events[:-1]].values

            off_durations = timedelta64_to_secs(off_durations)

            above_threshold_off_durations = np.where(off_durations >= min_off_duration)[0]

            # Now remove off_events and on_events
            switch_off_events = switch_off_events[
                np.concatenate([above_threshold_off_durations, [len(switch_off_events) - 1]])
            ]
            switch_on_events = switch_on_events[np.concatenate([[0], above_threshold_off_durations + 1])]
        assert len(switch_on_events) == len(switch_off_events)

        for on, off in zip(switch_on_events, switch_off_events):
            duration = (chunk.index[off] - chunk.index[on]).total_seconds()
            if duration < min_on_duration:
                continue
            on -= 1 + border
            if on < 0:
                on = 0
            off += border
            activation = chunk.iloc[on:off]
            # throw away any activation with any NaN values
            if not activation.isnull().values.any():
                yield activation


def get_appliance_activations_generator(
        appliance_elec: Electric, on_power_threshold: Optional[int] = None, **kwargs
) -> Iterator[pd.Series]:
    """The same function as `get_appliance_activations` but as a generator"""
    if not on_power_threshold is None:
        assert isinstance(on_power_threshold, int)
    assert isinstance(appliance_elec, Electric)
    # some appliances has more than one ElecMeter attached in one MeterGroup (e.g. split-phase mains, 3-phase mains
    # and dual-supply (240 volt) appliances)

    if len(appliance_elec.appliances) != 1:
        raise ValueError("Provided meter must include one appliance only")

    appliance: Appliance = appliance_elec.appliances[0]
    if on_power_threshold is None:
        app: Appliance = enilm.appliances.get_appliance(appliance_elec)
        on_power_threshold = get_known_on_power_threshold(appliance_elec.dataset(), app)
        if on_power_threshold is None:
            # fallback to nilmtk metadata
            on_power_threshold = appliance.on_power_threshold()
    yield from _get_appliance_activations_generator(appliance_elec, on_power_threshold=on_power_threshold, **kwargs)
