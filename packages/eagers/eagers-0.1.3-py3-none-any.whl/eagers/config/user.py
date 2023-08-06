"""User-facing configuration variables.

See eagers.ini for more information on configuration variables.
"""

import os

from .text import parse_bool_str


# Environment variables and their defaults.
DEBUG_MODE = parse_bool_str(os.environ.get("EAGERS_DEBUG_MODE", "False"))
USER_DIR = os.environ.get("EAGERS_USER_DIR", "Documents/eagers_user")
USER_DIR_EXCLUDED = os.environ.get(
    "EAGERS_USER_DIR_EXCLUDE_NAME", "IGNORED"
).replace(" ", "").splitlines()
