import configparser
import pathlib


# Suffixes.
CSV_SUFFIX = '.csv'
EPW_SUFFIX = '.epw'
HDF5_SUFFIX = '.h5'
IDF_SUFFIX = '.idf'
EIO_SUFFIX = '.eio'

# File names.
DATABASE_FILENAME = 'projects'
DEFAULT_OUTPUT_FILENAME = 'output'
DISPATCH_RESULT_FILENAME = 'dispatch_result.html'

# Paths.
TLD_ABSPATH = pathlib.Path(__file__).parents[2]
CONFIG_FILEPATH = TLD_ABSPATH / 'config.ini'
EXCEL_INTERFACE_PROJECT_HELP = \
    TLD_ABSPATH / 'eagers' / 'read' / 'excel_interface_project_help.txt'
parser = configparser.ConfigParser()
parser.read(CONFIG_FILEPATH)
DEMO_DIR = TLD_ABSPATH / 'demo_files'
USER_DIR = pathlib.Path.home() / parser['user'].get('user_dir')
USER_DIR_DATA_RETRIEVAL = USER_DIR / 'data_retrieval'
USER_DIR_EPLUS = USER_DIR / 'eplus_validation'
USER_DIR_HYDRO_DATA = USER_DIR / 'hydro_data'
USER_DIR_SIMRESULTS = USER_DIR / 'simulation_results'
USER_DIR_DATASETS = USER_DIR / 'data_sets'
USER_DIR_HDF5_DATASETS = USER_DIR_DATASETS / 'HDF5'
USER_DIR_BUILDINGS = USER_DIR / 'eplus_buildings'
USER_DIR_ENERGYPLUS_WEATHER = USER_DIR / 'eplus_weather'
USER_DIR_PROJECTS = USER_DIR / 'projects'
USER_DIR_TESTDATA = USER_DIR / 'test_data'
AUTO_CREATED_USER_DIRS = [
    USER_DIR_DATA_RETRIEVAL,
    USER_DIR_EPLUS,
    USER_DIR_HYDRO_DATA,
    USER_DIR_SIMRESULTS,
    USER_DIR_DATASETS,
    USER_DIR_HDF5_DATASETS,
    USER_DIR_BUILDINGS,
    USER_DIR_ENERGYPLUS_WEATHER,
    USER_DIR_PROJECTS,
    USER_DIR_TESTDATA,
]
# ConfigParser.get() strips empty space, so only splitlines() is needed.
# https://stackoverflow.com/a/11866695/7232335
USER_DIR_EXCLUDED = parser['user'].get('user_dir_excluded').splitlines()
