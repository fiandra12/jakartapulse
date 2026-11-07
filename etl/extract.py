import logging
import time

import requests

from etl.config import LOCATIONS

log = logging.getLogger(__name__)

AQ_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
WX_URL = "https://api.open-meteo.com/v1/forecast"
AQ_VARS = ["pm10", "pm2_5", "us_aqi"]
WX_VARS = ["temperature_2m", "relative_humidity_2m"]


def _get(url, params, retries=3):
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            log.warning("Request gagal (%s/%s): %s", attempt, retries, exc)
            if attempt == retries:
                raise
            time.sleep(2 ** attempt)


def parse_hourly(location, payload, variables):
    hourly = payload["hourly"]
    rows = []
    for i, ts in enumerate(hourly["time"]):
        row = {"location": location, "observed_at": ts}
        for var in variables:
            row[var] = hourly[var][i]
        rows.append(row)
    return rows


def extract(past_days=2):
    aq_rows, wx_rows = [], []
    for name, (lat, lon) in LOCATIONS.items():
        base = {
            "latitude": lat,
            "longitude": lon,
            "timezone": "Asia/Jakarta",
            "past_days": past_days,
            "forecast_days": 1,
        }
        aq = _get(AQ_URL, {**base, "hourly": ",".join(AQ_VARS)})
        wx = _get(WX_URL, {**base, "hourly": ",".join(WX_VARS)})
        aq_rows += parse_hourly(name, aq, AQ_VARS)
        wx_rows += parse_hourly(name, wx, WX_VARS)
        log.info("Extract %s selesai", name)
    return aq_rows, wx_rows
