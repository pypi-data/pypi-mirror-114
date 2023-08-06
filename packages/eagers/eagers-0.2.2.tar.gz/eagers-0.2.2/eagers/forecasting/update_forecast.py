from datetime import timedelta
from numpy import log
from scipy.stats import t

from eagers.basic.get_data import get_data
from eagers.forecasting.arima import arima
from eagers.forecasting.arma import arma
from eagers.forecasting.surface_forecast import surface_forecast
from eagers.forecasting.weather_forecast import weather_forecast


def update_forecast(options, date, test_data,subnet):
    """Update forecast using any of the following forecasting
    algorithms:
    Perfect     Perfect forecast. Requires future data, and therefore is
                only available in simulation mode.
    Surface     Surface forecast.
    ARMA        AutoRegressive Moving Average forecast.
    ARIMA       AutoRegressive Integrated Moving Average forecast.
    ANN         Artificial Neural Network forecast.
    
    Positional arguments:
    options - (Optimoptions) Project options.
    date - (list of timestamp) Timestamps for which a forecast is
        requested.
    test_data 
    subnet - (dict) Network data.
    """
    hist_prof = test_data['hist_prof']
    # Period of repetition (1 = 1 day). This is how far back the
    # forecasting methods are able to see. It is irrelevant if the
    # forecast is perfect.
    
    if not options['forecast'] in ['perfect','uncertain']:
        #TODO replace with observer history
        d0 = date[0] - timedelta(hours = 24+options['resolution'])
        prev_date = [d0 + timedelta(hours = i*options['resolution']) for i in range(round(24/options['resolution'],0)+1)]
        prev_data = get_data(test_data,prev_date,subnet['network_names'])
    forecast = {}
    forecast['timestamp'] = date
    if options['forecast'] != 'arima' and not options['forecast'] in ['perfect','uncertain']:
        forecast['weather'] = weather_forecast(test_data,prev_data, hist_prof, date)
    if options['forecast'] == 'arma':
        forecast['demand'] = arma(date, prev_data)
    elif options['forecast'] == 'arima':
        forecast = arima(date, prev_data, options)
    elif options['forecast'] == 'neural_net':
        pass
    #TODO # create neural network forecasting option
    elif options['forecast'] == 'surface':
        forecast['demand'] = surface_forecast(prev_data, hist_prof['demand'], date, forecast['weather']['t_dryb'],[])
    elif options['forecast'] in ['perfect','uncertain']:
        forecast = get_data(test_data, date, subnet['network_names'])
        if options['forecast'] == 'uncertain':
            forecast = make_uncertain(forecast,options['forecast_uncertainty'])
    elif options['forecast'] == 'building':
        pass
    else:
        raise RuntimeError('Forecast option not recognized.')
    ### Make first hour forecast "perfect"
    # make_perfect(forecast,options,test_data,date,subnet)
    if options['spin_reserve']:
        if 'demand' in forecast:
            #TODO update this
            forecast['sr_target'] += options['spin_reserve_perc'] / 100 * sum(
                forecast['demand']['e'], 2)
    return forecast

def make_perfect(forecast,options,test_data,date,subnet):
    #Make first step of forecast perfect:
    if options['method'].lower() == 'dispatch' and len(date) > 1:
        next_data = get_data(test_data, date[0], subnet['network_names'])
        for k in next_data:
            if isinstance(next_data[k], dict):
                for s_i in next_data[k]:
                    forecast[k][s_i][0] = next_data[k][s_i][0]
            else:
                forecast[k][0] = next_data[k][0]

def make_uncertain(forecast,sp):
    '''Apply forecast error to the given forecast, using the given
    random number generator.

    Positional arguments:
    forecast - (dict) Forecast information with the same structure as
        returned by get_data().
    sp - forecast scale paramater
    '''
    gamma = [float(log(i+2) * sp / 6.3138) for i in range(len(forecast['timestamp']))]
    node_names = list(forecast.keys())
    for node in node_names:
        if not node in ['weather','timestamp'] and 'demand' in forecast[node]:
            n = len(forecast[node]['demand'])
            ran = t.rvs(1, size=n)
            rscale = [max(0.5,(1+min(0.5,float(ran[i])*gamma[i]/100)))for i in range(n)]
            forecast[node]['demand'] = [forecast[node]['demand'][i]*rscale[i] for i in range(n)]
    # Weather.
    for k in ['glo_horz_irr','dir_norm_irr','dif_horz_irr','t_dryb','wspd']:
        if k in forecast['weather']:
            n = len(forecast['weather'][k])
            ran = t.rvs(1, size=n)
            rscale = [max(0.5,(1+min(0.5,float(ran[i])*gamma[i]/100)))for i in range(n)]
            forecast['weather'][k] = [forecast['weather'][k][i]*rscale[i] for i in range(n)]
    return forecast
