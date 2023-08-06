from typing import Callable

import pandas as pd

# Type alias for a loss function (see `nilmtk.losses`)
LossFunc = Callable[[pd.Series, pd.Series], float]

import enilm.losses.sae
import enilm.losses.f1
