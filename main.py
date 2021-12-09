import re
import datetime
import netCDF4
import pandas

from time import time

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from services import request_nasa_power_data

app = FastAPI()

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

INITIAL_DATE = "2015-01-01"
FINAL_DATE = "01/01/2020"

MIN_INITIAL_DATE = datetime.datetime(2000, 1, 1).date()
MAX_FINAL_DATE = datetime.datetime(2020, 12, 1).date()

DEFAULT_SPATIAL = SPATIALS[0]
DEFAULT_OUTPUT_FORMAT = OUTPUT_FORMAT[0]
DEFAULT_API_TYPE = API_TYPES[0]
DEFAULT_TEMPORAL = TEMPORALS[2]
DEFAULT_COMMUNITY = COMMUNITIES[0]


async def validate_dates(initial_date: str, final_date: str):
    formated_initial_date = await format_date(initial_date)
    formated_final_date = await format_date(final_date)

    if formated_initial_date > formated_final_date:
        raise HTTPException(
            status_code=406,
            detail = "Initial date is greater than final date"
        )

    elif formated_final_date < formated_initial_date:
        raise HTTPException(
            status_code=406,
            detail = "Final date is less than initial date"
        )
    elif formated_initial_date < MIN_INITIAL_DATE:
        raise HTTPException(
            status_code=406,
            detail = "Initial date is too early"
        )
    elif formated_final_date > MAX_FINAL_DATE:
        raise HTTPException(
            status_code=406,
            detail = "Final date is too late"
        )
    else:
        nasapower_start_date = format_nasapower_date(formated_initial_date)
        nasapower_end_date = format_nasapower_date(formated_final_date)

    return nasapower_start_date, nasapower_end_date


async def validate_coordinates(latitude: float, longitude: float):
    errors = []

    if latitude < -90 or latitude > 90:
        errors.append("Latitude out of bounds")

    if longitude < -180 or longitude > 180:
        errors.append("Longitude out of bounds")

    if errors:
        raise HTTPException(
            status_code=406,
            detail = " and ".join(errors)
        )


async def discover_date_template(date: str):
    if "/" in date:
        separator = "/"
    elif "-" in date:
        separator = "-"
    else:
        separator = ""

    if re.search(REGEX_DATE_ISO8601.replace("separator", separator), date):
        template = f"%Y{separator}%m{separator}%d"
    elif re.search(DEFAULT_REGEX_DATE.replace("separator", separator), date):
        template = f"%d{separator}%m{separator}%Y"
    else:
        template = f"%Y%m%d"

    return template

validate_str_date = lambda date, template : datetime.datetime.strptime(date, template).date()

format_nasapower_date = lambda date: date.strftime(NASAPOWER_DATE_FORMAT)

async def format_date(date: str):
    template = await discover_date_template(date)

    formated_date = validate_str_date(date, template)

    return formated_date

async def format_nasa_power_output(output: bytes, start_date: str, end_date: str):
    dataset = netCDF4.Dataset(b'', memory=output)

    dates = (
        datetime.date() for datetime in pandas.date_range(start_date, end_date)
    )

    zipped_variables = zip(dates, dataset.variables["T2M"], dataset.variables["T2M_MAX"], dataset.variables["T2M_MIN"])

    yield "date,temp,temp max,temp min\n"

    for date, ((t2m, ), ), ((t2m_max,),), ((t2m_min,), ) in zipped_variables:
        yield f"{date},{t2m},{t2m_max},{t2m_min}\n"


@app.get("/")
async def index(latitude: float, longitude: float, output: str = DEFAULT_OUTPUT_FORMAT):
    await validate_coordinates(latitude, longitude)

    nasapower_start_date, nasapower_end_date = await validate_dates(INITIAL_DATE, FINAL_DATE)

    response = await request_nasa_power_data(
        latitude,
        longitude,
        nasapower_start_date,
        nasapower_end_date,
        output,
        DEFAULT_SPATIAL,
        DEFAULT_API_TYPE,
        DEFAULT_TEMPORAL,
        DEFAULT_COMMUNITY
    )

    output = format_nasa_power_output(response, nasapower_start_date, nasapower_end_date)

    return StreamingResponse(output)