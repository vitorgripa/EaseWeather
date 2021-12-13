from datetime import datetime

SPATIALS = (
    "Point",
    "Regional",
    "Global"
)

OUTPUT_FORMAT = (
    "netcdf",
    "csv",
    "json",
    "ascii",
    "icasa",
    "xarray"
)

API_TYPES = (
    "temporal",
    "application",
    "system"
)

TEMPORALS = (
    "climatology",
    "monthly",
    "daily",
    "hourly"
)

COMMUNITIES = (
    "RE",
)

NASAPOWER_DATE_FORMAT = "%Y%m%d"

REGEX_DATE_ISO8601 = "\d{4}separator\d{2}separator\d{2}"
DEFAULT_REGEX_DATE = "\d{2}separator\d{2}separator\d{4}"

INITIAL_DATE = "1981-01-01"
FINAL_DATE = "01/11/2021"

MIN_INITIAL_DATE = datetime(1981, 1, 1).date()
MAX_FINAL_DATE = datetime(2021, 11, 1).date()

DEFAULT_SPATIAL = SPATIALS[0]
DEFAULT_OUTPUT_FORMAT = OUTPUT_FORMAT[0]
DEFAULT_API_TYPE = API_TYPES[0]
DEFAULT_TEMPORAL = TEMPORALS[2]
DEFAULT_COMMUNITY = COMMUNITIES[0]

NASA_POWER_API_URL = "https://power.larc.nasa.gov/api"

WEATHER_PARAMETERS = (
    "T2M",
    "T2M_MAX",
    "T2M_MIN"
)