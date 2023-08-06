"""Sanity checks"""

from enilm.nilmtk import TimeFrame


def check_timeframe(timeframe: TimeFrame):
    timeframe.check_tz()


def check_valid_date(year: int, month: int, day: int):
    raise NotImplementedError
