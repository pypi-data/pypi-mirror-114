import datetime 

from eagers.building.process.forecast_dr_capacity import forecast_dr_capacity
from eagers.basic.build_time_vector import build_time_vector
from eagers.basic.find_gen_node import find_gen_node
from eagers.setup.load_matrices import load_matrices
from eagers.setup.automatic_ic import automatic_ic
from eagers.simulate.renewable_output import renewable_output
from eagers.update.update_cost import update_cost
from eagers.forecasting.update_forecast import update_forecast
from eagers.forecasting.hydro_forecast import hydro_forecast
from eagers.setup.initialize_observer import initialize_observer
from eagers.solver.dispatch_loop import dispatch_loop


def water_year_forecast(gen,buildings,fluid_loop,observer,all_data_nodes,names,zones,pl,market,subnet,options,date,test_data):
    hydroforecast = False
    for i in range(len(gen)):
        if gen[i]['type']=='HydroStorage':
            hydroforecast = True
    if 'hydro_wy_timestamp' in observer and observer['hydro_wy_timestamp'] !=None:
        if observer['hydro_wy_timestamp'][-1]>=date[-1]:
            hydroforecast = False

    if hydroforecast:
        #first create the yearly dispatch data 
        # i.e. run Dispatch loop with updated information
        #these will be used for set points in the actual dispatch
        date_now = date[0]
        options['horizon'] = 364*24 #Yearly Horizon
        options['resolution'] = 7*24 #Week Resolution
        if date_now.month()<10 and date[-1].month()>=10:
            year = date_now.year()-1
            dy1 = datetime.datetime(date_now.year(),10,1,0,0,0)
            options['horizon'] = (53+round((date[-1]-dy1).days()/7+.5))*7*24 #ensure that water year forecast goes a week beyond the final date
        elif date_now.month()<10:
            year = date_now.year()-1
        else:
            year = date_now.year()
        d1 = datetime.datetime(year, 10, 1, 1, 0, 0) 
        date = build_time_vector(d1,options, to_timedelta=True)
        dt = [(date[t+1] - date[t]).seconds/3600 for t in range(len(date)-1)]
        b_names = [buildings[i].name for i in range(len(buildings))]
        op_mat_a = load_matrices(gen,b_names,fluid_loop,market,subnet,options,'A',dt) #build quadratic programming matrices for FitA
        op_mat_b = load_matrices(gen,b_names,fluid_loop,market,subnet,options,'B',dt) #build quadratic programming matrices for FitB
        one_step = load_matrices(gen,b_names,fluid_loop,market,subnet,options,'B',[]) #build quadratic programming matrices for single time step

        if observer['hydro_wy_timestamp'] == None:
            scale_cost = update_cost(date,gen,market)
            ic, data_t0, _ = automatic_ic(gen,buildings,fluid_loop,market,subnet,date[0],one_step,options,test_data,None,scale_cost) # set the initial conditions 
            wy_observer = initialize_observer(gen,subnet,fluid_loop,all_data_nodes, names, zones, pl,test_data,None,ic,50,date_now,data_t0,None)
        else:
            wy_observer = observer
        
        if date[-1]<=test_data['hydro']['timestamp'][-1]:
            forecast = update_forecast(options,date[1:],test_data,subnet)
            if 'weather' in forecast and 'dir_norm_irr' in forecast['weather']:
                forecast['renewable'] = [renewable_output(gen[i], date[1:], forecast['weather']['dir_norm_irr']) \
                                        if gen[i]['type'] in ['Renewable','Solar','Wind'] and gen[i]['enabled'] \
                                        else [] for i in range(len(gen))]
            forecast['building'],_,_,_ = forecast_dr_capacity(buildings,wy_observer,forecast['weather'],date)
            forecast = hydro_forecast(forecast,test_data,date[1:],subnet,[],options)
            solution,_ = dispatch_loop(gen,wy_observer,market,subnet,names,op_mat_a,op_mat_b,one_step,options,date,forecast,[])
            hydro_soc_init = [0 for n in range(len(subnet['hydro']['nodes']))]
            for n in range(len(subnet['hydro']['nodes'])):
                i = subnet['hydro']['equipment'][n]
                if gen[i]['type']=='HydroStorage':
                    hydro_soc_init[n] = observer.stor_state[i]
            solution['hydro_soc'] = [solution['hydro_soc'][n].insert(0,hydro_soc_init) for n in range(len(solution['hydro_soc']))]
            print('Water Year Forecast Completed for ' + str(year)+':',str(year+1))
            if observer.hydro_wy_timestamp==None:
                t = 0
                while solution['timestamp'][t+1]<date_now:
                    t+=1
                r = (solution['timestamp'][t+1]-date_now)/(solution['timestamp'][t+1]-solution['timestamp'][t])
                for i in range(len(gen)):
                    if gen[i]['type'] =='HydroStorage':
                        n = gen[i]['hydro']['subnet_node'] #dam #
                        observer['stor_state'][i] = r*solution['hydro_soc'][t][n] + (1-r)*solution['hydro_soc'][t+1][n]
            observer['hydro_wy_timestamp'] = solution['timestamp'] 
            observer['hydro_wy_soc'] = solution['hydro_soc']
    return observer
