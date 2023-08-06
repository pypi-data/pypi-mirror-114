"""Utilities for handling HDF5 files.

Context managers:
h5file_context

Functions:
new_hdf5_file
write_records_to_new_hdf5_table
write_user_attributes
write_hdf5_to_csv

Classes:
DatetimeFloatConverter
"""

from contextlib import contextmanager
import csv
import datetime as dt

import numpy as np
import tables as tb

from eagers.config.path_spec import USER_DIR_HDF5_DATASETS


@contextmanager
def h5file_context(*args, **kwargs):
    """HDF5 file context that automatically closes file when it's done
    being used.

    Refer to PyTables documentation on tables.open_file() for positional
    and keyword arguments.
    """
    h5_file = tb.open_file(*args, **kwargs)
    try:
        yield h5_file
    finally:
        h5_file.close()


def new_hdf5_file(filepath, *, overwrite=False):
    """Create a new, empty HDF5 file at the specified path.

    Positional arguments:
    filepath - (pathlib.Path) Path to file.

    Keyword arguments:
    overwrite - (bool) (Default: False) Whether an existing file at the
        given path should be overwritten.
    """
    if not overwrite and filepath.exists():
        raise ValueError(f"{filepath} already exists.")
    h5f = tb.open_file(filepath, 'w')
    h5f.close()


def write_records_to_new_hdf5_table(
        filepath, tablename, records, descr=None, *, timestamp_cols=None):
    """Write records to a new table in a pre-existing HDF5 file.

    Positional arguments:
    filepath - (pathlib.Path) Path to HDF5 file.
    tablename - (str) Name of new table.
    records - (list of tuples) Records to append to the new table.

    Keyword arguments:
    descr - (dict or tables.IsDescription or numpy.dtype) (Default:
        None) Table structure description. If None, records must be a
        NumPy structured array.
    timestamp_cols - (list of str) (Default: None) List of column names
        containing timestamps. These will be converted to floats.
    """
    if descr is None:
        try:
            descr = records.dtype
        except AttributeError:
            raise ValueError(
                "If descr is not passed, records must be a NumPy structured "
                "array.")
    # Open file in "r"ead-plus mode.  This allows addition of tables to
    # an existing file only.
    with h5file_context(filepath, 'r+') as h5f:
        # Create table based on specified dimensions.
        table = h5f.create_table('/', tablename, descr)
        table.append(records)


def write_user_attributes(filepath, tablename, attributes):
    """Write the specified user attributes to the HDF5 file at the given
    path.

    Positional arguments:
    filepath - (pathlib.Path) Path to HDF5 file.
    tablename - (str) Name of table to assign the attributes to.
    attributes - (dict) Name-value pairs of attributes to be written.
    """
    # Open file in "r"ead-plus mode.  This allows writing of attributes
    # to an existing file only.
    with h5file_context(filepath, 'r+') as h5f:
        table = getattr(h5f.root, tablename)
        for name, value in attributes.items():
            setattr(table.attrs, name, value)


def write_hdf5_to_csv(input_filename, category, to_datetime, output_filepath):
    """Write HDF5 data set to CSV format.

    Positional arguments:
    input_filename - (str) Data set name, w/ file extension.
    category - (str) Data set category.
    to_datetime - (bool) Whether to convert timestamps to datetime
        format.
    output_filepath - (pathlib.Path) Path to output file.
    """
    # Read specified file.
    input_filepath = USER_DIR_HDF5_DATASETS / category / input_filename
    with h5file_context(input_filepath, mode='r') as h5file:
        table = getattr(h5file.root, category)
        raw_data = table.read()
    # Convert datetimes if needed.
    headers = raw_data.dtype.names
    if to_datetime and 'timestamp' in headers:
        # Convert values.
        raw_data['timestamp'] = DatetimeFloatConverter.f2d_arr2arr(
            raw_data['timestamp']
        )
        # Convert data type.
        new_dtype = raw_data.dtype.descr
        new_dtype[headers.index('timestamp')] = ('timestamp', 'M8[us]')
        raw_data = raw_data.astype(new_dtype)
    # Write data to CSV file.
    with open(output_filepath, 'w', newline='') as csvf:
        writer = csv.writer(csvf)
        # Write metadata.
        writer.writerow([input_filename])
        # Write headers.
        writer.writerow(headers)
        # Write data.
        for row in raw_data:
            writer.writerow(row)


