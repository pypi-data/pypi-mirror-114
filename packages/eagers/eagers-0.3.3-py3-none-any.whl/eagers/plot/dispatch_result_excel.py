"""After-the-fact dispatch result plotting logic from Excel project
file.

Functions:
plot_dispatch_result - Plot a dispatch result.
extract_dispatch_data - Extract dispatch data from HDF5 result file.
"""

import datetime as dt

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

from eagers import Project
from eagers.config.network import NETWORK_NAMES
from eagers.config.path_spec import HDF5_SUFFIX, USER_DIR_SIMRESULTS
from eagers.config.plots import (
    DEFAULT_BAR_WIDTH, DEFAULT_FIG_WIDTH, DEFAULT_FIG_HEIGHT,
    ATFDISPATCH_WIDGET_SPACE, SUPTITLE_SPACE)
from eagers.basic.file_handling import find_file_in_userdir
from eagers.basic.hdf5 import h5file_context, DatetimeFloatConverter as DFC


def plot_dispatch_result(project_name, testdata_name):
    """Plot the dispatch result for a simulation that has run all the
    way through.
    """
    # Extract dispatch data from HDF5 file, using component properties
    # from the database to process the results.
    proj = Project.from_excel(project_name, testdata_name)
    disp_data, timestamp, comp_names = extract_dispatch_data(proj)

    # Get demand data.
    demand = proj.test_data.demand.read_timestamp_range(
        proj.options['start_date'],
        proj.options['start_date'] \
            + dt.timedelta(days=proj.options['interval']),
    )
    demand_ts = DFC.f2d_arr2arr(demand['timestamp'])

    # Parameters.
    # Network names should have the order defined in config.
    network_names = [x for x in NETWORK_NAMES
        if x in proj.plant.subnet.network_names]
    n_nets = len(network_names)
    I_MAX = 24  # TODO: Replace this with scrolling ability.
    time_res_sec = int(
        (timestamp[1] - timestamp[0]).astype('m8[s]').astype('u8'))
    bar_width = np.timedelta64(int(DEFAULT_BAR_WIDTH * time_res_sec), 's')

    # Use Matplotlib to plot.
    fig = plt.figure(figsize=(DEFAULT_FIG_WIDTH, DEFAULT_FIG_HEIGHT))
    axs = []
    gs = gridspec.GridSpec(n_nets, 1)
    fig.suptitle(f"Dispatch: {proj.name}", fontsize='x-large')

    # Stacked bar chart of Component generation for each network.
    for i, net in enumerate(network_names):
        axs.append(fig.add_subplot(gs[i]))
        axs[i].set_title(net.title().replace('_', ' '))
        bar_sum = np.zeros(I_MAX)
        for cname in comp_names:
            cdata = disp_data['power'][net][cname][:I_MAX]
            axs[i].bar(
                timestamp[:I_MAX], cdata, bar_width,
                bottom=bar_sum, label=cname)
            bar_sum += cdata

    # Line plot of total demand.
    axs[0].plot(
        demand_ts[:I_MAX], demand['e'][:I_MAX], 'or',
        label='Demand')

    # Add legend.
    axs[0].legend()

    # Auto-format time series x-axis.  This also results in shared tick
    # labels.
    fig.autofmt_xdate()
    # TODO: Align tick marks correctly.
    # https://stackoverflow.com/q/54727603/7232335

    # Constrain layout properly.
    gs.tight_layout(fig,
        rect=[0, ATFDISPATCH_WIDGET_SPACE, 1, 1 - SUPTITLE_SPACE])
    # Remove warning about tight_layout.
    fig.set_tight_layout(False)

    # Add text.
    x_text = 0.1
    y_text = 0.3
    text = fig.text(x_text, y_text, "Some text",
        family='sans-serif', size=14,
        horizontalalignment='left', verticalalignment='top',
        backgroundcolor='#de781f')

    plt.show()


def extract_dispatch_data(project):
    """Extract dispatch data for the given Eagers object.

    Returns a dictionary of the structure:
        data['power'][network][Component name] (kW)
    OR:
        data['soc'][network]['x' (timestamp) or 'y' (value)] (frac)
    """
    # Get data from HDF5 file.
    filepath = find_file_in_userdir(
        USER_DIR_SIMRESULTS, project.name, HDF5_SUFFIX)
    # Open file in read mode.
    with h5file_context(filepath, mode='r') as h5f:
        # Read generator state data from table.
        # Generator name order is assumed to correspond to column order.
        table = h5f.root.result
        # TODO: Get generator names from project file or database.  The
        # generator_names attribute is no longer stored in the HDF5
        # result files.
        comp_names = table.attrs.generator_names
        comp_state = table.col('dispatch/generator_state')
        timestamp = table.col('dispatch/timestamp')

    # Convert array of timestamp floats to array of datetimes.
    # HACK: Add one hour.  Reason for this is unknown.
    timestamp = DFC.f2d_arr2arr(timestamp) + np.timedelta64(1, 'h')

    # Make sense of results using Component properties.
    # Initialize dispatch data structure.
    network_names = [net.name for net in project.plant.network]
    disp_data = dict(
        power={
            net: {comp: np.zeros(len(timestamp)) for comp in comp_names}
            for net in network_names
        },
        soc={net: {'x': [], 'y': []} for net in network_names},
    )

    # Add timestamp information for power data.
    for net in network_names:
        disp_data['power'][net]['timestamp'] = timestamp

    # Populate dispatch data structure.
    for i, comp in enumerate(project.plant.generator):
        # Check the correspondence of Components.
        assert comp.name == comp_names[i], (
            "Component names do not correspond. "
            f"DB: {comp.name}, HDF5: {comp_names[i]}")
        # Use the Component's method for extracting dispatch data.
        for keypath, data in comp.extract_disp_data(
                comp_state[:,i], network_names, timestamp):
            type_, net = keypath.split('/')
            if type_ == 'power':
                disp_data[type_][net][comp_names[i]] = data
            elif type_ == 'soc':
                disp_data[type_][net]['x'].append(timestamp)
                disp_data[type_][net]['y'].append(data)

    return disp_data, timestamp, comp_names
