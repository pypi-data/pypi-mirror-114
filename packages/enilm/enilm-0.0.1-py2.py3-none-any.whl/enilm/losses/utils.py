import inspect
from typing import List

import enilm.nilmtk.losses


def get_all_losses() -> List[str]:
    """Get functions defined directly in `nilmtk.losses` (avoid imports)"""
    # https://docs.python.org/3/library/inspect.html#inspect.getmembers
    return [
        x[0] for x in inspect.getmembers(nilmtk.losses, lambda val: callable(val) and val.__module__ == "nilmtk.losses")
    ]
