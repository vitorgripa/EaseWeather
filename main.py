from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from services import request_nasa_power_data

app = FastAPI()

SPATIALS = (
    "Point",
    "Regional",
    "Global"
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

@app.get("/")
async def index():
    return await request_nasa_power_data(
        -22.45,
        -45.22,
        (
            "20000101",
            "20010101"
        ),
        "JSON",
        SPATIALS[0].lower(),
        API_TYPES[0].lower(),
        TEMPORALS_API[2].lower(),
        COMMUNITIES[0]
    )