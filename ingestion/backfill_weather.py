from datetime import datetime, timezone

import requests
import time 
from datetime import datetime, timezone
from db import get_connection
from weather import HOURLY_VARIABLES, LATITUDE, LONGITUDE, load_rows, to_rows


ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

START_DATE = "2024-11-01"
END_DATE = "2026-11-01"


def fetch_weather_history(start_date, end_date):
    """Fetch historical hourly weather from the Open-Meteo archive API."""
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ",".join(HOURLY_VARIABLES),
        "timezone": "UTC",
    }
    response = requests.get(ARCHIVE_URL, params=params, timeout=60)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    data = fetch_weather_history(START_DATE, END_DATE)
    rows = to_rows(data)
    load_rows(rows)
    print(f"Backfilled {len(rows)} rows from {START_DATE} to {END_DATE}")