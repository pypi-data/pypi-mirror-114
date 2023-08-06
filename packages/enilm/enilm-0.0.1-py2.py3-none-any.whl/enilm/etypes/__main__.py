from enum import Enum, auto
from typing import Union

from pydantic import PositiveInt

AppName = str
HouseNr = PositiveInt


class Datasets(Enum):
    """Enum of NILMTK supported and tested data sets, see `nilmtk.dataset_converters`"""
    DRED = auto()
    REDD = auto()
    BLOND = auto()
    REFIT = auto()
    SMART = auto()
    UKDALE = auto()
    SynD = auto()
    ECO = auto()


DatasetID = Union[Datasets, str]
