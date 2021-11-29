from typing import List, Tuple
from aiohttp import ClientSession

from datetime import datetime

from aiohttp.client import request

NASA_POWER_API_URL = "https://power.larc.nasa.gov/api"

WEATHER_PARAMETERS = (
    "T2M",
    "T2M_MAX",
    "T2M_MIN"
)

create_endpoint = lambda api_url, params, temporal, spatial : f"{api_url}/temporal/{temporal}/{spatial}?" + "&".join(f"{k}={v}" for k, v in params.items())

async def request_nasa_power_data(latitude: float, longitude: float, dates: Tuple[str, str], format: str, spatial: str, type: str, temporal: str, community: str):
    request_params = {
        "latitude": latitude,
        "longitude": longitude,
        "parameters": ",".join(WEATHER_PARAMETERS),
        "start": dates[0],
        "end": dates[1],
        "format": format,
        "community": community
    }

    endpoint = create_endpoint(NASA_POWER_API_URL, request_params, temporal, spatial)

    async with ClientSession() as session:
        async with session.get(endpoint) as response:
            return response.content

def validate_date():
    pass


def format_date():
    pass
