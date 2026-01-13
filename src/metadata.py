from sqlalchemy import create_engine, text
from datetime import datetime

def get_last_processed_date():
    engine = create_engine("sqlite:///database/fulfillment.db")

    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS pipeline_runs (
                run_time TEXT,
                rows_processed INTEGER,
                status TEXT,
                last_processed_date TEXT
            )
        """))

        result = conn.execute(
            text("SELECT MAX(last_processed_date) FROM pipeline_runs")
        ).fetchone()

        return result[0]

def log_pipeline_run(rows, status, last_date):
    engine = create_engine("sqlite:///database/fulfillment.db")

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO pipeline_runs
                (run_time, rows_processed, status, last_processed_date)
                VALUES (:run_time, :rows, :status, :last_date)
            """),
            {
                "run_time": datetime.now().isoformat(),
                "rows": rows,
                "status": status,
                "last_date": last_date
            }
        )
