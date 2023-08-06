"""Common plotting function with [py]echarts"""
import calendar
import datetime
from typing import List, Tuple, Dict, Optional

import numpy as np
import pandas as pd
from enilm.nilmtk import TimeFrame, MeterGroup
from enilm.nilmtk.electric import Electric
from pyecharts import options
from pyecharts.charts import Calendar, Bar

from enilm.appliances import get_elec
from enilm.nilmdt import get_month_timeframe, get_dates_in_month, get_day_timeframe
from enilm.constants import AGG_FUNCS


# @cached
# def _power_series_all_data()


def month_heatmap(
        elec: Electric, year: int, month: int, tzinfo: datetime.tzinfo, agg_fun: str = AGG_FUNCS[0], **kwargs
) -> Calendar:
    """
    Generate a monthly heatmap of provided electric meter

    Parameters
    ----------
    elec electric meter (to retrieve data via `power_series_all_data`)
    tzinfo time zone info (see `common.nilmdt.get_tzinfo_from_ds`)
    agg_fun aggregation function (see `AGG_FUNCS`)
    kwargs passed to `power_series_all_data` and must not include `sections`

    Returns
    -------
    Calendar pyechart
    """
    # parameters check
    assert agg_fun in AGG_FUNCS, "Unsupported aggregation function"
    assert "sections" not in kwargs, "Sections in kwargs are set automatically based on passed year and month"

    # get mean of each day in month from elec
    tf: TimeFrame = get_month_timeframe(year, month, tzinfo)
    month_data: pd.Series = elec.power_series_all_data(sections=[tf], **kwargs)
    assert len(month_data) != 0 and not month_data.isna().all(), "No data can be loaded for provided parameters"
    month_data = month_data.groupby(month_data.index.day).aggregate(agg_fun)

    # generate list of data for each day in month if available
    dates_in_month: List[datetime.datetime] = get_dates_in_month(year, month)
    data: List[Tuple[str, float]] = []
    for i in range(1, len(dates_in_month) + 1):
        data_point: float = 0
        if i in month_data.index:
            data_point = month_data.loc[i]
        if isinstance(data_point, np.float32):
            data_point = float(data_point)
        data.append(round(data_point, 3))

    # create echarts plot
    calendar = Calendar()
    calendar.add(
        series_name=f"Power {agg_fun}",
        yaxis_data=[(str(date), data[i]) for i, date in enumerate(dates_in_month)],
        calendar_opts={"range": f"{year}-{month}", "cellSize": [100, 30], "yearLabel": {"show": True}},
        tooltip_opts={"position": "top", "formatter": "{c}"},
    )
    calendar.set_global_opts(
        legend_opts=options.LegendOpts(is_show=False),
        visualmap_opts={
            "min": min(data),
            "max": max(data),
            "calculable": True,
            "orient": "horizontal",
            "left": "center",
            "top": "top",
        },
    )

    # TODO for each quarter of the day
    # https://echarts.apache.org/examples/en/editor.html?c=calendar-pie
    # "series": {
    #     "type": "scatter",
    #     "coordinateSystem": "calendar",
    #     "data": [
    #         (str(date), data[i], data[i] + 1) for i, date in enumerate(dates_in_month)
    #     ]
    # }

    return calendar


def _weekly_data(
        elec: MeterGroup, year: int, month: int, week: int, tzinfo: datetime.tzinfo, agg_fun: str = AGG_FUNCS[0],
        **kwargs
) -> Dict[str, List[float]]:
    """
    Returns
    -------
    Aggregated data per app for each day
    Example:
    ```
    {
      'fridge': [1, 2, 3, 4, 5, 6, 7], # for weeks towards the start of the end of a month fewer days may be expected
      'washer 3': ...
    }
    ```
    """
    # parameters check
    assert isinstance(elec, MeterGroup), "Elec must be a meter group"
    assert agg_fun in AGG_FUNCS, "Unsupported aggregation function"
    assert "sections" not in kwargs, "Sections in kwargs are set automatically based on passed parameters"

    month_weeks: List[List[int]] = calendar.monthcalendar(year, month)
    assert 0 <= week < len(month_weeks), f"Week number must be valid (>= 0 and <{len(month_weeks)})"

    # dates of each day in the week
    days_dates: List[int] = [d for d in month_weeks[week] if d != 0]

    # compute data for each app over each day in the week using the provided aggregation function
    app_agg_data: Dict[str, List[float]] = {}
    appliances_elecmeters: Dict[str, Electric] = {app.label(True): get_elec(app, elec) for app in elec.appliances}
    for day_num in days_dates:
        day_date: datetime.date = datetime.date(year, month, day_num)
        day_tf: TimeFrame = get_day_timeframe(day_date, tzinfo)
        for appliance_name, elec in appliances_elecmeters.items():
            series: pd.Series = elec.power_series_all_data(sections=[day_tf], **kwargs)
            agg_val: Optional[float] = None
            if series is not None:
                agg_val = series.aggregate(agg_fun)
            if appliance_name not in app_agg_data:
                app_agg_data[appliance_name] = []

            if agg_val is not None:
                app_agg_data[appliance_name].append(round(float(agg_val), 3))
            else:
                app_agg_data[appliance_name].append(0)
    return app_agg_data


def weekly_bars(
        elec: MeterGroup, year: int, month: int, week: int, tzinfo: datetime.tzinfo, agg_fun: str = AGG_FUNCS[0],
        **kwargs
):
    """
    Generate a bar chart, where the aggregated value (depending on the provided `agg_fun`) for each appliances in the
     provided meter group `elec` in each day of the week is plotted as a bar. Pay attention to the validity of the
     provided date data (year, month, week).

    Parameters
    ----------
    elec meter group
    week week number in that month (picked up from `calendar.monthcalendar`)
    tzinfo time zone info (see `common.nilmdt.get_tzinfo_from_ds`)
    agg_fun aggregation function (see `AGG_FUNCS`)
    kwargs passed to `power_series_all_data` and must not include `sections`

    Returns
    -------
    Bar pyechart
    """
    app_agg_data = _weekly_data(elec, year, month, week, tzinfo, agg_fun, **kwargs)

    # dates of each day in the week
    month_weeks: List[List[int]] = calendar.monthcalendar(year, month)
    days_dates: List[int] = [d for d in month_weeks[week] if d != 0]

    # Bar echarts
    # see this example: https://echarts.apache.org/examples/zh/editor.html?c=doc-example/mix-timeline-all
    chart = Bar()

    # chart options
    chart.set_global_opts(
        legend_opts={
            "data": list(app_agg_data.keys()),
            "selector": [{"type": "all or inverse", "title": "All"}, {"type": "inverse", "title": "Inv"}],
        },
        xaxis_opts={
            "type": "category",
            "boundaryGap": True,
            "rotate": 90,
            "axisLabel": {"interval": 0, "align": "center"},
        },
        yaxis_opts=options.AxisOpts(type_="value", name=f"Power {agg_fun}"),
    )

    # xaxis = day name + new line + date
    days_names: List[str] = []
    for day_num in days_dates:
        day_date: datetime.date = datetime.date(year, month, day_num)
        days_names.append(day_date.strftime("%A") + "\n" + str(day_date))
    chart.add_xaxis(days_names)

    # yaxis = aggregated app data
    for app_name, app_data in app_agg_data.items():
        chart.add_yaxis(app_name, app_data)

    return chart
