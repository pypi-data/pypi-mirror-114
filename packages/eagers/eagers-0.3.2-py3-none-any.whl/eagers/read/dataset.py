"""Functionality for reading data sets from JSON files.

Defines:
read_dataset
"""

import json

from dateutil import parser

from eagers.config.path_spec import JSON_SUFFIX, USER_DIR_DATASETS


def read_dataset(dataset_class, name, convert_timestamp=True):
    """Read a data set from a JSON file to a dictionary.

    Positional arguments:
    dataset_class - (str) Data set class name.
    name - (str) Name of the JSON file.

    Keyword arguments:
    convert_timestamp - (bool) When True, the resulting dictionary will
        be checked for a key called 'timestamp'. If it exists, all its
        values will be converted to datetimes.
    """
    # Ensure ".json" suffix.
    try:
        suffix = name.split('.')[1]
        if suffix != 'json':
            raise ValueError(
                f'File name {name} has a non-JSON suffix.')
    except IndexError:
        # No file suffix; add one.
        name += JSON_SUFFIX
    # Get file path.
    filepath = USER_DIR_DATASETS / dataset_class / name
    # Read.
    with open(filepath, 'r') as jf:
        result = json.load(jf)
    if convert_timestamp and 'timestamp' in result:
        result['timestamp'] = convert_to_datetime(result['timestamp'])
    return result


def convert_to_datetime(t):
    """Recursively convert the given string or sequence to datetime(s).
    If the given object is of neither type, return the object.
    """
    if isinstance(t, str):
        return parser.parse(t)
    elif isinstance(t, (list, tuple, set)):
        seq_type = type(t)
        return seq_type(map(convert_to_datetime, t))
    else:
        return t
