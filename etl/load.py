import psycopg2
from psycopg2.extras import execute_values

from etl.config import db_params


def get_conn():
    return psycopg2.connect(**db_params())


def _upsert(conn, table, cols, rows):
    if not rows:
        return 0
    values = [tuple(r[c] for c in cols) for r in rows]
    updates = ", ".join(
        f"{c} = EXCLUDED.{c}" for c in cols if c not in ("location", "observed_at")
    )
    sql = (
        f"INSERT INTO {table} ({', '.join(cols)}) VALUES %s "
        f"ON CONFLICT (location, observed_at) DO UPDATE SET {updates}, ingested_at = now()"
    )
    with conn.cursor() as cur:
        execute_values(cur, sql, values)
    return len(values)


def load_air_quality(conn, rows):
    cols = ["location", "observed_at", "pm10", "pm2_5", "us_aqi"]
    return _upsert(conn, "raw.air_quality", cols, rows)


def load_weather(conn, rows):
    cols = ["location", "observed_at", "temperature_2m", "relative_humidity_2m"]
    return _upsert(conn, "raw.weather", cols, rows)
