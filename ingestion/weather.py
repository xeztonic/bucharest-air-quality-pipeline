from datetime import datetime, timezone

import requests

from db import get_connection

BASE_URL = "https://api.open-meteo.com/v1/forecast"
LATITUDE = 44.43
LONGITUDE = 26.10
HOURLY_VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "precipitation",
]


def fetch_weather():
    """Fetch weather data from the Open-Meteo API."""
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": ",".join(HOURLY_VARIABLES),
        "timezone": "UTC",
        "past_days": 1,
        "forecast_days": 1
    }
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()

    return response.json()


def to_rows(data):
    """Convert the weather data into a list of tuples."""
    hourly = data["hourly"]
    time = hourly["time"]
    temperature = hourly["temperature_2m"]
    relative_humidity = hourly["relative_humidity_2m"]
    wind_speed = hourly["wind_speed_10m"]
    precipitation = hourly["precipitation"]
    tuples = list(zip(time, temperature, relative_humidity, wind_speed, precipitation))

    return tuples


INSERT_SQL = """
    INSERT INTO raw.weather_hourly (
        observed_at,
        temperature_2m,
        relative_humidity_2m,
        wind_speed_10m,
        precipitation
    )
    VALUES (%s, %s, %s, %s, %s)
"""


def to_rows(data):
    """Convert the hourly section from columns to rows (a list of tuples)."""
    hourly = data["hourly"]
    timestamps = [
        datetime.fromisoformat(t).replace(tzinfo=timezone.utc)
        for t in hourly["time"]
    ]
    return list(zip(
        timestamps,
        hourly["temperature_2m"],
        hourly["relative_humidity_2m"],
        hourly["wind_speed_10m"],
        hourly["precipitation"],
    ))


def load_rows(rows):
    """Insert the rows into raw.weather_hourly."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(INSERT_SQL, rows)



if __name__ == "__main__":
    data = fetch_weather()
    rows = to_rows(data)
    load_rows(rows)
    print(f"Inserted {len(rows)} rows")
