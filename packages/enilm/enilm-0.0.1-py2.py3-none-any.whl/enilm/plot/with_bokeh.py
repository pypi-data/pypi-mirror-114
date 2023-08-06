"""
TODOs:
- [ ] draw average line in month view
- [ ] highlight weekends
    - [ ] bands in month view
"""

import calendar
import copy
import datetime
from typing import List

import bokeh.palettes
import pandas as pd
from bokeh.models import ColumnDataSource, LinearColorMapper
from bokeh.plotting import Figure
from bokeh.transform import transform
from enilm.nilmtk import TimeFrame
from enilm.nilmtk.electric import Electric

from enilm.nilmdt import get_month_timeframe, get_year_timeframe
from enilm.constants import AGG_FUNCS


def line_month(elec: Electric, year: int, month: int, tzinfo: datetime.tzinfo, agg_fun: str = AGG_FUNCS[0],
               color_palette: List = bokeh.palettes.RdYlGn[11], **kwargs) -> Figure:
    """
    Agg. data of each day in month for elec

    Parameters
    ----------
    elec electric meter (to retrieve data via `power_series_all_data`)
    tzinfo time zone info (see `common.nilmdt.get_tzinfo_from_ds`)
    agg_fun aggregation function (see `AGG_FUNCS`)
    kwargs passed to `power_series_all_data` and must not include `sections`

    Returns
    -------
    Bokeh figure
    """
    # parameters check
    assert agg_fun in AGG_FUNCS, "Unsupported aggregation function"
    assert "sections" not in kwargs, "Sections in kwargs are set automatically based on passed year and month"

    # get agg of each day in month from elec
    tf: TimeFrame = get_month_timeframe(year, month, tzinfo)
    month_data: pd.Series = elec.power_series_all_data(sections=[tf], **kwargs)
    assert len(month_data) != 0 and not month_data.isna().all(), "No data can be loaded for provided parameters"

    # remove any reading not within the given and month
    month_data = month_data[(month_data.index.year == year) & (month_data.index.month == month)]

    # drop Na
    na_count = month_data.isna().sum()
    if na_count > 0:
        print(f'Dropping {na_count} NA values')
        month_data = month_data.dropna()

    # aggregate
    agg_data = month_data.groupby(pd.Grouper(freq='D')).aggregate(agg_fun)

    # data source for bokeh
    df = pd.DataFrame(
        {
            agg_fun: agg_data,
            'day': agg_data.index.day,
            'day_name': agg_data.index.dayofweek.map(lambda _: calendar.day_name[_]),
        },
        index=agg_data.index,
    )
    source = ColumnDataSource(df)

    # create plot
    mapper = LinearColorMapper(
        palette=color_palette,
        low=df[agg_fun].min(),
        high=df[agg_fun].max()
    )

    fig = bokeh.plotting.figure(
        sizing_mode="stretch_width",
        title=f'{agg_fun.capitalize()}s in {calendar.month_name[month]} {year}',
        x_axis_type='datetime',
    )

    fig.add_tools(bokeh.models.HoverTool(
        tooltips=[
            ("index", "$index"),
            (agg_fun, f'@{agg_fun}{{0}}'),
            ('date', f'@day.{month}.{year}'),
            ("day", f"@day_name"),
        ],
        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    ))

    fig.vbar(
        x='day',
        top=agg_fun,
        source=source,
        width=1,  # datetime.timedelta(hours=22),
        bottom=0,
        line_width=0,
        fill_color=transform('mean', mapper),
    )

    return fig


