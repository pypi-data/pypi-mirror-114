import dataclasses
import json
from pathlib import Path
from typing import Optional, Union, Dict, Iterable, List

import enilm
from enilm import nilmtk
import pandas as pd


@dataclasses.dataclass()
class DataSel:
    dataset: enilm.etypes.Datasets
    houses: Iterable[enilm.etypes.HouseNr]

    # with type: { house_nr: list of timeframes}
    sections: Optional[Dict[enilm.etypes.HouseNr, Iterable[nilmtk.TimeFrame]]] = None

    def asdict(self) -> Dict:
        res = dataclasses.asdict(self)

        # datasets names
        res['dataset'] = self.dataset.name

        # serialize timeframes in sections
        if self.sections is not None:
            for house_nr, timeframes_list in self.sections.items():
                res['sections'][house_nr] = [{
                    'start': str(tf.start),
                    'end': str(tf.end),
                } for tf in timeframes_list]

        return res

    @classmethod
    def fromdict(cls, d: Dict):
        # dataset
        ds_name = d['dataset']
        dataset = enilm.etypes.Datasets[ds_name]
        tz = enilm.nilmdt.get_tzinfo_from_ds(dataset)

        # houses
        houses = d['houses']

        # sections
        sections = None
        if 'sections' in d and d['sections'] is not None:
            # TODO: if sections is
            sections = {}
            for house_nr, house_sections in d['sections'].items():
                house_nr = int(house_nr)
                sections[house_nr] = []
                for sec in house_sections:
                    sections[house_nr].append(nilmtk.TimeFrame(
                        start=pd.Timestamp(sec['start']),
                        end=pd.Timestamp(sec['end']),
                    ))

        return cls(dataset, houses, sections)


@dataclasses.dataclass()
class ExpConfig:
    appliances: List[Union[nilmtk.Appliance, enilm.etypes.AppName]]
    win_size: int
    repeats: int
    epochs: int
    batch_size: int
    shuffle: bool
    validation_split: float
    model_id: str
    train: List[DataSel]

    # optional
    exp_n: int = -1
    test: Optional[List[DataSel]] = None
    sample_period: Optional[int] = None
    notes: str = ''

    # with defaults
    lr: float = 0.001

    # auto-generated but can be overwritten
    exp_name: str = dataclasses.field(init=False)

    def __post_init__(self):
        self.exp_name = f'exp{self.exp_n:0>2}'

        if self.test is None:
            self.test = self.train

        # if self.test.dataset != self.train.dataset and self.test.houses is None:
        #     raise ValueError('Please specify test houses')

        # TODO: make sure appliance are available in houses
        # for house in self.train_houses:
        #     elec = enilm.datasets.loaders.load(self.train_dataset, house).elec
        #     for app in self.appliances:
        #         if not app in elec.appliances

    def asdict(self):
        res = dataclasses.asdict(self)

        # call asdict for each data_sel
        for i, data_sel in enumerate(self.train):
            res['train'][i] = data_sel.asdict()
        for i, data_sel in enumerate(self.test):
            res['test'][i] = data_sel.asdict()

        # appliances
        res['appliances'] = enilm.appliances.to_str(self.appliances)

        return res

    @classmethod
    def fromdict(cls, d: Dict):
        res = cls(
            exp_n=d['exp_n'],
            appliances=d['appliances'],
            win_size=d['win_size'],
            repeats=d['repeats'],
            epochs=d['epochs'],
            batch_size=d['batch_size'],
            shuffle=d['shuffle'],
            validation_split=d['validation_split'],
            model_id=d['model_id'],
            train=[DataSel.fromdict(datasel) for datasel in d['train']],
        )

        # optional
        if 'test' in d:
            res.test = [DataSel.fromdict(datasel) for datasel in d['test']]
        if 'sample_period' in d:
            res.sample_period = d['sample_period']
        if 'notes' in d:
            res.notes = d['notes']
        if 'lr' in d:
            res.lr = d['lr']

        return res

    def to_json(self, path: Optional[Path] = None) -> Optional[str]:
        """
        :param path: if provided, results are saved to this file, otherwise returned as string
        """
        if path:
            with open(path, 'w') as fp:
                json.dump(self.asdict(), fp)
        else:
            return json.dumps(self.asdict(), indent=2)

    @classmethod
    def from_json(cls, str_or_path: Union[str, Path]):
        json_str: str = ''
        if isinstance(str_or_path, str):
            json_str = str_or_path
        elif isinstance(str_or_path, Path):
            json_str = str_or_path.read_text()

        return cls.fromdict(json.loads(json_str))
