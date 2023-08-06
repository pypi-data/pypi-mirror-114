from typing import Union, Iterable

from enilm.nilmtk import ElecMeter, MeterGroup
from enilm.nilmtk.electric import Electric

from enilm.appliances import get_appliance


def sample_rate_info(elecs: Union[Iterable[ElecMeter], ElecMeter]) -> str:
    """
    Sample output for mains, kettle and washing machine from REFIT building 3:
    ```
    Mains:
        Sample Period: 7
        Sample Rate: 0.14Hz
        Number of samples/day: 12,343
    Washer dryer:
        Sample Period: 7
        Sample Rate: 0.14Hz
        Number of samples/day: 12,343
    Washer dryer:
        Sample Period: 7
        Sample Rate: 0.14Hz
        Number of samples/day: 12,343
    ```


    :param elecs: elecs to report about
    :return: string of all elecs sample period, rate and number of samples per day
    """
    if isinstance(elecs, Electric):
        elecs = [elecs]

    results = ''
    for elec in elecs:

        if isinstance(elec, MeterGroup):
            # mains
            results += 'Mains:'
        elif isinstance(elec, ElecMeter):
            # appliance
            app_name = get_appliance(elec).label(True)
            results += f'{app_name.capitalize()}:'
        else:
            raise ValueError(f'Unexpected type of ElecMeter: {type(elec)}')

        results += f'\n\tSample Period: {elec.sample_period()} seconds'
        results += f'\n\tSample Rate: {1 / elec.sample_period():.2}Hz'
        results += f'\n\tNumber of samples/day: {round((1 / elec.sample_period()) * 60 * 60 * 24):,}'
        results += '\n'

    return results.strip()


if __name__ == '__main__':
    test_sample_rate_info = False
    if test_sample_rate_info:
        from enilm.loaders import load_refit

        loaded = load_refit(building_nr=1)
        print(sample_rate_info(loaded.elec))
        # print(sample_rate_info([
        #     loaded.elec,
        #     get_elec('washer dryer', loaded.elec),
        # ]))
