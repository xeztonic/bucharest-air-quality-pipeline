# Bucharest Air Quality Pipeline

A data pipeline that collects air-quality and weather data for Bucharest every day, stores it in PostgreSQL, transforms and tests it with dbt, and uses the result for a dashboard and a next-day PM2.5 forecast.

> **Status:** work in progress. The roadmap at the end of this file shows what is done and what comes next.

## Why this project

Air quality is a real issue in Bucharest, and the data is public, but it is spread across different sources and is hard to use as it is. I wanted to build the whole path from raw API responses to something useful: a clean, tested dataset, a dashboard that shows how pollution changes over time and across the city, and a simple model that tries to predict tomorrow's PM2.5 level.

It is also my way of working hands-on with the tools used in data engineering today: dbt for transformations, Airflow for scheduling and Docker for running everything the same way on any machine.

## How it works

```
OpenAQ (air quality) ─┐
                      ├─▶ Python ingestion ─▶ PostgreSQL (raw) ─▶ dbt (staging → marts + tests) ─▶ Dashboard
Open-Meteo (weather) ─┘                                                                         └─▶ PM2.5 forecast

                    Airflow runs the whole flow once a day · everything runs in Docker
```

1. **Ingestion:** Python scripts call the OpenAQ and Open-Meteo APIs and load new records into a `raw` schema in PostgreSQL. Loads are incremental: each run only fetches data newer than the last one.
2. **Transformation:** dbt cleans and standardizes the raw data (staging models), then builds the tables used for analysis (marts), such as daily averages per station and pollutant, days above the legal limits, and pollution and weather joined by day.
3. **Data quality:** dbt tests check for missing values, duplicates and values outside realistic ranges, so problems are caught before they reach the dashboard.
4. **Orchestration:** an Airflow DAG runs ingestion → `dbt run` → `dbt test` every day.
5. **Dashboard and forecast:** the marts feed a dashboard and a model that predicts the next day's PM2.5 from recent pollution levels and the weather.

## Tech stack

| Area | Tools |
|---|---|
| Language | Python, SQL |
| Storage | PostgreSQL |
| Transformations and tests | dbt Core |
| Orchestration | Apache Airflow |
| Environment | Docker, Docker Compose |
| Dashboard | Streamlit or Metabase |
| Forecasting | pandas, scikit-learn |
| Code quality | pytest, ruff, GitHub Actions |

## Data sources

| Source | What it provides |
|---|---|
| [OpenAQ](https://docs.openaq.org/) | PM2.5, PM10, NO₂ and O₃ measurements from monitoring stations (free API key) |
| [Open-Meteo](https://open-meteo.com/) | Current and historical weather: temperature, wind, humidity, precipitation (no key needed) |

## Project structure

```
bucharest-air-quality-pipeline/
├── ingestion/        # API clients and load scripts
├── dbt_project/      # dbt models (staging, marts) and tests
├── orchestration/    # Airflow DAGs
├── dashboard/        # dashboard app or setup notes
├── ml/               # forecasting notebooks and scripts
├── tests/            # unit tests for the ingestion code
├── docker-compose.yml
├── .env.example
└── requirements.txt
```

The structure will be filled in as each stage is built.

## Running it locally

_Setup instructions will be added once the first stages are in place. The goal is to start everything with:_

```bash
cp .env.example .env    # add your OpenAQ API key
docker compose up -d
```

## Roadmap

- [ ] **Setup:** PostgreSQL in Docker, Python environment, API keys in `.env`
- [ ] **Weather ingestion:** daily and historical data from Open-Meteo
- [ ] **Air-quality ingestion:** Bucharest stations from OpenAQ, with incremental loads and no duplicates
- [ ] **dbt models:** staging and marts, with data tests and generated docs
- [ ] **Orchestration:** daily Airflow DAG; the whole project starts with `docker compose up`
- [ ] **Dashboard:** pollution over time, comparison between stations, days above limits, pollution vs. weather
- [ ] **Forecast:** next-day PM2.5 model, compared against a simple "tomorrow = today" baseline using a time-based split
- [ ] **Polish:** CI with ruff and pytest, screenshots and results in this README

## Results

_Dashboard screenshots and forecast results will be added here as the project progresses._