def year_heatmap(elec: Electric, year: int, tzinfo: datetime.tzinfo, agg_fun: str = AGG_FUNCS[0],
                 color_palette: List = bokeh.palettes.RdYlGn[11], **kwargs) -> Figure:
    # parameters check
    assert agg_fun in AGG_FUNCS, "Unsupported aggregation function"
    assert "sections" not in kwargs, "Sections in kwargs are set automatically based on passed year and month"

    # get agg of each month in the year
    tf: TimeFrame = get_year_timeframe(year, tzinfo)
    data: pd.Series = elec.power_series_all_data(sections=[tf], **kwargs)
    assert len(data) != 0 and not data.isna().all(), "No data can be loaded for provided parameters"

    # remove any reading not within the given year
    data = data[data.index.year == year]

    # drop Na
    na_count = data.isna().sum()
    if na_count > 0:
        print(f'Dropping {na_count} NA values')
        data = data.dropna()

    # aggregate
    agg_data: pd.Series = data.groupby(pd.Grouper(freq='D')).aggregate(agg_fun)

    # group into df
    df = pd.DataFrame(
        {
            agg_fun: agg_data,
            'month': agg_data.index.month,
            'day': agg_data.index.day,
            'day_name': agg_data.index.dayofweek.map(lambda _: calendar.day_name[_]),
            'day_of_week': agg_data.index.dayofweek,  # 0 = Mo, 7 = Su
        },
        index=agg_data.index,
    )

    # plot
    mapper = LinearColorMapper(
        palette=bokeh.palettes.Plasma[10],
        low=df[agg_fun].min(),
        high=df[agg_fun].max()
    )

    y_tick_formatter_js_code = (
            '\n'.join([f'if (tick == {i}) return "{calendar.day_name[i]}";' for i in range(7)]) +
            '\nelse return "";'
    )

    fig = bokeh.plotting.figure(
        match_aspect=True,
        y_axis_label="day",
        sizing_mode="stretch_width",
        plot_height=300,
        y_range=(8, -2),
    )

    fig.xaxis.visible = False

    fig.tools = [
        bokeh.models.PanTool(),
        bokeh.models.WheelZoomTool(),
        bokeh.models.SaveTool(),
        bokeh.models.HoverTool(
            tooltips=[
                ("index", "$index"),
                (agg_fun, f"@{agg_fun}"),
                ("date", f"@day.@month.{year}"),
                ("day", f"@day_name"),
            ],
        ),
        bokeh.models.ResetTool()
    ]

    months_labels_x = []
    curr_draw_week = 0
    for month in range(1, 12 + 1):
        data = copy.deepcopy(df[df["month"] == month])

        # add start x for label
        months_labels_x.append(curr_draw_week)

        # create draw_week column
        draw_week = []
        curr_draw_week += 1  # add monthly gap
        for dayofweek in data.day_of_week.to_list():
            draw_week.append(curr_draw_week)
            if dayofweek == 6:
                curr_draw_week += 1
        data['draw_week'] = draw_week

        fig.rect(
            x="draw_week",
            y="day_of_week",
            source=ColumnDataSource(data),
            width=1,
            height=1,
            line_width=0,
            fill_color=transform(agg_fun, mapper),
        )

    # add months names inside the plot
    for i, x in enumerate(months_labels_x):
        fig.add_layout(bokeh.models.Label(x=x + 2, y=-1, text=calendar.month_abbr[i + 1]))

    fig.yaxis.ticker.num_minor_ticks = 0  # hide minor ticks
    fig.yaxis.ticker.max_interval = 1  # always show days
    fig.xgrid.grid_line_color = None  # hide vertical grid lines
    fig.ygrid.grid_line_color = None  # hide horizontal grid lines
    fig.yaxis[0].formatter = bokeh.models.FuncTickFormatter(code=y_tick_formatter_js_code)  # show days' names on y-axis

    return fig


if __name__ == '__main__':
    from bokeh.io import show
    from enilm.loaders import load_refit

    loaded = load_refit(building_nr=5)

    if False:
        show(line_month(
            loaded.elec,
            year=2014,
            month=4,
            tzinfo=loaded.tz,
            agg_fun='mean',
            sample_period=120,
        ))

    if True:
        show(year_heatmap(
            loaded.elec,
            year=2014,
            tzinfo=loaded.tz,
            agg_fun='mean',
            sample_period=60 * 5,
        ))
