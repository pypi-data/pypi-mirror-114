import os
import statistics
from abc import ABC
from copy import copy
from functools import cached_property
from operator import itemgetter
from pathlib import Path
from typing import Set, Dict, Optional, Union, List, Tuple

import pandas as pd
from jinja2 import Template
from enilm.nilmtk import MeterGroup, Appliance, TimeFrame
from enilm.nilmtk.timeframegroup import TimeFrameGroup
from plotly import graph_objects as go
from pyecharts import options
from pyecharts.charts import Pie

from enilm.activations import get_appliance_activations_generator
from enilm.active import active_appliances
from enilm.appliances import get_elec
from enilm.measures import ApplianceMeasures
from enilm.measures.measures import Measure
from enilm.etypes.measures import Report


class TotalMeasures(Measure, ABC):
    def __init__(self, elec: MeterGroup, **kwargs):
        """
        TODO

        Parameters
        ----------
        elec: meter groupr
        kwargs: passed to nilmtk.electric.Electric.load
            e.g. sections=[TimeFrame(start, stop), ...], ...
        """
        assert isinstance(elec, MeterGroup)
        super().__init__(elec, **kwargs)

    @cached_property
    def active_appliances(self) -> Set[Appliance]:
        return set(list(active_appliances(self.elec, **self.kwargs)))

    @cached_property
    def inactive_appliances(self) -> Set[Appliance]:
        return set(self.elec.appliances) - set(self.active_appliances)

    @cached_property
    def single_app_measures(self) -> Dict[Appliance, ApplianceMeasures]:
        result: Dict[Appliance, ApplianceMeasures] = {}
        for app in self.active_appliances:
            result[app] = ApplianceMeasures(get_elec(app, self.elec), **self.kwargs)
        return result

    @cached_property
    def total_number_of_appliances(self) -> int:
        """
        Number of appliances in the full dataset

        Returns
        -------
        total number of appliances in the dataset as reported by the MeterGroup of the dataset
        """
        return len(self.elec.appliances)

    def number_of_active_appliances(self, per: Optional[pd.Timedelta] = None) -> Union[int, float]:
        """
        Number of active appliances in a given timeframe
        - for training sections: indicate the "complexity" of the model
        - for testing sections: indicate how easy it is to disaggregate the test data

        Parameters
        ----------
        per: average results per provided timespan

        Returns
        -------
        The number of active appliances within the given timeframe
        """
        if per:
            # TODO this implementation is pretty inefficient due to multiple calls to `active_appliances`
            nactive: List[int] = []
            section: TimeFrame
            for section in self.sections:
                subsection: TimeFrame
                total_seconds = per.total_seconds()
                if not total_seconds.is_integer():
                    raise ValueError("per time span must be equal to an integer number of seconds")
                for subsection in section.split(int(total_seconds)):
                    kwargs = copy(self.kwargs)
                    kwargs["sections"] = [subsection]
                    nactive.append(len(list(active_appliances(self.elec, **kwargs))))
            return statistics.mean(nactive)
        return len(self.active_appliances)

    def number_of_inactive_appliances(self) -> Union[int, float]:
        """
        Number of inactive appliances in a given timeframe

        Returns
        -------
        The number of inactive appliances within the given timeframe
        """
        return self.total_number_of_appliances - self.number_of_active_appliances()

    def power_statistics(self) -> pd.DataFrame:
        """
        Power magnitude statistics: min, max, difference (max - min), mean, std, ... for all active appliances. All
          columns as reported by `pandas.Series.describe` with one extra column `diff = max - min` and number of
          activations `nactive`.

        Returns
        -------
        pandas.Series of results
        """
        single_app: List[pd.Series] = []
        for app in self.active_appliances:
            desc_ser: pd.Series = self.single_app_measures[app].power_statistics()
            desc_ser.name = app.label(True)  # rename series to app label
            single_app.append(desc_ser)
        return pd.concat(single_app, axis=1)

    @cached_property
    def activity_duration(self) -> pd.Timedelta:
        """
        Total time in which any appliance was active. See `docs/img/total_activity_algo.png` for case explanation.

        Returns
        -------
        Time duration
        """
        # collect each appliance activation time frame (start and end point of a time span)
        timeframes: List[TimeFrame] = []
        for app in self.elec.appliances:
            activation: pd.Series
            activations = get_appliance_activations_generator(get_elec(app, self.elec), **self.kwargs)
            for activation in activations:
                timeframes.append(TimeFrame(activation.index[0], activation.index[-1]))
                del activation

        # sort time frames by starting time
        timeframes.sort(key=lambda timef: timef.start)

        # keep essential timeframe (remove overlapping)
        ess_tfs: List[TimeFrame] = []
        for tf in timeframes:
            if len(ess_tfs) == 0:
                ess_tfs.append(tf)
            else:
                prev_tf = ess_tfs[-1]
                if tf.start < prev_tf.end:
                    if tf.end < prev_tf.end:  # case 1
                        continue
                    else:  # case 2
                        ess_tfs.pop()
                        ess_tfs.append(tf.union(prev_tf))
                else:  # case 3
                    ess_tfs.append(tf)

        return pd.Timedelta(TimeFrameGroup(ess_tfs).uptime())

    @cached_property
    def inactivity_duration(self) -> pd.Timedelta:
        """
        Total time in which no appliance was active

        Returns
        -------
        Time duration
        """
        return pd.Timedelta(self.total_duration - self.activity_duration)

    def report(self) -> "TotalMeasuresReport":
        """
        Generate report of all statistics

        Returns
        -------
        Report class
        """
        # TODO add progress bar
        return TotalMeasuresReport(self)


