from typing import List, Tuple

from datetime import datetime

from aiohttp import ClientSession

from aiohttp.client import request

from fastapi import HTTPException

from constants import WEATHER_PARAMETERS
from constants import NASA_POWER_API_URL


create_endpoint = lambda api_url, params, temporal, spatial : f"{api_url}/temporal/{temporal}/{spatial}?" + "&".join(f"{k}={v}" for k, v in params.items())

async def request_nasa_power_data(latitude: float, longitude: float, start: str, end: str, output_format: str, spatial: str, api_type: str, temporal: str, community: str):
    request_params = {
        "latitude": latitude,
        "longitude": longitude,
        "parameters": ",".join(WEATHER_PARAMETERS),
        "start": start,
        "end": end,
        "format": output_format,
        "community": community
    }

    endpoint = create_endpoint(NASA_POWER_API_URL, request_params, temporal, spatial)

    async with ClientSession() as session:

        async with session.get(endpoint) as response:
            match response.status:
                case 200:
                    return await response.read()
                case _:
                    raise HTTPException(
                        status_code=500,
                        detail = "Nasa power is unavailable"
                    )