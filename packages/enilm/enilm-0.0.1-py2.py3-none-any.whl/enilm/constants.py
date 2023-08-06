from enum import Enum, auto


# 0 = silent, 1 = progress bar, 2 = one line per epoch.
# https://www.tensorflow.org/api_docs/python/tf/keras/Model#fit
# use 2 when log to a file
class KerasOutputVerbose(Enum):
    SILENT = 0
    PROGRESS_BAR = 1
    ONE_LINE_PER_EPOCH = 2


class MemUnit(Enum):
    # https://en.wikipedia.org/wiki/Byte#Multiple-byte_units
    GB = 'gb'
    MB = 'mb'
    KB = 'kb'
    B = 'b'
    GiB = 'gib'
    MiB = 'mib'
    KiB = 'kib'


class ModelType(Enum):
    S2S = auto()
    S2P = auto()


AGG_FUNCS = ["mean", "sum", "min", "max", "size", "std", "var"]