class DatetimeFloatConverter:
    """Defines methods for converting between datetimes and floats.
    Since there is no way to store datetimes in HDF5 files, it is
    necessary to do this conversion in both directions - datetime to
    float for write operations and vice versa for reading. Floats
    represent the number of seconds since epoch (Unix time) (Jan 1,
    1970).

    Cf.:
    https://stackoverflow.com/questions/25706423/store-and-extract-numpy-datetimes-in-pytables
    https://stackoverflow.com/questions/6999726/how-can-i-convert-a-datetime-object-to-milliseconds-since-epoch-unix-time-in-p
    https://stackoverflow.com/questions/12137277/how-can-i-make-a-python-numpy-arange-of-datetime
    """

    @staticmethod
    def d2f_sgl2sgl(d):
        """Return single float representation of given single datetime
        as number of seconds since epoch (Jan 1, 1970).

        Positional arguments:
        d - (datetime) Datetime.
        """
        return (d - dt.datetime.utcfromtimestamp(0)) / dt.timedelta(seconds=1)

    @staticmethod
    def d2f_arr2arr(d):
        """Return NumPy float array representation of given NumPy
        datetime array as number of seconds since epoch (Jan 1, 1970).

        Positional arguments:
        d - (ndarray of datetimes) NumPy array of datetimes.
        """
        if d.dtype.kind == 'O':
            return (
                (d - dt.datetime.utcfromtimestamp(0)) / dt.timedelta(seconds=1)
            ).astype('f8')
        elif d.dtype.kind == 'M':
            # Convert to microsecond datetime64 first because conversion
            # to float differs depending on the datetime64 frequency.
            return d.astype('M8[us]').astype('f8') / 1e6

    @staticmethod
    def d2f_lst2arr(d):
        """Return NumPy float array representation of given Python
        datetime list as number of seconds since epoch (Jan 1, 1970).

        Positional arguments:
        d - (list of datetimes) List of datetimes.
        """
        return np.array([
            (x - dt.datetime.utcfromtimestamp(0)) / dt.timedelta(seconds=1)
            for x in d
        ])

    @staticmethod
    def d2f_lst2lst(d):
        """Return Python datetime list representation of given Python
        datetime list as number of seconds since epoch (Jan 1, 1970).

        Positional arguments:
        d - (list of datetimes) List of datetimes.
        """
        return [
            (x - dt.datetime.utcfromtimestamp(0)) / dt.timedelta(seconds=1)
            for x in d
        ]

    @staticmethod
    def f2d_sgl2sgl(f, dt64=False):
        """Return single datetime representation of given single float,
        which is the number of seconds since epoch (Jan 1, 1970).

        Positional arguments:
        f - (float) Float.

        Keyword arguments:
        dt64 - (bool) (Default: False) Whether to convert to a NumPy
            datetime64 object instead of datetime.datetime.
        """
        if dt64:
            return np.float64(f * 1e6).astype('M8[us]')
        return dt.datetime.utcfromtimestamp(0) + dt.timedelta(seconds=f)

    @staticmethod
    def f2d_arr2arr(f):
        """Return NumPy datetime array representation of given NumPy
        float array, which are the number of seconds since epoch (Jan 1,
        1970).

        Positional arguments:
        f - (ndarray of floats) NumPy array of floats.
        """
        return (f * 1e6).astype('M8[us]')

    @staticmethod
    def f2d_arr2lst(f):
        """Return Python datetime list representation of given NumPy
        float array, which are the number of seconds since epoch (Jan 1,
        1970).

        Positional arguments:
        f - (ndarray of floats) NumPy array of floats.
        """
        return (f * 1e6).astype('M8[us]').tolist()

    @staticmethod
    def f2d_lst2lst(f):
        """Return Python datetime list representation of given Python
        float list, which are the number of seconds since epoch (Jan 1,
        1970).

        Positional arguments:
        f - (list of floats) List of floats.
        """
        epoch = dt.datetime.utcfromtimestamp(0)
        return [epoch + dt.timedelta(seconds=x) for x in f]
