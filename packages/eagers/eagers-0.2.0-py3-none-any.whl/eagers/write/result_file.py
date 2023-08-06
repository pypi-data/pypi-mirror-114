"""Defines logic pertaining to the handling of HDF5 simulation results
files.

Functions:
new_result_file
new_h5_result_filepath
existing_h5_result_filepath
append_dispatch_ic
append_step_result
groom_for_record
write_dispatch_step
write_predicted_step
write_solution
write_data
read_dispatch
extract_dispatch_data
"""


import numpy as np

from eagers.config.path_spec import HDF5_SUFFIX, USER_DIR_SIMRESULTS
from eagers.config.user import DEBUG_MODE
from eagers.basic.gen_limit import chp_heat
from eagers.write.result_description import result_description
from eagers.basic.file_handling import \
    ensure_dirpath, ensure_suffix, find_file_in_userdir
from eagers.basic.hdf5 import h5file_context, DatetimeFloatConverter as DFC


DICT_ACCESS_PROTOCOL = lambda x, p: x.get(p)


def new_result_file(proj_name, names, dimensions, zones, pl):
    """Create a new HDF5 results file.

    Positional arguments:
    proj_name - (str) Name of the project. This becomes the name of the
        file.
    names - (dict of list of str) all generator, storage, node, line, building and fluid_loop names in
        the project.
    dimensions - (dict) Dimension counts for space to be allocated in
        result file structures.
    """
    # Check that the given file name does not already exist.
    filepath = new_h5_result_filepath(proj_name)
    if not DEBUG_MODE and filepath.exists():
        raise ValueError(f'File with name {proj_name!r} already exists.')

    # Open file in "w"rite mode.
    with h5file_context(
            filepath, mode='w', title=f'{proj_name} results') as h5file:
        # Create tables based on specified dimensions.
        disp, pred, solu = result_description(names, dimensions, zones, pl)
        h5file.create_table('/', 'dispatch', disp)
        h5file.create_table('/', 'predicted', pred)
        h5file.create_table('/', 'solution', solu)
      

def result_file_dimensions(preload,plant,date,zones,pl):
    # Create dictionary of element names for results to be saved in.
    names = {}
    names['components'] = [g['name'] for g in preload['gen_qp_form']]
    names['storage'] = [g['name'] for g in preload['gen_qp_form'] if 'stor' in g]
    names['nodes'] = [n['name'] for n in plant['network']]
    names['lines'] = []
    for net in preload['subnet']['network_names']:
        snl = preload['subnet'][net]['line']
        names['lines'].extend([snl['node1'][i]+'_to_'+snl['node2'][i] for i in range(len(snl['node1']))])
    names['buildings'] = [b.name for b in plant['building']]
    names['fluid_loop'] = [fl.name for fl in plant['fluid_loop']]
    if 'district_heat' in preload['subnet']:
        names['heating_nodes'] = [n[0] for n in preload['subnet']['district_heat']['nodes']]
    else:
        names['heating_nodes'] = []
    if 'district_cool' in preload['subnet']:
        names['cooling_nodes'] = [n[0] for n in preload['subnet']['district_cool']['nodes']]
    else:
        names['cooling_nodes'] = []
    names['hydro'] = [g['name'] for g in preload['gen_qp_form'] if g['type'] == 'HydroStorage' ]
    dimensions = dict(
        horizon = len(date)-1,
        zone = max(zones),
        plantloop = max(pl),
        timer = 3,
    )
    return names, dimensions


def new_h5_result_filepath(filename):
    """Generate the path to a new HDF5 results file with the given name.
    """
    return ensure_dirpath(
        USER_DIR_SIMRESULTS / ensure_suffix(filename, HDF5_SUFFIX))


def existing_h5_result_filepath(filename):
    """Generate the path to the existing HDF5 results file with the
    given name.
    """
    return find_file_in_userdir(USER_DIR_SIMRESULTS, filename, HDF5_SUFFIX)


def append_dispatch_ic(proj_name, disp_ic):
    """Append an initial condition result to the file corresponding to
    the given project name.

    Positional arguments:
    proj_name - (str) Name of the project.
    disp_ic - (dict) Data for the initial condition dispatch result.
    """
    # Convert vanilla Python lists to NumPy arrays, and remove empty
    # lists.
    groomed_disp = groom_for_record(disp_ic)
    # Open file in append mode, requiring its existence already.
    filepath = existing_h5_result_filepath(proj_name)
    with h5file_context(filepath, mode='r+') as h5file:
        table = h5file.root.dispatch
        row = table.row
        write_dispatch_step(row, groomed_disp, DICT_ACCESS_PROTOCOL)
        row.append()


