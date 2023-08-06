"""Contains structure descriptions for results to be saved in HDF5
format.
"""

import tables as tb


# ----------------
# Module constants
# ----------------

# Conversion from shape codes to dimension info field names.
# These provide the mapping between given dimension info field names and
# the letters used in column shape specifications.
#
# ASSUMPTION:
# column_realization assumes that every shape code is a single letter.
# Be careful when adding new ones to either follow the current
# convention or update it.
SHAPECODE_TO_DIMFIELD = dict(
    h='horizon',
    z='zone',
    p='plantloop', #largest number of plant water loops at any building
    t='timer',
)


# ------------------------------------------
# Table column description factory functions
# ------------------------------------------
#
# If a column is specified as a dictionary, shape can be specified as a
# tuple of strings.  The SHAPECODE_TO_DIMFIELD variable defines the
# mapping between field names specified in the given dimension
# information dictionary and letters used in column shape
# specifications.
#
# ASSUMPTIONS:
# column_realization assumes:
#   - every dimension specification contains at most one shape code.
#       E.g. shape=('g+h',) will not work.
# Be careful when modifying column descriptions to either follow the
# current convention or update it.

def nodedata_descr(node_names,v_shape,v_pos):
    def make_nd_dict(pos,v_shape):
        f_list = ['demand','demand_history','inflow','outflow','inflow_history','outflow_history']
        desc = dict(_v_pos=pos,)
        for j,f in enumerate(f_list):
            desc[f] = dict(col='Float64Col', pos=j)
            if not v_shape is None:
                desc[f]['shape'] = (v_shape)
        return desc
    nddesc = {}
    for i, n in enumerate(node_names):
        nddesc[n] = make_nd_dict(i,v_shape)
    nddesc['_v_pos'] = v_pos
    return nddesc


def weather_descr(v_shape,v_pos):
    weather = {}
    w_names = ['glo_horz_irr', 'dir_norm_irr','dif_horz_irr','t_dryb','t_dewp','rh','pres_pa','wdir','wspd','tot_cld','opq_cld']
    for k,n in enumerate(w_names):
        weather[n] = dict(col='Float32Col', pos=k)
        if not v_shape == None:
            weather[n]['shape'] = (v_shape)
    weather['_v_pos'] = v_pos
    return weather

def gen_descr(names,v_shape,v_pos):
    gendesc = {}
    for k,n in enumerate(names):
        gendesc[n] = dict(col='Float64Col', pos=k)
        if not v_shape == None:
            gendesc[n]['shape'] = (v_shape)
    gendesc['_v_pos'] = v_pos
    return gendesc

def building_descr(build_names, z_dif, pl_dif,v_shape,v_pos):
    def make_build_dict(pos,v_shape,z_dif,pl_dif):
        if v_shape is None:
            f_list = ['avg_T','Tzone','electric','cooling','heating','return_','supply']
            s_list = [None,'z',None,None,None,'p','p']
        else:
            if z_dif is None:
                f_list = ['heating','cooling','temperature']
                s_list = [None,None,None]
            else:
                f_list = ['avg_T','Tzone','electric','cooling','heating']
                s_list = [None,'z',None,None,None]
        
        desc = dict(_v_pos=pos,)
        for j,f in enumerate(f_list):
            if s_list[j] is None:
                desc[f] = dict(col='Float64Col', pos=j)    
                if not v_shape is None:
                    desc[f]['shape'] = (v_shape)
            else:
                sh = s_list[j]
                if sh == 'z' and z_dif>0:
                    sh = sh + '-' + str(int(z_dif))
                elif sh == 'p' and pl_dif>0:
                    sh = sh + '-' + str(int(pl_dif))
                if v_shape is None:
                    desc[f] = dict(col='Float64Col', pos=j, shape=(sh))
                else:
                    desc[f] = dict(col='Float64Col', pos=j, shape=[v_shape,sh])
        return desc
    build = {}
    for i, n in enumerate(build_names):
        if z_dif is None:
            build[n] = make_build_dict(i,v_shape,None,None)
        else:
            build[n] = make_build_dict(i,v_shape,z_dif[i],pl_dif[i])
    build['_v_pos'] = v_pos
    return build


def dispatch_descr(names, z_dif, pl_dif):
    dispatch = dict(timestamp=tb.Time64Col(pos=0))
    dispatch['generator_state'] = gen_descr(names['components'],None,1)
    dispatch['storage_state'] = gen_descr(names['storage'],None,2)
    dispatch['line_flow'] = gen_descr(names['lines'],None,3) 
    dispatch['fluid_loop'] = gen_descr(names['fluid_loop'],None,4) 
    dispatch['building'] = building_descr(names['buildings'], z_dif, pl_dif,None,5)
    dispatch['nodedata'] = nodedata_descr(names['nodes'],None,6)
    dispatch['weather']= weather_descr(None,7)
    return dispatch


