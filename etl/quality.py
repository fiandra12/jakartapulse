import logging

log = logging.getLogger(__name__)

FRESHNESS_SQL = """
SELECT COALESCE(
  EXTRACT(EPOCH FROM ((now() AT TIME ZONE 'Asia/Jakarta') - max(observed_at))) / 3600,
  999)
FROM staging.stg_hourly
"""

DUPLICATE_SQL = """
SELECT count(*) FROM (
  SELECT 1 FROM mart.daily_air_quality
  GROUP BY location, obs_date HAVING count(*) > 1
) d
"""

# (nama_check, sql, fungsi_lulus)
CHECKS = [
    ("raw_not_empty", "SELECT count(*) FROM raw.air_quality", lambda v: v > 0),
    (
        "pm25_in_range",
        "SELECT count(*) FROM raw.air_quality WHERE pm2_5 < 0 OR pm2_5 > 1000",
        lambda v: v == 0,
    ),
    (
        "pm25_null_ratio",
        "SELECT COALESCE(avg((pm2_5 IS NULL)::int), 0) FROM staging.stg_hourly",
        lambda v: v < 0.2,
    ),
    ("data_freshness_hours", FRESHNESS_SQL, lambda v: v <= 6),
    ("mart_no_duplicates", DUPLICATE_SQL, lambda v: v == 0),
    (
        "all_locations_present",
        "SELECT count(DISTINCT location) FROM mart.daily_air_quality",
        lambda v: v == 5,
    ),
]


def run_checks(conn):
    failures = []
    for name, sql, is_ok in CHECKS:
        with conn.cursor() as cur:
            cur.execute(sql)
            value = float(cur.fetchone()[0])
        status = "PASS" if is_ok(value) else "FAIL"
        log.info("[DQ] %-24s value=%s -> %s", name, value, status)
        if status == "FAIL":
            failures.append(name)
    return failures