class TotalMeasuresReport(Report):
    def __init__(self, tm: TotalMeasures):
        self.tm = tm

    def _repr_html_(self):
        # pie chart of activity
        active_pie = go.Figure()
        active_pie.add_pie(
            labels=["active", "inactive"],
            values=[
                self.tm.activity_duration / self.tm.total_duration,
                self.tm.inactivity_duration / self.tm.total_duration,
            ],
        )

        # list of tuples: (app name, #activations),...
        app_nactive: List[Tuple[str, int]] = [
            (app.label(True), len(self.tm.single_app_measures[app].activations)) for app in self.tm.active_appliances
        ]

        # sort app_nactive by number of activations
        app_nactive.sort(key=itemgetter(1))
        app_nactive = list(reversed(app_nactive))

        # bar chart of active appliance and number of activations
        nactive_bar = go.Figure()
        nactive_bar.add_bar(x=list(map(itemgetter(0), app_nactive)), y=list(map(itemgetter(1), app_nactive)))
        nactive_bar.update_layout(yaxis_title="Total number of activations")

        # pie chart of number of activations per appliance
        # pie = Pie(options.InitOpts(width='300px'))
        pie = Pie()
        pie.add(
            "Number of activations",
            [options.PieItem(app_name, n_activations) for app_name, n_activations in app_nactive],
        )
        pie.load_javascript()
        app_nactive_pie: str = pie.render_notebook()._repr_html_()

        html: str = Path(
            os.path.join(Path(__file__).parent, "templates", "total_measures_report.html.jinja")
        ).read_text()
        template: Template = Template(html)
        return template.render(
            dict(
                duration=self.tm.total_duration,
                napps=self.tm.total_number_of_appliances,
                nactive_apps=self.tm.number_of_active_appliances(),
                ninactive_apps=self.tm.number_of_inactive_appliances(),
                activity_duration=self.tm.activity_duration,
                inactivity_duration=self.tm.inactivity_duration,
                active_apps=self.tm.active_appliances,
                inactive_apps=self.tm.inactive_appliances,
                nactive_per_day=self.tm.number_of_active_appliances(pd.Timedelta("1day")),
                nactive_per_hour=self.tm.number_of_active_appliances(pd.Timedelta("1h")),
                power_stats_html=self.tm.power_statistics()._repr_html_(),
                active_pie_html=active_pie.to_html(full_html=False),
                nactive_bar_html=nactive_bar.to_html(full_html=False),
                app_nactive_pie=app_nactive_pie,
            )
        )