def predicted_descr(names, z_dif, pl_dif,h):
    predicted = dict(timestamp = tb.Time64Col(pos=0, shape=h))
    predicted['cost'] = dict(col='Time64Col', pos=1,)
    predicted['lb_relax'] = dict(col='Time64Col', pos=2,)
    predicted['generator_state'] = gen_descr(names['components'],'h',3)
    predicted['storage_state'] = gen_descr(names['storage'],'h',4)
    predicted['line_flow'] = gen_descr(names['lines'],'h',5) 
    predicted['building'] = building_descr(names['buildings'], z_dif, pl_dif,'h',6)
    predicted['fluid_loop'] = gen_descr(names['fluid_loop'],'h',7) 
    predicted['nodedata'] = nodedata_descr(names['nodes'],'h',8)
    predicted['weather'] = weather_descr('h',9)
    return predicted


def solution_descr(names,h):
    sol = dict(timestamp=tb.Time64Col(pos=0, shape=h+1),
               timer=tb.Time64Col(pos=0, shape=3))
    sol['generator_state'] = gen_descr(names['components'],'h',2)
    sol['storage_state'] = gen_descr(names['storage'],'h',3)
    sol['excess_heat'] = gen_descr(names['heating_nodes'],'h',4) 
    sol['excess_cool'] = gen_descr(names['cooling_nodes'],'h',5) 
    sol['line_flow'] = gen_descr(names['lines'],'h',6) 
    sol['line_loss'] = gen_descr(names['lines'],'h',7) 
    sol['fluid_loop'] = gen_descr(names['fluid_loop'],'h',8) 
    sol['building'] = building_descr(names['buildings'], None, None,'h',9)
    return  sol


# ----------------
# Module functions
# ----------------

def result_description(names, dimensions, zones, pl):
    """Return the result description, accounting for the different
    project-related dimensions specified.

    Positional arguments:
    node_names - (list of str) Node names.
    dimensions - (dict) Dictionary specifying dimension counts for
        different project elements.
    """
    z_dif = [dimensions['zone'] - z for z in zones]
    pl_dif = [dimensions['plantloop'] - n for n in pl]
    h = dimensions['horizon']
    # Update dispatch description.
    disp = realize_all_columns(dispatch_descr(names, z_dif, pl_dif), dimensions)
    # Update predicted description.
    pred = realize_all_columns(predicted_descr(names, z_dif, pl_dif,h), dimensions)
    # Update solution description.
    solu = realize_all_columns(solution_descr(names,h), dimensions)
    # Create and return result description.
    return disp, pred, solu


def realize_all_columns(descr, dimensions):
    """Use dictionary column specifications to create PyTables column
    instances.

    Positional arguments:
    descr - (dict) Description specification whose columns are to be
        realized.
    dimensions - (dict) Dimensional count information.
    """
    realized = {}
    for k, v in descr.items():
        if isinstance(v, dict):
            if 'col' in v:
                col_realzn = column_realization(v, dimensions)
            else:
                col_realzn = realize_all_columns(v, dimensions)
                if set(col_realzn.keys()) == {'_v_pos'}:
                    # Only key is '_v_pos'.
                    del col_realzn['_v_pos']
            if col_realzn:
                realized[k] = col_realzn
        else:
            realized[k] = v
    return realized


def column_realization(col, dimensions):
    """Return a PyTables column instance based on the given
    specification.

    Assumptions:
    - Every shape code is a single letter.
    - Every column shape specification contains at most one shape code,
        which comes at the beginning of each dimension specification.

    Positional arguments:
    col - (dict) Column specification. This will be converted to a
        PyTables column instance.
    dimensions - (dict) Dimensional information for this column.
    """
    coltype = getattr(tb, col.pop('col'))
    try:
        shape_spec = col['shape']
    except KeyError:
        return coltype(**col)
    # Create shape based on given dimensional information.
    new_shape = []
    if isinstance(shape_spec,(str,list)):
        for spec in shape_spec:
            # Evaluate the shape specification.
            shapecode = spec[0]
            dimfield = SHAPECODE_TO_DIMFIELD.get(shapecode)
            if dimfield:
                # Shape code corresponds to a potential dimension key.
                dim = dimensions.get(dimfield)
                if dim:
                    # A dimension number was given for the key.
                    new_spec = f"{dim}{spec[1:]}"
                else:
                    return
            else:
                new_spec = spec
            new_shape.append(eval(new_spec))
    if any(new_shape):
        col['shape'] = tuple(new_shape)
        return coltype(**col)
    # If all dimensions are zero, None is returned.
