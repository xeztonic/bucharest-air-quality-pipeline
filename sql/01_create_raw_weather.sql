CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.weather_hourly(
    observed_at            TIMESTAMPTZ  NOT NULL,
    temperature_2m         NUMERIC(4, 1),
    relative_humidity_2m   SMALLINT,
    wind_speed_10m         NUMERIC(5, 1),
    precipitation          NUMERIC(5, 2),
    ingested_at            TIMESTAMPTZ  NOT NULL DEFAULT now(),

    PRIMARY KEY (observed_at)
);