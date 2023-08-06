from numpy import cos, deg2rad

from eagers.basic.solar_calc import solar_calc
from eagers.setup.update_qpform_all import assign_type


def renewable_output(gen, date, irradiation,location = None):
    """date is the vector of time points at which you request data."""
    panel = None
    turbine = None
    if not isinstance(gen,dict):
        if assign_type(gen) == 'Solar':
            panel = gen.__dict__
            panel['location'] = location
        elif assign_type(gen) == 'Wind':
            turbine = gen.__dict__
    else:
        if gen['type'] == 'Solar':
            panel = gen
        elif gen['type'] ==  'Wind':
            turbine = gen
    power = []
    if not panel is None:
        _, _, azimuth, zenith = solar_calc(panel['location']['longitude'],panel['location']['latitude'],panel['location']['time_zone'],date)
        if panel['tracking'] == 'fixed':
            for t in range(len(azimuth)):
                power.append(panel['size_m2']*(irradiation[t]/1000)*cos(deg2rad(zenith[t]-panel['tilt'])) \
                * max([0, cos(deg2rad(azimuth[t] - panel['azimuth']))])* panel['eff'])
        elif panel['tracking'] in ['1_axis', '1axis']:
            print("Did you mean 'one_axis'?")
        elif panel['tracking'] == 'one_axis':
            for t in range(len(zenith)):
                power.append(panel['size_m2']* (irradiation[t]/1000) * cos(deg2rad(zenith[t] - panel['tilt']))*panel['eff'])
        else:  # Dual axis.
            for t in range(len(irradiation)):
                power.append(panel['size_m2']*(irradiation[t]/1000)*panel['eff'])
    if not turbine is None:
        print('Need to update renewable_output.py for Wind.')
        pass
    return power
