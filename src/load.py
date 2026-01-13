from sqlalchemy import create_engine
import os

def load_to_sqlite(df, table_name):
    os.makedirs("database", exist_ok=True)
    engine = create_engine("sqlite:///database/fulfillment.db")

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False
    )

    print(f"✔ Loaded data into table: {table_name}")
