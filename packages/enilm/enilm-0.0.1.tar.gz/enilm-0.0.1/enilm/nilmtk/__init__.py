from .elecmeter import ElecMeter
from .metergroup import MeterGroup
from .timeframe import TimeFrame
from .appliance import Appliance
from .dataset import DataSet
from .datastore import TmpDataStore

global_meter_group = MeterGroup()
STATS_CACHE = TmpDataStore()
