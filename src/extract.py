import pandas as pd

def extract_new_orders(file_path, last_processed_date):
    print("📥 Reading full dataset...")

    df = pd.read_csv(
        file_path,
        parse_dates=["order_date", "shipped_at"]
    )

    if last_processed_date:
        df = df[df["order_date"] > pd.to_datetime(last_processed_date)]

    print(f"✔ Extracted {len(df)} new records")
    return df
