import base64
from pathlib import Path
from typing import Dict

from IPython.display import HTML

import enilm

curr_folder = Path(__file__).parent.resolve()

ds_img: Dict[enilm.etypes.Datasets, Dict] = {
    enilm.etypes.Datasets.REFIT: {
        'img': Path(curr_folder, 'img/refit.png'),
        'attr': 'D. Murray, L. Stankovic, and V. Stankovic, “REFIT: An electrical load measurements dataset of United Kingdom households from a two-year longitudinal study,” Scientific Data, vol. 4, no. 1, Art. no. 1, Jan. 2017, doi: 10.1038/sdata.2016.122.',
    }
}


def availability(dataset: enilm.etypes.Datasets):
    if dataset in ds_img:
        with open(ds_img[dataset]["img"], 'rb') as img:
            img_b64 = base64.b64encode(img.read())
        attr = ds_img[dataset]['attr']
        return HTML(f'''
            <div>
                <img src="data:image/png;base64, {img_b64.decode()}"/>
                <p>{attr}</p>
            <div/>
        ''')
