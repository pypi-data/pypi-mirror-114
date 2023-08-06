from eagers.simulate.assign_disparity import assign_disparity
from eagers.simulate.building_response import building_response
from eagers.solver.dispatch_loop import dispatch_loop
from eagers.basic.all_demands import all_demands
from eagers.simulate.renewable_output import renewable_output
from eagers.basic.component_output import component_output
from eagers.update.update_cost import update_cost
from eagers.basic.marginal_cost import node_marginal


def plant_response(
        gen, building, fluid_loop, observer, market, subnet, names, actual_data,
        preload, options, forecast, date, solution):
    """Assigns where disparity between actual load and optimal dispatch
    goes. Building water loops absorb error in heating/cooling if there
    is a building model.
    """
    
    # 'control' mode runs real-time optimization that handles imbalance.
    if options['method'] =='control':
        # TODO: Reconstitute real-time control (Threshold and MPC).
        pass
    elif options['method'] =='dispatch':
        re_opt = False
        n_b = len(building)
        tol = dict(electrical = 1e-3, direct_current = 1e-3, transmission_1 = 1e-3, district_heat = 5e-2, district_cool = 5e-2, heating_2 = 5e-2, cooling_water = 5e-2, hydrogen = 1e-3, liq_hydrogen = 1e-3, hydro = 1e-3) 
        dt_now = (date[1] - date[0]).seconds/3600
        node_demand = all_demands(actual_data,subnet,[0])
        setpoint = {}
        if len(names['buildings'])>0:
            setpoint['temperature'] = [solution['building'][k]['temperature'][0] for k in names['buildings']]
        nn = list(node_demand.keys())
        # Sim all generators to determine actual heating, cooling, and waste heat to cooling loop
        for i in range(len(gen)):
            if gen[i]['type'] in ['Renewable','Solar','Wind']:
                renew = renewable_output(gen[i], [date[1]], actual_data['weather']['dir_norm_irr'])
                solution['dispatch'][i][1] = renew[0]
                solution['generator_state'][gen[i]['name']][0] = renew[0]
        gs_now = {}
        for k in solution['generator_state']:
            gs_now[k] = solution['generator_state'][k][0]
        scale_cost = update_cost(date[1:], gen,market)
        ##TODO add capacity (particularly capacity for response by buildings for use in assign disparity)
        marginal = node_marginal(gen,subnet,solution['dispatch'],scale_cost,solution['value_heat'])
        #sim fluid loops to assign thermal disparity to water loop
        for i in range(len(observer['fluid_loop_temperature'])):
            production = component_output(gen,subnet['cooling_water'],gs_now)
            observer['fluid_loop_temperature'][i] += dt_now/observer['fluid_loop_capacitance'][i]*production[i]
        #Assign disparity for heating/cooling to utility/storage/buildings or re-optimize if none are present
        for net in ['district_heat', 'district_cool']:
            if net in nn:
                production = component_output(gen,subnet[net],gs_now)
                request = building_request(names['buildings'],net,subnet[net],solution['building'],forecast['building'],[0])
                setpoint[net] = assign_disparity(net, names, gen, subnet[net],production,node_demand[net],request, solution, marginal, dt_now, tol[net], options['excess_heat'], re_opt)
                nn.remove(net)
        #Sim buildings 
        if n_b > 0:
            weather_now = {}
            for i in actual_data['weather']:
                weather_now[i] = actual_data['weather'][i][0]
            observer,net_electric = building_response(building,observer, weather_now, actual_data['building'], dt_now, setpoint,date[0])
            actual_data['building']['E0'][0] = net_electric
            actual_data['building']['C0'][0] = [solution['building'][k]['cooling'][0] for k in names['buildings']]
            actual_data['building']['H0'][0] = [solution['building'][k]['heating'][0] for k in names['buildings']]

        #rebalance other networks if necessary
        for net in nn:
            request =  None 
            if net == 'electrical' and 'buildings' in subnet[net] and any([len(n)>0 for n in subnet[net]['buildings']]):
                request = {}
                request['nominal'] = net_electric
            if not re_opt:
                production = component_output(gen,subnet[net],gs_now)
                assign_disparity(net, names, gen, subnet[net], production, node_demand[net], request, solution, marginal, dt_now, tol[net], False, re_opt)
        if re_opt:
            # Redo optimization due to disparity with actual data
            # and no slack bus, e.g. utility or storage.
            for k in forecast:
                if isinstance(forecast[k],dict) and 'demand' in forecast[k]:
                    forecast[k]['demand'][0] = actual_data[k]['demand'][0]
            if n_b > 0:
                forecast['building']['h_min'][0] = actual_data['building']['H0'][0]
                forecast['building']['c_min'][0] = actual_data['building']['C0'][0]
                forecast['building']['E0'][0] = actual_data['building']['E0'][0] 
                forecast['building']['C0'][0] = actual_data['building']['C0'][0]
                forecast['building']['H0'][0] = actual_data['building']['H0'][0]

            solution, _ = dispatch_loop(gen, observer, market, subnet, names, preload.op_mat_a, preload.op_mat_b,
                preload.one_step, options, date, forecast, solution['dispatch'])

    elif options['method'] =='planning':
        n_b = len(building)
        n_s = len(date)-1
        for t in range(n_s):
            dt_now = (date[t+1] - date[t]).seconds/3600
            if n_b > 0:
                setpoint = {}
                setpoint['temperature'] = [solution['building'][k]['temperature'][t] for k in names['buildings']]
                setpoint['district_heat'] = [solution['building'][k]['heating'][t]*1000 for k in names['buildings']]
                setpoint['district_cool'] = [solution['building'][k]['cooling'][t]*1000 for k in names['buildings']]
                weather_now = {}
                for i in actual_data['weather']:
                    weather_now[i] = actual_data['weather'][i][t]
                observer,net_electric = building_response(building,observer, weather_now, {},dt_now,setpoint,date[t])
                actual_data['building']['E0'][t] = net_electric
                actual_data['building']['C0'][t] = [solution['building'][k]['cooling'][t] for k in names['buildings']]
                actual_data['building']['H0'][t] = [solution['building'][k]['heating'][t] for k in names['buildings']]
            for i in range(len(observer['fluid_loop_temperature'])):
                gs_now = {}
                for k in solution['generator_state']:
                    gs_now[k] = solution['generator_state'][k][t]
                production = component_output(gen,subnet['cw'],gs_now)
                observer['fluid_loop_temperature'][i] += dt_now/observer['fluid_loop_capacitance'][i]*production[i]


