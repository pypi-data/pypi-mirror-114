from typing import Union

from enilm.constants import MemUnit


def size(n: Union[float, int], from_unit: MemUnit, to_unit: MemUnit) -> float:
    # https://en.wikipedia.org/wiki/Byte#Multiple-byte_units
    n_bytes: Union[float, int] = n
    if from_unit == MemUnit.GiB:
        n_bytes = n * 1024.0 ** 3
    elif from_unit == MemUnit.MiB:
        n_bytes = n * 1024.0 ** 2
    elif from_unit == MemUnit.KiB:
        n_bytes = n * 1024.0 ** 1
    elif from_unit == MemUnit.GB:
        n_bytes = n * 1000.0 ** 1
    elif from_unit == MemUnit.MB:
        n_bytes = n * 1000.0 ** 1
    elif from_unit == MemUnit.KB:
        n_bytes = n * 1000.0 ** 1

    if to_unit == MemUnit.GiB:
        return n_bytes / 1024.0 ** 3
    if to_unit == MemUnit.MiB:
        return n_bytes / 1024.0 ** 2
    if to_unit == MemUnit.KiB:
        return n_bytes / 1024.0
    if to_unit == MemUnit.GB:
        return n_bytes / 1000.0 ** 3
    if to_unit == MemUnit.MB:
        return n_bytes / 1000.0 ** 2
    if to_unit == MemUnit.KB:
        return n_bytes / 1000.0
    if to_unit == MemUnit.B:
        return n_bytes
    raise ValueError
