"""Logic for updating energy purchase costs.

Functions:
update_cost
interp_scale_cost
"""

import datetime as dt

from eagers.config.units import kWh_per_MMBtu_natgas
from eagers.basic.get_data import interp_data


def update_cost(date, gen, market):
    """Update energy purchase costs for the current time.

    Positional arguments:
    date - (list of datetime) Dates for horizon (current time not
        included).
    gen - (list of dict) Generator information.
    market - Market information.
    """
    n_s = len(date)
    n_g = len(gen)
    source = [None] * n_g
    scale_cost = [[] for i in range(n_g)]
    market_rate = None
    # Get the rate for each utility.
    # Assumes there is only one utility for each network type.
    for i, g in enumerate(gen):
        if g['type'] == 'Utility':
            source[i] = g['source']
            utility = g
            if 'sum_start_month' in utility:
                # Ensure summer and winter seasons don't start on the same day.
                yr = date[0].year
                sum_start = dt.datetime(yr, utility['sum_start_month'], utility['sum_start_day'])
                if utility['win_start_month'] > utility['sum_start_month'] or \
                    (utility['win_start_month'] == utility['sum_start_month'] \
                        and utility['win_start_day'] > utility['sum_start_day']):
                    yr +=1
                win_start = dt.datetime(yr, utility['win_start_month'], utility['win_start_day'])
                # Whether the winter pricing season starts this year, as
                rate = []
                for d in date:
                    h = d.hour
                    day = d.weekday()
                    if d > sum_start and d <= win_start:
                        j = utility['sum_rate_table'][day][h] - 1
                        rate.append(utility['sum_rates'][j][0])
                    else:
                        j = utility['win_rate_table'][day][h] - 1
                        rate.append(utility['win_rates'][j][0])
                scale_cost[i] = rate  # Utility rate in $/kWh.
            else:
                # Time series utility.
                ut_yr = utility['timestamp'][0].year
                d_yr = date[0].year
                diff = dt.datetime(ut_yr,1,1) - dt.datetime(d_yr,1,1)
                date_num=[(d+diff).replace(tzinfo=dt.timezone.utc).timestamp() for d in date]
                j = 0
                n_u = len(utility['timestamp'])
                while j<n_u-2 and utility['timestamp'][j+1]<date[0]+diff:
                    j+=1
                jj = j+1
                while jj<n_u-1 and utility['timestamp'][jj]<date[-1]+diff:
                    jj+=1
                
                i_list = [i for i in range(j,jj)]
                if jj==len(utility['timestamp'])-1:
                    i_list.append(0)
                    diff = dt.datetime(ut_yr-1,1,1) - dt.datetime(d_yr,1,1)
                    while i_list[-1]<n_u-1 and utility['timestamp'][i_list[-1]]<date[-1]+diff:
                        i_list.append(i_list[-1]+1)
                else:
                    i_list.append(jj)
                conversion = 1
                if source[i] in ('ng', 'diesel'):
                    # Convert gas rate from $/MMBTU to $/kWh.
                    conversion = 1 / kWh_per_MMBtu_natgas
                # Interpolate rate.
                scale_cost[i] = interp_scale_cost(utility, conversion, i_list, date_num)
        elif g['type']=='Tradepoint': 
            #TODO update tradpoint coefficients b0,b1 and s0,s1
            six_param = g['six_param']
            scale_cost[i] = [[six_param] for i in range(n_s)]
        elif g['type']=='Market': #Market varaible/bids is empty during initialization
            if market_rate == None:
                market_rate = [[]]
                m_num = 0
            else:
                market_rate.append([])
                m_num += 1
            na = len(market['award']['time'])
            awarded = 0
            for j in range(na):
                if market['award']['time'] > date[0]:
                    # Identify how many awards have already passed.
                    awarded += 1
            n = na - awarded
            for d in date:
                while n < na and d < market['award']['time'][n]:
                    n += 1
                market_rate[m_num].append(market['award']['price'][m_num][n])
            scale_cost[i] = market_rate[m_num]

    # Match each utility-fueled generator with its corresponding utility
    # cost, if a corresponding utility exists.
    for i, g in enumerate(gen):
        util_fueled = ('ElectricGenerator', 'CombinedHeatPower', 'Chiller',
            'Heater', 'CoolingTower', 'Electrolyzer', 'HydrogenGenerator')
        if g['type'] in util_fueled:
            try:
                util_index = source.index(g['source'])
            except ValueError:
                # No utility (don't scale costs).
                util_index = None
                scale_cost[i] = [1] * n_s
            if util_index is not None:
                scale_cost[i] = scale_cost[util_index]
    return scale_cost


def interp_scale_cost(utility, conversion, i_list, date_num):
    x_vals = []
    for i in i_list:
        t_add = utility['timestamp'][i]
        if i <i_list[0]:
            # Add year.
            t_add += dt.timedelta(days = 365)
        x_vals.append((t_add).replace(tzinfo=dt.timezone.utc).timestamp())
    y_vals = {}
    if 'SP' in utility:
        # Spot market.  Get spot market price signal.
        y_vals['rate']=[utility['SP'][t] * conversion for t in i_list]
    else:
        y_vals['rate']=[utility['rate'][t] * conversion for t in i_list]
    dtq1 = x_vals[1]-x_vals[0]
    scale = interp_data(x_vals, y_vals, date_num, ['rate'], None, dtq1)['rate']
    return scale
