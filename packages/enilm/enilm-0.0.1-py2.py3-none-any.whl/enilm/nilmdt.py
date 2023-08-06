"""
Helpers to deal with `datetime` (standard library) and `TimeFrame` (nilmtk) objects.
"""

import datetime
import calendar
from typing import List, Iterable, Union

import pytz
import pandas as pd
from enilm.nilmtk import TimeFrame, DataSet

import enilm


def get_tzinfo_from_ds(ds: Union[DataSet, enilm.etypes.Datasets]) -> datetime.tzinfo:
    if isinstance(ds, DataSet):
        return pytz.timezone(ds.metadata.get("timezone"))
    if isinstance(ds, enilm.etypes.Datasets):
        return pytz.timezone(enilm.datasets.get_nilmtk_dataset(ds).metadata.get("timezone"))
    raise ValueError('Unsupported dataset type')


def get_day_timeframe(day_date: datetime.date, tzinfo: datetime.tzinfo) -> TimeFrame:
    """Get timeframe of one day"""
    return TimeFrame(start=day_date, end=day_date + pd.Timedelta("1day"), tz=tzinfo)


def get_month_timeframe(year: int, month: int, tzinfo: datetime.tzinfo) -> TimeFrame:
    """Get time frame of one month"""
    return TimeFrame(
        start=datetime.datetime(year, month, 1, 1, 1, 1, tzinfo=tzinfo),
        end=datetime.datetime(year, month, get_last_day_of_month(year, month), 23, 59, 59, tzinfo=tzinfo),
    )


def get_year_timeframe(year: int, tzinfo: datetime.tzinfo) -> TimeFrame:
    """Get time frame of one month"""
    return TimeFrame(
        start=datetime.datetime(year, 1, 1, 1, 1, 1, tzinfo=tzinfo),
        end=datetime.datetime(year, 12, get_last_day_of_month(year, 12), 23, 59, 59, tzinfo=tzinfo),
    )


def get_last_day_of_month(year: int, month: int) -> int:
    """Get last day of month"""
    # https://stackoverflow.com/a/43663/1617883
    return calendar.monthrange(year, month)[1]


def get_dates_in_year(year: int) -> List[datetime.date]:
    """Returns a list with datetimes for each day a year"""
    d1 = datetime.date(year, 1, 1)
    d2 = datetime.date(year, 12, get_last_day_of_month(year, 12))
    delta = d2 - d1
    return [d1 + datetime.timedelta(i) for i in range(delta.days + 1)]


def get_dates_in_month(year: int, month: int) -> List[datetime.datetime]:
    """Returns a list with datetimes for each day a year"""
    d1 = datetime.date(year, month, 1)
    d2 = datetime.date(year, month, get_last_day_of_month(year, month))
    delta = d2 - d1
    return [d1 + datetime.timedelta(i) for i in range(delta.days + 1)]


def get_months_in_year(year: int, data_tf: TimeFrame) -> List[int]:
    """Get all months in year"""
    # TODO better month selection not only based on start and end but also on actual data e.g. if there is
    #  missing data in-between
    if year == data_tf.start.date().year:
        return list(range(data_tf.start.date().month, 13))
    elif year == data_tf.end.date().year:
        return list(range(1, data_tf.end.date().month + 1))
    return list(range(1, 13))


def dates_to_timeframes(data: Iterable[datetime.date], tzinfo: datetime.tzinfo) -> List[TimeFrame]:
    """
    dates in data are converted into a list of nilmtk TimeFrame (thus making it easier to pass the results directly to load
    methods of data stores as the `sections` parameter)
    """
    sections: List[TimeFrame] = []
    create_dt = lambda y, m, d: datetime.datetime(year=y, month=m, day=d, tzinfo=tzinfo)
    for day in data:
        end = day + datetime.timedelta(days=1)
        sections.append(TimeFrame(create_dt(day.year, day.month, day.day), create_dt(end.year, end.month, end.day)))
    return sections


def get_week(date: datetime.date) -> int:
    # https://stackoverflow.com/a/2600864/1617883
    return date.isocalendar()[1]


def timeframe_to_str(timeframe: TimeFrame) -> str:
    # .replace(':', '-') is for windows filenames compatability
    return f'{timeframe.start.isoformat().replace(":", "-")}_{timeframe.end.isoformat().replace(":", "-")}'
