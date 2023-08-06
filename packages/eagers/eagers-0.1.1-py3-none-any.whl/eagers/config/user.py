"""User-facing configuration variables.

See config.ini for more information on configuration variables.
"""

import configparser

from .path_spec import CONFIG_FILEPATH


parser = configparser.ConfigParser()
parser.read(CONFIG_FILEPATH)

DEBUG_MODE = parser['user'].getboolean('debug_mode')
