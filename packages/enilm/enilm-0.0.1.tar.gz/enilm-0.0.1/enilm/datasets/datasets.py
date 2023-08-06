"""Helpers to get datasets paths and avoid navigating to the config file `config.toml`"""

import getpass
import os
import socket
import sys
import io
from pathlib import Path
from typing import Dict

from enilm import nilmtk
import yaml
import pandas as pd

import enilm


def get_all_datasets_paths() -> Dict[str, str]:
    """
    Read config.toml are return the path to the dataset.
    If paths[.PLATFORM[.HOSTNAME[.USERNAME]]] are specified, returns platform specific paths

    Returns
    -------
    Dictionary which keys are the datasets names and values are the paths
    """
    config_file_path: Path = Path(__file__).parent.parent.parent / "config.yaml"
    ds_paths = yaml.safe_load(config_file_path.read_text())['paths']['datasets']

    platform = sys.platform
    hostname = socket.gethostname()
    username = getpass.getuser()

    # check for submatch
    paths = {}
    if platform in ds_paths:
        paths = ds_paths[platform]
        if hostname in paths:
            paths = paths[hostname]
            if username in paths:
                paths = paths[username]
    return paths


def id_to_str(dataset_id: enilm.etypes.DatasetID) -> str:
    if isinstance(dataset_id, enilm.etypes.Datasets):
        return dataset_id.name
    return dataset_id


def get_dataset_path(dataset: enilm.etypes.DatasetID) -> str:
    """
    Read config.toml are return the path to the dataset.
    If paths[.PLATFORM[.HOSTNAME[.USERNAME]]] are specified, returns platform specific paths

    Parameters
    ----------
    dataset: desired dataset

    Returns
    -------
    Dataset path from config file
    """
    paths = get_all_datasets_paths()
    dataset_name = id_to_str(dataset)

    if dataset_name in paths:
        path: str = paths[dataset_name]
        if not os.path.exists(path):
            raise ValueError(f"File in {path} for dataset {dataset_name} does not exist")
        return path
    raise ValueError(f"Cannot find the dataset {dataset_name} in the config file")


def get_nilmtk_dataset(dataset: enilm.etypes.DatasetID) -> nilmtk.DataSet:
    """
    Parameters
    ----------
    dataset: desired dataset

    Returns
    -------
    NILMTK DataSet
    """
    return nilmtk.DataSet(get_dataset_path(dataset))


def overview() -> pd.DataFrame:
    data = '''
    Dataset ,Country Code,Year,Type                 ,#H   ,#A  ,Summed up Duration [d],Agg Sampling  , Appl Sampling
    UK-DALE ,GBR         ,2017,residential          ,5    ,109 ,2247                  ,"6 s, 16 kHz" ,6 s
    REDD    ,USA         ,2011,residential          ,6    ,92  ,119                   ,"1 Hz, 15 kHz",1 Hz3
    AMPds(2),CAN         ,2016,residential          ,1    ,20  ,730                   ,1 min         ,1 min
    REFIT   ,GBR         ,2016,residential          ,20   ,177 ,14600                 ,8 s           ,8 s
    dataport,USA         ,2015,residential          ,1200+,8598,1376120               ,"1 Hz, 1 min" ,"1 Hz, 1 min"
    ECO     ,CHE         ,2016,residential          ,6    ,45  ,1227                  ,1 Hz          ,1 Hz
    DRED    ,NLD         ,2014,residential          ,1    ,12  ,183                   ,1 Hz          ,1 Hz
    Enertalk,KOR         ,2019,residential          ,22   ,75  ,1714                  ,15 Hz         ,15 Hz
    HES     ,GBR         ,2010,residential          ,251  ,5860,15976                 ,2-10 min      ,2-10 min
    IDEAL   ,GBR         ,-   ,residential          ,-    ,-   ,-                     ,1 Hz          ,1 or 5 Hz
    IMD     ,BRA         ,2020,industrial           ,1    ,8   ,111                   ,1 Hz          ,1 Hz
    PLAID   ,USA         ,2014,residential          ,65   ,1876,1-20 s                ,-             ,30 kHz
    SynD    ,AUT         ,2020,synthetic residential,1    ,21  ,180                   ,5 z           ,5 Hz
    '''
    return pd.read_csv(io.StringIO(data), sep=',')


if __name__ == '__main__':
    print(get_all_datasets_paths())
