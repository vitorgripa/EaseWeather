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
    "NetCDF",
    "ASCII",
    "JSON",
    "CSV"
)

API_TYPES = (
    "Temporal",
    "Application",
    "System"
)

TEMPORALS_API = (
    "Climatology",
    "Monthly",
    "Daily",
    "Hourly"
)

COMMUNITIES = (
    "RE",
)

INITIAL_DATE = ""
FINAL_DATE = ""


async def validate_coordinates(latitude: float, longitude: float):
    errors = []

    if latitude < -90 or latitude > -80:
        errors.append("Latitude out of bounds")

    if longitude < -180 or longitude > 180:
        errors.append("Longitude out of bounds")

    return errors


@app.get("/")
async def index(latitude: float, longitude: float):
    errors = await validate_coordinates(latitude, longitude)

    if errors:
        raise HTTPException(
            status_code=406,
            detail = " and ".join(errors)
        )

    