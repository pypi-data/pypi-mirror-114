"""
Quick loaders for common datasets with frequently used setting
"""
import datetime
from typing import Tuple

from enilm import nilmtk
from enilm.nilmtk import DataSet, MeterGroup
from pydantic import PositiveInt
from pydantic.main import BaseModel

import enilm
from enilm.datasets import get_nilmtk_dataset
from enilm.nilmdt import get_tzinfo_from_ds


class DatasetInfo(BaseModel):
    dataset: enilm.etypes.DatasetID
    building_nr: PositiveInt


def load_dsinfo(ds_info: DatasetInfo) -> Tuple[nilmtk.DataSet, nilmtk.MeterGroup]:
    ds = get_nilmtk_dataset(ds_info.dataset)
    elec = ds.buildings[ds_info.building_nr].elec  # MeterGroup
    return ds, elec


class LoadResult(BaseModel):
    ds_info: DatasetInfo
    ds: DataSet
    elec: MeterGroup
    tz: datetime.tzinfo

    class Config:
        arbitrary_types_allowed = True


def load(dataset: enilm.etypes.DatasetID, building_nr: PositiveInt) -> LoadResult:
    ds_info = DatasetInfo(dataset=dataset, building_nr=building_nr)
    ds, elec = load_dsinfo(ds_info)
    return LoadResult(
        ds_info=ds_info,
        ds=ds,
        elec=elec,
        tz=get_tzinfo_from_ds(ds),
    )
