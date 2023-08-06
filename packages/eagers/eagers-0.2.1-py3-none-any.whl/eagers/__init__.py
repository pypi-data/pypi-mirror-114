from .basic.file_handling import ensure_dirpath
from .config.path_spec import AUTO_CREATED_DIRS


# Ensure user directories exist whenever eagers is imported.
for user_dirpath in AUTO_CREATED_DIRS:
    ensure_dirpath(user_dirpath)


from .read.online_data import download_all_datasets, get_dataset_names, load_dataset