def append_step_predicted(proj_name, pred_step):
    """Append a single step prediction to the file corresponding to the
    given project name.

    Positional arguments:
    proj_name - (str) Name of the project.
    pred_step - (dict) Data for this step's predicted result.
    """
    # Convert vanilla Python lists to NumPy arrays, and remove empty lists.
    groomed_pred = groom_for_record(pred_step)
    # Open file in append mode, requiring its existence already.
    filepath = existing_h5_result_filepath(proj_name)
    with h5file_context(filepath, mode='r+') as h5file:
        # Get the table's Row object, write to it, then append it to the
        # table.
        table = h5file.root.predicted
        row = table.row
        write_predicted_step(row, groomed_pred, DICT_ACCESS_PROTOCOL)
        row.append()


def append_step_solution(proj_name, solution):
    """Append a single step solution to the file corresponding to the
    given project name.

    Positional arguments:
    proj_name - (str) Name of the project.
    solution - (dict) Data for this step's solution result.
    """
    # Convert vanilla Python lists to NumPy arrays, and remove empty lists.
    groomed_solu = groom_for_record(solution)
    # Open file in append mode, requiring its existence already.
    filepath = existing_h5_result_filepath(proj_name)
    with h5file_context(filepath, mode='r+') as h5file:
        # Get the table's Row object, write to it, then append it to the
        # table.
        table = h5file.root.solution
        row = table.row
        write_solution(row, groomed_solu, DICT_ACCESS_PROTOCOL)
        row.append()


def append_step_dispatch(proj_name, disp_step):
    """Append a single step result to the file corresponding to the
    given project name.

    Positional arguments:
    proj_name - (str) Name of the project.
    disp_step - (dict) Data for this step's dispatch result.
    """
    # Convert vanilla Python lists to NumPy arrays, and remove empty lists.
    groomed_disp = groom_for_record(disp_step)
    # Open file in append mode, requiring its existence already.
    filepath = existing_h5_result_filepath(proj_name)
    with h5file_context(filepath, mode='r+') as h5file:
        # Get the table's Row object, write to it, then append it to the
        # table.
        table = h5file.root.dispatch
        row = table.row
        write_dispatch_step(row, groomed_disp, DICT_ACCESS_PROTOCOL)
        row.append()


def groom_for_record(data):
    """Convert the given data structure's vanilla Python lists to NumPy
    arrays.

    Positional arguments:
    data - (dict) Data structure.
    """
    # Define function to handle NumPy arrays.
    def groom_ndarray(a):
        if 0 not in a.shape:
            # The array is not empty.
            # If the array can be flattened, flatten it to match the
            # shape of its column description.
            if a.ndim > 1:
                # Number of dimensions > 1.
                n_largedim = np.count_nonzero(np.array(a.shape) > 1)
                if n_largedim <= 1:
                    a = a.flatten()
            return a

    result = {}
    for k, v in data.items():
        if isinstance(v, dict):
            result[k] = groom_for_record(v)
        elif isinstance(v, list):
            if v != []:
                result[k] = groom_ndarray(np.array(v))
        elif isinstance(v, np.ndarray):
            result[k] = groom_ndarray(v)
        elif v != None:
            result[k] = v
    return result


def write_dispatch_step(row, disp_step, access):
    """Write one step of dispatch results to HDF5 file."""
    # Write timestamp.
    row['timestamp'] = DFC.d2f_sgl2sgl(
        access(disp_step, 'timestamp'))
    l = list(disp_step.keys())
    l.remove('timestamp')
    # Write dispatch data.
    for h in l:
        k_list = list(disp_step[h].keys())
        if any([isinstance(disp_step[h][k],dict) for k in k_list]):
            for k in k_list:
                write_data(row, disp_step, access,h+'/'+k+'/')
        else:
            write_data(row, disp_step, access,h+'/')


def write_predicted_step(row, pred_step, access):
    """Write one step of predicted results to HDF5 file."""
    # Write timestamp.
    row['timestamp'] = DFC.d2f_sgl2sgl(
        access(pred_step, 'timestamp'))
    row['cost'] = access(pred_step, 'cost')
    l = list(pred_step.keys())
    l.remove('timestamp')
    l.remove('cost')
    # Write predicted data.
    for h in l:
        k_list = list(pred_step[h].keys())
        if any([isinstance(pred_step[h][k],dict) for k in k_list]):
            for k in k_list:
                write_data(row, pred_step, access,h+'/'+k+'/')
        else:
            write_data(row, pred_step, access,h+'/')


