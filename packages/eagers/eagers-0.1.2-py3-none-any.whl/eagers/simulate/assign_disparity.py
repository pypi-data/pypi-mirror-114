
from eagers.basic.component_output import component_output
from eagers.simulate.dispatch_network import dispatch_network

def assign_disparity(net,names,gen,subnet,production,demand,request,solution,marginal,dt,tol,excess,re_opt):
    #check if there is a disparity with forecast
    #check if there is a utility (slack bus)
    #if not check if storage has enough capacity to be slack bus
    #if it is heating and cooling, assign disparity to buildings hot/cold water loops
    #otherwise re-optimize
    i_utility = []
    i_storage = []
    capacity = []
    thermal = None
    acdc = any([gen[i]['type']=='ACDCConverter' for i in range(len(gen))])
    if acdc:
        acdc_i = [i for i in range(len(gen)) if gen[i]['type']=='ACDCConverter']
        ac2dc = gen[acdc_i[0]]['output']['dc'][-1][0]
        dc2ac = gen[acdc_i[0]]['output']['e'][-1][1]
    for i in range(len(gen)):
        if subnet['abbreviation'] in gen[i]['output']:
            if gen[i]['type'] == 'Utility':
                    i_utility.append(i)
            elif gen[i]['type'] in ['ThermalStorage', 'ElectricStorage','HydroStorage','HydrogenStorage']:
                    i_storage.append(i)
        if gen[i]['type'] == 'ElectricStorage' and acdc and ((net == 'electrical' and 'dc' in gen[i]['output']) or (net == 'direct_current' and 'e' in gen[i]['output'])):
            i_storage.append(i)
        if gen[i]['type'] == 'Utility' and acdc and ((net == 'electrical' and 'dc' in gen[i]['output']) or (net == 'direct_current' and 'e' in gen[i]['output'])):
            i_utility.append(i)
    ##TODO solve a nodal problem to determine any shortfall/excess energy in the network
    prod = sum(production)
    req = sum([demand[k] for k in demand])
    if not request is None and 'nominal' in request:
        req += sum(request['nominal'])
        thermal = [j*1000 for j in request['nominal']]
    e_error = None
    if ((prod == 0 and req>0) or (prod>0 and abs(prod-req)/prod>tol)):
        e_error = req - prod #Positive means there is unmet demand, negative means excess production
        if e_error<0 and excess: #can dump heat or cooling
            e_error = None
    ######
    # e_error = dispatch_network(names,subnet,production,demand,request,marginal,capacity,True)
    ######
    
    if not e_error is None:
        if len(i_utility)==0 and len(i_storage)==0:
            re_opt = True
        elif len(i_storage)==0:  #no storage, grid handles error
            i = i_utility[0]
            if subnet['abbreviation'] in gen[i]['output']:
                solution['dispatch'][i][1] += e_error
            elif acdc and net == 'electrical':
                solution['dispatch'][i][1] += e_error/dc2ac
                solution['dispatch'][acdc_i[0]][1] -= e_error/dc2ac
            elif acdc and net == 'direct_current':
                solution['dispatch'][i][1] += e_error/ac2dc
                solution['dispatch'][acdc_i[0]][1] += e_error/ac2dc
            solution['generator_state'][gen[i]['name']][0] = solution['dispatch'][i][1]
        else: # add up storage capacity to meet error & split proportional to available capacity            
            cap = [0 for i in range(len(i_storage))]
            for i in range(len(i_storage)):
                k = i_storage[i]
                gs = gen[k]['stor']
                if e_error>0: #extra demand, what stored charge can be called upon
                    cap[i] = min(gs['peak_disch'],gs['disch_eff']*(gs['usable_size'] - solution['dispatch'][k][1])/dt)
                else: #less demand, what remaining storage capacity can be called upon
                    cap[i] = -min(gs['peak_charge'],(1/gs['charge_eff'])*solution['dispatch'][k][1]/dt)
                if subnet['abbreviation'] not in gen[i]['output'] and acdc and net == 'electrical':
                    cap[i] = cap[i]*dc2ac
                elif subnet['abbreviation'] not in gen[i]['output'] and acdc and net == 'direct_current':
                    cap[i] = cap[i]*ac2dc
            if len(i_utility)==0: #no grid, all error is absorbed by storage (if possible? otherwise re-optimize)
                if abs(sum(cap))<abs(e_error): #if unable to meet error, re-optimize
                    re_opt = True
                else:
                    r = abs(e_error)/abs(sum(cap))
                    if e_error>0: #extra demand, what stored charge can be called upon
                        power = r*cap[i]/gs['disch_eff']
                    else: #less demand, what remaining storage capacity can be called upon
                        power = r*cap[i]*gs['charge_eff']
                    if subnet['abbreviation'] not in gen[i]['output'] and acdc and net == 'electrical':
                        power = power/dc2ac
                        solution['dispatch'][acdc_i[0]][1] -= power
                        solution['generator_state'][gen[acdc_i[0]]['name']][0] -= power
                    elif subnet['abbreviation'] not in gen[i]['output'] and acdc and net == 'direct_current':
                        power = power/ac2dc
                        solution['dispatch'][acdc_i[0]][1] += power
                        solution['generator_state'][gen[acdc_i[0]]['name']][0] += power
                    solution['dispatch'][k][1] -= power*dt
                    solution['generator_state'][gen[k]['name']][0] += power
                    solution['storage_state'][gen[k]['name']][0] -= power*dt
            else: #split the error between utility and energy storage based on storage behavior
                charging = []
                discharging = []
                for k in i_storage:
                    ##TODO factor in loss term
                    if solution['dispatch'][k][1]>solution['dispatch'][k][0]: #charging
                        charging.append((1/gen[k]['stor']['charge_eff'])*(solution['dispatch'][k][1] - solution['dispatch'][k][0])/dt)
                        discharging.append(0)
                    else:
                        charging.append(0)
                        discharging.append(gen[k]['stor']['disch_eff']*(solution['dispatch'][k][0] - solution['dispatch'][k][1])/dt)
                r = 0
                if e_error>0 and sum(charging)>0: #If more demand than anticipated, reduce all storage charging, otherwise resort to grid
                    r = 1 - max([0,(sum(charging)-e_error)])/sum(charging)
                    e_error -= r*sum(charging)
                elif e_error<0 and sum(discharging)>0: #if discharging and less demand than anticipated reduce discharging
                    r = 1 - max([0,(sum(discharging) + e_error)])/sum(discharging)
                    e_error += r*sum(discharging)

                for i,k in enumerate(i_storage):
                    if e_error>0:
                        power = -r*charging[i]*gen[k]['stor']['charge_eff'] #(negative) amount less power devoted to charging
                    else:
                        power = r*discharging[i]/gen[k]['stor']['disch_eff'] #amount less power from discharging
                    if subnet['abbreviation'] not in gen[i]['output'] and acdc and net == 'electrical':
                        power = power/dc2ac
                        solution['dispatch'][acdc_i[0]][1] += power
                        solution['generator_state'][gen[acdc_i[0]]['name']][0] += power
                    elif subnet['abbreviation'] not in gen[i]['output'] and acdc and net == 'direct_current':
                        power = power/ac2dc
                        solution['dispatch'][acdc_i[0]][1] -= power
                        solution['generator_state'][gen[acdc_i[0]]['name']][0] -= power
                    solution['dispatch'][k][1] += power*dt
                    solution['generator_state'][gen[k]['name']][0] -= power
                    solution['storage_state'][gen[k]['name']][0] += power*dt

                #Utility makes up the difference
                i = i_utility[0]
                if subnet['abbreviation'] in gen[i]['output']:
                    solution['dispatch'][i][1] += e_error
                elif acdc and net == 'electrical':
                    solution['dispatch'][i][1] += e_error/dc2ac
                    solution['dispatch'][acdc_i[0]][1] -= e_error/dc2ac
                elif acdc and net == 'direct_current':
                    solution['dispatch'][i][1] += e_error/ac2dc
                    solution['dispatch'][acdc_i[0]][1] += e_error/ac2dc
                solution['generator_state'][gen[i]['name']][0] = solution['dispatch'][i][1]
        if 'buildings' in subnet and net in ['district_heat','district_cool']:
            gs_now = {}
            for k in solution['generator_state']:
                gs_now[k] = solution['generator_state'][k][0]
            production = component_output(gen,subnet,gs_now)
            thermal = distribute_heat_cool(names,subnet,production,demand,request,marginal,capacity)
    return thermal


def distribute_heat_cool(names,subnet,production,demand,request,marginal,capacity):
    ''' Find the thermal energy available for buildings at each node in the thermal network
    Then evenly distrubute amongs buildings at that node to minimize percent deviation from request
    Requires a optimization if there is a thermal network with line losses 
    output: thermal a list of the thermal energy provided to each building'''
    nn = subnet['nodes']
    if len(nn) == 1: #can handle multiple buildings at a single thermal node
        net_thermal = sum(production)
        if nn[0] in list(demand.keys()):
            net_thermal -= sum(demand[nn[0]]['demand'])
        net_request = sum(request['nominal'])
        thermal = [j*(net_thermal/net_request)*1000 for j in request['nominal']]
    else:
        thermal = dispatch_network(names,subnet,production,demand,request,marginal,capacity,False)
    return thermal