def building_request(b_names,net,subnet,solution,forecast,t_sel):
    request = {}
    request['minimum'] = [[0] for n in range(len(b_names))]
    request['maximum'] = [[0] for n in range(len(b_names))]
    request['nominal'] = [[0] for n in range(len(b_names))]
    for i in range(len(b_names)):
        t_avg = solution[b_names[i]]['temperature'][0]
        if net == 'district_cool':
            t_bar = forecast['tc_bar'][0][i]
            ua = forecast['ua_c'][0][i]
            min_e = forecast['c_min'][0][i]
            t_min = forecast['Tmax'][0][i] #switched because Tmax should be temperature with minimum cooling
            t_max = forecast['Tmin'][0][i]
        elif net == 'district_heat':
            t_bar = forecast['th_bar'][0][i]
            ua = forecast['ua_h'][0][i]
            min_e = forecast['h_min'][0][i]
            t_min = forecast['Tmin'][0][i]
            t_max = forecast['Tmax'][0][i]
        request['nominal'][i] = max([(t_bar[0]-t_avg)*ua[0],(t_avg-t_bar[1])*ua[1],min_e])
        request['minimum'][i] = min([request['nominal'][i],max([(t_bar[0]-t_min)*ua[0],(t_min-t_bar[1])*ua[1],min_e])])
        request['maximum'][i] = max([request['nominal'][i],(t_bar[0]-t_max)*ua[0],(t_max-t_bar[1])*ua[1],min_e])
    return request