"""For loading data sets from the web. Inspired by the approach at:
https://github.com/mwaskom/seaborn/blob/master/seaborn/utils.py

Functions:
get_dataset_names
load_dataset
download_all_datasets
"""

import re
import requests

from eagers.config.path_spec import DATA_CACHE_PATH


def get_dataset_names():
    """Report available example datasets (requires internet)."""
    url = "https://github.com/n8jhj/eagers-public-data"
    response = requests.get(url)
    pattern = r"/n8jhj/eagers-public-data/blob/main/([\w\.]*(\.xlsx|\.eio|\.idf|\.epw))"
    datasets = [match.group(1) for match in re.finditer(pattern, response.text)]
    return datasets


def load_dataset(filename, overwrite_cache=False):
    """Load an example dataset from either the cache or the online data
    repository (requires internet).

    This function provides quick access to a number of example data sets
    that are useful for helping a new user get started.

    Use get_dataset_names to see a list of available datasets.

    Returns a pathlib.Path object pointing to the requested file in the
    cache.

    Positional arguments:
    filename - (str) Name of the data set with its file suffix.

    Keyword arguments:
    overwrite_cache - (bool) (Default: False) If True, download the data
        set afresh, overwriting what's in the cache.
    """
    cache_path = DATA_CACHE_PATH / filename

    if overwrite_cache or not cache_path.exists():
        if filename not in get_dataset_names():
            raise ValueError(f"{filename!r} is not one of the example data sets.")
        url = (
            "https://raw.githubusercontent.com/n8jhj/eagers-public-data/main/"
            f"{filename}"
        )
        response = requests.get(url, stream=True)
        with open(cache_path, "wb") as f:
            f.write(response.content)

    return cache_path


def download_all_datasets(overwrite_cache=False):
    """Call load_dataset for all datasets in the collection returned by
    get_dataset_names (requires internet).

    Keyword arguments:
    overwrite_cache - (bool) (Default: False) Whether to overwrite any
        conflicting files in the cache with the downloaded files.
    """
    for dataset_name in get_dataset_names():
        load_dataset(dataset_name, overwrite_cache=overwrite_cache)
        print(f"Downloaded {dataset_name}")
