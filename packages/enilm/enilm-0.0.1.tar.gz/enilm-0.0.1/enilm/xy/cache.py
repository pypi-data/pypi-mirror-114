from pathlib import Path

import enilm
import numpy as np


def save_xyarry(xy: enilm.etypes.xy.XYArray, folder: Path):
    assert folder.exists() and folder.is_dir()
    np.save(str(Path(folder, 'x.npy')), xy.x)
    for an in xy.y.keys():
        np.save(str(Path(folder, f'y_{an}.npy')), xy.y[an])


def load_xyarry(folder: Path) -> enilm.etypes.xy.XYArray:
    assert folder.exists() and folder.is_dir()
    x = np.load(str(Path(folder, 'x.npy')))
    y = {}
    for app_arr_file in folder.glob('y_*.npy'):
        an = app_arr_file.name[2:-4]
        y[an] = np.load(str(app_arr_file))
    return enilm.etypes.xy.XYArray(x, y)
