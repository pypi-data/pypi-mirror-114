from abc import ABC
from functools import cached_property
from typing import List, Union

import pandas as pd
from enilm.nilmtk import MeterGroup, ElecMeter, TimeFrame
from enilm.nilmtk.timeframegroup import TimeFrameGroup

# from .reports import Report
# from ..activations import get_appliance_activations
# from ..load_kwargs import LoadKwargs
import enilm


class Measure(ABC):
    def __init__(self, elec: Union[ElecMeter, MeterGroup], **kwargs):
        enilm.load_kwargs.LoadKwargs.validate(kwargs)
        self.elec = elec
        self.kwargs = kwargs

    @cached_property
    def sections(self) -> List[TimeFrame]:
        """
        Extracts sections either from provided kwargs or total duration of provided meter
         see: `nilmtk.elecmeter.ElecMeter._get_stat_from_cache_or_compute`

        Returns
        -------
        List of sections (i.e. TimeFrame's)
        """
        sections = self.kwargs.get("sections")
        if sections is None:
            tf = self.elec.get_timeframe()
            tf.include_end = True
            sections = [tf]
        return sections

    @cached_property
    def total_duration(self) -> pd.Timedelta:
        """
        Extracts total duration (of data regardless of activity) for given elec

        Returns
        -------
        Total duration as pandas timedelta
        """
        return pd.Timedelta(TimeFrameGroup(self.sections).uptime())

    def power_statistics(self):
        raise NotImplementedError

    @cached_property
    def activity_duration(self) -> pd.Timedelta:
        raise NotImplementedError

    @cached_property
    def inactivity_duration(self) -> pd.Timedelta:
        raise NotImplementedError

    def report(self) -> enilm.etypes.measures.Report:
        raise NotImplementedError


class ApplianceMeasures(Measure, ABC):
    def __init__(self, elec: Union[ElecMeter, MeterGroup], **kwargs):
        """
        TODO

        Parameters
        ----------
        elec: meter of the appliance (**one** appliance only!)
        kwargs: passed to nilmtk.electric.Electric.load
            e.g. sections=[TimeFrame(start, stop), ...], ...
        """
        assert len(elec.appliances) == 1
        super().__init__(elec, **kwargs)

    @cached_property
    def activations(self) -> List[pd.Series]:
        return  enilm.activations.get_appliance_activations(self.elec, **self.kwargs)

    @cached_property
    def power_series_all_data(self) -> pd.Series:
        return self.elec.power_series_all_data(**self.kwargs)

    def power_statistics(self) -> pd.Series:
        """
        Power magnitude statistics: min, max, difference (max - min), mean, std,... for single appliance. All columns
         as reported by `pandas.Series.describe` with one extra column `diff = max - min` and number of activations `
         nactive`.

        Returns
        -------
        pandas.Series of results
        """
        desc: pd.Series = self.power_series_all_data.describe()
        desc["diff"] = desc["max"] - desc["min"]
        desc["nactive"] = len(self.activations)
        return desc

    @cached_property
    def activity_duration(self) -> pd.Timedelta:
        """
        Total time in which the appliance was active

        Returns
        -------
        Time duration
        """
        duration = pd.Timedelta(0)
        for activation in self.activations:
            start = activation.index[0]
            end = activation.index[-1]
            duration += end - start
        return duration

    @cached_property
    def inactivity_duration(self) -> pd.Timedelta:
        """
        Total time in which the appliance was inactive

        Returns
        -------
        Time duration
        """
        return pd.Timedelta(self.total_duration - self.activity_duration)
