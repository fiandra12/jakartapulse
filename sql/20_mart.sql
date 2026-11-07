CREATE TABLE IF NOT EXISTS mart.daily_air_quality (
    location          TEXT,
    obs_date          DATE,
    avg_pm25          NUMERIC(8,2),
    max_pm25          NUMERIC(8,2),
    avg_pm10          NUMERIC(8,2),
    avg_us_aqi        NUMERIC(8,2),
    avg_temp_c        NUMERIC(5,2),
    avg_humidity_pct  NUMERIC(5,2),
    hours_recorded    INT,
    PRIMARY KEY (location, obs_date)
);

TRUNCATE mart.daily_air_quality;

INSERT INTO mart.daily_air_quality
SELECT
    location,
    observed_at::date,
    ROUND(AVG(pm2_5), 2),
    ROUND(MAX(pm2_5), 2),
    ROUND(AVG(pm10), 2),
    ROUND(AVG(us_aqi), 2),
    ROUND(AVG(temperature_c), 2),
    ROUND(AVG(humidity_pct), 2),
    COUNT(*)
FROM staging.stg_hourly
GROUP BY location, observed_at::date;

CREATE OR REPLACE VIEW mart.hourly_air_quality AS
SELECT * FROM staging.stg_hourly;
