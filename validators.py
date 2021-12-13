from datetime import datetime

from fastapi.exceptions import HTTPException

from formatters import format_date
from formatters import format_nasa_power_output

from constants import MAX_FINAL_DATE
from constants import MIN_INITIAL_DATE
from constants import NASAPOWER_DATE_FORMAT


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
        nasapower_start_date = formated_initial_date.strftime(NASAPOWER_DATE_FORMAT)
        nasapower_end_date = formated_final_date.strftime(NASAPOWER_DATE_FORMAT)

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