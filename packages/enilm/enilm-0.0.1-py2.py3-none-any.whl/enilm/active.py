"""Helper methods related to retrieving [in]active days"""

import datetime
import math
from typing import Set, List, Iterator

import numpy as np
import pandas as pd
from enilm.nilmtk import ElecMeter, TimeFrame, Appliance, MeterGroup
from enilm.nilmtk.appliance import ApplianceID
from enilm.nilmtk.electric import Electric

from enilm.activations import get_appliance_activations, get_appliance_activations_generator
from enilm.appliances import get_elec


def get_appliance_activations_days(appliance_elec: ElecMeter, **kwargs) -> Set[datetime.date]:
    """

    Parameters
    ----------
    appliance_elec
    kwargs passed to get_appliance_activations

    Returns
    -------

    """
    active_days: Set[datetime.date] = set()
    for activation in get_appliance_activations(appliance_elec, **kwargs):
        start, end = activation.index[0], activation.index[-1]
        # usually the same date (i.e. start == end), but if the activations spans two days (i.e. overnight) then the
        # two days (in which the activation started and ended) are considered
        active_days.add(start.date())
        active_days.add(end.date())

    return active_days


def get_days_data(
    active_days_rate: float, appliance_elec: ElecMeter, timeframe: TimeFrame, seed=None, **kwargs
) -> Set[datetime.date]:
    """
    active_days_rate = x => return floor(x * active_days_in_tf) active days and ((1-x) * inactive_days_in_tf) inactive
    days where tf is the timeframe of the data
    E.g.
        data has 40 days (with 12 active days and 28 inactive days)
        active_days_rate = 0 => return 28 inactive days
        active_days_rate = 1 => return 12 active days
        active_days_rate = 0.5 => return 6 active days and 6 inactive days (randomly sampled)
        active_days_rate = 0.25 => return 3 active days and 21 inactive days (randomly sampled)
        active_days_rate = 0.7 => return 8 active days and 19 inactive days (randomly sampled)

    Cautions
    --------
    - Length of returned days depends on the active rate!
    - Order of returned days is random

    Parameters
    ----------
    active_days_rate rate of active days as a float
    appliance_elec passed to get_appliance_activations_days
    timeframe passed to get_appliance_activations_days
    seed passed to numpy.random.defaul_rng
    kwargs passed to get_appliance_activations

    Returns
    -------
    object
    Set of day dates
    """
    # sanity checks
    assert isinstance(active_days_rate, float)
    assert 0 <= active_days_rate <= 1
    assert kwargs.get("sections") is None

    # add timeframe to kwargs to load it
    kwargs["sections"] = [timeframe]

    # active days
    active_days: Set[datetime.date] = get_appliance_activations_days(appliance_elec, **kwargs)

    # inactive days = all \ active days
    inactive_days: Set[datetime.date] = set()
    timeframe_duration_days: int = (timeframe.end - timeframe.start).days
    day: pd.Timestamp
    for day in (timeframe.start + datetime.timedelta(days=n) for n in range(timeframe_duration_days)):
        dt: datetime.date = day.to_pydatetime().date()
        if not dt in active_days:
            inactive_days.add(dt)

    # handle 0, 1
    if active_days_rate == 1:
        return active_days
    if active_days_rate == 0:
        return inactive_days

    # determinate number of days in each set
    n_active: int = math.floor(active_days_rate * len(active_days))
    n_inactive: int = math.floor((1 - active_days_rate) * len(inactive_days))

    # convert to lists to work with np
    active_days_list: List[datetime.date] = list(active_days)
    inactive_days_list: List[datetime.date] = list(inactive_days)

    # sample
    rng = np.random.default_rng(seed)
    result: List[datetime.date] = list(rng.choice(active_days_list, n_active, replace=False))
    result.extend(rng.choice(inactive_days_list, n_inactive, replace=False))
    rng.shuffle(result)  # randomize order (in-place)
    assert len(result) == n_active + n_inactive

    return set(result)


def active_appliances(elec: MeterGroup, **kwargs) -> Iterator[Appliance]:
    """

    Parameters
    ----------
    elec: meter group
    kwargs: passed to nilmtk.electric.Electric.load
        e.g. sections=[TimeFrame(start, stop), ...], ...

    Returns
    -------
    A generator of all active appliances within the given timeframe
    """
    for appliance in elec.appliances:
        meter: Electric = get_elec(appliance, elec)
        activations_gen: Iterator[pd.Series] = get_appliance_activations_generator(meter, **kwargs)
        active = next(activations_gen, None) is not None
        if active:
            yield appliance


def inactive_appliances(elec: MeterGroup, **kwargs) -> Set[Appliance]:
    """

    Parameters
    ----------
    elec: meter group
    kwargs: passed to nilmtk.electric.Electric.load
        e.g. sections=[TimeFrame(start, stop), ...], ...

    Returns
    -------
    A set of all inactive appliances within the given timeframe
    """
    active_apps = set(active_appliances(elec, **kwargs))
    all_apps = set(elec.appliances)
    return all_apps - active_apps
