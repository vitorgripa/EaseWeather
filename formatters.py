from datetime import datetime

from pandas import date_range
from netCDF4 import Dataset

from utils import discover_date_template


async def format_date(date: str):
    template = await discover_date_template(date)

    formated_date = datetime.strptime(date, template).date()

    return formated_date
    

async def format_nasa_power_output(output: bytes, start_date: str, end_date: str):
    dataset = Dataset(b'', memory=output)

    dates = (
        datetime.date() for datetime in date_range(start_date, end_date)
    )

    zipped_variables = zip(dates, dataset.variables["T2M"], dataset.variables["T2M_MAX"], dataset.variables["T2M_MIN"])

    yield "date,temp,temp max,temp min\n"

    for date, ((t2m, ), ), ((t2m_max,),), ((t2m_min,), ) in zipped_variables:
        yield f"{date},{t2m},{t2m_max},{t2m_min}\n"