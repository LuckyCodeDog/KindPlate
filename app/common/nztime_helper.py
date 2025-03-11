from datetime import datetime
from pytz import timezone


nz_timezone = timezone("Pacific/Auckland")


def nz_datetime(format="%Y-%m-%d %H:%M:%S %Z%z"):
    global nz_timezone
    # Convert to Asia/Kolkata time zone
    return datetime.now(nz_timezone).strftime(format)


def nz_today():
    format = "%Y-%m-%d"
    return nz_datetime(format)


def nz_now():
    format = "%H:%M:%S"
    return nz_datetime(format)
