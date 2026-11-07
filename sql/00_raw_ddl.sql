CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS mart;

CREATE TABLE IF NOT EXISTS raw.air_quality (
    location     TEXT        NOT NULL,
    observed_at  TIMESTAMP   NOT NULL,
    pm10         NUMERIC,
    pm2_5        NUMERIC,
    us_aqi       NUMERIC,
    ingested_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (location, observed_at)
);

CREATE TABLE IF NOT EXISTS raw.weather (
    location              TEXT        NOT NULL,
    observed_at           TIMESTAMP   NOT NULL,
    temperature_2m        NUMERIC,
    relative_humidity_2m  NUMERIC,
    ingested_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (location, observed_at)
);