def write_solution(row, solu, access):
    """Write solution results to HDF5 file."""
    row['timestamp'] = DFC.d2f_sgl2sgl(
        access(solu, 'timestamp'))
    row['timer'] = access(solu, 'timer')
    # row['value_heat'] = access(solu, 'value_heat')
    l = list(solu.keys())
    l.remove('timestamp')
    l.remove('timer')
    l.remove('value_heat')
    # Write solution data.
    for h in l:
        k_list = list(solu[h].keys())
        if any([isinstance(solu[h][k],dict) for k in k_list]):
            for k in k_list:
                write_data(row, solu, access,h+'/'+k+'/')
        else:
            write_data(row, solu, access,h+'/')


def write_data(row, source, access, preamble):
    """Generalization for writing data from a given set of fields to the
    corresponding HDF5 table location.

    Positional arguments:
    row - (tables.tableextension.Row) Row iterator to write to.
    source - (object) Object to be read from.
    access - (function) Access protocol. Must accept two arguments. The
        first is the object to be accessed. The second is the name of
        the field to access.
    preamble - (str) String specifying the path within the HDF5 table to
        the write location.
    """
    # Use specified preamble to get to the part of source we care about.
    # The trailing '/' exists for consistency between top-level access,
    # (i.e. preamble = '') and lower-level access, (i.e. preamble =
    # 'x/.../').  This, along with the [:-1] indexing, ensures we end up
    # with an empty list in the top-level case and the correct levels in
    # lower-level cases.
    levels = preamble.split('/')[:-1]
    for lvl in levels:
        source = access(source, lvl)

    # Write data.
    fields = set(source.keys())
    for f in fields:
        to_insert = access(source, f)
        # Use type check instead of equality check to accommodate NumPy
        # arrays, which return a boolean array when compared to another
        # value.
        # Looking for one of these:
        #   - Raw values (e.g. 3, -2.9, 'electric').
        #   - Non-empty NumPy arrays.
        # Shouldn't encounter a non-empty dict or list here.
        if not isinstance(to_insert, type(None)) \
                and (not isinstance(to_insert, (dict, list, np.ndarray))
                    or len(to_insert)):
            row[f'{preamble}{f}'] = to_insert


def read_dispatch(project_name, *args):
    """Return dispatch data for the given project."""
    from eagers.read.excel_interface import ProjectTemplateReader
    from eagers.setup.preload import preload
    proj = ProjectTemplateReader.read_userfile(project_name)
    # ProjectPreload(proj['plant'], proj['test_data'] ,proj['options'])
    proj['preload'] = preload(proj['plant'], proj['test_data'] ,proj['options'])
    components = proj['preload']['gen_qp_form']
    subnet = proj['preload']['subnet']
    filepath = existing_h5_result_filepath(project_name)
    with h5file_context(filepath, 'r') as h5f:
        table = getattr(h5f.root, 'dispatch')
        descr = table.description._v_colobjects
        r_str = dict(components='generator_state', storage = 'storage_state', nodes = 'nodedata', lines = 'line_flow', buildings = 'building', fluid_loop = 'fluid_loop')
        names = {}
        for v in r_str:
            k = r_str[v]
            if k in descr:
                names[v] = descr[k]._v_names
        gen_state = {}
        stor_state = {}
        for net in subnet['network_names']:
            gen_state[net] = {}
            stor_state[net] = {}
            for comp in components:
                k = comp['name']
                if any(k in ne for ne in subnet[net]['equipment']):
                    gen_state[net][k] = table.read(field='generator_state/'+k)
                    if comp['type'] == 'ACDCConverter':
                        if net == 'direct_current':
                            gen_state[net][k] = [j*comp['output']['e'][0][1] if j>0 else j for j in gen_state[net][k]]
                        elif net == 'electrical':
                            gen_state[net][k] = [-j*comp['output']['dc'][0][0] if j<0 else -j for j in gen_state[net][k]]
                    if comp['type'] == 'CombinedHeatPower' and net == 'district_heat':
                        gen_state[net][k] = chp_heat(comp,gen_state[net][k])
                    if k in names['storage']:
                        unusable = comp['stor']['size'] - comp['stor']['usable_size']
                        st_soc = table.read(field='storage_state/'+k)
                        stor_state[net][k] = [j + unusable for j in st_soc]
    return gen_state, stor_state