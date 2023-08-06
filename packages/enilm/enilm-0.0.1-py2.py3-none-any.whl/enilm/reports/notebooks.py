"""Generate notebook reports"""

from pathlib import Path

import papermill as pm


curr_file_dir = Path(__file__).parent


def gen_nb(exp_res_dir: Path, output_nb: Path):
    if output_nb.suffix == 'ipynb':
        raise ValueError('Output notebook must end with ipynb')

    pm.execute_notebook(
        curr_file_dir / 'template.ipynb',
        output_nb,
        parameters=dict(
            base_dir=str(exp_res_dir),
        )
    )
