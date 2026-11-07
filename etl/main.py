import logging
import os
import sys

from etl.extract import extract
from etl.load import get_conn, load_air_quality, load_weather
from etl.quality import run_checks
from etl.transform import run_sql_file

log = logging.getLogger("jakartapulse")


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    past_days = int(os.getenv("PAST_DAYS", "2"))
    conn = get_conn()
    try:
        run_sql_file(conn, "00_raw_ddl.sql")
        conn.commit()

        aq_rows, wx_rows = extract(past_days)
        n_aq = load_air_quality(conn, aq_rows)
        n_wx = load_weather(conn, wx_rows)
        conn.commit()
        log.info("Loaded air_quality=%s weather=%s", n_aq, n_wx)

        run_sql_file(conn, "10_staging.sql")
        run_sql_file(conn, "20_mart.sql")
        conn.commit()

        failures = run_checks(conn)
        if failures:
            log.error("Data quality gagal: %s", failures)
            return 1
    except Exception:
        log.exception("Pipeline gagal")
        conn.rollback()
        return 1
    finally:
        conn.close()
    log.info("Pipeline sukses")
    return 0


if __name__ == "__main__":
    sys.exit(main())
