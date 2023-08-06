"""Defines some common type aliases"""

import datetime
from typing import Union, List, Optional, Dict

import pandas as pd
from enilm.nilmtk import TimeFrame
from pydantic import PositiveInt
from pydantic.main import BaseModel

from enilm.nilmdt import get_year_timeframe

TimeType = Union[str, pd.Timestamp, datetime.datetime]


class ResampleKwargs(BaseModel):
    fill_method: Optional[str]  # default: ffill
    how: Optional[str]  # default: mean
    limit: Optional[PositiveInt]


class LoadKwargs(BaseModel):
    """
    kwargs passed to data loading functions like: `nilmtk.elecmeter.ElecMeter.load`
    see docstring of `nilmtk.elecmeter.ElecMeter.load` for more details
    """

    verbose: Optional[bool]
    sample_period: Optional[PositiveInt]
    sections: Optional[List[TimeFrame]]
    resample: Optional[bool]
    resample_kwargs: Optional[ResampleKwargs]

    class Config:
        arbitrary_types_allowed = True  # to allow `TimeFrame`

    def to_dict(self) -> Dict:
        """
        Convert to dict and remove None attributes
        """
        return {
            k: v for k, v in self.dict().items() if v is not None
        }


if __name__ == '__main__':
    load_kwargs: LoadKwargs = LoadKwargs(
        sample_period=6,
        sections=[get_year_timeframe(2013, None)],
    )
    print(load_kwargs.to_dict())
