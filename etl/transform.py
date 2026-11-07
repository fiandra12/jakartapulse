from pathlib import Path

SQL_DIR = Path(__file__).resolve().parent.parent / "sql"


def run_sql_file(conn, filename):
    sql = (SQL_DIR / filename).read_text()
    with conn.cursor() as cur:
        cur.execute(sql)
