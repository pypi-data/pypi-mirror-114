"""Helper methods for nilmtk appliances"""
from typing import Union, Iterable, List

import enilm
from enilm import nilmtk
from enilm.nilmtk import Appliance, MeterGroup, ElecMeter
from enilm.etypes import AppName
from enilm.nilmtk.electric import Electric

__all__ = ["get_appliance", "to_str", "get_elec"]


def get_appliance(appliance_elec: Electric) -> Appliance:
    """
    Returns appliance of provided meter, if none or more than one appliance are attached to the meter an error is raised
    The type can be used to retrieve the appliance from the meter group and uniquely identify it (see `get_elec`)

    Parameters
    ----------
    appliance_elec electricity meter of the appliance (either ElecMeter or MeterGroup)

    Returns
    -------
    appliance id
    """
    assert hasattr(appliance_elec, "appliances")
    if not len(appliance_elec.appliances) == 1:
        raise ValueError("An ElecMeter with exactly one appliance is expected")
    return appliance_elec.appliances[0]


def get_elec(app: Union[Appliance, str], elec: MeterGroup) -> Union[ElecMeter, MeterGroup]:
    """
    Returns meter (either one meter as `ElecMeter` or multiple meters as a `MeterGroup`) of the corresponding appliance
    from the provided meter group `elec`
    """
    assert isinstance(elec, MeterGroup)
    try:
        if isinstance(app, str):
            return elec[app]
        elif isinstance(app, Appliance):
            return elec[app.identifier.type, app.identifier.instance]
        else:
            raise ValueError(
                "App is expected to be either a string (that uniquley identify the required appliance) or an instance "
                "of `nilmtk.appliance.Appliance`"
            )
    except Exception as e:
        if isinstance(app, str):
            # get `Appliance` from string
            some_app: Appliance
            for some_app in elec.appliances:
                if some_app.type["type"] == app:
                    app = some_app
                    break
            else:
                raise ValueError(
                    f"Cannot find provided app {app} in elec meter")

        if e.args[0].startswith("search terms match"):
            # in REFIT both fridge,1 and freezer,1 are classified as of type fridge and thus calling `elec['freezer', 1]`
            # would generate an Exception with the following message: "search terms match 2 appliances"
            # WARN this is only a workaround and not tested thoroughly!
            for meter in elec.meters:
                if len(meter.appliances) == 1 and meter.appliances[0] == app:
                    return meter
        raise e


def to_str(
        apps_names: Iterable[Union[nilmtk.Appliance, AppName]]
) -> List[AppName]:
    res = []
    for app in apps_names:
        if isinstance(app, nilmtk.Appliance):
            res.append(app.label(True).lower())
        else:
            assert isinstance(app, enilm.etypes.AppName)
            res.append(app)
    return res
