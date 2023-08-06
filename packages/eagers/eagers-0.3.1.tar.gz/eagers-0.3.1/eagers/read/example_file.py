"""For reading example files."""

import shutil

from eagers.config.path_spec import DEMO_FILES_DIR, USER_DIR_EXAMPLE_FILES


def load_example_file(filename, overwrite_cache=False):
    """Load an example dataset from either the cache or the demo_files
    folder included in the repository.

    This function provides quick access to an example data set that is
    useful for helping a new user get started.

    Returns a pathlib.Path object pointing to the requested file in the
    example files cache directory.

    Positional arguments:
    filename - (str) Name of the data set with its file suffix.

    Keyword arguments:
    overwrite_cache - (bool) (Default: False) If True, overwrite the
        data set with the file in the demo_files directory.
    """
    cache_path = USER_DIR_EXAMPLE_FILES / filename

    if overwrite_cache or not cache_path.exists():
        demo_file_path = DEMO_FILES_DIR / filename
        assert demo_file_path.exists(), f"{demo_file_path!r} does not exist"
        shutil.copyfile(demo_file_path, cache_path)

    return cache_path
