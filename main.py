from fastapi import FastAPI

from fastapi.responses import StreamingResponse

from constants import DEFAULT_OUTPUT_FORMAT
from constants import INITIAL_DATE
from constants import FINAL_DATE
from constants import DEFAULT_SPATIAL
from constants import DEFAULT_API_TYPE
from constants import DEFAULT_TEMPORAL
from constants import DEFAULT_COMMUNITY

from validators import validate_coordinates
from validators import validate_dates

from services import request_nasa_power_data

from formatters import format_nasa_power_output


app = FastAPI()


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