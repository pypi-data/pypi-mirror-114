from .basic.file_handling import ensure_dirpath
from .config.path_spec import AUTO_CREATED_USER_DIRS


# Ensure user directories exist whenever eagers is imported.
for user_dirpath in AUTO_CREATED_USER_DIRS:
    ensure_dirpath(user_dirpath)
