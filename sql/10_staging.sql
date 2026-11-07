CREATE OR REPLACE VIEW staging.stg_hourly AS
SELECT
    a.location,
    a.observed_at,
    a.pm10,
    a.pm2_5,
    a.us_aqi,
    w.temperature_2m        AS temperature_c,
    w.relative_humidity_2m  AS humidity_pct,
    CASE
        WHEN a.us_aqi IS NULL THEN 'Unknown'
        WHEN a.us_aqi <= 50   THEN 'Good'
        WHEN a.us_aqi <= 100  THEN 'Moderate'
        WHEN a.us_aqi <= 150  THEN 'Unhealthy for Sensitive Groups'
        WHEN a.us_aqi <= 200  THEN 'Unhealthy'
        WHEN a.us_aqi <= 300  THEN 'Very Unhealthy'
        ELSE 'Hazardous'
    END AS aqi_category
FROM raw.air_quality a
LEFT JOIN raw.weather w
       ON w.location = a.location AND w.observed_at = a.observed_at
WHERE a.observed_at <= (now() AT TIME ZONE 'Asia/Jakarta');
