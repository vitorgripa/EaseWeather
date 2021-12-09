from re import search

from constants import REGEX_DATE_ISO8601
from constants import DEFAULT_REGEX_DATE


async def discover_date_template(date: str):
    if "/" in date:
        separator = "/"
    elif "-" in date:
        separator = "-"
    else:
        separator = ""

    if search(REGEX_DATE_ISO8601.replace("separator", separator), date):
        template = f"%Y{separator}%m{separator}%d"
    elif search(DEFAULT_REGEX_DATE.replace("separator", separator), date):
        template = f"%d{separator}%m{separator}%Y"
    else:
        template = f"%Y%m%d"

    return template