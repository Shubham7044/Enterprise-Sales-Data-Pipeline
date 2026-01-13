import pandas as pd

def transform_orders(df):
    print("🧹 Transforming data...")

    # 🔒 Robust datetime parsing (CRITICAL FIX)
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce",
        dayfirst=True
    )

    df["shipped_at"] = pd.to_datetime(
        df["shipped_at"],
        errors="coerce",
        dayfirst=True
    )

    # Drop rows where order_date could not be parsed
    df = df[df["order_date"].notnull()]

    df["order_day"] = df["order_date"].dt.date
    df["is_shipped"] = df["shipped_at"].notnull().astype(int)

    daily_metrics = (
        df.groupby("order_day")
        .agg(
            total_orders=("order_id", "nunique"),
            total_quantity=("prod_qty", "sum"),
            shipped_orders=("is_shipped", "sum")
        )
        .reset_index()
    )

    print("✔ Transformation completed")
    return daily_metrics
